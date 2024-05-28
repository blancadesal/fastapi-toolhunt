from fastapi import APIRouter, Depends

from toolhunt.config import get_settings, Settings


router = APIRouter()


@router.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing,
        "database_url": settings.database_url,
        "toolhub_api_endpoint": settings.toolhub_api_endpoint,
    }
