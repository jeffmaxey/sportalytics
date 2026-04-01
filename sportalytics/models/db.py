from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Sport(Base):
    __tablename__ = "sports"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    abbreviation = Column(String(10), nullable=False, unique=True)
    teams = relationship("Team", back_populates="sport")
    players = relationship("Player", back_populates="sport")


class Team(Base):
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
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    sport_id = Column(Integer, ForeignKey("sports.id"), nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    status = Column(String(20), default="scheduled")
    home_score = Column(Integer)
    away_score = Column(Integer)
    season = Column(String(20))
    week = Column(Integer)
    odds_lines = relationship("OddsLine", back_populates="game")
    picks = relationship("Pick", back_populates="game")


class OddsLine(Base):
    __tablename__ = "odds_lines"
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    sportsbook = Column(String(50), nullable=False)
    market_type = Column(String(30), nullable=False)
    home_line = Column(Float)
    away_line = Column(Float)
    total = Column(Float)
    vig = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_opening = Column(Boolean, default=False)
    is_closing = Column(Boolean, default=False)
    game = relationship("Game", back_populates="odds_lines")


class Pick(Base):
    __tablename__ = "picks"
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    sport_id = Column(Integer, ForeignKey("sports.id"), nullable=False)
    pick_type = Column(String(30), nullable=False)
    selection = Column(String(100), nullable=False)
    line = Column(Float)
    model_version = Column(String(50))
    confidence_tier = Column(String(5))
    rationale = Column(Text)
    result = Column(String(10))
    profit_loss = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime)
    game = relationship("Game", back_populates="picks")


class ModelVersion(Base):
    __tablename__ = "model_versions"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    sport_id = Column(Integer, ForeignKey("sports.id"))
    version = Column(String(20), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class Expert(Base):
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
    __tablename__ = "expert_picks"
    id = Column(Integer, primary_key=True)
    expert_id = Column(Integer, ForeignKey("experts.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    pick_type = Column(String(30), nullable=False)
    selection = Column(String(100), nullable=False)
    line = Column(Float)
    result = Column(String(10))
    profit_loss = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    expert = relationship("Expert", back_populates="expert_picks")


class PlayerStat(Base):
    __tablename__ = "player_stats"
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    stat_type = Column(String(50), nullable=False)
    value = Column(Float, nullable=False)
    context = Column(String(200))
    player = relationship("Player", back_populates="stats")
