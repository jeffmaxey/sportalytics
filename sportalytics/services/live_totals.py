SAMPLE_LIVE_GAMES = [
    {
        "game_id": "nba-live-001",
        "sport": "NBA",
        "matchup": "Lakers vs Celtics",
        "period": "3rd Quarter",
        "time_remaining": "4:32",
        "home_score": 78,
        "away_score": 82,
        "current_total": 160,
        "opening_total": 224.5,
        "current_line": 224.5,
        "projected_total": 221.3,
        "pace_factor": 1.02,
        "recommendation": "Under",
        "live_odds": {"over": -115, "under": -105},
    },
    {
        "game_id": "nhl-live-001",
        "sport": "NHL",
        "matchup": "Bruins vs Rangers",
        "period": "2nd Period",
        "time_remaining": "11:20",
        "home_score": 2,
        "away_score": 1,
        "current_total": 3,
        "opening_total": 5.5,
        "current_line": 4.5,
        "projected_total": 5.1,
        "pace_factor": 0.97,
        "recommendation": "Over",
        "live_odds": {"over": -110, "under": -110},
    },
    {
        "game_id": "nfl-live-001",
        "sport": "NFL",
        "matchup": "Chiefs vs Bills",
        "period": "2nd Quarter",
        "time_remaining": "2:15",
        "home_score": 14,
        "away_score": 10,
        "current_total": 24,
        "opening_total": 48.5,
        "current_line": 47.5,
        "projected_total": 49.2,
        "pace_factor": 1.05,
        "recommendation": "Over",
        "live_odds": {"over": -120, "under": 100},
    },
]


def get_live_games(sport: str | None = None) -> list[dict]:
    """Return currently live games with pace data."""
    games = list(SAMPLE_LIVE_GAMES)
    if sport:
        games = [g for g in games if g["sport"] == sport]
    return games


def get_pace_data(game_id: str) -> dict:
    """Return detailed pace data for a specific game."""
    for game in SAMPLE_LIVE_GAMES:
        if game["game_id"] == game_id:
            return {
                **game,
                "scoring_by_period": [28, 34, 38, 0],
                "pace_trend": "slowing",
                "model_confidence": 0.71,
            }
    return {}
