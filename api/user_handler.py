from http import HTTPStatus
from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.depends import get_auth_service, validate_auth_user, get_user_service, validate_auth_admin
from dto.user_dto import RegisterUserDTO
from infrastructure.models import User
from services.auth_service import AuthService
from services.user_service import UserService

router = APIRouter()


@router.post("", response_model=None, status_code=HTTPStatus.CREATED)
async def create_user(
        dto: RegisterUserDTO,
        user_service: UserService = Depends(get_user_service),
        user=Depends(validate_auth_admin)
):
    try:
        await user_service.create(dto)
        return {"message": "User created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{username}", response_model=None, status_code=HTTPStatus.OK)
async def delete_user(
        username: str,
        user_service: UserService = Depends(get_user_service),
        user=Depends(validate_auth_admin)
):
    try:
        await user_service.delete(username)
        return {"message": "User deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("", response_model=None, status_code=HTTPStatus.OK)
async def get_users(
        user_service: UserService = Depends(get_user_service),
        user=Depends(validate_auth_admin)
):
    try:
        return await user_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
