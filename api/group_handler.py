from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.depends import validate_auth_admin, get_department_service, get_specialty_service, get_group_service
from dto.department_dto import CreateDepartmentDTO
from dto.group_dto import CreateGroupDTO
from dto.message_dto import CreateMessageDTO
from dto.notification_dto import CreateNotificationDTO
from dto.specialty_dto import CreateSpecialtyDTO
from services.department_service import DepartmentService
from services.group_service import GroupService
from services.specialty_service import SpecialtyService

router = APIRouter()


@router.post("", response_model=dict, status_code=HTTPStatus.CREATED)
async def create_group(
        dto: CreateGroupDTO,
        group_service: GroupService = Depends(get_group_service),
        user=Depends(validate_auth_admin)
):
    try:
        await group_service.create(dto)
        return {"message": "Group created"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/{shortname}/message", response_model=dict, status_code=HTTPStatus.OK)
async def send_message(
        shortname: str,
        dto: CreateMessageDTO,
        group_service: GroupService = Depends(get_group_service),
        #user=Depends(validate_auth_admin)
):
    try:
        await group_service.send_notification(shortname, dto)
        return {"message": "Notification sent"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/{shortname}/notification", response_model=dict, status_code=HTTPStatus.OK)
async def send_notification(
        shortname: str,
        dto: CreateNotificationDTO,
        group_service: GroupService = Depends(get_group_service),
        # user=Depends(validate_auth_admin)
):
    try:
        await group_service.create_advanced_notification(shortname, dto)
        return {"message": "Notification created"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{group_id}", response_model=dict, status_code=HTTPStatus.CREATED)
async def delete_group(
        group_id: int,
        group_service: GroupService = Depends(get_group_service),
        user=Depends(validate_auth_admin)
):
    try:
        await group_service.delete(group_id)
        return {"message": "Group deleted"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{shortname}", response_model=None, status_code=HTTPStatus.OK)
async def get_group_by_shortname(
        shortname: str,
        group_service: GroupService = Depends(get_group_service),
        user=Depends(validate_auth_admin)
):
    try:
        return await group_service.get_by_shortname(shortname)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("", response_model=None, status_code=HTTPStatus.OK)
async def get_groups(
        group_service: GroupService = Depends(get_group_service),
        user=Depends(validate_auth_admin)
):
    try:
        return await group_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
