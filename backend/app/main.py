from sqlalchemy import inspect, text
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.doctors import router as doctors_router
from app.database import Base, configure_database, engine, SessionLocal
from app.models.doctor import Doctor
from app.seed_data import seed_doctors



# AGENTIC_SDLC_ADDITIVE_SCHEMA_UPGRADE: preserve existing project data while adding new ORM fields.
def _ensure_additive_schema_updates():
    inspector = inspect(engine)
    with engine.begin() as connection:
        for table in Base.metadata.sorted_tables:
            if not inspector.has_table(table.name):
                continue
            existing_columns = {column["name"] for column in inspector.get_columns(table.name)}
            for column in table.columns:
                if column.primary_key or column.name in existing_columns:
                    continue
                table_name = table.name.replace('"', '""')
                column_name = column.name.replace('"', '""')
                column_type = column.type.compile(dialect=engine.dialect)
                connection.execute(
                    text(
                        f'ALTER TABLE "{table_name}" ADD COLUMN IF NOT EXISTS '
                        f'"{column_name}" {column_type}'
                    )
                )

app = FastAPI(title="Doctor Search API", version="1.0.0")
app.include_router(doctors_router)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    query_errors = [error for error in exc.errors() if "q" in error.get("loc", ())]
    if query_errors:
        return JSONResponse(
            status_code=400,
            content={"error": "invalid_request", "message": "Search query cannot be empty"},
        )
    return JSONResponse(
        status_code=400,
        content={"error": "invalid_request", "message": "Invalid request"},
    )


@app.exception_handler(HTTPException)
async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    if isinstance(exc.detail, dict) and "error" in exc.detail and "message" in exc.detail:
        content = exc.detail
    else:
        content = {"error": "http_error", "message": str(exc.detail)}
    return JSONResponse(status_code=exc.status_code, content=content, headers=exc.headers)


@app.on_event("startup")
def initialize_database() -> None:
    configure_database()
    if engine is None or SessionLocal is None:
        raise RuntimeError("Database configuration failed")
    _ensure_additive_schema_updates()
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_doctors(db)
    finally:
        db.close()


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/health")
async def _agentic_health():
    return {"status": "healthy"}

# AGENTIC_SDLC_SPA_STATIC: serve the built frontend from ./static on the deploy URL.
import os as _spa_os
import mimetypes as _spa_mimetypes
from pathlib import Path as _SpaPath
from fastapi.responses import FileResponse as _SpaFileResponse

# Browsers enforce strict MIME types for ES modules (.mjs) and WebAssembly
# (.wasm). Python's default mimetypes serves them as application/octet-stream,
# which the browser rejects ("non-JavaScript MIME type"), breaking modern
# bundles (Vite chunks, the pdf.js worker, etc). Register + map them explicitly.
_spa_mimetypes.add_type("text/javascript", ".js")
_spa_mimetypes.add_type("text/javascript", ".mjs")
_spa_mimetypes.add_type("application/wasm", ".wasm")
_spa_mimetypes.add_type("application/json", ".map")

_SPA_MEDIA_TYPES = {
    ".js": "text/javascript",
    ".mjs": "text/javascript",
    ".wasm": "application/wasm",
    ".css": "text/css",
    ".json": "application/json",
    ".map": "application/json",
    ".svg": "image/svg+xml",
}


def _spa_media_type(path):
    return _SPA_MEDIA_TYPES.get(_SpaPath(str(path)).suffix.lower())


def _spa_file_response(path):
    media = _spa_media_type(path)
    return _SpaFileResponse(path, media_type=media) if media else _SpaFileResponse(path)


def _spa_find_static_dir() -> _SpaPath:
    here = _SpaPath(__file__).resolve()
    candidates = [
        here.parent.parent / "static",
        here.parent / "static",
        here.parent.parent.parent / "static",
        _SpaPath(_spa_os.getcwd()) / "static",
        _SpaPath("/app/static"),
    ]
    for cand in candidates:
        if (cand / "index.html").is_file():
            return cand
    for cand in candidates:
        if cand.is_dir():
            return cand
    return candidates[0]


_STATIC_DIR = _spa_find_static_dir()


@app.get("/")
async def _agentic_spa_root():
    index = _STATIC_DIR / "index.html"
    if index.is_file():
        return _spa_file_response(index)
    return {"message": "API is running", "status": "healthy"}


@app.get("/{full_path:path}")
async def _agentic_spa_fallback(full_path: str):
    reserved = ("api", "health", "docs", "openapi.json", "redoc")
    first = (full_path or "").split("/", 1)[0]
    if first in reserved:
        from fastapi.responses import JSONResponse as _SpaJSON
        return _SpaJSON({"detail": "Not Found"}, status_code=404)
    candidate = (_STATIC_DIR / full_path).resolve()
    static_root = _STATIC_DIR.resolve()
    if str(candidate).startswith(str(static_root)) and candidate.is_file():
        return _spa_file_response(candidate)
    # Missing JS/CSS/font assets must 404 — returning index.html here breaks the UI.
    asset_ext = (".js", ".mjs", ".wasm", ".css", ".map", ".woff", ".woff2", ".ttf", ".svg", ".png", ".jpg", ".ico")
    if full_path and full_path.lower().endswith(asset_ext):
        from fastapi.responses import JSONResponse as _SpaJSON
        return _SpaJSON({"detail": "Not Found"}, status_code=404)
    index = _STATIC_DIR / "index.html"
    if index.is_file():
        return _spa_file_response(index)
    from fastapi.responses import JSONResponse as _SpaJSON
    return _SpaJSON({"detail": "Not Found"}, status_code=404)


# AGENTIC_SDLC_TABLE_BOOTSTRAP: import every mapped model, then create missing tables.
# `create_all` only creates what is registered on `Base.metadata`, and a model
# module that no import chain reaches registers nothing — which is how a
# deployed app ends up answering `UndefinedTable` for its own tables.
_AGENTIC_MODEL_MODULES = (
    'app.models.doctor',
)


def _agentic_bootstrap_tables() -> None:
    import importlib
    import logging as _agentic_logging
    import time as _agentic_time

    _agentic_log = _agentic_logging.getLogger("agentic_sdlc.bootstrap")
    _agentic_backoff = 2
    for _module_name in _AGENTIC_MODEL_MODULES:
        try:
            importlib.import_module(_module_name)
        except Exception as _exc:  # a broken model must not mask the others
            _agentic_log.warning("model module %s not imported: %s", _module_name, _exc)
    def _agentic_create_all() -> None:
        Base.metadata.create_all(bind=engine)

    _agentic_attempts = 5
    for _agentic_attempt in range(1, _agentic_attempts + 1):
        try:
            _agentic_create_all()
            break
        except Exception as _exc:
            if _agentic_attempt == _agentic_attempts:
                _agentic_log.error(
                    "schema bootstrap failed after %s attempts: %s; the app will "
                    "still start so /docs and /health respond, but every "
                    "database-backed route will fail until the schema exists — "
                    "restart this container once the database is reachable",
                    _agentic_attempt,
                    _exc,
                )
                break
            _agentic_log.warning(
                "schema bootstrap attempt %s/%s failed (%s); retrying in %ss",
                _agentic_attempt,
                _agentic_attempts,
                _exc,
                _agentic_backoff,
            )
            _agentic_time.sleep(_agentic_backoff)

    _agentic_log.info(
        "startup schema ready: %s", ", ".join(sorted(Base.metadata.tables)) or "no tables"
    )


# Do NOT touch the database while unit tests import this module: create_all opens
# a real connection and, with no DB reachable in the test sandbox, hangs until the
# 60s test timeout. Tests set up their own DB via fixtures/overrides. Production
# (uvicorn) has no `pytest` imported, so the bootstrap runs normally.
import sys as _agentic_sys

if "pytest" not in _agentic_sys.modules:
    _agentic_bootstrap_tables()
