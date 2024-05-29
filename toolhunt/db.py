import logging
import os

from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise

log = logging.getLogger("uvicorn")

TORTOISE_ORM = {
    "connections": {"default": os.getenv("DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["toolhunt.models.tortoise", "aerich.models"],
            "default_connection": "default",
        }
    },
}


def register_tortoise(app: FastAPI) -> RegisterTortoise:
    return RegisterTortoise(
        app,
        db_url=os.getenv("DATABASE_URL"),
        modules={"models": ["toolhunt.models.tortoise"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )
