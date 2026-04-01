from datetime import date, datetime

SPORTS = ["NBA", "NFL", "NHL", "MLB", "UFC", "CFB", "CBB"]
CONFIDENCE_TIERS = ["A", "B", "C"]

SAMPLE_PICKS = [
    {
        "game_id": "nba-001",
        "sport": "NBA",
        "matchup": "Lakers vs Celtics",
        "pick_type": "spread",
        "selection": "Celtics -3.5",
        "line": -3.5,
        "confidence": "A",
        "rationale": (
            "Celtics have covered 8 of last 10 at home. Lakers missing key rotation players."
        ),
        "model_version": "v2.1",
        "created_at": datetime.utcnow().isoformat(),
    },
    {
        "game_id": "nfl-001",
        "sport": "NFL",
        "matchup": "Chiefs vs Bills",
        "pick_type": "moneyline",
        "selection": "Chiefs ML",
        "line": -145,
        "confidence": "B",
        "rationale": "Chiefs 12-3 ATS as favorites. Mahomes 8-1 vs Bills in last 9.",
        "model_version": "v2.1",
        "created_at": datetime.utcnow().isoformat(),
    },
    {
        "game_id": "nhl-001",
        "sport": "NHL",
        "matchup": "Bruins vs Rangers",
        "pick_type": "total",
        "selection": "Under 5.5",
        "line": 5.5,
        "confidence": "B",
        "rationale": "Both teams top-5 defensive units. Goalies are hot.",
        "model_version": "v2.1",
        "created_at": datetime.utcnow().isoformat(),
    },
    {
        "game_id": "mlb-001",
        "sport": "MLB",
        "matchup": "Yankees vs Red Sox",
        "pick_type": "moneyline",
        "selection": "Yankees ML",
        "line": -120,
        "confidence": "C",
        "rationale": "Cole on mound. Yankees 65% win rate with Cole starting.",
        "model_version": "v2.1",
        "created_at": datetime.utcnow().isoformat(),
    },
    {
        "game_id": "ufc-001",
        "sport": "UFC",
        "matchup": "Jones vs Miocic",
        "pick_type": "moneyline",
        "selection": "Jones ML",
        "line": -280,
        "confidence": "A",
        "rationale": "Jones dominant grappling advantage. Miocic 38, age factor.",
        "model_version": "v2.1",
        "created_at": datetime.utcnow().isoformat(),
    },
    {
        "game_id": "cfb-001",
        "sport": "CFB",
        "matchup": "Alabama vs Georgia",
        "pick_type": "spread",
        "selection": "Georgia +3",
        "line": 3.0,
        "confidence": "B",
        "rationale": "Georgia 7-2 ATS as road underdog. Alabama secondary injuries.",
        "model_version": "v2.1",
        "created_at": datetime.utcnow().isoformat(),
    },
    {
        "game_id": "cbb-001",
        "sport": "CBB",
        "matchup": "Duke vs UNC",
        "pick_type": "total",
        "selection": "Over 147",
        "line": 147.0,
        "confidence": "A",
        "rationale": (
            "Both teams pace top 20 nationally. Low defensive efficiency in rivalry games."
        ),
        "model_version": "v2.1",
        "created_at": datetime.utcnow().isoformat(),
    },
]


def get_daily_picks(sport: str | None = None, target_date: date | None = None) -> list[dict]:
    """Return daily picks, optionally filtered by sport."""
    picks = list(SAMPLE_PICKS)
    if sport:
        picks = [p for p in picks if p["sport"] == sport]
    return picks


def get_pick_rationale(game_id: str) -> dict:
    """Return detailed rationale for a specific pick."""
    for pick in SAMPLE_PICKS:
        if pick["game_id"] == game_id:
            return {
                "game_id": game_id,
                "rationale": pick["rationale"],
                "model_version": pick["model_version"],
                "confidence": pick["confidence"],
                "factors": [
                    {"name": "Historical ATS", "weight": 0.35, "signal": "positive"},
                    {"name": "Injuries", "weight": 0.25, "signal": "positive"},
                    {"name": "Weather/Rest", "weight": 0.15, "signal": "neutral"},
                    {"name": "Line Movement", "weight": 0.25, "signal": "positive"},
                ],
            }
    return {"game_id": game_id, "rationale": "Pick not found", "factors": []}
