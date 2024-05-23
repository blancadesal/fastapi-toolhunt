import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager

from toolhunt.api import ping
from toolhunt.db import init_db


log = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting up...")
    init_db(app)
    yield
    log.info("Shutting down...")

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(ping.router, prefix="/api/v1")
    return app

app = create_app()
