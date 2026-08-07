"""
ConnectX Tournament System — Paired evaluation and leaderboards.

Provides:
    - BotRegistry: manages named bots
    - Tournament: runs paired matches between registered bots
    - Leaderboard: maintains and queries performance stats
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Sequence

from connectx.engine import play_game, play_game_seated, GameRecord


# ── Bot Registry ───────────────────────────────────────────────────────────────


class BotRegistry:
    """
    Registry for bot functions.

    Usage:
        reg = BotRegistry()
        reg.register("random", random_bot)
        reg.register("minimax", minimax_bot)
        bot_fn = reg["minimax"]
    """

    def __init__(self) -> None:
        self._bots: dict[str, Callable] = {}

    def register(self, name: str, fn: Callable) -> None:
        """Register a bot under a name."""
        if name in self._bots:
            raise ValueError(f"Bot '{name}' already registered")
        self._bots[name] = fn

    def __getitem__(self, name: str) -> Callable:
        """Retrieve a bot by name."""
        if name not in self._bots:
            raise KeyError(f"Bot '{name}' not found")
        return self._bots[name]

    def names(self) -> list[str]:
        """Return list of registered bot names."""
        return list(self._bots.keys())

    def __len__(self) -> int:
        return len(self._bots)

    def __contains__(self, name: str) -> bool:
        return name in self._bots


# ── Match result ───────────────────────────────────────────────────────────────


@dataclass
class MatchResult:
    """Result of a single paired match (seat-reversed)."""
    bot_a: str
    bot_b: str
    board_rows: int
    board_cols: int
    board_inarow: int
    games: list[GameRecord]
    bot_a_wins: int = 0
    bot_b_wins: int = 0
    draws: int = 0

    @property
    def total_games(self) -> int:
        return len(self.games)

    @property
    def bot_a_win_pct(self) -> float:
        if self.total_games == 0:
            return 0.0
        return self.bot_a_wins / self.total_games * 100

    @property
    def bot_b_win_pct(self) -> float:
        if self.total_games == 0:
            return 0.0
        return self.bot_b_wins / self.total_games * 100

    @property
    def draw_pct(self) -> float:
        if self.total_games == 0:
            return 0.0
        return self.draws / self.total_games * 100

    def summary(self) -> str:
        n = self.total_games
        if n == 0:
            return f"{self.bot_a} vs {self.bot_b}: 0 games"
        return (
            f"{self.bot_a} vs {self.bot_b}: {n} games — "
            f"{self.bot_a_wins}A {self.draws}D {self.bot_b_wins}B"
        )


# ── Leaderboard ────────────────────────────────────────────────────────────────


@dataclass
class BotStats:
    """Accumulated statistics for a single bot across many matches."""
    name: str
    games_played: int = 0
    wins: int = 0
    losses: int = 0
    draws: int = 0
    timeout_count: int = 0
    crash_count: int = 0
    invalid_count: int = 0

    @property
    def win_pct(self) -> float:
        if self.games_played == 0:
            return 0.0
        return self.wins / self.games_played * 100

    @property
    def loss_pct(self) -> float:
        if self.games_played == 0:
            return 0.0
        return self.losses / self.games_played * 100

    @property
    def draw_pct(self) -> float:
        if self.games_played == 0:
            return 0.0
        return self.draws / self.games_played * 100


class Leaderboard:
    """
    Accumulates match results and tracks per-bot statistics.

    Usage:
        lb = Leaderboard()
        lb.add_match(result)
        sorted_bots = lb.ranked()
    """

    def __init__(self) -> None:
        self._stats: dict[str, BotStats] = {}

    def _ensure(self, name: str) -> BotStats:
        if name not in self._stats:
            self._stats[name] = BotStats(name=name)
        return self._stats[name]

    def add_match(self, result: MatchResult) -> None:
        """Accumulate results from a paired match."""
        sa = self._ensure(result.bot_a)
        sb = self._ensure(result.bot_b)

        n = result.total_games  # total games in the match (both seats)
        sa.games_played += n
        sb.games_played += n

        # MatchResult already has correct win counts per bot (seat-aware).
        # Each game is played in both seat orientations, so the total
        # games_played per bot is 2× the number of pairs.
        sa.wins += result.bot_a_wins
        sa.losses += result.bot_b_wins
        sa.draws += result.draws

        sb.wins += result.bot_b_wins
        sb.losses += result.bot_a_wins
        sb.draws += result.draws

    def bot(self, name: str) -> BotStats:
        """Get stats for a bot."""
        return self._stats[name]

    def ranked(self) -> list[tuple[str, BotStats]]:
        """Return (name, stats) sorted by win_pct descending."""
        items = list(self._stats.items())
        items.sort(key=lambda x: x[1].win_pct, reverse=True)
        return items

    def names(self) -> list[str]:
        return list(self._stats.keys())


# ── Tournament runner ─────────────────────────────────────────────────────────


class Tournament:
    """
    Run pairwise matches between registered bots.

    Usage:
        reg = BotRegistry()
        reg.register("random", random_bot)
        reg.register("minimax", shallow_minimax_bot)

        tourney = Tournament(reg, games_per_pair=10)
        results = tourney.run()

        lb = Leaderboard()
        for r in results:
            lb.add_match(r)
    """

    def __init__(
        self,
        registry: BotRegistry,
        games_per_pair: int = 10,
        rows: int = 6,
        cols: int = 7,
        inarow: int = 4,
    ) -> None:
        self.registry = registry
        self.games_per_pair = games_per_pair
        self.rows = rows
        self.cols = cols
        self.inarow = inarow

    def run_pair(self, name_a: str, name_b: str,
                 games: int | None = None) -> MatchResult:
        """
        Run ``games`` seat-reversed games between two named bots.

        Args:
            name_a: first bot name
            name_b: second bot name
            games: number of games per seat (defaults to self.games_per_pair)

        Returns:
            MatchResult with all game records
        """
        n = games if games is not None else self.games_per_pair
        bot_a_fn = self.registry[name_a]
        bot_b_fn = self.registry[name_b]

        games_list: list[GameRecord] = []
        bot_a_wins = 0
        bot_b_wins = 0
        draws = 0

        for _ in range(n):
            g1, g2 = play_game_seated(
                bot_a_fn, bot_b_fn,
                self.rows, self.cols, self.inarow,
            )
            games_list.extend([g1, g2])

            # g1: bot_a is P1, bot_b is P2
            # g2: bot_b is P1, bot_a is P2  (seats reversed)
            for g, p1_is_a in ((g1, True), (g2, False)):
                if g.winner == 0:
                    draws += 1
                elif g.winner == 1:
                    # Player 1 won
                    if p1_is_a:
                        bot_a_wins += 1
                    else:
                        bot_b_wins += 1
                elif g.winner == 2:
                    # Player 2 won
                    if p1_is_a:
                        bot_b_wins += 1
                    else:
                        bot_a_wins += 1

        return MatchResult(
            bot_a=name_a,
            bot_b=name_b,
            board_rows=self.rows,
            board_cols=self.cols,
            board_inarow=self.inarow,
            games=games_list,
            bot_a_wins=bot_a_wins,
            bot_b_wins=bot_b_wins,
            draws=draws,
        )

    def run_all(self) -> list[MatchResult]:
        """
        Run every pair of bots against each other.

        Returns:
            List of MatchResult objects
        """
        names = self.registry.names()
        results: list[MatchResult] = []

        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                result = self.run_pair(names[i], names[j])
                results.append(result)

        return results

    def summary(self, results: list[MatchResult]) -> str:
        """Print a formatted summary of all results."""
        lines = ["=== Tournament Results ==="]
        for r in results:
            lines.append(f"  {r.summary()}")
        lines.append("")
        return "\n".join(lines)