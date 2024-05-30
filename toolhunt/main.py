import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from toolhunt.api import contributions, ping, tasks, tools
from toolhunt.db import register_tortoise

log = logging.getLogger("uvicorn")

API_PREFIX = "/api/v1"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    log.info("Starting up...")
    async with register_tortoise(app):
        log.info("Database registered.")
        yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(ping.router, prefix=API_PREFIX)
    app.include_router(tasks.router, prefix=API_PREFIX, tags=["tasks"])
    app.include_router(tools.router, prefix=API_PREFIX, tags=["tools"])
    app.include_router(contributions.router, prefix=API_PREFIX, tags=["contributions"])
    return app


app = create_app()
