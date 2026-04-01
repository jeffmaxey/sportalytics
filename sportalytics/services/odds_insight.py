"""Odds insight service backed by SQLAlchemy with Redis caching."""

from collections import defaultdict

from sqlalchemy import select
from sqlalchemy.orm import aliased

from sportalytics.models.db import Game, OddsLine, Sport, Team, init_db, session_scope
from sportalytics.services.cache import cache_get_json, cache_set_json, make_cache_key

SPORTSBOOKS = [
    "DraftKings", "FanDuel", "BetMGM", "Caesars",
    "PointsBet", "BetRivers", "WynnBet",
]


def _best_home_book(lines: dict[str, dict]) -> str:
    return max(lines.items(), key=lambda item: item[1]["home"])[0]


def _best_away_book(lines: dict[str, dict]) -> str:
    return max(lines.items(), key=lambda item: item[1]["away"])[0]


def get_odds_comparison(sport: str | None = None) -> list[dict]:
    """
    Return odds comparison data across all sportsbooks.

    Parameters
    ----------
    sport : str, optional
        Filter results by sport abbreviation, e.g. ``'NBA'``.
        When ``None`` all games are returned.

    Returns
    -------
    list of dict
        Each dict contains ``'game_id'``, ``'sport'``, ``'matchup'``, ``'market'``, ``'lines'``, ``'best_home'``, ``'best_away'``, ``'consensus_home'``, and ``'consensus_away'`` keys.
    """
    init_db()
    key = make_cache_key("odds_comparison", sport=sport or "ALL")
    cached = cache_get_json(key)
    if cached is not None:
        return cached

    with session_scope() as session:
        home_team = aliased(Team)
        away_team = aliased(Team)
        stmt = (
            select(OddsLine, Game, Sport, home_team, away_team)
            .join(Game, OddsLine.game_id == Game.id)
            .join(Sport, Game.sport_id == Sport.id)
            .join(home_team, Game.home_team_id == home_team.id)
            .join(away_team, Game.away_team_id == away_team.id)
            .where(OddsLine.market_type.in_(["moneyline", "spread"]))
            .order_by(OddsLine.timestamp.desc())
        )
        if sport:
            stmt = stmt.where(Sport.abbreviation == sport)

        grouped: dict[tuple[str, str], dict] = defaultdict(dict)
        for row, game, sport_row, home, away in session.execute(stmt):
            game_key = (game.external_id or f"game-{game.id}", row.market_type)
            bucket = grouped[game_key]
            if not bucket:
                bucket.update(
                    {
                        "game_id": game.external_id or f"game-{game.id}",
                        "sport": sport_row.abbreviation,
                        "matchup": f"{home.name} vs {away.name}",
                        "market": row.market_type,
                        "lines": {},
                    }
                )
            if row.sportsbook in bucket["lines"]:
                continue
            bucket["lines"][row.sportsbook] = {"home": row.home_line, "away": row.away_line}

    payload = []
    for game_data in grouped.values():
        lines = game_data["lines"]
        if not lines:
            continue
        home_values = [v["home"] for v in lines.values() if v["home"] is not None]
        away_values = [v["away"] for v in lines.values() if v["away"] is not None]
        game_data["best_home"] = _best_home_book(lines)
        game_data["best_away"] = _best_away_book(lines)
        game_data["consensus_home"] = round(sum(home_values) / len(home_values), 2) if home_values else None
        game_data["consensus_away"] = round(sum(away_values) / len(away_values), 2) if away_values else None
        payload.append(game_data)

    cache_set_json(key, payload, ttl_seconds=60)
    return payload


def get_line_movement(game_id: str) -> list[dict]:
    """
    Return timestamped line-movement history for a specific game.

    Parameters
    ----------
    game_id : str
        Unique game identifier string, e.g. ``'nba-001'``.

    Returns
    -------
    list of dict
        Each dict contains ``'timestamp'``, ``'sportsbook'``, ``'home'``, and ``'away'`` keys.

    Notes
    -----
    The current implementation returns sample data regardless of
    ``game_id``.  Future versions will query live odds feeds.
    """
    init_db()
    key = make_cache_key("line_movement", game_id=game_id)
    cached = cache_get_json(key)
    if cached is not None:
        return cached

    with session_scope() as session:
        game = session.execute(select(Game).where(Game.external_id == game_id)).scalar_one_or_none()
        if game is None:
            return []

        stmt = (
            select(OddsLine)
            .where(OddsLine.game_id == game.id, OddsLine.market_type.in_(["moneyline", "spread"]))
            .order_by(OddsLine.timestamp.asc())
        )
        payload = [
            {
                "timestamp": row.timestamp.isoformat() if row.timestamp else None,
                "sportsbook": row.sportsbook,
                "home": row.home_line,
                "away": row.away_line,
            }
            for row in session.execute(stmt).scalars()
        ]

    cache_set_json(key, payload, ttl_seconds=60)
    return payload

