from sqlalchemy import Column, ForeignKey, Table

from .base import Base

survey_animes = Table(
    "survey_animes",
    Base.metadata,
    Column("survey_id", ForeignKey("surveys.id", ondelete="CASCADE"), primary_key=True),
    Column("anime_id", ForeignKey("animes.id", ondelete="CASCADE"), primary_key=True),
)
