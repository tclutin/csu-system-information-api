from io import BytesIO
from typing import Annotated, Optional

from PIL import Image
from annotated_types import MinLen, MaxLen
from fastapi import UploadFile
from pydantic import BaseModel, constr

class CreateTicketDTO(BaseModel):
    type_ticket: str
    tgchat_id: int
    fullname: Optional[constr(min_length=15, max_length=50)] = None
    wish_group: Optional[str] = None
    message: Optional[str] = None
    photo: Optional[bytes] = None

    @classmethod
    async def from_form(
            cls,
            type_ticket: str,
            tgchat_id: int,
            fullname: Optional[str],
            wish_group: Optional[str],
            message: Optional[str],
            photo: UploadFile
    ):
        image_data = None
        if photo:
            if not photo.content_type.startswith('image/'):
                raise ValueError("The uploaded file is not an image.")

            if photo.size > 5 * 1024 * 1024:
                raise ValueError("The uploaded file is too large.")

            try:
                image_data = await photo.read()
                image = Image.open(BytesIO(image_data))
                image.verify()
            except Exception:
                raise ValueError("The uploaded file is not a valid image.")

        return cls(
            type_ticket=type_ticket,
            tgchat_id=tgchat_id,
            fullname=fullname,
            wish_group=wish_group,
            message=message,
            photo=image_data
        )

