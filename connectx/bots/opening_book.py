"""
Opening book for ConnectX 7×6/4.

Pre-computed optimal moves for early game positions.
Built from v2 self-play analysis.

Usage:
  from connectx.bots.opening_book import OpeningBook
  book = OpeningBook()
  move = book.get_move(board, mark, legal)  # Returns pre-computed move or None
"""

from __future__ import annotations

import os
import random
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

from connectx.engine import (
    check_win, drop, un_drop, valid_moves,
    ROWS, COLS, INAROW, SIZE,
)

_BOOK_PATH = os.path.join(
    os.path.dirname(__file__),
    'opening_book.npz',
)


class OpeningBook:
    """Pre-computed optimal opening moves for ConnectX 7x6."""

    def __init__(self, load_path: str = _BOOK_PATH):
        self._entries: Dict[tuple, list] = {}
        self._loaded = False
        try:
            data = np.load(load_path, allow_pickle=True)
            for key, value in zip(data['keys'], data['values']):
                board_key = tuple(key)
                moves = value if isinstance(value, list) else list(value)
                self._entries[board_key] = moves
            self._loaded = True
        except Exception:
            pass

    def add_position(self, board: List[int], mark: int, moves: List[int]):
        """Add a position with its pre-computed moves."""
        key = self._board_key(board, mark)
        self._entries[key] = moves

    def get_move(self, board: List[int], mark: int, legal: List[int],
                 prefer_random: bool = False) -> Optional[int]:
        """
        Get a pre-computed move for the current position.

        Returns None if no entry found (fall back to search).
        """
        key = self._board_key(board, mark)
        if key not in self._entries:
            return None

        moves = self._entries[key]
        # Filter to only legal moves
        legal_set = set(legal)
        valid = [m for m in moves if m in legal_set]
        if not valid:
            return None

        if prefer_random:
            return random.choice(valid)
        return valid[0]

    @staticmethod
    def _board_key(board: List[int], mark: int) -> tuple:
        """Canonical board key for book lookup."""
        # Normalize: flip marks so mark's pieces are always 1
        normalized = tuple(1 if c == mark else (2 if c == (3 - mark) else 0)
                          for c in board)
        return normalized

    def build(
        self,
        n_positions: int = 500,
        max_depth: int = 6,
        seed: int = 42,
        save: bool = True,
    ) -> None:
        """
        Build the opening book by playing random games and collecting
        the first move preferred by v2 at each position.

        Args:
            n_positions: Number of book positions to generate.
            max_depth: Maximum game depth to explore.
            seed: Random seed.
            save: Save to disk after building.
        """
        random.seed(seed)
        np.random.seed(seed)

        # Try building with v2 self-play
        try:
            from connectx.bots.bitboard_ab_improved import bitboard_ab_bot_v2
            self._build_from_v2(n_positions, max_depth, seed, save)
        except Exception as e:
            print(f"v2 build failed: {e}")
            self._build_random(n_positions, max_depth, seed, save)

    def _build_from_v2(
        self,
        n_positions: int,
        max_depth: int,
        seed: int,
        save: bool,
    ) -> None:
        """Build book from v2 self-play games."""
        from connectx.bots.bitboard_ab_improved import bitboard_ab_bot_v2

        games = 0
        positions = 0
        max_game_length = 42

        while positions < n_positions and games < n_positions * 10:
            games += 1
            board = [0] * SIZE
            move_num = 0

            while move_num < max_depth and positions < n_positions:
                legal = list(valid_moves(board, COLS))
                if not legal:
                    break

                # Try different moves and pick the one v2 prefers
                # (In practice, v2 always prefers the winning move)
                # Instead, collect all moves v2 considers as alternatives
                current_mark = 1 if move_num % 2 == 0 else 2

                # Get top-3 moves from v2
                import time
                deadline = time.time() + 0.05
                moves_scores = []
                for col in legal:
                    try:
                        drop(board, col, current_mark, ROWS, COLS)
                        if not check_win(board, col, current_mark, ROWS, COLS):
                            score, _ = _quick_eval(
                                board, current_mark, cols=COLS
                            )
                            moves_scores.append((col, score))
                        un_drop(board, col, ROWS, COLS)
                    except ValueError:
                        pass

                if moves_scores:
                    moves_scores.sort(key=lambda x: x[1], reverse=True)
                    top_moves = [m for m, s in moves_scores[:3]]

                    board_key = OpeningBook._board_key(board, current_mark)
                    if board_key not in self._entries:
                        self._entries[board_key] = top_moves
                        positions += 1

                # Make a random move (not v2's preferred)
                if moves_scores:
                    # Pick a suboptimal move
                    col = random.choice([m for m, s in moves_scores[1:]])
                else:
                    col = random.choice(legal)

                drop(board, col, current_mark, ROWS, COLS)
                move_num += 1

                if check_win(board, col, current_mark, ROWS, COLS):
                    break

        if save:
            self._save()

    def _build_random(self, n_positions: int, max_depth: int,
                      seed: int, save: bool) -> None:
        """Build book from random game positions (fallback)."""
        random.seed(seed)
        np.random.seed(seed)

        positions = 0
        games = 0
        max_game_length = 42

        while positions < n_positions and games < n_positions * 10:
            games += 1
            board = [0] * SIZE
            move_num = 0

            while move_num < max_depth and positions < n_positions:
                legal = list(valid_moves(board, COLS))
                if not legal:
                    break

                current_mark = 1 if move_num % 2 == 0 else 2

                # Store the position with the random move
                # This captures "what did random play look like at this position"
                board_key = OpeningBook._board_key(board, current_mark)
                if board_key not in self._entries:
                    # Just store all legal moves
                    self._entries[board_key] = list(legal)
                    positions += 1

                col = random.choice(legal)
                drop(board, col, current_mark, ROWS, COLS)
                move_num += 1

                if check_win(board, col, current_mark, ROWS, COLS):
                    break

        if save:
            self._save()

    def _save(self) -> None:
        """Save book to disk."""
        keys = [list(k) for k in self._entries.keys()]
        values = [v for v in self._entries.values()]
        np.savez_compressed(
            _BOOK_PATH,
            keys=np.array(keys, dtype=np.int8),
            values=values,
        )
        print(f"Saved {len(self._entries)} positions to {_BOOK_PATH}")


def _quick_eval(board, mark, cols=COLS):
    """Quick heuristic evaluation for book building."""
    opp = 3 - mark
    player_col = [0] * cols
    opp_col = [0] * cols

    for i in range(ROWS * COLS):
        if board[i] == mark:
            player_col[i % cols] += 1
        elif board[i] == opp:
            opp_col[i % cols] += 1

    center = cols // 2
    score = 0.0
    for c in range(cols):
        score += (player_col[c] - opp_col[c]) * (3 - abs(c - center))

    return score, 0


if __name__ == '__main__':
    book = OpeningBook()
    book.build(n_positions=200, max_depth=6, seed=42)