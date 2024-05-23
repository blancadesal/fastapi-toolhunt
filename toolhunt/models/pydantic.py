from pydantic import BaseModel


class ToolSchema(BaseModel):
    name: str
