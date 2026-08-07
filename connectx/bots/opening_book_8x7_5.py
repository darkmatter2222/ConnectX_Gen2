"""Opening book for bitboard_ab_bot_8x7_5.

Pre-computes optimal moves for early-game positions using the 8×7/5
alpha-beta bot's search. During play, the bot checks the book first
for instant move selection.

Board encoding: flat board string where each digit is the row index
of the highest piece in that column (0 = bottom row, no piece = '0').

Usage:
    # Generate the book:
    python connectx/bots/opening_book_8x7_5.py --build --max-depth 10

    # Or import in code:
    from connectx.bots.opening_book_8x7_5 import OpeningBook_8x7_5
    book = OpeningBook_8x7_5("book_8x7_5.json")
    move = book.best_move(board, mark, legal)
"""

from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, '.')
import connectx
from connectx.bots.bitboard_ab_8x7_5 import (
    bitboard_ab_bot_8x7_5 as _ab,
    ROWS, COLS, INAROW, SIZE,
)

_DEFAULT_PATH = "book_8x7_5.json"
ROWS_8x7_5 = ROWS
COLS_8x7_5 = COLS
INAROW_8x7_5 = INAROW


def _board_key(board: List[int]) -> str:
    """Convert board to compact string key for book lookup."""
    return ''.join(str(x) for x in board)


def _best_move(bot_board: List[int], mark: int, legal: List[int], deadline: float = 0.1) -> int:
    """Get the AB bot's best move with a time limit.

    Short deadlines are fine for opening book positions — even shallow
    search (depth 2-4) produces optimal early-game moves.
    """
    try:
        return _ab(bot_board, mark, legal, COLS_8x7_5, move_deadline=deadline)
    except Exception:
        return legal[0] if legal else 0


def build_book(max_depth: int = 10, branching: int = 5, timeout_s: float = 300.0) -> dict:
    """Build the 8×7/5 opening book.

    Explores positions via DFS from the empty board. At each position
    (with pieces placed by both sides), runs the AB bot and records
    the best move for both marks.

    Args:
        max_depth: Maximum ply depth to explore.
        branching: Number of candidate moves to try at each node.
        timeout_s: Maximum build time in seconds.

    Returns:
        Dict of { board_key: { mark: best_col } }.
    """
    start_time = time.time()
    book: Dict[str, Dict[int, int]] = {}
    nodes_explored = 0

    def dfs(board: List[int], mark: int, pieces: int, depth: int):
        nonlocal nodes_explored
        elapsed = time.time() - start_time
        if elapsed > timeout_s:
            return
        if depth > max_depth:
            return

        board_key = _board_key(board)

        # Store book entry if we have pieces and haven't stored this yet
        if pieces > 0 and board_key not in book:
            legal = connectx.valid_moves(board, COLS_8x7_5)
            if not legal:
                return

            best_moves: Dict[int, int] = {}
            remaining = max(0.05, timeout_s - elapsed)

            # Search for mark
            try:
                m1 = _best_move(board, mark, legal, min(0.3, remaining))
                if m1 in legal:
                    best_moves[mark] = m1
            except Exception:
                pass

            opp = 3 - mark
            try:
                m2 = _best_move(board, opp, legal, min(0.3, remaining))
                if m2 in legal:
                    best_moves[opp] = m2
            except Exception:
                pass

            if best_moves:
                book[board_key] = best_moves

        if time.time() - start_time > timeout_s:
            return

        # Generate children: explore branching candidates
        legal = connectx.valid_moves(board, COLS_8x7_5)
        if not legal:
            return

        # Sort by center preference
        center = COLS_8x7_5 // 2
        ordered = sorted(legal, key=lambda c: abs(c - center))
        candidates = ordered[:branching]

        for col in candidates:
            row = connectx.drop(board, col, mark, ROWS_8x7_5, COLS_8x7_5)
            nodes_explored += 1
            dfs(board, 3 - mark, pieces + 1, depth + 1)
            connectx.un_drop(board, col, ROWS_8x7_5, COLS_8x7_5, row=row)

    board = connectx.make_board(ROWS_8x7_5, COLS_8x7_5)
    dfs(board, 1, 0, 0)
    return book


def save_book(book: dict, path: str = _DEFAULT_PATH) -> None:
    """Save book to JSON file."""
    Path(path).write_text(json.dumps(book, indent=2))
    print(f"Saved {len(book):,} entries to {path}")


def load_book(path: str = _DEFAULT_PATH) -> dict:
    """Load book from JSON file."""
    return json.loads(Path(path).read_text())


class OpeningBook_8x7_5:
    """Pre-computed optimal opening moves for ConnectX 8×7/5."""

    def __init__(self, path: str | None = None) -> None:
        self._entries: Dict[str, Dict[int, int]] = {}
        self._loaded = False
        if path:
            self.load(path)

    def load(self, path: str) -> None:
        """Load book from JSON file."""
        with open(path) as f:
            self._entries = json.load(f)
        self._loaded = True

    def best_move(self, board: List[int], mark: int, legal: Optional[List[int]] = None) -> Optional[int]:
        """Get best move from book for the given board state and mark.

        Args:
            board: 56-cell board list.
            mark: Current player's mark (1 or 2).
            legal: Optional legal moves list (for validation).

        Returns:
            Best move column index, or None if no book entry found.
        """
        if not self._loaded:
            return None

        key = _board_key(board)
        if key in self._entries:
            entries = self._entries[key]
            # Handle both int and str keys (JSON parses numbers as strings)
            mark_key = str(mark) if not isinstance(mark, str) else mark
            if mark_key in entries:
                move = entries[mark_key]
                if legal is None or move in legal:
                    return move
        return None

    def in_book(self, board: List[int]) -> bool:
        """Check if board state is in the book."""
        if not self._loaded:
            return False
        return _board_key(board) in self._entries


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Build 8×7/5 opening book')
    parser.add_argument('--max-depth', type=int, default=8,
                        help='Maximum ply depth (default: 8)')
    parser.add_argument('--branching', type=int, default=5,
                        help='Number of candidate moves per node (default: 5)')
    parser.add_argument('--timeout', type=float, default=120.0,
                        help='Max build time in seconds (default: 120)')
    parser.add_argument('--output', type=str, default=_DEFAULT_PATH,
                        help='Output file path (default: book_8x7_5.json)')
    parser.add_argument('--info', action='store_true',
                        help='Show book info and exit')
    args = parser.parse_args()

    if args.info:
        try:
            book = load_book(args.output)
            print(f"Book size: {len(book):,} entries")
            empty_key = '0' * SIZE
            if empty_key in book:
                print(f"Empty board: {book[empty_key]}")
            else:
                print("No empty board entry")
        except FileNotFoundError:
            print(f"Book not found: {args.output}")
            sys.exit(1)
    else:
        print(f"Building 8×7/5 opening book...")
        print(f"  Board: {COLS_8x7_5}×{ROWS_8x7_5}/{INAROW_8x7_5} ({SIZE} cells)")
        print(f"  max_depth={args.max_depth}, branching={args.branching}, timeout={args.timeout}s")

        start = time.time()
        book = build_book(args.max_depth, args.branching, args.timeout)
        elapsed = time.time() - start

        save_book(book, args.output)
        print(f"  Nodes explored: {sum(len(v) for v in book.values()):,}")
        print(f"  Time: {elapsed:.1f}s")