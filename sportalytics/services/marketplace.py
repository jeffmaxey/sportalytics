"""
Expert marketplace service for Sportalytics.

Provides access to verified and unverified expert cappers, their
historical pick records, and individual pick histories.
"""

SAMPLE_EXPERTS = [
    {
        "id": "e001",
        "username": "sharpsteve",
        "display_name": "Sharp Steve",
        "verified": True,
        "bio": "15 years of professional handicapping. Specializes in NFL and NBA spreads.",
        "win_rate": 0.587,
        "roi": 8.4,
        "total_picks": 412,
        "sports": ["NFL", "NBA"],
        "monthly_price": 49.99,
        "last_5": ["W", "W", "L", "W", "W"],
    },
    {
        "id": "e002",
        "username": "mlbgrinder",
        "display_name": "MLB Grinder",
        "verified": True,
        "bio": "Full-time baseball bettor since 2015. 162-game grinder.",
        "win_rate": 0.562,
        "roi": 5.7,
        "total_picks": 890,
        "sports": ["MLB"],
        "monthly_price": 29.99,
        "last_5": ["W", "L", "W", "W", "L"],
    },
    {
        "id": "e003",
        "username": "nhlprophet",
        "display_name": "NHL Prophet",
        "verified": False,
        "bio": "Hockey stats nerd. Advanced metrics focus.",
        "win_rate": 0.541,
        "roi": 3.2,
        "total_picks": 187,
        "sports": ["NHL"],
        "monthly_price": 19.99,
        "last_5": ["L", "W", "W", "L", "W"],
    },
]


def get_experts(sport: str | None = None, verified_only: bool = False) -> list[dict]:
    """
    Return a list of expert cappers, with optional filtering.

    Parameters
    ----------
    sport : str, optional
        Filter experts by sport abbreviation, e.g. ``'NFL'``.
        When ``None`` all sports are returned.
    verified_only : bool, optional
        When ``True`` only verified experts are returned.
        Default is ``False``.

    Returns
    -------
    list of dict
        Each dict contains expert metadata: ``'id'``, ``'display_name'``, 
        ``'verified'``, ``'bio'``, ``'win_rate'``, ``'roi'``, 
        ``'total_picks'``, ``'sports'``, ``'monthly_price'``, 
        and ``'last_5'``.
    """
    experts = list(SAMPLE_EXPERTS)
    if sport:
        experts = [e for e in experts if sport in e["sports"]]
    if verified_only:
        experts = [e for e in experts if e["verified"]]
    return experts


def get_expert_picks(expert_id: str) -> list[dict]:
    """
    Return historical picks for a specific expert.

    Parameters
    ----------
    expert_id : str
        Unique expert identifier string, e.g. ``'e001'``.

    Returns
    -------
    list of dict
        Each dict contains ``'date'``, ``'matchup'``, ``'pick'``, 
        ``'result'``, and ``'units'`` keys.

    Notes
    -----
    The current implementation returns sample data regardless of
    ``expert_id``.  Future versions will query the database.
    """
    return [
        {"date": "2024-01-10", "matchup": "Chiefs vs Bills",    "pick": "Chiefs -3",   "result": "W", "units":  1.00},
        {"date": "2024-01-09", "matchup": "Lakers vs Celtics",  "pick": "Celtics ML",  "result": "W", "units":  0.91},
        {"date": "2024-01-08", "matchup": "Yankees vs Red Sox", "pick": "Under 9",     "result": "L", "units": -1.00},
        {"date": "2024-01-07", "matchup": "Bruins vs Rangers",  "pick": "Bruins ML",   "result": "W", "units":  0.87},
        {"date": "2024-01-06", "matchup": "Duke vs UNC",        "pick": "Over 147",    "result": "W", "units":  0.91},
    ]
