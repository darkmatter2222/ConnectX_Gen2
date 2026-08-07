"""
ConnectX Baseline Bots

Built-in reference bots for tournament evaluation.
Each bot is a callable with this signature:

    def bot(board: Sequence[int], mark: int, legal: Sequence[int], cols: int) -> int:
        ...
"""

from connectx.bots.random_bot import random_bot
from connectx.bots.win_seek_block import win_seek_block_bot
from connectx.bots.shallow_minimax import shallow_minimax_bot, depth2_minimax_bot

__all__ = [
    "random_bot",
    "win_seek_block_bot",
    "shallow_minimax_bot",
    "depth2_minimax_bot",
]