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
from connectx.bots.bitboard_ab import bitboard_ab_bot, bitboard_ab_bot_fast
from connectx.bots.bitboard_ab_improved import bitboard_ab_bot_v2, bitboard_ab_bot_fast_v2
from connectx.bots.bitboard_ab_8x7_5 import bitboard_ab_bot_8x7_5, bitboard_ab_bot_fast_8x7_5
from connectx.bots.bitboard_ab_8x7_5_deep import (
    bitboard_ab_bot_8x7_5_deep,
    bitboard_ab_bot_8x7_5_fast_deep,
)
from connectx.bots.mcts import mcts_bot, mcts_bot_fast, mcts_bot_value, mcts_bot_heuristic
from connectx.bots.mcts_puct import mcts_puct_bot
from connectx.bots.mcts_8x7_5 import (
    mcts_bot_8x7_5,
    mcts_bot_fast_8x7_5,
    mcts_bot_heuristic_8x7_5,
)
from connectx.bots.mcts_8x7_5_puct import (
    mcts_puct_bot_8x7_5,
    mcts_puct_bot_fast_8x7_5,
)
from connectx.bots.mcts_8x7_5_tactical import (
    mcts_tactical_bot_8x7_5,
    mcts_tactical_bot_fast_8x7_5,
)
from connectx.bots.mcts_8x7_5_ab import (
    mcts_ab_bot_8x7_5,
    mcts_ab_bot_fast_8x7_5,
)
from connectx.bots.bitboard_ab_8x7_5_v2 import (
    bitboard_ab_bot_8x7_5_v2,
    bitboard_ab_bot_fast_8x7_5_v2,
)
from connectx.bots.opening_book_8x7_5 import (
    OpeningBook_8x7_5,
    build_book,
)
from connectx.bots.bitboard_ab_8x7_5_booked import (
    bitboard_ab_bot_8x7_5_booked,
    bitboard_ab_bot_fast_8x7_5_booked,
)

__all__ = [
    "random_bot",
    "win_seek_block_bot",
    "shallow_minimax_bot",
    "depth2_minimax_bot",
    "bitboard_ab_bot",
    "bitboard_ab_bot_fast",
    "bitboard_ab_bot_v2",
    "bitboard_ab_bot_fast_v2",
    "bitboard_ab_bot_8x7_5",
    "bitboard_ab_bot_fast_8x7_5",
    "bitboard_ab_bot_8x7_5_deep",
    "bitboard_ab_bot_8x7_5_fast_deep",
    "mcts_bot",
    "mcts_bot_fast",
    "mcts_bot_value",
    "mcts_bot_heuristic",
    "mcts_puct_bot",
    "mcts_bot_8x7_5",
    "mcts_bot_fast_8x7_5",
    "mcts_bot_heuristic_8x7_5",
    "mcts_puct_bot_8x7_5",
    "mcts_puct_bot_fast_8x7_5",
    "mcts_tactical_bot_8x7_5",
    "mcts_tactical_bot_fast_8x7_5",
    "mcts_ab_bot_8x7_5",
    "mcts_ab_bot_fast_8x7_5",
    "bitboard_ab_bot_8x7_5_booked",
    "bitboard_ab_bot_fast_8x7_5_booked",
    "bitboard_ab_bot_8x7_5_v2",
    "bitboard_ab_bot_fast_8x7_5_v2",
    "OpeningBook_8x7_5",
]