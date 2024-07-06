from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.depends import validate_auth_admin, get_department_service, get_specialty_service, get_notification_service
from dto.department_dto import CreateDepartmentDTO
from dto.specialty_dto import CreateSpecialtyDTO
from services.department_service import DepartmentService
from services.notification_service import NotificationService
from services.specialty_service import SpecialtyService

router = APIRouter()


@router.get("/{tgchat_id}", response_model=None, status_code=HTTPStatus.OK)
async def get_notifications_by_tgchat_id(
        tgchat_id: int,
        notification_service: NotificationService = Depends(get_notification_service),
        #user=Depends(validate_auth_admin)
):
    try:
        return await notification_service.get_all_by_tgchat_id(tgchat_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("", response_model=None, status_code=HTTPStatus.OK)
async def get_all(
        notification_service: NotificationService = Depends(get_notification_service),
        #user=Depends(validate_auth_admin)
):
    try:
        return await notification_service.get_by_repeat()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
