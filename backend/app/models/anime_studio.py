from sqlalchemy import Column, ForeignKey, Table

from app.models.base import Base

anime_studios = Table(
    "anime_studios",
    Base.metadata,
    Column("anime_id", ForeignKey("animes.id", ondelete="CASCADE"), primary_key=True),
    Column("studio_id", ForeignKey("studios.id"), primary_key=True),
)
