import random
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.expressions import Q

from toolhunt.config import get_settings
from toolhunt.models.pydantic import TaskSchema
from toolhunt.models.tortoise import Task

router = APIRouter()

settings = get_settings()


# CRUD
async def get_tasks_from_db(
    field_name: Optional[str] = None, tool_name: Optional[str] = None
) -> List[TaskSchema]:
    query = Task.all().prefetch_related("tool_name", "field_name")

    if field_name:
        query = query.filter(field_name=field_name)
    if tool_name:
        query = query.filter(tool_name=tool_name)

    if settings.environment != "dev":
        # Filter out tasks attempted in the last 24 hours
        twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
        query = query.filter(
            Q(last_attempted__isnull=True) | Q(last_attempted__lt=twenty_four_hours_ago)
        )

    tasks = await query
    random_tasks = random.sample(tasks, min(len(tasks), 10))

    # Update last_attempted and times_attempted fields
    for task in random_tasks:
        task.last_attempted = datetime.now()
        task.times_attempted += 1
        await task.save(update_fields=["last_attempted", "times_attempted"])

    return [
        TaskSchema(id=task.id, tool=task.tool_name, field=task.field_name)
        for task in random_tasks
    ]


async def get_task_from_db(task_id: int) -> Optional[TaskSchema]:
    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
    query = Task.filter(id=task_id)

    if settings.environment != "dev":
        query = query.filter(
            Q(last_attempted__isnull=True) | Q(last_attempted__lt=twenty_four_hours_ago)
        )

    task = await query.first()
    if task:
        task.last_attempted = datetime.now()
        task.times_attempted += 1
        await task.save(update_fields=["last_attempted", "times_attempted"])
        return TaskSchema(id=task.id, tool=task.tool_name, field=task.field_name)
    return None


# Routes
@router.get(
    "/tasks",
    response_model=List[TaskSchema],
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_tasks(
    field_name: Optional[str] = Query(None), tool_name: Optional[str] = Query(None)
):
    tasks = await get_tasks_from_db(field_name=field_name, tool_name=tool_name)
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    return tasks


@router.get(
    "/tasks/{id}",
    response_model=TaskSchema,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_task(id: int):
    task = await get_task_from_db(id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
