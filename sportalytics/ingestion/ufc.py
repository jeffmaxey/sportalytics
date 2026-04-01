from sportalytics.ingestion.base import BaseIngester, IngestionResult


class UFCIngester(BaseIngester):
    sport = "UFC"

    def fetch_schedule(self, season: str) -> list[dict]:
        return [
            {
                "game_id": "ufc-20240113-jones-miocic",
                "home_team": "Jon Jones",
                "away_team": "Stipe Miocic",
                "scheduled_at": "2024-01-13T22:00:00",
                "season": season,
            }
        ]

    def fetch_player_stats(self, game_id: str) -> list[dict]:
        return [
            {
                "player_id": "p040",
                "player_name": "Jon Jones",
                "significant_strikes": 45,
                "takedowns": 3,
                "submission_attempts": 1,
            },
            {
                "player_id": "p041",
                "player_name": "Stipe Miocic",
                "significant_strikes": 30,
                "takedowns": 0,
                "submission_attempts": 0,
            },
        ]

    def fetch_team_stats(self, season: str) -> list[dict]:
        return [
            {
                "fighter": "Jon Jones", "wins": 27, "losses": 1,
                "ko_tko_wins": 10, "submission_wins": 6,
            },
            {
                "fighter": "Stipe Miocic", "wins": 20, "losses": 4,
                "ko_tko_wins": 12, "submission_wins": 1,
            },
        ]

    def _run_impl(self, result: IngestionResult) -> None:
        schedule = self.fetch_schedule("2024")
        result.records_fetched = len(schedule)
        result.records_inserted = len(schedule)
