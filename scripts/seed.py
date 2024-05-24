import json

from tortoise import Tortoise, run_async
from toolhunt.models.tortoise import Tool, Field, Task, CompletedTask
from toolhunt.db import TORTOISE_ORM

async def init():
    await Tortoise.init(config=TORTOISE_ORM)

async def seed():
    await init()

    # Load tool data from data.json
    with open('tests/fixtures/data.json', 'r') as f:
        data = json.load(f)

    # Insert tool data
    for tool_data in data[0]['tool_data']:
        await Tool.create(
            name=tool_data['name'],
            title=tool_data['title'],
            description=tool_data['description'],
            url=tool_data['url'],
            last_updated=tool_data['modified_date']
        )

    # Insert completed task data
    for task_data in data[1]['task_data']:
        await CompletedTask.create(
            tool_name=task_data['tool_name'],
            tool_title=task_data['tool_title'],
            field=task_data['field'],
            user=task_data['user'],
            completed_date=task_data['completed_date']
        )

    # Load field data from fields.json
    with open('tests/fixtures/fields.json', 'r') as f:
        fields_data = json.load(f)

    # Insert field data
    for field_data in fields_data:
        await Field.create(
            name=field_data['name'],
            description=field_data['description'],
            input_options=json.dumps(field_data.get('input_options', None)),
            pattern=field_data.get('pattern', None)
        )

    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(seed())
