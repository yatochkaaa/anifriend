import asyncio

from httpx import AsyncClient
from sqlalchemy import select

from app.core.db import async_session_maker
from app.integrations import MalClient
from app.integrations.mal import MalAnime
from app.models import Anime, AnimeSynonym, Genre, Studio


def convert_anime_mal_to_db(
    anime: MalAnime, genres_map: dict[int, Genre], studios_map: dict[int, Studio]
) -> Anime:
    alt = anime.alternative_titles
    picture = anime.main_picture
    start_season = anime.start_season
    broadcast = anime.broadcast

    return Anime(
        mal_id=anime.id,
        name=anime.title,
        english=alt.en if alt else None,
        japanese=alt.ja if alt else None,
        poster_url=picture.medium if picture else None,
        synopsis=anime.synopsis,
        score=anime.mean,
        rank=anime.rank,
        popularity=anime.popularity,
        nsfw=anime.nsfw,
        kind=anime.media_type,
        status=anime.status,
        episodes=anime.num_episodes,
        source=anime.source,
        average_episode_duration=anime.average_episode_duration,
        aired_on=anime.start_date,
        released_on=anime.end_date,
        aired_year=start_season.year if start_season else None,
        season=start_season.season if start_season else None,
        broadcast_day=broadcast.day_of_the_week if broadcast else None,
        broadcast_time=broadcast.start_time if broadcast else None,
        genres=[genres_map[mal_genre.id] for mal_genre in anime.genres],
        studios=[studios_map[mal_studio.id] for mal_studio in anime.studios],
        synonyms=[AnimeSynonym(value=v) for v in (alt.synonyms if alt else [])],
    )


async def seed_animes() -> None:
    animes_map: dict[int, MalAnime] = {}
    genres_map: dict[int, Genre] = {}
    studios_map: dict[int, Studio] = {}

    async with async_session_maker() as session:
        db_genres = await session.execute(select(Genre))
        for db_genre in db_genres.scalars():
            genres_map[db_genre.mal_id] = db_genre
        db_studios = await session.execute(select(Studio))
        for db_studio in db_studios.scalars():
            studios_map[db_studio.mal_id] = db_studio

        existing = await session.execute(select(Anime.mal_id))
        existing_mal_ids = set(existing.scalars())

        async with AsyncClient() as client:
            mal_client = MalClient(client)
            offset = 0

            while offset < 5000:
                mal_animes = await mal_client.list_ranking(offset=offset)

                if not len(mal_animes):
                    break

                for mal_anime in mal_animes:
                    if mal_anime.id in existing_mal_ids:
                        continue

                    animes_map[mal_anime.id] = mal_anime

                    for mal_genre in mal_anime.genres:
                        if mal_genre.id not in genres_map:
                            genres_map[mal_genre.id] = Genre(
                                mal_id=mal_genre.id, name=mal_genre.name
                            )
                    for mal_studio in mal_anime.studios:
                        if mal_studio.id not in studios_map:
                            studios_map[mal_studio.id] = Studio(
                                mal_id=mal_studio.id, name=mal_studio.name
                            )

                offset += 500

        for genre in genres_map.values():
            session.add(genre)
        for studio in studios_map.values():
            session.add(studio)
        await session.commit()

        for anime in animes_map.values():
            db_anime = convert_anime_mal_to_db(anime, genres_map, studios_map)
            session.add(db_anime)
        await session.commit()


asyncio.run(seed_animes())
