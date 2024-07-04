import os
import uuid

import aiofiles
import aiofiles.os as aios


class UploadService:
    def __init__(self):
        self.path = "./uploads/"
        self.ensure_upload_dir_exists()

    # UploadService
    async def upload_file(self, image_data: bytes) -> str:
        file_name = f"{uuid.uuid4()}.jpg"
        file_path = os.path.join(self.path, file_name)
        try:
            await self.ensure_upload_dir_exists()
            async with aiofiles.open(file_path, "wb") as file:
                await file.write(image_data)
        except Exception as e:
            raise ValueError(f"Failed to save file '{file_name}': {str(e)}")

        return file_name.rsplit(".jpg", maxsplit=1)[0]

    async def get_file(self, file_name: str) -> bytes:
        file_path = os.path.join(self.path, file_name + ".jpg")

        exists = await aios.path.exists(file_path)
        if not exists:
            raise ValueError("File does not exist")

        try:
            await self.ensure_upload_dir_exists()
            async with aiofiles.open(file_path, "rb") as file:
                image_data = await file.read()
                return image_data
        except Exception as e:
            raise ValueError(f"Failed to read file '{file_name}': {str(e)}")

    async def ensure_upload_dir_exists(self):
        exists = await aios.path.exists(self.path)
        if not exists:
            await aios.makedirs(self.path)
