from sportalytics.ingestion.base import BaseIngester, IngestionResult


class MLBIngester(BaseIngester):
    sport = "MLB"

    def fetch_schedule(self, season: str) -> list[dict]:
        return [
            {
                "game_id": "mlb-20240415-nyy-bos",
                "home_team": "Yankees",
                "away_team": "Red Sox",
                "scheduled_at": "2024-04-15T19:05:00",
                "season": season,
            }
        ]

    def fetch_player_stats(self, game_id: str) -> list[dict]:
        return [
            {
                "player_id": "p030",
                "player_name": "Aaron Judge",
                "at_bats": 4,
                "hits": 2,
                "home_runs": 1,
                "rbi": 3,
            },
            {
                "player_id": "p031",
                "player_name": "Rafael Devers",
                "at_bats": 4,
                "hits": 1,
                "home_runs": 0,
                "rbi": 0,
            },
        ]

    def fetch_team_stats(self, season: str) -> list[dict]:
        return [
            {"team": "Yankees", "wins": 82, "losses": 80, "runs_per_game": 4.8, "era": 3.95},
            {"team": "Red Sox", "wins": 78, "losses": 84, "runs_per_game": 4.5, "era": 4.20},
        ]

    def _run_impl(self, result: IngestionResult) -> None:
        schedule = self.fetch_schedule("2024")
        result.records_fetched = len(schedule)
        result.records_inserted = len(schedule)
