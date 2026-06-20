from sqlalchemy import Column, ForeignKey, Table

from app.models.base import Base

anime_genres = Table(
    "anime_genres",
    Base.metadata,
    Column("anime_id", ForeignKey("animes.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True),
)
