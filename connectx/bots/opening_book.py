"""Opening book for bitboard_ab_bot_fast_v2.

Pre-computes optimal moves for the first ~20 ply using v2's search.
During play, the bot checks the book first for instant move selection.

Board encoding: flat board string of digits (e.g., "000000000000...").
The key is the board state BEFORE the move is played.

Usage:
    # Generate the book:
    python -m connectx.bots.opening_book build --output book.json --max-depth 20

    # Or import in code:
    from connectx.bots.opening_book import OpeningBook
    book = OpeningBook("book.json")
    move = book.best_move(board_str)
"""

from __future__ import annotations

import argparse
import importlib
import json
import random
import sys
import time
from pathlib import Path
from typing import Dict, Optional

from connectx.engine import (
    check_win, drop, un_drop, valid_moves,
    ROWS, COLS, INAROW, SIZE, EMPTY,
)

_DEFAULT_PATH = "book.json"


class OpeningBook:
    """Pre-computed optimal opening moves for ConnectX 7x6/4.

    Storage: JSON with a flat-dict ``book`` keyed by board-string,
    each value is ``{ mark: best_col }``.
    """

    def __init__(self, path: str | None = None) -> None:
        self._entries: Dict[str, Dict[int, int]] = {}
        self._loaded = False
        if path:
            self.load(path)

    # ── I/O ────────────────────────────────────────────────────────────────

    def load(self, path: str) -> None:
        """Load a book JSON file."""
        with open(path, "r") as f:
            data = json.load(f)
        self._meta = data.get("meta", {})
        self._entries = {
            k: {int(mk): mv for mk, mv in v.items()}
            for k, v in data.get("book", {}).items()
        }
        self._loaded = True

    def save(self, path: str | None = None) -> None:
        """Save the book to a JSON file."""
        dest = path or _DEFAULT_PATH
        data = {
            "meta": {
                "version": 1,
                "generated": time.strftime("%Y-%m-%d"),
                "entries": len(self._entries),
            },
            "book": {
                k: {str(mk): mv for mk, mv in v.items()}
                for k, v in self._entries.items()
            },
        }
        Path(dest).parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Saved {len(self._entries)} positions to {dest}")

    # ── API ────────────────────────────────────────────────────────────────

    def size(self) -> int:
        """Number of unique board states in the book."""
        return len(self._entries)

    def contains(self, board_str: str) -> bool:
        """Check if the book has an entry for this board state."""
        return board_str in self._entries

    def best_move(self, board_str: str, mark: int | None = None) -> Optional[int]:
        """Return the book's best column for *board_str*, optionally filtered by mark.

        If mark is given, returns the entry for that mark only.
        If mark is None, returns any mark's entry (first found).
        Returns None when no entry exists.
        """
        entry = self._entries.get(board_str)
        if entry is None:
            return None

        if mark is not None:
            return entry.get(mark)

        # No mark specified — return the first available
        if entry:
            return next(iter(entry.values()))
        return None

    # ── Build helpers ──────────────────────────────────────────────────────

    def add(self, board_str: str, mark: int, col: int) -> None:
        """Record (or overwrite) the best move for a board + mark."""
        if board_str not in self._entries:
            self._entries[board_str] = {}
        self._entries[board_str][mark] = col

    def add_if_new(self, board_str: str, mark: int, col: int) -> bool:
        """Add only if this board+mark pair isn't already in the book.

        Returns True if a new entry was added.
        """
        if board_str not in self._entries:
            self._entries[board_str] = {}
        if mark in self._entries[board_str]:
            return False
        self._entries[board_str][mark] = col
        return True

    # ── Static ─────────────────────────────────────────────────────────────

    @staticmethod
    def board_to_string(board) -> str:
        """Convert a flat board list to its canonical string key."""
        return "".join(str(c) for c in board)


# ── Book generation ───────────────────────────────────────────────────────────


def _generate_book(
    max_depth: int = 20,
    move_budget: float = 0.05,
    seed: int = 42,
    output: str = _DEFAULT_PATH,
    book_path: str | None = None,
    max_entries: int = 20000,
) -> None:
    """
    Generate an opening book by calling v2 search at each position.

    Algorithm:
      1. Start from the empty board.
      2. For each unique position in the game tree:
         - Call v2's search to find the best move for BOTH marks (1 and 2).
         - Record (board_string, mark -> best_col) in the book.
         - Branch: try up to 3 legal moves (or fewer if less than 3 are legal).
      3. Limit total depth to max_depth ply AND total entries to max_entries.

    Branching factor is limited to MAX_BRANCH=3 to keep book size manageable.
    At depth 5 with branching 3: ~243 leaf nodes, ~364 total positions.
    Each position requires ~2 v2 calls, each ~50ms → ~36 seconds total.

    The book naturally merges different move orders that reach the same board state.

    Args:
        max_depth: Maximum ply depth to explore.
        move_budget: Seconds per v2 search call.
        seed: Random seed for branch ordering.
        output: Output JSON path.
        book_path: Existing book to extend.
        max_entries: Hard cap on total unique entries.
    """
    MAX_BRANCH = 3  # max children per node
    rng = random.Random(seed)

    # ── Lazy import v2 (or v3 fallback) ──────────────────────────────────
    try:
        mod = importlib.import_module("connectx.bots.bitboard_ab_improved")
        v2_fn = mod.bitboard_ab_bot_fast_v2
        print("Using v2 (bitboard_ab_bot_fast_v2) for book generation.")
    except ImportError:
        try:
            mod = importlib.import_module(
                "connectx.bots.bitboard_ab_improved_v3"
            )
            v2_fn = mod.bitboard_ab_bot_fast_v3
            print("NOTE: v2 not found. Using v3 (bitboard_ab_bot_fast_v3) as proxy.")
        except ImportError:
            print("ERROR: No v2 or v3 bot found. Cannot build book.")
            sys.exit(1)

    book = OpeningBook()
    if book_path:
        book.load(book_path)

    total_positions = 0
    new_entries = 0

    def _v2_move(board, mark, deadline):
        """Call v2 search for the given board and mark."""
        try:
            legal = valid_moves(board, COLS)
            return v2_fn(board, mark, legal, move_deadline=deadline)
        except Exception:
            center = COLS // 2
            legal = valid_moves(board, COLS)
            return center if center in legal else (legal[0] if legal else 0)

    def record_position(board, depth):
        """Record v2's best move at this board state for both marks."""
        nonlocal total_positions, new_entries

        board_str = OpeningBook.board_to_string(board)

        for mark in (1, 2):
            deadline = time.time() + move_budget
            best_col = _v2_move(board, mark, deadline)
            legal = valid_moves(board, COLS)
            if best_col not in legal:
                best_col = legal[0] if legal else 0
            added = book.add_if_new(board_str, mark, best_col)
            if added:
                new_entries += 1
            total_positions += 1

    def expand(board, next_mark):
        """Generate up to MAX_BRANCH child positions from this board state."""
        legal = valid_moves(board, COLS)
        if not legal:
            return []

        # Shuffle to add variety to the explored positions
        shuffled = list(legal)
        rng.shuffle(shuffled)
        selected = shuffled[:MAX_BRANCH]

        children = []
        for col in selected:
            try:
                row = drop(board, col, next_mark, ROWS, COLS)
            except ValueError:
                continue

            child_str = OpeningBook.board_to_string(board)
            children.append((list(board), next_mark, col, row))
            un_drop(board, col, ROWS, COLS, row=row)

        return children

    def recurse(board, current_mark, depth):
        """DFS through the game tree, recording v2's best move at each node."""
        nonlocal total_positions, new_entries

        if depth > max_depth or new_entries >= max_entries:
            return

        board_str = OpeningBook.board_to_string(board)

        # Record position
        record_position(board, depth)

        if new_entries >= max_entries:
            return

        # Expand children
        next_mark = 3 - current_mark  # whose turn now

        # Check for win after current position (unlikely at record time)
        # Actually, we record BEFORE making a move, so no need to check wins here.

        children = expand(board, next_mark)
        for child_board, child_mark, col, row in children:
            if new_entries >= max_entries:
                break

            child_str = OpeningBook.board_to_string(child_board)

            # Check if already in book (via different path — dedup)
            if book.contains(child_str):
                continue

            recurse(child_board, child_mark, depth + 1)

    # ── Entry point: start from empty board ──────────────────────────────
    print(
        f"Generating opening book (max_depth={max_depth}, "
        f"move_budget={move_budget}s, seed={seed}, max_entries={max_entries})..."
    )

    empty_board = [EMPTY] * SIZE
    # depth=1: empty board, both marks to consider
    recurse(empty_board, 1, 1)

    print(
        f"\nGenerated {total_positions} positions, "
        f"{new_entries} unique book entries saved to {output}"
    )
    book.save(output)


# ── CLI ───────────────────────────────────────────────────────────────────────


def _cli_main() -> None:
    """CLI entry point: python -m connectx.bots.opening_book build|info ..."""
    parser = argparse.ArgumentParser(
        description="ConnectX Opening Book — build or inspect",
    )
    sub = parser.add_subparsers(dest="command")

    # --- build ---
    build_p = sub.add_parser("build", help="Generate an opening book")
    build_p.add_argument(
        "--output", "-o", default=_DEFAULT_PATH,
        help="Output JSON path (default: book.json)",
    )
    build_p.add_argument(
        "--max-depth", "-d", type=int, default=20,
        help="Maximum ply depth (default: 20)",
    )
    build_p.add_argument(
        "--move-budget", type=float, default=0.05,
        help="Seconds per v2 move (default: 0.05)",
    )
    build_p.add_argument(
        "--seed", type=int, default=42,
        help="Random seed for book generation (default: 42)",
    )
    build_p.add_argument(
        "--book-path", type=str, default=None,
        help="Existing book path to extend (default: none)",
    )
    build_p.add_argument(
        "--max-entries", type=int, default=20000,
        help="Hard cap on unique book entries (default: 20000)",
    )

    # --- info ---
    info_p = sub.add_parser("info", help="Show book statistics")
    info_p.add_argument(
        "path", nargs="?", default=_DEFAULT_PATH,
        help="Book JSON path (default: book.json)",
    )

    args = parser.parse_args()

    if args.command == "build":
        _generate_book(
            max_depth=args.max_depth,
            move_budget=args.move_budget,
            seed=args.seed,
            output=args.output,
            book_path=args.book_path,
            max_entries=args.max_entries,
        )
    elif args.command == "info":
        try:
            book = OpeningBook(args.path)
            meta = getattr(book, "_meta", {})
            print(f"Book path: {args.path}")
            print(f"Entries:   {book.size()}")
            if meta:
                for k, v in meta.items():
                    print(f"  {k}: {v}")
        except FileNotFoundError:
            print(f"File not found: {args.path}")
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    _cli_main()