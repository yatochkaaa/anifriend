#! /usr/bin/env bash

set -e

# Run migrations
alembic upgrade head

# Create genres in DB
python scripts/seed_genres.py