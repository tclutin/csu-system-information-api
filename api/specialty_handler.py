from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.depends import validate_auth_admin, get_department_service, get_specialty_service
from dto.department_dto import CreateDepartmentDTO
from dto.specialty_dto import CreateSpecialtyDTO
from services.department_service import DepartmentService
from services.specialty_repository import SpecialtyService

router = APIRouter()


@router.post("", response_model=dict, status_code=HTTPStatus.CREATED)
async def create_specialty(
        dto: CreateSpecialtyDTO,
        specialty_service: SpecialtyService = Depends(get_specialty_service),
        user=Depends(validate_auth_admin)
):
    try:
        await specialty_service.create(dto)
        return {"message": "Specialty created"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("", response_model=None, status_code=HTTPStatus.OK)
async def get_specialties(
        specialty_service: SpecialtyService = Depends(get_specialty_service),
        user=Depends(validate_auth_admin)
):
    try:
        return await specialty_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{specialty_name}", response_model=dict, status_code=HTTPStatus.OK)
async def get_departments(
        specialty_name: str,
        specialty_service: SpecialtyService = Depends(get_specialty_service),
        user=Depends(validate_auth_admin)
):
    try:
        await specialty_service.delete(specialty_name)
        return {"message": "Specialty deleted"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
