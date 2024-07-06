import io
from http import HTTPStatus

from fastapi import HTTPException, Depends, APIRouter, UploadFile
from fastapi.params import File, Form
from starlette import status
from starlette.responses import StreamingResponse

from api.depends import validate_auth_admin, get_student_service
from dto.message_dto import CreateMessageDTO
from services.student_service import StudentService

router = APIRouter()


@router.get("/{tgchat_id}", response_model=None, status_code=HTTPStatus.OK)
async def get_student_by_tgchat_id(
        tgchat_id: int,
        student_service: StudentService = Depends(get_student_service),
        #user=Depends(validate_auth_admin)
):
    try:
        return await student_service.get_by_tgchat_id(tgchat_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{tgchat_id}", response_model=None, status_code=HTTPStatus.OK)
async def delete_student_by_tgchat_id(
        tgchat_id: int,
        student_service: StudentService = Depends(get_student_service),
        #user=Depends(validate_auth_admin)
):
    try:
        await student_service.delete(tgchat_id)
        return {"message": "Student deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/{student_id}/message", response_model=dict, status_code=HTTPStatus.OK)
async def send_message(
        student_id: int,
        dto: CreateMessageDTO,
        student_service: StudentService = Depends(get_student_service),
        #user=Depends(validate_auth_admin)
):
    try:
        await student_service.send_notification(student_id, dto)
        return {"message": "Notification sent"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("", response_model=None, status_code=HTTPStatus.OK)
async def get_students(
        student_service: StudentService = Depends(get_student_service),
        #user=Depends(validate_auth_admin)
):
    try:
        return await student_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
