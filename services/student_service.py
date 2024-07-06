import uuid
from typing import List, Optional

import aiofiles
import aiofiles.os as aios
import os

from dto.message_dto import CreateMessageDTO
from dto.student_dto import CreateStudentDTO
from infrastructure.models import Student
from repositories.student_repository import StudentRepository
from services.group_service import GroupService
from services.message_service import MessageService
from services.upload_service import UploadService


class StudentService:
    def __init__(self, student_repository: StudentRepository, group_service: GroupService, upload_service: UploadService, message_service: MessageService):
        self.student_repository = student_repository
        self.group_service = group_service
        self.upload_service = upload_service
        self.message_service = message_service

    # StudentService
    async def create(self, dto: CreateStudentDTO) -> Student:
        group = await self.group_service.get_by_id(dto.group_id)
        if group is None:
            raise ValueError('Group does not exist')

        student = await self.get_by_tgchat_id(dto.tgchat_id)
        if student is not None:
            raise ValueError('Student already exists with this tgchat_id')

        #file_name = await self.upload_service.upload_file(dto.student_card)

        student = Student(
            tgchat_id=dto.tgchat_id,
            group_id=dto.group_id,
            fullname=dto.fullname,
            student_card=dto.student_card,
        )

        await self.group_service.update_user_count(group.group_id)

        return await self.student_repository.create(student)

    async def delete(self, tgchat_id: int) -> None:
        student = await self.get_by_tgchat_id(tgchat_id)
        if student is None:
            raise ValueError('Student does not exist')

        await self.message_service.send(student.tgchat_id, "Вы были исключены из группы.")
        await self.student_repository.delete(student)

    async def get_all(self) -> List[Student]:
        return await self.student_repository.get_all()

    async def get_by_tgchat_id(self, tgchat_id: int) -> Optional[Student]:
        return await self.student_repository.get_by_tgchat_id(tgchat_id)

    async def get_by_id(self, student_id: int) -> Optional[Student]:
        return await self.student_repository.get_student_by_id(student_id)

    async def send_notification(self, student_id: int, message: CreateMessageDTO) -> None:
        student = await self.get_by_id(student_id)
        if student is None:
            raise ValueError('Student does not exist')

        await self.message_service.send(student.tgchat_id, message.message)



