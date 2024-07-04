import io
from http import HTTPStatus

from fastapi import HTTPException, Depends, APIRouter, UploadFile
from fastapi.params import File, Form
from starlette import status
from starlette.responses import StreamingResponse

from api.depends import validate_auth_admin, get_student_service
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


@router.get("", response_model=None, status_code=HTTPStatus.OK)
async def get_students(
        student_service: StudentService = Depends(get_student_service),
        #user=Depends(validate_auth_admin)
):
    try:
        return await student_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

