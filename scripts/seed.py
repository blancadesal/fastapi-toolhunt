import sys
import os
import json
from tortoise import Tortoise, run_async
from tortoise.exceptions import IntegrityError, DoesNotExist

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toolhunt.models.tortoise import Tool, Field, CompletedTask
from toolhunt.db import TORTOISE_ORM
from update_db import run_pipeline


async def init():
    await Tortoise.init(config=TORTOISE_ORM)


async def seed():
    await init()

    # Load field data
    with open("tests/fixtures/field_data.json", "r") as f:
        fields_data = json.load(f)

    # Insert field data
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
            print(f"Field {field_data['name']} already exists.")

    await Tortoise.close_connections()

    # Load tool data and create tasks
    with open("tests/fixtures/tool_data.json", "r") as f:
        tool_data = json.load(f)

    await run_pipeline(test_data=tool_data)

    await init()  # Reinitialize connection for completed tasks

    # Load completed task data
    with open("tests/fixtures/completed_task_data.json", "r") as f:
        completed_task_data = json.load(f)

    # Insert completed task data
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
            print(
                f"CompletedTask for tool {task_data['tool_name']} and field {task_data['field']} already exists."
            )
        except DoesNotExist:
            print(
                f"Tool or Field does not exist for CompletedTask with tool {task_data['tool_name']} and field {task_data['field']}."
            )

    await Tortoise.close_connections()


def main():
    run_async(seed())


if __name__ == "__main__":
    main()
