"""
ConnectX Gym — Universal Connect Four Environment

A benchmark-ready, deterministic ConnectX (7×6/4) environment for agent
development, tournament, and research.

Public API:
    from connectx import ConnectXEnv, play_game, play_game_seated

    # Environment usage
    env = ConnectXEnv()
    env.reset()
    state = env.step(3)  # drop in column 3

    # Direct game play
    record = play_game(random_bot, minimax_bot)
"""

from connectx.engine import (
    ROWS, COLS, INAROW, SIZE, EMPTY, PLAYER_1, PLAYER_2,
    make_board, valid_moves, legal_actions, drop, un_drop,
    check_win, is_terminal, count_moves, seat_reverse,
    all_winning_lines,
    ConnectXEnv,
    GameRecord,
    play_game,
    play_game_seated,
)

__all__ = [
    # Constants
    "ROWS", "COLS", "INAROW", "SIZE", "EMPTY",
    "PLAYER_1", "PLAYER_2",
    # Pure functions
    "make_board", "valid_moves", "legal_actions",
    "drop", "un_drop", "check_win",
    "is_terminal", "count_moves", "seat_reverse",
    "all_winning_lines",
    # Classes
    "ConnectXEnv", "GameRecord",
    # Game play
    "play_game", "play_game_seated",
]

__version__ = "0.1.0"