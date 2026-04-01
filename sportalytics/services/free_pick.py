"""Free daily pick service backed by SQLAlchemy with Redis caching."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import aliased

from sportalytics.models.db import Game, Pick, Sport, Team, init_db, session_scope
from sportalytics.services.cache import cache_get_json, cache_set_json, make_cache_key


def get_free_pick(target_date: date | None = None) -> dict:
    """
    Return today's free ML-graded pick.

    Parameters
    ----------
    target_date : date, optional
        Reserved for future use.  Currently ignored; the current daily
        pick is always returned.

    Returns
    -------
    dict
        A pick dict with keys ``'date'``, ``'sport'``, ``'matchup'``,
        ``'pick'``, ``'line'``, ``'pick_type'``, ``'confidence'``,
        ``'grade'``, ``'rationale'``, ``'model_version'``, and
        ``'ml_score'``.
    """
    init_db()
    key = make_cache_key("free_pick", date=str(target_date or "latest"))
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
            .where(Pick.is_free_pick.is_(True), Pick.result.is_(None))
            .order_by(Pick.created_at.desc())
            .limit(1)
        )
        row = session.execute(stmt).first()

    if row is None:
        return {}

    pick, game, sport, home, away = row
    payload = {
        "date": pick.created_at.date().isoformat() if pick.created_at else None,
        "sport": sport.abbreviation,
        "matchup": f"{home.name} vs {away.name}",
        "pick": pick.selection,
        "line": pick.line,
        "pick_type": pick.pick_type,
        "confidence": pick.confidence_tier or "B",
        "grade": pick.grade or "B",
        "rationale": pick.rationale or "",
        "model_version": pick.model_version or "v1.0",
        "ml_score": pick.ml_score or 0.5,
    }
    cache_set_json(key, payload, ttl_seconds=300)
    return payload


def get_free_pick_history() -> list[dict]:
    """
    Return recent historical free pick results.

    Returns
    -------
    list of dict
        Each dict contains ``'date'``, ``'matchup'``, ``'pick'``,
        ``'result'``, and ``'grade'`` keys.
    """
    init_db()
    key = make_cache_key("free_pick_history")
    cached = cache_get_json(key)
    if cached is not None:
        return cached

    with session_scope() as session:
        home_team = aliased(Team)
        away_team = aliased(Team)
        stmt = (
            select(Pick, home_team, away_team)
            .join(Game, Pick.game_id == Game.id)
            .join(home_team, Game.home_team_id == home_team.id)
            .join(away_team, Game.away_team_id == away_team.id)
            .where(Pick.is_free_pick.is_(True), Pick.result.is_not(None))
            .order_by(Pick.created_at.desc())
            .limit(10)
        )
        rows = session.execute(stmt).all()

    payload = [
        {
            "date": p.created_at.date().isoformat() if p.created_at else None,
            "matchup": f"{h.name} vs {a.name}",
            "pick": p.selection,
            "result": p.result,
            "grade": p.grade or "B",
        }
        for p, h, a in rows
    ]
    cache_set_json(key, payload, ttl_seconds=300)
    return payload
