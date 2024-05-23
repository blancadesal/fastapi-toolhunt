import os


TORTOISE_ORM = {
    "connections": {
        "default": os.getenv("DATABASE_URL")
    },
    "apps": {
        "models": {
            "models": ["toolhunt.models.tortoise", "aerich.models"],
            "default_connection": "default",
        }
    }
}


