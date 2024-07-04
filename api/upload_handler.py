import io
from http import HTTPStatus


from fastapi import HTTPException, Depends, APIRouter, UploadFile
from starlette import status
from starlette.responses import StreamingResponse

from api.depends import validate_auth_admin, get_student_service, get_upload_service

from services.upload_service import UploadService

router = APIRouter()



@router.get("/{file_name}", response_class=StreamingResponse, status_code=HTTPStatus.CREATED)
async def get_file(
        file_name: str,
        upload_service: UploadService = Depends(get_upload_service),
        #user=Depends(validate_auth_admin)
):

    try:
        photo_data = await upload_service.get_file(file_name)
        if photo_data is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

        return StreamingResponse(io.BytesIO(photo_data), media_type="image/jpeg")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

