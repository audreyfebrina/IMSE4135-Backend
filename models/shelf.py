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


class ShelfModel(BaseModel):
    """
    Container for a single shelf record.
    """

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    capacity: int = Field(..., gt=0)
    shelf_name: str = Field(..., min_length=1)
    last_updated: datetime = Field(default_factory=hk_time_now)
    last_updated_by: PyObjectId = Field(...)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "example": {
                "capacity": 20,
                "shelf_name": "Shelf A",
                "last_updated": "2023-04-23T12:00:00Z",
                "last_updated_by": "000000006175647265793032",
            }
        },
    }


class UpdateShelfModel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    capacity: Optional[int] = None
    shelf_name: Optional[str] = None
    last_updated: Optional[datetime] = None
    last_updated_by: Optional[PyObjectId] = None

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "capacity": 20,
                "shelf_name": "Shelf A",
                "last_updated": "2023-04-23T12:00:00Z",
                "last_updated_by": "000000006175647265793032",
            }
        },
    }


class ShelfCollection(BaseModel):
    """
    A container holding a list of `ShelfModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    shelves: list[ShelfModel]
