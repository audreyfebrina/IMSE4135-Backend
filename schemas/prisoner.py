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


class PrisonerModel(BaseModel):
    """
    Container for a single prisoner record.
    """

    # The primary key for the PrisonerModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    id_number: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    gender: str = Field(...)
    last_updated: datetime = Field(default_factory=hk_time_now)
    last_updated_by: PyObjectId = Field(...)
    officer_id: PyObjectId = Field(...)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "example": {
                "id_number": "12345678",
                "first_name": "John",
                "last_name": "Doe",
                "gender": "Male",
                "last_updated": "2023-04-23T12:00:00Z",
                "last_updated_by": "000000006175647265793032",
                "officer_id": "000000006175647265793032",
            }
        },
    }


class UpdatePrisonerModel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    id_number: Optional[str] = None
    last_updated: Optional[datetime] = None
    last_updated_by: Optional[PyObjectId] = None
    officer_id: Optional[PyObjectId] = None

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "gender": "Male",
                "id_number": "12345678",
                "last_updated": "2023-04-23T12:00:00Z",
                "last_updated_by": "000000006175647265793032",
                "officer_id": "000000006175647265793032",
            }
        },
    }


class PrisonerCollection(BaseModel):
    """
    A container holding a list of `PrisonerModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    prisoners: list[PrisonerModel]
