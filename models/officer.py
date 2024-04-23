from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class OfficerModel(BaseModel):
    """
    Container for a single officer record.
    """

    # The custom ID for the officer

    # The ObjectId version of the custom ID
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    officer_id: str = Field(...)
    password: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    officer_rank: str = Field(...)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "example": {
                "officer_id": "12345",
                "password": "testing123",
                "first_name": "John",
                "last_name": "Doe",
                "officer_rank": "Lieutenant",
            }
        },
    }


class UpdateOfficerModel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    officer_rank: Optional[str] = None

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "officer_rank": "Lieutenant",
            }
        },
    }


class OfficerCollection(BaseModel):
    """
    A container holding a list of `OfficerModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    officers: list[OfficerModel]


class LoginModel(BaseModel):
    officer_id: str
    password: str

    model_config = {
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "example": {
                "officer_id": "12345",
                "password": "testing123",
            }
        },
    }


class SignupModel(LoginModel):
    first_name: str
    last_name: str
    officer_rank: str

    model_config = {
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "example": {
                "officer_id": "12345",
                "password": "testing123",
                "first_name": "John",
                "last_name": "Doe",
                "officer_rank": "Lieutenant",
            }
        },
    }
