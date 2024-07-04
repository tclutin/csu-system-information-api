from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.depends import validate_auth_admin, get_department_service, get_specialty_service, get_group_service, \
    get_faq_service, get_faqfinder_service
from dto.department_dto import CreateDepartmentDTO
from dto.faq_dto import CreateFAQDTO, CreateFAQListDTO, SearchFAQDTO
from dto.group_dto import CreateGroupDTO
from dto.specialty_dto import CreateSpecialtyDTO
from infrastructure.faqfinder import FAQFinderService
from services.department_service import DepartmentService
from services.faq_service import FAQService
from services.group_service import GroupService
from services.specialty_repository import SpecialtyService

router = APIRouter()


@router.post("", response_model=dict, status_code=HTTPStatus.CREATED)
async def create_faq(
        dto: CreateFAQListDTO,
        faq_service: FAQService = Depends(get_faq_service),
        user=Depends(validate_auth_admin)
):
    try:
        await faq_service.create(dto)
        return {"message": "Faq created"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{faq_id}", response_model=dict, status_code=HTTPStatus.CREATED)
async def delete_faq(
        faq_id: int,
        faq_service: FAQService = Depends(get_faq_service),
        user=Depends(validate_auth_admin)
):
    try:
        await faq_service.delete(faq_id)
        return {"message": "Faq deleted"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/search", response_model=None, status_code=HTTPStatus.OK)
async def search_faqs(
        dto: SearchFAQDTO,
        faqfinder_service: FAQFinderService = Depends(get_faqfinder_service),
        #user=Depends(validate_auth_admin)
):
    try:
        return await faqfinder_service.search_faqs(dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("", response_model=None, status_code=HTTPStatus.OK)
async def get_faqs(
        faq_service: FAQService = Depends(get_faq_service),
        user=Depends(validate_auth_admin)
):
    try:
        return await faq_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
