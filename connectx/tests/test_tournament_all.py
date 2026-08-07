"""Full leaderboard tournament: all 8 bots, all pairs, seat-reversed 20-game matchups.

Usage: python connectx/tests/test_tournament_all.py [--games N]
"""
import sys
import itertools
import random
from dataclasses import dataclass, field

sys.path.insert(0, '.')
import connectx
from connectx.bots.random_bot import random_bot


@dataclass
class MatchupResult:
    p1_name: str
    p2_name: str
    p1_wins: int = 0
    p2_wins: int = 0
    draws: int = 0
    games: int = 0
    p1_invalid: int = 0
    p2_invalid: int = 0
    notes: list = field(default_factory=list)


def get_bot(name):
    """Get a bot function by name."""
    if name == 'random':
        return random_bot
    if name == 'bitboard_ab':
        from connectx.bots.bitboard_ab import bitboard_ab_bot
        return bitboard_ab_bot
    if name == 'bitboard_ab_book':
        from connectx.bots.bitboard_ab_book import bitboard_ab_bot_v2_book
        return bitboard_ab_bot_v2_book
    if name == 'bitboard_ab_ensemble':
        from connectx.bots.bitboard_ab_ensemble import bitboard_ab_ensemble_bot
        return bitboard_ab_ensemble_bot
    if name == 'bitboard_ab_improved':
        from connectx.bots.bitboard_ab_improved import bitboard_ab_bot_v2
        return bitboard_ab_bot_v2
    if name == 'bitboard_ab_improved_v3':
        from connectx.bots.bitboard_ab_improved_v3 import bitboard_ab_bot_v3
        return bitboard_ab_bot_v3
    if name == 'bitboard_ab_value':
        from connectx.bots.bitboard_ab_value import bitboard_ab_bot_vvalue
        return bitboard_ab_bot_vvalue
    if name == 'bitboard_ab_with_nn':
        from connectx.bots.bitboard_ab_with_nn import bitboard_ab_nn_bot
        return bitboard_ab_nn_bot
    if name == 'mcts_bc':
        from connectx.bots.mcts_bc import mcts_bc_bot
        return mcts_bc_bot
    raise ValueError(f"Unknown bot: {name}")


BOT_NAMES = [
    'bitboard_ab', 'bitboard_ab_book', 'bitboard_ab_ensemble',
    'bitboard_ab_improved', 'bitboard_ab_improved_v3',
    'bitboard_ab_value', 'bitboard_ab_with_nn', 'mcts_bc',
]


def play_game(p1_name, p2_name, seed, time_limit=0.5):
    """Play one game. Returns ('P1', p1_invalid, p2_invalid) or ('draw', ...) or ('P2', ...)."""
    random.seed(seed)
    p1_fn = get_bot(p1_name)
    p2_fn = get_bot(p2_name)

    board = connectx.make_board(7, 6)
    invalid_count = [0, 0]

    for turn in range(42):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 7)
        if not legal:
            break

        bot_idx = 0 if turn % 2 == 0 else 1
        fn = p1_fn if bot_idx == 0 else p2_fn

        try:
            action = fn(board, mark, legal, 7, time_limit, 0.0, seed + turn)
        except Exception:
            action = random.choice(legal) if legal else 0

        if action not in legal:
            invalid_count[bot_idx] += 1
            action = random.choice(legal) if legal else 0

        connectx.drop(board, action, mark)

        # Check if this move won
        if connectx.check_win(board, action, mark, 6, 7, 4):
            if mark == 1:
                return 'P1', invalid_count[0], invalid_count[1]
            else:
                return 'P2', invalid_count[0], invalid_count[1]

    # Check if board is full (draw)
    if all(cell != 0 for cell in board):
        return 'draw', invalid_count[0], invalid_count[1]

    return 'draw', invalid_count[0], invalid_count[1]


def run_matchup(p1_name, p2_name, num_games=20, time_limit=0.5):
    """Run a seat-reversed matchup."""
    results = MatchupResult(p1_name=p1_name, p2_name=p2_name)
    for i in range(num_games):
        outcome, inv1, inv2 = play_game(p1_name, p2_name, seed=i * 7 + 3, time_limit=time_limit)
        results.games += 1
        if outcome == 'P1':
            results.p1_wins += 1
        elif outcome == 'P2':
            results.p2_wins += 1
        else:
            results.draws += 1
        results.p1_invalid += inv1
        results.p2_invalid += inv2
    return results


def main():
    num_games = 20
    if '--games' in sys.argv:
        idx = sys.argv.index('--games')
        if idx + 1 < len(sys.argv):
            num_games = int(sys.argv[idx + 1])

    print(f"Full Leaderboard Tournament: {num_games} games per matchup")
    print(f"Bots: {', '.join(BOT_NAMES)}")
    print(f"Time limit: {num_games} games, {len(BOT_NAMES) * (len(BOT_NAMES) - 1) // 2} matchups")
    print("=" * 80)

    standings = {}
    for name in BOT_NAMES:
        standings[name] = {'wins': 0, 'losses': 0, 'draws': 0, 'games': 0, 'invalid': 0}

    matchups = list(itertools.combinations(BOT_NAMES, 2))
    total = len(matchups)

    for i, (p1, p2) in enumerate(matchups):
        print(f"\n[{i+1}/{total}] {p1} vs {p2} ({num_games} games each direction)")

        # P1 as mark 1, P2 as mark 2
        r1 = run_matchup(p1, p2, num_games)
        # P2 as mark 1, P1 as mark 2 (seat-reversed)
        r2 = run_matchup(p2, p1, num_games)

        # Combine results
        combined = MatchupResult(
            p1_name=p1,
            p2_name=p2,
            p1_wins=r1.p1_wins + r2.p2_wins,
            p2_wins=r1.p2_wins + r2.p1_wins,
            draws=r1.draws + r2.draws,
            games=r1.games + r2.games,
            p1_invalid=r1.p1_invalid + r2.p2_invalid,
            p2_invalid=r1.p2_invalid + r2.p1_invalid,
        )

        # Update standings
        standings[p1]['wins'] += combined.p1_wins
        standings[p1]['losses'] += combined.p2_wins
        standings[p1]['draws'] += combined.draws
        standings[p1]['games'] += combined.games
        standings[p1]['invalid'] += combined.p1_invalid

        standings[p2]['wins'] += combined.p2_wins
        standings[p2]['losses'] += combined.p1_wins
        standings[p2]['draws'] += combined.draws
        standings[p2]['games'] += combined.games
        standings[p2]['invalid'] += combined.p2_invalid

        pct = combined.p1_wins / combined.games * 100 if combined.games > 0 else 0
        print(f"  {p1}: {combined.p1_wins}W {combined.p2_wins}L {combined.draws}D ({combined.games}g, {combined.p1_invalid} inv)")
        print(f"  {p2}: {combined.p2_wins}W {combined.p1_wins}L {combined.draws}D ({combined.games}g, {combined.p2_invalid} inv)")
        print(f"  -> {p1} win%: {pct:.0f}%")

    # Print standings table
    print("\n" + "=" * 80)
    print("STANDINGS")
    print("=" * 80)
    print(f"{'Bot':<25} {'W':>4} {'L':>4} {'D':>4} {'G':>4} {'Win%':>6} {'Inv':>5}")
    print("-" * 80)

    sorted_standings = sorted(standings.items(), key=lambda x: x[1]['wins'], reverse=True)
    for name, s in sorted_standings:
        win_pct = s['wins'] / s['games'] * 100 if s['games'] > 0 else 0
        print(f"{name:<25} {s['wins']:>4} {s['losses']:>4} {s['draws']:>4} {s['games']:>4} {win_pct:>5.0f}% {s['invalid']:>5}")

    print("=" * 80)

    # Check for invalid moves
    total_invalid = sum(s['invalid'] for s in standings.values())
    total_games = sum(s['games'] for s in standings.values())
    if total_invalid > 0:
        print(f"\nWARNING: {total_invalid} invalid moves detected across all bots!")
        for name, s in standings.items():
            if s['invalid'] > 0:
                print(f"  {name}: {s['invalid']} invalid moves")
    else:
        print(f"\nAll valid moves — 0 invalid across all {total_games} games.")


if __name__ == '__main__':
    main()