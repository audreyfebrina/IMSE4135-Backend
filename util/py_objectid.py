from pydantic import BeforeValidator
from typing import Annotated

# Python type for a bson.ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]
