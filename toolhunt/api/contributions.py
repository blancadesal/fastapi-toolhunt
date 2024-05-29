from typing import List, Optional

from fastapi import APIRouter, Query

from toolhunt.models.pydantic import CompletedTaskSchema
from toolhunt.models.tortoise import CompletedTask

router = APIRouter()


@router.get("/contributions", response_model=List[CompletedTaskSchema])
async def get_contributions(
    limit: Optional[int] = Query(
        None, description="Limit the number of contributions returned"
    ),
):
    query = CompletedTask.all().order_by("-completed_date")
    if limit:
        query = query.limit(limit)

    results = await query.values(
        "completed_date", "field__name", "tool__name", "tool_title", "user"
    )
    contributions = [
        {
            "completed_date": result["completed_date"].strftime("%Y-%m-%dT%H:%M:%S"),
            "field": result["field__name"],
            "tool_name": result["tool__name"],
            "tool_title": result["tool_title"],
            "user": result["user"],
        }
        for result in results
    ]
    return contributions
