from fastapi import APIRouter, HTTPException
from tortoise.exceptions import OperationalError

from toolhunt.models.pydantic import ToolNamesResponse
from toolhunt.models.tortoise import Tool

router = APIRouter(prefix="/tools")


@router.get("/names", response_model=ToolNamesResponse)
async def get_tool_names():
    """Get the human-readable titles of all tools, and their Toolhub names."""
    try:
        tools = await Tool.all().values("name", "title")
        title_collection = {
            "allTitles": [tool["title"] for tool in tools],
            "titles": {},
        }
        for tool in tools:
            title_collection["titles"][tool["title"]] = tool["name"]
        return title_collection
    except OperationalError:
        raise HTTPException(
            status_code=503, detail="Database connection failed. Please try again."
        )
