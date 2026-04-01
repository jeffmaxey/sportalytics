"""
Base ingestion abstractions for Sportalytics.

Defines the shared dataclass result envelope and abstract ingester
interface used by sport-specific ingestion pipelines.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class IngestionResult:
    """
    Structured result payload emitted by ingestion runs.

    Parameters
    ----------
    sport : str
        Sport code for the ingester that produced this result.
    records_fetched : int, optional
        Number of records fetched from upstream sources.
    records_inserted : int, optional
        Number of new records inserted into storage.
    records_updated : int, optional
        Number of existing records updated.
    errors : list of str, optional
        Error messages collected during processing.
    started_at : datetime, optional
        UTC timestamp when ingestion started.
    completed_at : datetime or None, optional
        UTC timestamp when ingestion finished.
    """

    sport: str
    records_fetched: int = 0
    records_inserted: int = 0
    records_updated: int = 0
    errors: list[str] = field(default_factory=list)
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: datetime | None = None


class BaseIngester(ABC):
    """
    Abstract base class for all sport-specific ingesters.

    Subclasses must implement schedule, player-stat, and team-stat
    fetch methods, then rely on :meth:`run` for standard execution and
    error capture.
    """

    sport: str

    @abstractmethod
    def fetch_schedule(self, season: str) -> list[dict]:
        """
        Fetch the game schedule for a season.

        Parameters
        ----------
        season : str
            Season identifier string.

        Returns
        -------
        list of dict
            Raw schedule records.
        """
        ...

    @abstractmethod
    def fetch_player_stats(self, game_id: str) -> list[dict]:
        """
        Fetch player statistics for a game.

        Parameters
        ----------
        game_id : str
            Unique game identifier.

        Returns
        -------
        list of dict
            Raw player-stat records.
        """
        ...

    @abstractmethod
    def fetch_team_stats(self, season: str) -> list[dict]:
        """
        Fetch team statistics for a season.

        Parameters
        ----------
        season : str
            Season identifier string.

        Returns
        -------
        list of dict
            Raw team-stat records.
        """
        ...

    def run(self) -> IngestionResult:
        """
        Execute ingestion and capture completion metadata.

        Returns
        -------
        IngestionResult
            Final result with counts, errors, and completion timestamp.
        """
        result = IngestionResult(sport=self.sport)
        try:
            self._run_impl(result)
        except Exception as e:
            result.errors.append(str(e))
        finally:
            result.completed_at = datetime.now(timezone.utc)
        return result

    def _run_impl(self, result: IngestionResult) -> None:
        """
        Optional internal execution hook for subclasses.

        Parameters
        ----------
        result : IngestionResult
            Mutable result object populated during ingestion.
        """
        pass
