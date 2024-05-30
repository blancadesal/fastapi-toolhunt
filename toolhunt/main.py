import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import toml
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


def get_project_metadata():
    with open("pyproject.toml", "r") as pyproject_file:
        pyproject_data = toml.load(pyproject_file)
        metadata = pyproject_data["tool"]["poetry"]
        return metadata["name"], metadata["version"]


title, version = get_project_metadata()


def create_app() -> FastAPI:
    app = FastAPI(
        title=title,
        version=version,
        openapi_tags=[
            {
                "name": "contributions",
                "description": "Get information about contributions made using Toolhunt.",
            },
            {
                "name": "tasks",
                "description": "Get incomplete tasks and submit data to Toolhub.",
            },
            {"name": "tools", "description": "Get information about tools."},
        ],
        lifespan=lifespan,
    )
    # routers
    app.include_router(ping.router, prefix=API_PREFIX)
    app.include_router(tasks.router, prefix=API_PREFIX, tags=["tasks"])
    app.include_router(tools.router, prefix=API_PREFIX, tags=["tools"])
    app.include_router(contributions.router, prefix=API_PREFIX, tags=["contributions"])
    return app


app = create_app()
