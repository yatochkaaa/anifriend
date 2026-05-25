# Install uv
FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1

# Install uv
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.11.14 /uv /uvx /bin/

# Disable development dependencies
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-a-project
ENV UV_NO_DEV=1

# Compile bytecode
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
ENV UV_COMPILE_BYTECODE=1

# uv Cache
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#caching
ENV UV_LINK_MODE=copy

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app/

# Place executables in the environment at the front of the path
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment
ENV PATH="/app/.venv/bin:$PATH"

COPY uv.lock pyproject.toml ./

# Install dependencies
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
RUN --mount=type=cache,id=s/533d3a56-ef55-44c6-abf6-355b3c466748-/root/.cache/uv,target=/root/.cache/uv \
    uv sync --locked --no-install-project

COPY ./scripts /app/backend/scripts

COPY ./pyproject.toml ./alembic.ini /app/backend/
COPY ./alembic /app/backend/alembic

COPY ./app /app/backend/app

# Sync the project
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
RUN --mount=type=cache,id=s/533d3a56-ef55-44c6-abf6-355b3c466748-/root/.cache/uv,target=/root/.cache/uv \
    uv sync --frozen --no-install-workspace

WORKDIR /app/backend/

CMD fastapi run app/main.py --port $PORT