from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel


class CreateMessageDTO(BaseModel):
    message: Annotated[str, MinLen(5), MaxLen(100)]

