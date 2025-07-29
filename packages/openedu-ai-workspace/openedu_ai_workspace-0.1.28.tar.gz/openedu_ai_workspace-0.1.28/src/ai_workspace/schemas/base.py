from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from pydantic import ConfigDict as Config
from datetime import datetime


class BaseSchema(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id", default=None)

    model_config = Config(
        arbitrary_types_allowed=True,
        json_encoders={
            ObjectId: str,
        },
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
