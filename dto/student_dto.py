import base64
from io import BytesIO
from typing import Annotated

from PIL import Image
from annotated_types import MinLen, MaxLen
from fastapi import UploadFile
from pydantic import BaseModel


class CreateStudentDTO(BaseModel):
    fullname: Annotated[str, MinLen(5), MaxLen(50)]
    group_id: int
    tgchat_id: int
    student_card: str
