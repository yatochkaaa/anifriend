import psycopg
from alembic.config import Config

from alembic import command

POSTGRES_DEFAULT_DB = "postgres"
POSTGRES_TEST_DB = "anifriend_test"
POSTGRES_SERVER = "localhost"
POSTGRES_PORT = 5432
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"

DEFAULT_DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DEFAULT_DB}"
TEST_DB_URL = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_TEST_DB}"


async def create_test_db() -> None:
    conn = await psycopg.AsyncConnection.connect(DEFAULT_DB_URL, autocommit=True)
    await conn.execute("DROP DATABASE IF EXISTS anifriend_test WITH (FORCE)")
    await conn.execute("CREATE DATABASE anifriend_test")
    await conn.close()


async def drop_test_db() -> None:
    conn = await psycopg.AsyncConnection.connect(DEFAULT_DB_URL, autocommit=True)
    await conn.execute("DROP DATABASE anifriend_test")
    await conn.close()


def run_test_migrations(db_url: str) -> None:
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)
    command.upgrade(alembic_cfg, "head")
