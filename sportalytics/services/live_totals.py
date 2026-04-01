"""Live totals service backed by SQLAlchemy with Redis caching."""

from sqlalchemy import select
from sqlalchemy.orm import aliased

from sportalytics.models.db import Game, OddsLine, Sport, Team, init_db, session_scope
from sportalytics.services.cache import cache_get_json, cache_set_json, make_cache_key


def _game_payload(game: Game, sport: Sport, home: Team, away: Team, odds: dict[str, float]) -> dict:
    current_total = (game.home_score or 0) + (game.away_score or 0)
    return {
        "game_id": game.external_id or f"live-{game.id}",
        "sport": sport.abbreviation,
        "matchup": f"{home.name} vs {away.name}",
        "period": game.period or "In Progress",
        "time_remaining": game.time_remaining or "0:00",
        "home_score": game.home_score or 0,
        "away_score": game.away_score or 0,
        "current_total": current_total,
        "opening_total": game.opening_total,
        "current_line": game.current_line,
        "projected_total": game.projected_total,
        "pace_factor": game.pace_factor,
        "recommendation": game.recommendation or "Under",
        "live_odds": odds,
    }


def get_live_games(sport: str | None = None) -> list[dict]:
    """
    Return currently live games with pace and projection data.

    Parameters
    ----------
    sport : str, optional
        Filter results by sport abbreviation, e.g. ``'NBA'``.
        When ``None`` all live games are returned.

    Returns
    -------
    list of dict
        Each dict contains ``'game_id'``, ``'sport'``, ``'matchup'``, ``'period'``, ``'time_remaining'``, ``'home_score'``, ``'away_score'``, ``'current_total'``, ``'opening_total'``, ``'current_line'``, ``'projected_total'``, ``'pace_factor'``, ``'recommendation'``, and ``'live_odds'`` keys.
    """
    init_db()
    key = make_cache_key("live_totals", sport=sport or "ALL")
    cached = cache_get_json(key)
    if cached is not None:
        return cached

    with session_scope() as session:
        home_team = aliased(Team)
        away_team = aliased(Team)
        stmt = (
            select(Game, Sport, home_team, away_team)
            .join(Sport, Game.sport_id == Sport.id)
            .join(home_team, Game.home_team_id == home_team.id)
            .join(away_team, Game.away_team_id == away_team.id)
            .where(Game.status == "live")
        )
        if sport:
            stmt = stmt.where(Sport.abbreviation == sport)

        games = []
        for game, sport_row, home, away in session.execute(stmt):
            odds_stmt = (
                select(OddsLine)
                .where(OddsLine.game_id == game.id, OddsLine.market_type == "total_odds")
                .order_by(OddsLine.timestamp.desc())
                .limit(1)
            )
            odds_row = session.execute(odds_stmt).scalar_one_or_none()
            odds = {
                "over": odds_row.home_line if odds_row else -110,
                "under": odds_row.away_line if odds_row else -110,
            }
            games.append(_game_payload(game, sport_row, home, away, odds))

    cache_set_json(key, games, ttl_seconds=30)
    return games


def get_pace_data(game_id: str) -> dict:
    """
    Return detailed pace data for a specific live game.

    Parameters
    ----------
    game_id : str
        Unique game identifier string, e.g. ``'nba-live-001'``.

    Returns
    -------
    dict
        The base game dict augmented with ``'scoring_by_period'`` *(list of int)*, ``'pace_trend'`` *(str)*, and ``'model_confidence'`` *(float)* keys.  Returns an empty dict if the game is not found.
    """
    for game in get_live_games():
        if game["game_id"] == game_id:
            return {
                **game,
                "scoring_by_period": [
                    max(0, int(game["current_total"] * 0.18)),
                    max(0, int(game["current_total"] * 0.24)),
                    max(0, int(game["current_total"] * 0.28)),
                    max(0, int(game["current_total"] * 0.30)),
                ],
                "pace_trend": "accelerating" if (game.get("pace_factor") or 1) >= 1 else "slowing",
                "model_confidence": 0.71,
            }
    return {}
