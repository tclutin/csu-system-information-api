from typing import Optional

from pydantic import BaseModel
from datetime import datetime, time

from pydantic.v1 import root_validator, validator


class CreateNotificationDTO(BaseModel):
    message: str
    is_repeating: bool
    time: Optional[str] = None
    day_of_week: Optional[int] = None
    week_parity: Optional[str] = None
    date: Optional[datetime] = None
