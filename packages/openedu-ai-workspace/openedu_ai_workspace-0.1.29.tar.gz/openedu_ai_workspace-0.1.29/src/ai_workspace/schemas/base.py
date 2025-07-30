from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from pydantic import ConfigDict as Config
from datetime import datetime
from ai_workspace.packages.shared import IDGenerator


class BaseSchema(BaseModel):
    id: Optional[str] = Field(alias="_id", default_factory=IDGenerator.generate)

    model_config = Config(
        arbitrary_types_allowed=True, populate_by_name=True, from_attributes=True
    )
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation time of the workspace"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last update time of the workspace"
    )
    deleted_at: Optional[datetime] = Field(
        default=None, description="Deletion time of the workspace"
    )
