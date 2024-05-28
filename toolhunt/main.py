import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

# from toolhunt.db import init_db
from tortoise.contrib.fastapi import RegisterTortoise

from toolhunt.api import ping, tasks

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
    return app


app = create_app()
