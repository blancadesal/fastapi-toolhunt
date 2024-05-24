import sys
import os
import json
from tortoise import Tortoise, run_async
from tortoise.exceptions import IntegrityError


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toolhunt.models.tortoise import Tool, Field, CompletedTask
from toolhunt.db import TORTOISE_ORM


async def init():
    await Tortoise.init(config=TORTOISE_ORM)


async def seed():
    await init()

    # Load tool data from data.json
    with open("tests/fixtures/data.json", "r") as f:
        data = json.load(f)

    # Insert tool data
    for tool_data in data[0]["tool_data"]:
        try:
            await Tool.get_or_create(
                name=tool_data["name"],
                defaults={
                    "title": tool_data["title"],
                    "description": tool_data["description"],
                    "url": tool_data["url"],
                    "last_updated": tool_data["modified_date"],
                },
            )
        except IntegrityError:
            print(f"Tool {tool_data['name']} already exists.")

    # Insert completed task data
    for task_data in data[1]["task_data"]:
        try:
            await CompletedTask.get_or_create(
                tool_name=task_data["tool_name"],
                tool_title=task_data["tool_title"],
                field=task_data["field"],
                user=task_data["user"],
                defaults={"completed_date": task_data["completed_date"]},
            )
        except IntegrityError:
            print(
                f"CompletedTask for tool {task_data['tool_name']} and field {task_data['field']} already exists."
            )

    # Load field data from fields.json
    with open("tests/fixtures/fields.json", "r") as f:
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


def main():
    run_async(seed())


if __name__ == "__main__":
    main()
