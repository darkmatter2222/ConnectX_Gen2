"""Smoke test all bitboard bots for valid moves."""
import sys
sys.path.insert(0, '.')
import connectx
import random
import importlib

BOT_MODULES = {
    'bitboard_ab': ('bitboard_ab', 'bitboard_ab_bot'),
    'bitboard_ab_book': ('bitboard_ab_book', 'bitboard_ab_bot_v2_book'),
    'bitboard_ab_ensemble': ('bitboard_ab_ensemble', 'bitboard_ab_ensemble_bot'),
    'bitboard_ab_improved': ('bitboard_ab_improved', 'bitboard_ab_bot_v2'),
    'bitboard_ab_improved_v3': ('bitboard_ab_improved_v3', 'bitboard_ab_bot_v3'),
    'bitboard_ab_value': ('bitboard_ab_value', 'bitboard_ab_bot_vvalue'),
    'bitboard_ab_with_nn': ('bitboard_ab_with_nn', 'bitboard_ab_nn_bot'),
    'mcts_bc': ('mcts_bc', 'mcts_bc_bot'),
}

RANDOM_FNS = [
    ('connectx.bots.random_bot', 'random_bot'),
    ('connectx.bots.random', 'random_bot'),
]


def get_random_bot():
    """Try to get a random bot function."""
    for mod_name, fn_name in RANDOM_FNS:
        try:
            mod = __import__(mod_name, fromlist=[fn_name])
            return getattr(mod, fn_name)
        except (ImportError, AttributeError):
            continue
    return None


def smoke_test_bot(bot_module, bot_fn_name, name):
    """Test a bot for valid moves across 5 games."""
    try:
        mod = importlib.import_module(f'connectx.bots.{bot_module}')
        bot_fn = getattr(mod, bot_fn_name)
    except Exception as e:
        print(f'  SKIP: {name} ({e})')
        return 0, 0

    random_bot = get_random_bot()
    if random_bot is None:
        print(f'  SKIP: {name} (no random bot found)')
        return 0, 0

    invalid = 0
    total = 0
    for game in range(5):
        random.seed(game)
        board = connectx.make_board(7, 6)
        for turn in range(42):
            mark = 1 if turn % 2 == 0 else 2
            legal = connectx.valid_moves(board, 7)
            if not legal:
                break
            if mark == 1:
                try:
                    action = bot_fn(board, 1, legal, 7, 0.5, 0.0)
                except Exception as e:
                    print(f'    Game {game}: ERROR {e}')
                    invalid += 2
                    break
            else:
                try:
                    action = random_bot(legal, 1, 7, 6, 4, 0.5, 0.0)
                except Exception:
                    action = random.choice(legal)
            if action not in legal:
                print(f'    Game {game}: INVALID {action} (legal={legal})')
                invalid += 1
            total += 1
            connectx.drop(board, action, mark)

    return total, invalid


if __name__ == '__main__':
    total_all = 0
    invalid_all = 0
    for name, (mod, fn) in BOT_MODULES.items():
        t, inv = smoke_test_bot(mod, fn, name)
        total_all += t
        invalid_all += inv
        status = 'PASS' if inv == 0 else 'FAIL'
        print(f'{name}: {t} moves, {inv} invalid [{status}]')

    print(f'\nTotal: {total_all} moves, {invalid_all} invalid')
    if invalid_all == 0:
        print('ALL BOTS PASS smoke test.')
    else:
        print(f'{invalid_all} invalid moves detected!')
        sys.exit(1)