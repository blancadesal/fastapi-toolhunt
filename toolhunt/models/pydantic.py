import json
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, field_validator
from pydantic import Field as PydanticField


class FieldSchema(BaseModel):
    name: str
    description: str
    input_options: Optional[Dict] = None
    pattern: Optional[str] = None

    @field_validator("input_options", mode="before")
    def serialize_input_options(cls, v):
        """Convert input_options from JSON string to dict or return None."""
        if v in (None, "null"):
            return None
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError as e:
                print(f"An error occurred: {e}")
        return v

    class Config:
        from_attributes = True


class ToolSchema(BaseModel):
    name: str
    title: str
    description: str
    url: str

    class Config:
        from_attributes = True


class TaskSchema(BaseModel):
    id: Optional[int] = PydanticField(
        None, alias="id", description="The ID of the task"
    )
    tool: Optional[ToolSchema] = None
    field: Optional[FieldSchema] = None

    class Config:
        from_attributes = True


class ToolNamesResponse(BaseModel):
    allTitles: List[str]
    titles: Dict[str, str]


class CompletedTaskSchema(BaseModel):
    completed_date: datetime
    field: str
    tool_name: str
    tool_title: str
    user: str

    class Config:
        from_attributes = True
