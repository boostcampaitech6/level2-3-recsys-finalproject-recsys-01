from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated


PyObjectId = Annotated[str, BeforeValidator(str)]