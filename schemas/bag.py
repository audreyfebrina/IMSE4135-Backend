from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from datetime import datetime

from util.hk_time_now import hk_time_now

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class BagModel(BaseModel):
    """
    Container for a single bag record.
    """

    # The primary key for the BagModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    rfid_epc: str = Field(...)
    box_id: PyObjectId = Field(...)
    date_registered: datetime = Field(default_factory=hk_time_now)
    items: List[str] = Field(default=[])
    officer_id: str = Field(...)
    prisoner_id: PyObjectId = Field(...)
    last_updated: datetime = Field(default_factory=hk_time_now)
    last_updated_by: str = Field(...)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "example": {
                "rfid_epc": "12345678",
                "box_id": "6627c8ee88dd306b763be9aa",
                "date_registered": "2023-04-23T11:00:00Z",
                "items": ["2 pens", "1 notebook"],
                "officer_id": "johndoe",
                "prisoner_id": "000000004631323334353637",
                "last_updated": "2023-04-23T12:00:00Z",
                "last_updated_by": "johndoe",
            }
        },
    }


class UpdateBagModel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    rfid_epc: Optional[str] = None
    box_id: Optional[PyObjectId] = None
    date_registered: Optional[datetime] = None
    items: Optional[List[str]] = None
    officer_id: Optional[str] = None
    prisoner_id: Optional[PyObjectId] = None
    last_updated: Optional[datetime] = None
    last_updated_by: Optional[str] = None

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "rfid_epc": "12345678",
                "box_id": "6627c8ee88dd306b763be9aa",
                "date_registered": "2023-04-23T11:00:00Z",
                "items": ["2 pens", "1 notebook"],
                "officer_id": "johndoe",
                "prisoner_id": "000000004631323334353637",
                "last_updated": "2023-04-23T12:00:00Z",
                "last_updated_by": "johndoe",
            }
        },
    }


class BagCollection(BaseModel):
    """
    A container holding a list of `BagModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    bags: list[BagModel]
