from http import HTTPStatus
from typing import Optional, Dict

from fastapi import APIRouter, Depends, HTTPException, Form

from starlette import status

from api.depends import http_bearer, get_auth_service, validate_auth_user, validate_auth_admin
from dto.user_dto import LoginUserDTO, RegisterUserDTO

from services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=dict, status_code=HTTPStatus.CREATED)
async def register_user(
        dto: RegisterUserDTO,
        auth_service: AuthService = Depends(get_auth_service),
        user=Depends(validate_auth_admin)
):

    try:
        access_token = await auth_service.register(dto)
        return {'access_token': access_token}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/login", response_model=dict, status_code=HTTPStatus.OK)
async def login_user(
        dto: LoginUserDTO,
        auth_service: AuthService = Depends(get_auth_service)
):

    try:
        access_token = await auth_service.login(dto)
        return {'access_token': access_token}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/me", response_model=None, status_code=HTTPStatus.OK)
async def me(
        auth_service: AuthService = Depends(get_auth_service),
        payloads=Depends(validate_auth_user)
):

    try:
        return await auth_service.me(payloads["sub"])
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

