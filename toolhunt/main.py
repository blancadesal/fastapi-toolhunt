import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise

from toolhunt.api import contributions, ping, tasks, tools

log = logging.getLogger("uvicorn")

API_PREFIX = "/api/v1"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # app startup
    async with RegisterTortoise(
        app,
        db_url=os.getenv("DATABASE_URL"),
        modules={"models": ["toolhunt.models.tortoise"]},
        generate_schemas=False,
        add_exception_handlers=True,
    ):
        # db connected
        yield
        # app teardown
    # db connections closed


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(ping.router, prefix=API_PREFIX)
    app.include_router(tasks.router, prefix=API_PREFIX, tags=["tasks"])
    app.include_router(tools.router, prefix=API_PREFIX, tags=["tools"])
    app.include_router(contributions.router, prefix=API_PREFIX, tags=["contributions"])
    return app


app = create_app()
