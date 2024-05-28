import json
from tortoise import Tortoise, run_async
from tortoise.exceptions import IntegrityError, DoesNotExist

from toolhunt.models.tortoise import Tool, Field, CompletedTask
from toolhunt.db import TORTOISE_ORM
from toolhunt.api.utils import logger
from update_db import run_pipeline


async def init():
    """Initialize the Tortoise ORM with the given configuration."""
    await Tortoise.init(config=TORTOISE_ORM)


async def insert_fields():
    """Insert field data from a JSON file into the database."""
    with open("tests/fixtures/field_data.json", "r") as f:
        fields_data = json.load(f)

    for field_data in fields_data:
        try:
            await Field.get_or_create(
                name=field_data["name"],
                defaults={
                    "description": field_data["description"],
                    "input_options": json.dumps(field_data.get("input_options", None)),
                    "pattern": field_data.get("pattern", None),
                },
            )
        except IntegrityError:
            logger.info(f"Field {field_data['name']} already exists.")


async def insert_tools():
    """Insert tool data from a JSON file and create tasks."""
    with open("tests/fixtures/tool_data.json", "r") as f:
        tool_data = json.load(f)

    await run_pipeline(test_data=tool_data)


async def insert_completed_tasks():
    """Insert completed task data from a JSON file into the database."""
    await init()

    with open("tests/fixtures/completed_task_data.json", "r") as f:
        completed_task_data = json.load(f)

    for task_data in completed_task_data:
        try:
            tool = await Tool.get(name=task_data["tool_name"])
            field = await Field.get(name=task_data["field"])
            await CompletedTask.get_or_create(
                tool=tool,
                tool_title=task_data["tool_title"],
                field=field,
                user=task_data["user"],
                defaults={"completed_date": task_data["completed_date"]},
            )
        except IntegrityError:
            logger.info(
                f"CompletedTask for tool {task_data['tool_name']} and field {task_data['field']} already exists."
            )
        except DoesNotExist:
            logger.info(
                f"Tool or Field does not exist for CompletedTask with tool {task_data['tool_name']} and field {task_data['field']}."
            )


async def seed():
    """Run the seeding process to insert fields, tools, and completed tasks."""
    await init()
    await insert_fields()
    await Tortoise.close_connections()

    await insert_tools()
    await Tortoise.close_connections()

    await insert_completed_tasks()
    await Tortoise.close_connections()


def main():
    run_async(seed())


if __name__ == "__main__":
    main()
