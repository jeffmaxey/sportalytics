"""
Model performance tracking service for Sportalytics.

Provides aggregated win/loss records, ROI statistics, and monthly
performance data used by the Model Tracker page.
"""

SAMPLE_MODEL_STATS = {
    "overall": {
        "record": "127-98",
        "win_rate": 0.564,
        "roi": 4.2,
        "total_picks": 225,
        "units_won": 9.45,
    },
    "by_sport": [
        {"sport": "NBA", "record": "45-32", "win_rate": 0.584, "roi": 6.1, "picks": 77},
        {"sport": "NFL", "record": "28-22", "win_rate": 0.560, "roi": 4.8, "picks": 50},
        {"sport": "NHL", "record": "22-18", "win_rate": 0.550, "roi": 3.5, "picks": 40},
        {"sport": "MLB", "record": "18-15", "win_rate": 0.545, "roi": 2.8, "picks": 33},
        {"sport": "UFC", "record": "8-5", "win_rate": 0.615, "roi": 7.2, "picks": 13},
        {"sport": "CFB", "record": "4-4", "win_rate": 0.500, "roi": -1.0, "picks": 8},
        {"sport": "CBB", "record": "2-2", "win_rate": 0.500, "roi": 0.0, "picks": 4},
    ],
    "by_tier": [
        {"tier": "A", "record": "42-25", "win_rate": 0.627, "roi": 9.4, "picks": 67},
        {"tier": "B", "record": "61-48", "win_rate": 0.560, "roi": 3.8, "picks": 109},
        {"tier": "C", "record": "24-25", "win_rate": 0.490, "roi": -1.2, "picks": 49},
    ],
    "monthly": [
        {"month": "Jan 2024", "wins": 22, "losses": 18, "roi": 5.2},
        {"month": "Feb 2024", "wins": 19, "losses": 14, "roi": 6.1},
        {"month": "Mar 2024", "wins": 25, "losses": 20, "roi": 3.8},
        {"month": "Apr 2024", "wins": 18, "losses": 17, "roi": 1.2},
        {"month": "May 2024", "wins": 16, "losses": 14, "roi": 2.5},
        {"month": "Jun 2024", "wins": 27, "losses": 15, "roi": 8.9},
    ],
}


def get_model_performance() -> dict:
    """
    Return the full model performance statistics dictionary.

    Returns
    -------
    dict
        A nested dict with the following top-level keys:

        * ``'overall'`` — overall record, win rate, ROI, and total picks.
        * ``'by_sport'`` — list of per-sport performance dicts.
        * ``'by_tier'`` — list of per-confidence-tier performance dicts.
        * ``'monthly'`` — list of monthly ROI dicts.
    """
    return SAMPLE_MODEL_STATS


def get_performance_by_sport(sport: str) -> dict:
    """
    Return model performance statistics for a single sport.

    Parameters
    ----------
    sport : str
        Sport abbreviation, e.g. ``'NBA'``, ``'NFL'``.

    Returns
    -------
    dict
        Performance dict for the requested sport, or an empty dict if
        the sport is not found.
    """
    for s in SAMPLE_MODEL_STATS["by_sport"]:
        if s["sport"] == sport:
            return s
    return {}


def get_monthly_roi() -> list[dict]:
    """
    Return monthly ROI data for chart rendering.

    Returns
    -------
    list of dict
        Each dict contains ``'month'`` *(str)*, ``'wins'`` *(int)*,
        ``'losses'`` *(int)*,  and ``'roi'`` *(float)* keys.
    """
    return SAMPLE_MODEL_STATS["monthly"]
