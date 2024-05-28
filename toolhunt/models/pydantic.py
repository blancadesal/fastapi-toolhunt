import json
from typing import Dict, Optional

from pydantic import BaseModel, field_validator
from pydantic import Field as PydanticField


class FieldSchema(BaseModel):
    name: str
    description: str
    input_options: Optional[Dict] = None
    pattern: Optional[str] = None

    @field_validator("input_options", pre=True, always=True)
    def serialize_input_options(cls, v):
        """Convert input_options from bytes obj to dict."""
        if v and not isinstance(v, dict):
            try:
                input_options = v.decode().replace("'", '"')
                return json.loads(input_options)
            except Exception as e:
                print(f"An error occurred: {e}")
        return v

    class Config:
        orm_mode = True


class ToolSchema(BaseModel):
    name: str
    title: str
    description: str
    url: str

    class Config:
        orm_mode = True


class TaskSchema(BaseModel):
    id: Optional[int] = PydanticField(
        None, alias="id", description="The ID of the task"
    )
    tool_name: str
    tool: Optional[ToolSchema] = None
    field_name: str
    field: Optional[FieldSchema] = None

    class Config:
        orm_mode = True
