"""
This script updates the database with tool and task information from the Toolhub API.
It performs the following steps:
1. Extracts raw tool data from the Toolhub API.
2. Cleans and transforms the raw data.
3. Upserts tool records and removes stale tools.
4. Inserts or updates task records and removes stale tasks.
"""

import datetime
from dataclasses import dataclass

from tortoise import run_async

from toolhunt.models.tortoise import Tool, Task
from toolhunt.api.utils import logger, ToolhubClient
from toolhunt.config import get_settings

settings = get_settings()
toolhub_client = ToolhubClient(settings.toolhub_api_endpoint)

# Transform

# Parameters
ANNOTATIONS = {
    "audiences",
    "content_types",
    "tasks",
    "subject_domains",
    "wikidata_qid",
    "icon",
    "tool_type",
    "repository",
    "api_url",
    "translate_url",
    "bugtracker_url",
}


# Functions
@dataclass
class ToolhuntTool:
    name: str
    title: str
    description: str
    url: str
    missing_annotations: set[str]
    deprecated: bool

    @property
    def is_completed(self):
        return len(self.missing_annotations) == 0


def is_deprecated(tool):
    return tool["deprecated"] or tool["annotations"]["deprecated"]


def get_missing_annotations(tool_info, filter_by=ANNOTATIONS):
    missing = set()

    for k, v in tool_info["annotations"].items():
        value = v or tool_info.get(k, v)
        if value in (None, [], "") and k in filter_by:
            missing.add(k)

    return missing


def clean_tool_data(tool_data):
    tools = []
    for tool in tool_data:
        t = ToolhuntTool(
            name=tool["name"],
            title=tool["title"],
            description=tool["description"],
            url=tool["url"],
            missing_annotations=get_missing_annotations(tool),
            deprecated=is_deprecated(tool),
        )
        if not t.deprecated and not t.is_completed:
            tools.append(t)
    return tools


# Load


async def upsert_tool(tool, timestamp):
    """Inserts a tool in the Tool table if it doesn't exist, and updates it if it does."""
    await Tool.update_or_create(
        defaults={
            "title": tool.title,
            "description": tool.description,
            "url": tool.url,
            "last_updated": timestamp,
        },
        name=tool.name,
    )


async def remove_stale_tools(timestamp):
    """Removes expired tools from the Tool table."""
    await Tool.filter(last_updated__ne=timestamp).delete()


async def update_tool_table(tools, timestamp):
    """Upserts tool records and removes stale tools"""
    for tool in tools:
        await upsert_tool(tool, timestamp)
    await remove_stale_tools(timestamp)


async def insert_or_update_task(tool_name, field, timestamp):
    """Inserts a task in the Task table if it doesn't exist or updates a timestamp."""
    task, created = await Task.update_or_create(
        defaults={"last_updated": timestamp},
        tool_name=tool_name,
        field_name=field,
    )


async def remove_stale_tasks(timestamp):
    """Removes expired tasks from the Task table."""
    await Task.filter(last_updated__ne=timestamp).delete()


async def update_task_table(tools, timestamp):
    """Inserts task records"""
    for tool in tools:
        for field in tool.missing_annotations:
            await insert_or_update_task(tool.name, field, timestamp)
    await remove_stale_tasks(timestamp)


# Pipeline
# This will populate the db if empty, or update all tool and task records if not.
async def run_pipeline():
    # Extract
    try:
        logger.info("Starting database update...")
        tools_raw_data = toolhub_client.get_all()
        logger.info("Raw data received.  Cleaning...")
        # Transform
        tools_clean_data = clean_tool_data(tools_raw_data)
        logger.info("Raw data cleaned.  Updating tools..")
        # Load
        timestamp = datetime.datetime.now(datetime.timezone.utc)
        await update_tool_table(tools_clean_data, timestamp)
        logger.info("Tools updated.  Updating tasks...")
        await update_task_table(tools_clean_data, timestamp)
        logger.info("Tasks updated.  Database update completed.")
    except Exception as err:
        logger.error(f"{err.args}")


if __name__ == "__main__":
    run_async(run_pipeline())
