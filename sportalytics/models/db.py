"""
SQLAlchemy ORM models for Sportalytics.

Defines the relational schema for sports, teams, players, games, odds,
model picks, experts, and player statistics.
"""

from contextlib import contextmanager
from datetime import datetime, timezone
import os

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
    select,
)
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, relationship, sessionmaker


class Base(DeclarativeBase):
    """
    Base declarative model class for all ORM tables.

    Notes
    -----
    All SQLAlchemy ORM entities in this module inherit from this class.
    """


class Sport(Base):
    """
    Sport dimension table.

    Stores supported sports and their abbreviations.

    Attributes
    ----------
    id : int
        Primary key.
    name : str
        Human-readable sport name.
    abbreviation : str
        Short sport code (for example, ``NBA``).
    """
    __tablename__ = "sports"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    abbreviation = Column(String(10), nullable=False, unique=True)
    teams = relationship("Team", back_populates="sport")
    players = relationship("Player", back_populates="sport")


class Team(Base):
    """
    Team dimension table.

    Associates teams to sports and optional conference/division metadata.

    Attributes
    ----------
    id : int
        Primary key.
    name : str
        Team full name.
    abbreviation : str
        Team short code.
    sport_id : int
        Foreign key to :class:`Sport`.
    city : str or None
        Team city.
    conference : str or None
        Conference name, if applicable.
    division : str or None
        Division name, if applicable.
    """
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    abbreviation = Column(String(10), nullable=False)
    sport_id = Column(Integer, ForeignKey("sports.id"), nullable=False)
    city = Column(String(100))
    conference = Column(String(50))
    division = Column(String(50))
    sport = relationship("Sport", back_populates="teams")
    players = relationship("Player", back_populates="team")


class Player(Base):
    """
    Player dimension table.

    Stores roster entities and links them to teams and sports.

    Attributes
    ----------
    id : int
        Primary key.
    name : str
        Player full name.
    position : str or None
        Position label.
    team_id : int or None
        Foreign key to :class:`Team`.
    sport_id : int
        Foreign key to :class:`Sport`.
    active : bool
        Whether the player is currently active.
    external_id : str or None
        Upstream provider identifier.
    """
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    position = Column(String(20))
    team_id = Column(Integer, ForeignKey("teams.id"))
    sport_id = Column(Integer, ForeignKey("sports.id"), nullable=False)
    active = Column(Boolean, default=True)
    external_id = Column(String(100))
    team = relationship("Team", back_populates="players")
    sport = relationship("Sport", back_populates="players")
    stats = relationship("PlayerStat", back_populates="player")


class Game(Base):
    """
    Scheduled game/event table.

    Represents matchups between two teams for a specific sport and date.

    Attributes
    ----------
    id : int
        Primary key.
    home_team_id : int
        Foreign key to home :class:`Team`.
    away_team_id : int
        Foreign key to away :class:`Team`.
    sport_id : int
        Foreign key to :class:`Sport`.
    scheduled_at : datetime
        Scheduled start time.
    status : str
        Game status string (for example, ``scheduled`` or ``final``).
    home_score : int or None
        Home team score.
    away_score : int or None
        Away team score.
    season : str or None
        Season identifier.
    week : int or None
        Week or round number where applicable.
    """
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    external_id = Column(String(64), unique=True)
    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    sport_id = Column(Integer, ForeignKey("sports.id"), nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    status = Column(String(20), default="scheduled")
    home_score = Column(Integer)
    away_score = Column(Integer)
    period = Column(String(40))
    time_remaining = Column(String(20))
    opening_total = Column(Float)
    current_line = Column(Float)
    projected_total = Column(Float)
    pace_factor = Column(Float)
    recommendation = Column(String(10))
    season = Column(String(20))
    week = Column(Integer)
    odds_lines = relationship("OddsLine", back_populates="game")
    picks = relationship("Pick", back_populates="game")


class OddsLine(Base):
    """
    Sportsbook odds snapshot table.

    Captures market-specific lines and opening/closing flags.

    Attributes
    ----------
    id : int
        Primary key.
    game_id : int
        Foreign key to :class:`Game`.
    sportsbook : str
        Sportsbook name.
    market_type : str
        Market identifier (for example, ``moneyline``).
    home_line : float or None
        Home-side line.
    away_line : float or None
        Away-side line.
    total : float or None
        Total points/runs/goals line.
    vig : float or None
        Market vig value.
    timestamp : datetime
        UTC timestamp when the line snapshot was captured.
    is_opening : bool
        Whether this snapshot is the opening line.
    is_closing : bool
        Whether this snapshot is the closing line.
    """
    __tablename__ = "odds_lines"
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    sportsbook = Column(String(50), nullable=False)
    market_type = Column(String(30), nullable=False)
    home_line = Column(Float)
    away_line = Column(Float)
    total = Column(Float)
    vig = Column(Float)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_opening = Column(Boolean, default=False)
    is_closing = Column(Boolean, default=False)
    game = relationship("Game", back_populates="odds_lines")


class Pick(Base):
    """
    Model-generated pick table.

    Stores prediction metadata, rationale, and post-game result fields.

    Attributes
    ----------
    id : int
        Primary key.
    game_id : int
        Foreign key to :class:`Game`.
    sport_id : int
        Foreign key to :class:`Sport`.
    pick_type : str
        Bet type (for example, ``spread``).
    selection : str
        Chosen side or outcome.
    line : float or None
        Applied betting line.
    model_version : str or None
        Model version identifier.
    confidence_tier : str or None
        Tier label (for example, ``A``/``B``/``C``).
    rationale : str or None
        Human-readable model rationale.
    result : str or None
        Settlement result code.
    profit_loss : float or None
        Profit/loss in units or currency.
    created_at : datetime
        UTC creation timestamp.
    resolved_at : datetime or None
        UTC settlement timestamp.
    """
    __tablename__ = "picks"
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    sport_id = Column(Integer, ForeignKey("sports.id"), nullable=False)
    pick_type = Column(String(30), nullable=False)
    selection = Column(String(100), nullable=False)
    line = Column(Float)
    model_version = Column(String(50))
    confidence_tier = Column(String(5))
    grade = Column(String(5))
    ml_score = Column(Float)
    is_free_pick = Column(Boolean, default=False)
    rationale = Column(Text)
    result = Column(String(10))
    profit_loss = Column(Float)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    resolved_at = Column(DateTime)
    game = relationship("Game", back_populates="picks")


class ModelVersion(Base):
    """
    Model version metadata table.

    Tracks deployed model versions and their descriptions by sport.

    Attributes
    ----------
    id : int
        Primary key.
    name : str
        Model family name.
    sport_id : int or None
        Optional foreign key to :class:`Sport`.
    version : str
        Version tag.
    description : str or None
        Model changelog/description.
    created_at : datetime
        UTC creation timestamp.
    """
    __tablename__ = "model_versions"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    sport_id = Column(Integer, ForeignKey("sports.id"))
    version = Column(String(20), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Expert(Base):
    """
    Expert capper profile table.

    Stores marketplace-facing expert metadata and performance metrics.

    Attributes
    ----------
    id : int
        Primary key.
    username : str
        Unique username.
    display_name : str
        Public display name.
    verified : bool
        Verification status flag.
    bio : str or None
        Expert biography.
    win_rate : float or None
        Historical win rate.
    roi : float or None
        Historical ROI percentage.
    total_picks : int
        Total number of tracked picks.
    """
    __tablename__ = "experts"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    display_name = Column(String(100), nullable=False)
    verified = Column(Boolean, default=False)
    bio = Column(Text)
    win_rate = Column(Float)
    roi = Column(Float)
    total_picks = Column(Integer, default=0)
    expert_picks = relationship("ExpertPick", back_populates="expert")


class ExpertPick(Base):
    """
    Expert pick history table.

    Stores picks made by experts and their eventual outcomes.

    Attributes
    ----------
    id : int
        Primary key.
    expert_id : int
        Foreign key to :class:`Expert`.
    game_id : int
        Foreign key to :class:`Game`.
    pick_type : str
        Bet type.
    selection : str
        Chosen side or outcome.
    line : float or None
        Applied betting line.
    result : str or None
        Settlement result code.
    profit_loss : float or None
        Profit/loss value.
    created_at : datetime
        UTC creation timestamp.
    """

    __tablename__ = "expert_picks"
    id = Column(Integer, primary_key=True)
    expert_id = Column(Integer, ForeignKey("experts.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    pick_type = Column(String(30), nullable=False)
    selection = Column(String(100), nullable=False)
    line = Column(Float)
    result = Column(String(10))
    profit_loss = Column(Float)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expert = relationship("Expert", back_populates="expert_picks")


class PlayerStat(Base):
    """
    Player game-stat table.

    Stores stat observations for a player in a specific game context.

    Attributes
    ----------
    id : int
        Primary key.
    player_id : int
        Foreign key to :class:`Player`.
    game_id : int
        Foreign key to :class:`Game`.
    stat_type : str
        Statistic label (for example, ``points``).
    value : float
        Recorded stat value.
    context : str or None
        Additional context (for example, split or segment).
    """

    __tablename__ = "player_stats"
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    stat_type = Column(String(50), nullable=False)
    value = Column(Float, nullable=False)
    context = Column(String(200))
    player = relationship("Player", back_populates="stats")


DEFAULT_DATABASE_URL = os.getenv("SPORTALYTICS_DATABASE_URL", "sqlite:///./sportalytics.db")

_engine: Engine | None = None
_session_factory: sessionmaker[Session] | None = None
_db_initialized = False


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(DEFAULT_DATABASE_URL, future=True)
    return _engine


def get_session_factory() -> sessionmaker[Session]:
    global _session_factory
    if _session_factory is None:
        _session_factory = sessionmaker(bind=get_engine(), expire_on_commit=False, future=True)
    return _session_factory


@contextmanager
def session_scope() -> Session:
    session = get_session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db() -> None:
    global _db_initialized
    if _db_initialized:
        return

    Base.metadata.create_all(get_engine())
    with session_scope() as session:
        if session.scalar(select(Sport.id).limit(1)) is None:
            _seed_demo_data(session)
    _db_initialized = True


def _seed_demo_data(session: Session) -> None:
    sports_map: dict[str, Sport] = {}
    for abbr, name in [
        ("NBA", "National Basketball Association"),
        ("NFL", "National Football League"),
        ("NHL", "National Hockey League"),
        ("MLB", "Major League Baseball"),
        ("UFC", "Ultimate Fighting Championship"),
        ("CFB", "College Football"),
        ("CBB", "College Basketball"),
    ]:
        sport = Sport(name=name, abbreviation=abbr)
        session.add(sport)
        sports_map[abbr] = sport

    session.flush()

    teams_map: dict[tuple[str, str], Team] = {}

    def _team(sport_abbr: str, name: str, city: str = "") -> Team:
        key = (sport_abbr, name)
        if key in teams_map:
            return teams_map[key]
        team = Team(
            name=name,
            abbreviation=(name[:3] if len(name) >= 3 else name).upper(),
            sport_id=sports_map[sport_abbr].id,
            city=city,
        )
        session.add(team)
        session.flush()
        teams_map[key] = team
        return team

    now = datetime.now(timezone.utc)

    game_specs = [
        ("nba-001", "NBA", "Lakers", "Celtics", "scheduled"),
        ("nfl-001", "NFL", "Chiefs", "Bills", "scheduled"),
        ("nhl-001", "NHL", "Bruins", "Rangers", "scheduled"),
        ("mlb-001", "MLB", "Yankees", "Red Sox", "scheduled"),
        ("ufc-001", "UFC", "Jones", "Miocic", "scheduled"),
        ("cfb-001", "CFB", "Alabama", "Georgia", "scheduled"),
        ("cbb-001", "CBB", "Duke", "UNC", "scheduled"),
        ("nba-live-001", "NBA", "Lakers", "Celtics", "live"),
        ("nhl-live-001", "NHL", "Bruins", "Rangers", "live"),
        ("nfl-live-001", "NFL", "Chiefs", "Bills", "live"),
        ("nba-free-001", "NBA", "Celtics", "Knicks", "scheduled"),
    ]

    games_map: dict[str, Game] = {}
    for ext_id, sport, home_name, away_name, status in game_specs:
        home = _team(sport, home_name)
        away = _team(sport, away_name)
        game = Game(
            external_id=ext_id,
            home_team_id=home.id,
            away_team_id=away.id,
            sport_id=sports_map[sport].id,
            scheduled_at=now,
            status=status,
        )
        games_map[ext_id] = game
        session.add(game)

    session.flush()

    # Live game metrics used by live_totals service
    live_updates = {
        "nba-live-001": dict(period="3rd Quarter", time_remaining="4:32", home_score=78, away_score=82, opening_total=224.5, current_line=224.5, projected_total=221.3, pace_factor=1.02, recommendation="Under"),
        "nhl-live-001": dict(period="2nd Period", time_remaining="11:20", home_score=2, away_score=1, opening_total=5.5, current_line=4.5, projected_total=5.1, pace_factor=0.97, recommendation="Over"),
        "nfl-live-001": dict(period="2nd Quarter", time_remaining="2:15", home_score=14, away_score=10, opening_total=48.5, current_line=47.5, projected_total=49.2, pace_factor=1.05, recommendation="Over"),
    }
    for ext_id, values in live_updates.items():
        game = games_map[ext_id]
        for key, value in values.items():
            setattr(game, key, value)

    picks_seed = [
        ("nba-001", "spread", "Celtics -3.5", -3.5, "A", "A", 0.84, "Celtics have covered 8 of last 10 at home. Lakers missing key rotation players."),
        ("nfl-001", "moneyline", "Chiefs ML", -145, "B", "B", 0.72, "Chiefs 12-3 ATS as favorites. Mahomes 8-1 vs Bills in last 9."),
        ("nhl-001", "total", "Under 5.5", 5.5, "B", "B", 0.68, "Both teams top-5 defensive units. Goalies are hot."),
        ("mlb-001", "moneyline", "Yankees ML", -120, "C", "C", 0.59, "Cole on mound. Yankees 65% win rate with Cole starting."),
        ("ufc-001", "moneyline", "Jones ML", -280, "A", "A", 0.86, "Jones dominant grappling advantage. Miocic age factor."),
        ("cfb-001", "spread", "Georgia +3", 3.0, "B", "B", 0.7, "Georgia 7-2 ATS as road underdog. Alabama secondary injuries."),
        ("cbb-001", "total", "Over 147", 147.0, "A", "A", 0.81, "Both teams pace top 20 nationally with high-scoring profiles."),
    ]
    for ext_id, pick_type, selection, line, confidence, grade, ml_score, rationale in picks_seed:
        game = games_map[ext_id]
        session.add(
            Pick(
                game_id=game.id,
                sport_id=game.sport_id,
                pick_type=pick_type,
                selection=selection,
                line=line,
                model_version="v2.1",
                confidence_tier=confidence,
                grade=grade,
                ml_score=ml_score,
                rationale=rationale,
                created_at=now,
            )
        )

    # Current free pick
    free_game = games_map["nba-free-001"]
    session.add(
        Pick(
            game_id=free_game.id,
            sport_id=free_game.sport_id,
            pick_type="spread",
            selection="Celtics -5.5",
            line=-5.5,
            model_version="v2.1",
            confidence_tier="A",
            grade="A+",
            ml_score=0.84,
            rationale="Celtics are 8-2 ATS in last 10 home games. Knicks missing Brunson.",
            is_free_pick=True,
            created_at=now,
        )
    )

    # Free-pick history (graded)
    history = [
        ("nfl-001", "Chiefs -3", "W", "A"),
        ("nba-001", "Celtics ML", "W", "B"),
        ("mlb-001", "Under 9", "L", "B"),
        ("nhl-001", "Bruins ML", "W", "A"),
        ("cbb-001", "Over 147", "W", "A"),
        ("nhl-001", "Over 6", "L", "C"),
        ("cfb-001", "Georgia +3", "W", "B"),
    ]
    for idx, (ext_id, selection, result, grade) in enumerate(history, start=1):
        game = games_map[ext_id]
        session.add(
            Pick(
                game_id=game.id,
                sport_id=game.sport_id,
                pick_type="spread",
                selection=selection,
                line=None,
                model_version="v2.1",
                confidence_tier=grade[0],
                grade=grade,
                ml_score=0.6,
                rationale="Historical free pick result.",
                is_free_pick=True,
                result=result,
                created_at=now.replace(day=max(1, now.day - idx)),
            )
        )

    # Odds snapshots for odds-insight and live totals odds
    odds_seed = [
        ("nba-001", "moneyline", "DraftKings", 145, -165),
        ("nba-001", "moneyline", "FanDuel", 150, -172),
        ("nba-001", "moneyline", "BetMGM", 140, -160),
        ("nba-001", "moneyline", "Caesars", 145, -168),
        ("nba-001", "moneyline", "PointsBet", 155, -175),
        ("nba-001", "moneyline", "BetRivers", 142, -162),
        ("nba-001", "moneyline", "WynnBet", 148, -170),
        ("nfl-001", "spread", "DraftKings", -3.0, 3.0),
        ("nfl-001", "spread", "FanDuel", -3.5, 3.5),
        ("nfl-001", "spread", "BetMGM", -3.0, 3.0),
        ("nfl-001", "spread", "Caesars", -3.5, 3.5),
        ("nfl-001", "spread", "PointsBet", -3.0, 3.0),
        ("nfl-001", "spread", "BetRivers", -3.5, 3.5),
        ("nfl-001", "spread", "WynnBet", -3.0, 3.0),
        ("nba-live-001", "total_odds", "DraftKings", -115, -105),
        ("nhl-live-001", "total_odds", "DraftKings", -110, -110),
        ("nfl-live-001", "total_odds", "DraftKings", -120, 100),
    ]
    for ext_id, market, book, home_line, away_line in odds_seed:
        game = games_map[ext_id]
        session.add(
            OddsLine(
                game_id=game.id,
                sportsbook=book,
                market_type=market,
                home_line=home_line,
                away_line=away_line,
                timestamp=now,
            )
        )

