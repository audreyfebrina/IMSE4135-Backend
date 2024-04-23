from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from datetime import datetime

from utils.hk_time_now import hk_time_now

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class BoxModel(BaseModel):
    """
    Container for a single box record.
    """

    # The primary key for the BoxModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    last_date_accessed: Optional[datetime] = None    
    shelf_id: PyObjectId = Field(...)
    last_updated: datetime = Field(default_factory=hk_time_now)
    last_updated_by: PyObjectId = Field(...)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "example": {
                "last_date_accessed": "2023-04-23T11:00:00Z",
                "shelf_id": "507f1f77bcf86cd799439014",
                "last_updated": "2023-04-23T12:00:00Z",
                "last_updated_by": "000000006175647265793032",
            }
        },
    }


class UpdateBoxModel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    last_date_accessed: Optional[datetime] = None
    shelf_id: Optional[PyObjectId] = None
    last_updated: Optional[datetime] = None
    last_updated_by: Optional[PyObjectId] = None

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "last_date_accessed": "2023-04-23T11:00:00Z",
                "shelf_id": "507f1f77bcf86cd799439014",
                "last_updated": "2023-04-23T12:00:00Z",
                "last_updated_by": "000000006175647265793032",
            }
        },
    }


class BoxCollection(BaseModel):
    """
    A container holding a list of `BoxModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    boxes: list[BoxModel]
