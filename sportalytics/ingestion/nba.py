from sportalytics.ingestion.base import BaseIngester, IngestionResult


class NBAIngester(BaseIngester):
    sport = "NBA"

    def fetch_schedule(self, season: str) -> list[dict]:
        return [
            {
                "game_id": "nba-20240101-lal-bos",
                "home_team": "Lakers",
                "away_team": "Celtics",
                "scheduled_at": "2024-01-01T20:00:00",
                "season": season,
            }
        ]

    def fetch_player_stats(self, game_id: str) -> list[dict]:
        return [
            {
                "player_id": "p001", "player_name": "LeBron James",
                "points": 28, "rebounds": 7, "assists": 9,
            },
            {
                "player_id": "p002", "player_name": "Jayson Tatum",
                "points": 32, "rebounds": 9, "assists": 5,
            },
        ]

    def fetch_team_stats(self, season: str) -> list[dict]:
        return [
            {"team": "Lakers", "wins": 25, "losses": 20, "ppg": 115.2, "opp_ppg": 113.8},
            {"team": "Celtics", "wins": 35, "losses": 10, "ppg": 120.5, "opp_ppg": 111.2},
        ]

    def _run_impl(self, result: IngestionResult) -> None:
        schedule = self.fetch_schedule("2023-24")
        result.records_fetched = len(schedule)
        result.records_inserted = len(schedule)
