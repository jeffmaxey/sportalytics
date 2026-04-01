from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class IngestionResult:
    sport: str
    records_fetched: int = 0
    records_inserted: int = 0
    records_updated: int = 0
    errors: list[str] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None


class BaseIngester(ABC):
    sport: str

    @abstractmethod
    def fetch_schedule(self, season: str) -> list[dict]: ...

    @abstractmethod
    def fetch_player_stats(self, game_id: str) -> list[dict]: ...

    @abstractmethod
    def fetch_team_stats(self, season: str) -> list[dict]: ...

    def run(self) -> IngestionResult:
        result = IngestionResult(sport=self.sport)
        try:
            self._run_impl(result)
        except Exception as e:
            result.errors.append(str(e))
        finally:
            result.completed_at = datetime.utcnow()
        return result

    def _run_impl(self, result: IngestionResult) -> None:
        pass
