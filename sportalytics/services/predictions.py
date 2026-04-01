"""AI/ML predictions service backed by SQLAlchemy with Redis caching."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import aliased

from sportalytics.models.db import Game, Pick, Sport, Team, init_db, session_scope
from sportalytics.services.cache import cache_get_json, cache_set_json, make_cache_key

SPORTS = ["NBA", "NFL", "NHL", "MLB", "UFC", "CFB", "CBB"]
CONFIDENCE_TIERS = ["A", "B", "C"]


def _serialize_pick(pick: Pick, game: Game, sport: Sport, home: Team, away: Team) -> dict:
    return {
        "game_id": game.external_id or f"{sport.abbreviation.lower()}-{game.id}",
        "sport": sport.abbreviation,
        "matchup": f"{home.name} vs {away.name}",
        "pick_type": pick.pick_type,
        "selection": pick.selection,
        "line": pick.line,
        "confidence": pick.confidence_tier or "B",
        "rationale": pick.rationale or "",
        "model_version": pick.model_version or "v1.0",
        "created_at": pick.created_at.isoformat() if pick.created_at else None,
    }


def get_daily_picks(sport: str | None = None, target_date: date | None = None) -> list[dict]:
    """
    Return daily AI/ML picks, optionally filtered by sport.

    Parameters
    ----------
    sport : str, optional
        Filter by sport abbreviation, e.g. ``'NBA'``.
        When ``None`` picks from all sports are returned.
    target_date : date, optional
        Reserved for future use.  Currently ignored; the full sample
        pick set is always returned.

    Returns
    -------
    list of dict
        Each dict contains ``'game_id'``, ``'sport'``, ``'matchup'``,
        ``'pick_type'``, ``'selection'``, ``'line'``, ``'confidence'``,
        ``'rationale'``, ``'model_version'``, and ``'created_at'`` keys.
    """
    init_db()
    key = make_cache_key("predictions", sport=sport or "ALL", date=str(target_date or "today"))
    cached = cache_get_json(key)
    if cached is not None:
        return cached

    with session_scope() as session:
        home_team = aliased(Team)
        away_team = aliased(Team)
        stmt = (
            select(Pick, Game, Sport, home_team, away_team)
            .join(Game, Pick.game_id == Game.id)
            .join(Sport, Pick.sport_id == Sport.id)
            .join(home_team, Game.home_team_id == home_team.id)
            .join(away_team, Game.away_team_id == away_team.id)
            .where(Pick.is_free_pick.is_(False))
            .order_by(Pick.created_at.desc())
        )
        if sport:
            stmt = stmt.where(Sport.abbreviation == sport)
        if target_date:
            stmt = stmt.where(Pick.created_at >= target_date)

        picks = [_serialize_pick(p, g, s, h, a) for p, g, s, h, a in session.execute(stmt)]

    cache_set_json(key, picks, ttl_seconds=120)
    return picks


def get_pick_rationale(game_id: str) -> dict:
    """
    Return detailed model rationale for a specific pick.

    Parameters
    ----------
    game_id : str
        Unique game identifier string, e.g. ``'nba-001'``.

    Returns
    -------
    dict
        A dict with keys ``'game_id'``, ``'rationale'``,
        ``'model_version'``, ``'confidence'``, and ``'factors'``
        *(list of factor dicts with name, weight, and signal)*.
        Returns a default "not found" dict if the game ID is unknown.
    """
    for pick in get_daily_picks():
        if pick["game_id"] == game_id:
            return {
                "game_id": game_id,
                "rationale": pick["rationale"],
                "model_version": pick["model_version"],
                "confidence": pick["confidence"],
                "factors": [
                    {"name": "Historical ATS", "weight": 0.35, "signal": "positive"},
                    {"name": "Injuries",        "weight": 0.25, "signal": "positive"},
                    {"name": "Weather/Rest",    "weight": 0.15, "signal": "neutral"},
                    {"name": "Line Movement",   "weight": 0.25, "signal": "positive"},
                ],
            }
    return {"game_id": game_id, "rationale": "Pick not found", "factors": []}
