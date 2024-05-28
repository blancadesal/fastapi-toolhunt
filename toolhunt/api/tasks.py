import random
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError

from toolhunt.models.pydantic import TaskSchema
from toolhunt.models.tortoise import Task

router = APIRouter()


# CRUD
async def get_tasks_from_db() -> List[TaskSchema]:
    tasks = await Task.all().prefetch_related("tool_name", "field_name")
    random_tasks = random.sample(tasks, min(len(tasks), 10))
    return [
        TaskSchema(id=task.id, tool=task.tool_name, field=task.field_name)
        for task in random_tasks
    ]


async def get_task_from_db(task_id: int) -> Optional[TaskSchema]:
    task = (
        await Task.filter(id=task_id)
        .prefetch_related("tool_name", "field_name")
        .first()
    )
    if task:
        return TaskSchema(id=task.id, tool=task.tool_name, field=task.field_name)
    return None


# Routes
@router.get(
    "/tasks",
    response_model=List[TaskSchema],
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_tasks():
    tasks = await get_tasks_from_db()
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
