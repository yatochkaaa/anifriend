import json
from pathlib import Path

from fastapi.openapi.utils import get_openapi

from app.main import app

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "openapi.json"

openapi_schema = get_openapi(
    title=app.title,
    version=app.version,
    routes=app.routes,
)

with open(OUTPUT_PATH, "w") as f:
    json.dump(openapi_schema, f, indent=2)
