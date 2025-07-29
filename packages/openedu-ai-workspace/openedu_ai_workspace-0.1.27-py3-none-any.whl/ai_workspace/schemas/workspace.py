from typing import Optional
from pydantic import Field
from .base import BaseSchema


class WorkspaceSchema(BaseSchema):
    workspace_id: Optional[str] = Field(
        description="The id of the workspace", default=None
    )
    title: str = Field(description="The name of the workspace")
    user_id: str = Field(description="The id of the user")
    chat_sessions: list[str] = Field(
        description="The chat sessions of the workspace", default_factory=list
    )
    description: str = Field(description="The description of the workspace")
    instructions: str = Field(description="The instructions of the workspace")
