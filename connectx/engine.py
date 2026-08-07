"""
ConnectX Gym — Core Engine (7×6/4)

Official Kaggle ConnectX rules:
  - 7 columns, 6 rows, 4 in a row
  - 2 players: mark 1 (first) and mark 2 (second)
  - Board stored as flat array of 42 cells, row-major
  - Gravity: piece drops to lowest empty cell in column
  - Win: 4 in a row horizontally, vertically, or diagonally
  - Draw: board full with no winner

This module provides:
  - ConnectXEnv: full game environment with turn-by-turn play
  - GameRecord: replay-capable game record
  - Pure Python — no external dependencies
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional, Sequence

# ── Constants ──────────────────────────────────────────────────────────────────

ROWS: int = 6
COLS: int = 7
INAROW: int = 4
SIZE: int = ROWS * COLS  # 42
EMPTY: int = 0
PLAYER_1: int = 1
PLAYER_2: int = 2

# Direction vectors for win-check (row_delta, col_delta)
_DIRS: list[tuple[int, int]] = [
    (0, 1),   # horizontal
    (1, 0),   # vertical
    (1, 1),   # diagonal down-right
    (1, -1),  # diagonal down-left
]


# ── Pure functions ─────────────────────────────────────────────────────────────


def make_board(rows: int = ROWS, cols: int = COLS) -> list[int]:
    """Return a fresh empty board (flat list, row-major)."""
    return [EMPTY] * (rows * cols)


def row_col(index: int, cols: int = COLS) -> tuple[int, int]:
    """Convert flat index to (row, col)."""
    return index // cols, index % cols


def index(row: int, col: int, cols: int = COLS) -> int:
    """Convert (row, col) to flat index."""
    return row * cols + col


def valid_moves(board: Sequence[int], cols: int = COLS) -> list[int]:
    """Return list of column indices where a drop is legal."""
    # A column is legal if its top cell (row 0) is empty.
    # Pieces stack from the bottom (gravity), so if the top cell
    # is occupied, the entire column is full. If it's empty,
    # there's at least one empty slot below.
    return [c for c in range(cols) if board[c] == EMPTY]


def legal_actions(board: Sequence[int], cols: int = COLS) -> list[int]:
    """Alias for valid_moves — public API name."""
    return valid_moves(board, cols)


def drop(board: list[int], col: int, mark: int,
         rows: int = ROWS, cols: int = COLS) -> int:
    """
    Drop a piece into ``col`` on ``board`` with gravity.

    The piece falls to the lowest empty row in the column.
    Returns the row where the piece landed.
    Raises ValueError on invalid column (full or out-of-bounds).
    """
    if not (0 <= col < cols):
        raise ValueError(f"Column {col} out of bounds [0, {cols})")
    if board[col] != EMPTY:
        raise ValueError(f"Column {col} is full")
    # Gravity: find the lowest empty row
    for r in range(rows - 1, -1, -1):
        if board[index(r, col, cols)] == EMPTY:
            board[index(r, col, cols)] = mark
            return r
    raise ValueError(f"Column {col} is full (exhausted all rows)")


def un_drop(board: list[int], col: int, rows: int = ROWS,
           cols: int = COLS, row: int | None = None) -> int:
    """
    Remove a piece from ``col`` at ``row``.

    If ``row`` is given, clears that exact row.
    If ``row`` is None, clears the lowest non-empty cell (original behavior).
    Returns the (row, col) of the removed piece.
    Raises ValueError if the column is empty or the specified row is not occupied.
    """
    if row is not None:
        if board[index(row, col, cols)] == EMPTY:
            raise ValueError(f"Column {col} row {row} is empty")
        board[index(row, col, cols)] = EMPTY
        return row, col
    for r in range(rows - 1, -1, -1):
        if board[index(r, col, cols)] != EMPTY:
            board[index(r, col, cols)] = EMPTY
            return r, col
    raise ValueError(f"Column {col} is empty")


def _in_a_row(board: Sequence[int], start_row: int, start_col: int,
              dr: int, dc: int, mark: int, inarow: int,
              rows: int = ROWS, cols: int = COLS) -> bool:
    """Check if *inarow* consecutive cells starting at (start_row, start_col)
    in direction (dr, dc) all equal ``mark``."""
    count = 0
    r, c = start_row, start_col
    for _ in range(inarow):
        if 0 <= r < rows and 0 <= c < cols and board[index(r, c, cols)] == mark:
            count += 1
        else:
            break
        r += dr
        c += dc
    return count == inarow


def check_win(board: Sequence[int], col: int, mark: int,
              rows: int = ROWS, cols: int = COLS,
              inarow: int = INAROW) -> bool:
    """
    After dropping ``mark`` at the top of ``col``, check if it won.

    Optimised: only check lines passing through the dropped piece's position.
    Search from top to find the first piece — handles both gravity-compliant
    boards and pre-filled board states used in evaluation.
    """
    # Find the row where the piece landed (topmost non-empty for this mark)
    placed_row = None
    for r in range(rows):
        if board[index(r, col, cols)] == mark:
            placed_row = r
            break
    if placed_row is None:
        return False

    for dr, dc in _DIRS:
        if _in_a_row(board, placed_row, col, dr, dc, mark, inarow, rows, cols):
            return True
        if _in_a_row(board, placed_row, col, -dr, -dc, mark, inarow, rows, cols):
            return True

    return False


def is_terminal(board: Sequence[int], rows: int = ROWS,
                cols: int = COLS) -> bool:
    """Return True if the board is full (draw position)."""
    return all(cell != EMPTY for cell in board)


def count_moves(board: Sequence[int]) -> int:
    """Count the number of pieces already on the board."""
    return sum(1 for cell in board if cell != EMPTY)


def seat_reverse(board: Sequence[int], cols: int = COLS,
                 rows: int = ROWS) -> list[int]:
    """
    Return a copy of the board with columns reversed (mirror horizontally).
    This is used for symmetric evaluation.
    """
    result = list(board)
    for r in range(rows):
        left = index(r, 0, cols)
        right = index(r, cols - 1, cols)
        result[left], result[right] = result[right], result[left]
        mid = 1
        while left + mid < right - mid + 1:
            lc = index(r, mid, cols)
            rc = index(r, cols - 1 - mid, cols)
            result[lc], result[rc] = result[rc], result[lc]
            mid += 1
    return result


# ── Game record ────────────────────────────────────────────────────────────────


@dataclass
class GameRecord:
    """Immutable record of a complete ConnectX game."""
    board_init: list[int]  # initial board state
    board_full: list[int]  # final board state
    moves: list[tuple[int, int, int]]  # (turn, col, mark) tuples
    winner: int  # 0=draw, 1=player1, 2=player2
    terminal_reason: str  # "win", "draw", "timeout", "invalid", "crash"
    player1_action: list[int]  # columns played by player 1
    player2_action: list[int]  # columns played by player 2
    metadata: dict = field(default_factory=dict)


# ── Environment ────────────────────────────────────────────────────────────────


class ConnectXEnv:
    """
    Turn-based ConnectX environment.

    Usage:
        env = ConnectXEnv()
        state = env.reset()
        action = bot1(state)
        state = env.step(action)  # returns (board, player, done, info)
    """

    def __init__(self, rows: int = ROWS, cols: int = COLS,
                 inarow: int = INAROW) -> None:
        self.rows = rows
        self.cols = cols
        self.inarow = inarow
        self.reset()

    @property
    def board(self) -> list[int]:
        """Current board state (mutable list)."""
        return self._board

    @property
    def current_player(self) -> int:
        """Player whose turn it is: 1 or 2."""
        return self._player

    @property
    def move_number(self) -> int:
        """Number of moves played so far (0-indexed)."""
        return self._move_number

    def reset(self, board: Optional[Sequence[int]] = None) -> list[int]:
        """
        Reset the environment to the initial state (or a custom board).

        Returns the board.
        """
        if board is not None:
            self._board = list(board)
        else:
            self._board = make_board(self.rows, self.cols)
        self._player = PLAYER_1
        self._move_number = 0
        self._terminal = False
        self._winner = EMPTY
        self._terminal_reason = ""
        self._actions: list[tuple[int, int]] = []  # (move_num, col)
        self._player1_actions: list[int] = []
        self._player2_actions: list[int] = []
        return self._board

    def step(self, action: int) -> dict:
        """
        Execute an action (column index) for the current player.

        Returns a dict with keys:
            board: current board state
            player: who just moved
            done: True if game is over
            info: dict with additional metadata
        """
        if self._terminal:
            raise RuntimeError("Game is already terminal. Call reset().")

        # Validate action
        if not (0 <= action < self.cols):
            raise ValueError(f"Action {action} out of bounds [0, {self.cols})")

        valid = valid_moves(self._board, self.cols)
        if action not in valid:
            raise ValueError(f"Action {action} is invalid (column is full)")

        # Place the piece
        row = drop(self._board, action, self._player, self.rows, self.cols)

        # Record
        self._actions.append((self._move_number, action))
        if self._player == PLAYER_1:
            self._player1_actions.append(action)
        else:
            self._player2_actions.append(action)

        self._move_number += 1

        # Check win
        if check_win(self._board, action, self._player,
                     self.rows, self.cols, self.inarow):
            self._terminal = True
            self._winner = self._player
            self._terminal_reason = "win"
            return self._info()

        # Check draw
        if is_terminal(self._board, self.rows, self.cols):
            self._terminal = True
            self._winner = EMPTY
            self._terminal_reason = "draw"
            return self._info()

        # Switch player
        self._player = PLAYER_2 if self._player == PLAYER_1 else PLAYER_1
        # Also update after step() call — the engine tracks whose turn it IS after this move
        # (already done above, but we need to ensure it happens)
        return self._info()

    def _info(self) -> dict:
        """Build the info dict returned by step()."""
        return {
            "board": list(self._board),
            "player": self._player,
            "move_number": self._move_number,
            "done": self._terminal,
            "terminal_reason": self._terminal_reason,
            "winner": self._winner,
        }

    def legal_moves(self) -> list[int]:
        """Return list of legal column indices."""
        return valid_moves(self._board, self.cols)

    def is_done(self) -> bool:
        """Return True if the game has ended."""
        return self._terminal

    def winner(self) -> int:
        """Return the winner: 0=draw, 1=player1, 2=player2."""
        return self._winner

    def terminal_reason(self) -> str:
        """Return the reason the game ended."""
        return self._terminal_reason

    def to_record(self) -> GameRecord:
        """Convert the current state to a GameRecord."""
        return GameRecord(
            board_init=make_board(self.rows, self.cols),
            board_full=list(self._board),
            moves=list(
                (mn, col, PLAYER_1 if mn % 2 == 0 else PLAYER_2)
                for mn, col in self._actions
            ),
            winner=self._winner,
            terminal_reason=self._terminal_reason,
            player1_action=list(self._player1_actions),
            player2_action=list(self._player2_actions),
        )


# ── Paired play ────────────────────────────────────────────────────────────────


def play_game(
    bot1_fn: Callable,
    bot2_fn: Callable,
    rows: int = ROWS,
    cols: int = COLS,
    inarow: int = INAROW,
    seat: int = 1,
) -> GameRecord:
    """
    Play a complete game between two bots.

    Args:
        bot1_fn: callable(board) -> int (column index)
        bot2_fn: callable(board) -> int (column index)
        rows, cols, inarow: board dimensions
        seat: 1 = bot1 plays first, 2 = bot2 plays first

    Returns:
        GameRecord with full game history.
    """
    env = ConnectXEnv(rows, cols, inarow)
    env.reset()

    # Assign first-player and second-player bots
    if seat == 1:
        first_fn, second_fn = bot1_fn, bot2_fn
    else:
        first_fn, second_fn = bot2_fn, bot1_fn

    try:
        while not env.is_done():
            if env.current_player == PLAYER_1:
                bot_fn = first_fn
            else:
                bot_fn = second_fn

            legal = env.legal_moves()
            action = bot_fn(env.board, env.current_player, legal, cols)

            # Validate bot output
            if action not in legal:
                raise ValueError(
                    f"Bot returned invalid action {action} "
                    f"(legal: {legal})"
                )

            env.step(action)
    except Exception as exc:
        # Bot crashed — treat as terminal
        env._terminal = True
        env._terminal_reason = "crash"
        env._winner = PLAYER_2 if env.current_player == PLAYER_1 else PLAYER_1

    return env.to_record()


def play_game_seated(
    bot1: Callable,
    bot2: Callable,
    rows: int = ROWS,
    cols: int = COLS,
    inarow: int = INAROW,
) -> tuple[GameRecord, GameRecord]:
    """
    Play two seat-reversed games between bot1 and bot2.

    Returns:
        (game_1st, game_2nd) — game where bot1 is first, then bot1 is second.
    """
    g1 = play_game(bot1, bot2, rows, cols, inarow, seat=1)
    g2 = play_game(bot1, bot2, rows, cols, inarow, seat=2)
    return g1, g2


# ── Helper: check all winning lines ────────────────────────────────────────────


def all_winning_lines(rows: int = ROWS, cols: int = COLS,
                      inarow: int = INAROW) -> list[tuple[int, ...]]:
    """
    Return all winning lines on the board as tuples of flat indices.

    Used for precomputed evaluation and solver integration.
    """
    lines: list[tuple[int, ...]] = []
    for r in range(rows):
        for c in range(cols):
            # Horizontal
            if c + inarow <= cols:
                line = tuple(index(r, c + k, cols) for k in range(inarow))
                lines.append(line)
            # Vertical
            if r + inarow <= rows:
                line = tuple(index(r + k, c, cols) for k in range(inarow))
                lines.append(line)
            # Diagonal down-right
            if r + inarow <= rows and c + inarow <= cols:
                line = tuple(index(r + k, c + k, cols) for k in range(inarow))
                lines.append(line)
            # Diagonal down-left
            if r + inarow <= rows and c - inarow + 1 >= 0:
                line = tuple(index(r + k, c - k, cols) for k in range(inarow))
                lines.append(line)
    return tuple(lines)