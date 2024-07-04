from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.depends import validate_auth_admin, get_department_service
from dto.department_dto import CreateDepartmentDTO
from services.department_service import DepartmentService

router = APIRouter()


@router.post("", response_model=dict, status_code=HTTPStatus.CREATED)
async def create_department(
        dto: CreateDepartmentDTO,
        department_service: DepartmentService = Depends(get_department_service),
        user=Depends(validate_auth_admin)
):

    try:
        await department_service.create(dto)
        return {"message": "Department created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("", response_model=None, status_code=HTTPStatus.OK)
async def get_departments(
        department_service: DepartmentService = Depends(get_department_service),
        user=Depends(validate_auth_admin)
):

    try:
        return await department_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{department_name}", response_model=dict, status_code=HTTPStatus.OK)
async def get_departments(
        department_name: str,
        department_service: DepartmentService = Depends(get_department_service),
        user=Depends(validate_auth_admin)
):

    try:
        await department_service.delete(department_name)
        return {"message": "Department deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
