"""
Player props service for Sportalytics.

Provides AI-graded player prop recommendations and historical prop
results used by the Player Props page.
"""

SAMPLE_PROPS = [
    {
        "player_id": "p001",
        "player_name": "LeBron James",
        "sport": "NBA",
        "team": "Lakers",
        "game": "Lakers vs Celtics",
        "prop_type": "points",
        "line": 25.5,
        "recommendation": "Over",
        "grade": "A",
        "hit_rate_last_10": 0.80,
        "avg_last_10": 28.3,
        "implied_prob": 0.72,
        "model_edge": 0.12,
    },
    {
        "player_id": "p002",
        "player_name": "Patrick Mahomes",
        "sport": "NFL",
        "team": "Chiefs",
        "game": "Chiefs vs Bills",
        "prop_type": "passing_yards",
        "line": 287.5,
        "recommendation": "Over",
        "grade": "B",
        "hit_rate_last_10": 0.70,
        "avg_last_10": 305.0,
        "implied_prob": 0.65,
        "model_edge": 0.07,
    },
    {
        "player_id": "p003",
        "player_name": "Connor McDavid",
        "sport": "NHL",
        "team": "Oilers",
        "game": "Oilers vs Flames",
        "prop_type": "points",
        "line": 1.5,
        "recommendation": "Over",
        "grade": "A",
        "hit_rate_last_10": 0.75,
        "avg_last_10": 1.9,
        "implied_prob": 0.68,
        "model_edge": 0.10,
    },
    {
        "player_id": "p004",
        "player_name": "Aaron Judge",
        "sport": "MLB",
        "team": "Yankees",
        "game": "Yankees vs Red Sox",
        "prop_type": "home_runs",
        "line": 0.5,
        "recommendation": "Over",
        "grade": "B",
        "hit_rate_last_10": 0.60,
        "avg_last_10": 0.7,
        "implied_prob": 0.55,
        "model_edge": 0.06,
    },
]


def get_player_props(sport: str | None = None, grade: str | None = None) -> list[dict]:
    """
    Return player prop recommendations with optional filtering.

    Parameters
    ----------
    sport : str, optional
        Filter by sport abbreviation, e.g. ``'NBA'``.
        When ``None`` all sports are returned.
    grade : str, optional
        Filter by grade tier: ``'A'``, ``'B'``, ``'C'``, or ``'D'``.
        When ``None`` all grades are returned.

    Returns
    -------
    list of dict
        Each dict contains ``'player_id'``, ``'player_name'``, ``'sport'``, ``'team'``, ``'game'``, ``'prop_type'``, ``'line'``, ``'recommendation'``, ``'grade'``, ``'hit_rate_last_10'``, ``'avg_last_10'``, ``'implied_prob'``, and ``'model_edge'`` keys.
    """
    props = list(SAMPLE_PROPS)
    if sport:
        props = [p for p in props if p["sport"] == sport]
    if grade:
        props = [p for p in props if p["grade"] == grade]
    return props


def get_player_history(player_id: str) -> list[dict]:
    """
    Return historical prop results for a specific player.

    Parameters
    ----------
    player_id : str
        Unique player identifier string, e.g. ``'p001'``.

    Returns
    -------
    list of dict
        Each dict contains ``'date'``, ``'prop_type'``, ``'line'``, ``'result'`` *(actual value)*, and ``'hit'`` *(bool)* keys.

    Notes
    -----
    The current implementation returns sample data regardless of
    ``player_id``.  Future versions will query the database.
    """
    return [
        {"date": "2024-01-10", "prop_type": "points", "line": 24.5, "result": 28,  "hit": True},
        {"date": "2024-01-08", "prop_type": "points", "line": 25.5, "result": 22,  "hit": False},
        {"date": "2024-01-06", "prop_type": "points", "line": 26.5, "result": 31,  "hit": True},
    ]
