from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from kb_api.api import documents
from kb_api.db import engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield  # the app serves requests here
    await engine.dispose()  # close database connections on shutdown


def create_app() -> FastAPI:
    app = FastAPI(title="kb-api", version="0.1.0", lifespan=lifespan)
    app.include_router(documents.router)

    @app.get("/healthz", tags=["health"])
    async def healthz() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
