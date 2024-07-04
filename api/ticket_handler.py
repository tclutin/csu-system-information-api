from http import HTTPStatus
from typing import List, Dict, Optional

from fastapi import HTTPException, Depends, APIRouter, UploadFile, File
from fastapi.params import Form
from starlette import status

from api.depends import get_auth_service, validate_auth_user, get_user_service, validate_auth_admin, get_ticket_service
from dto.message_dto import CreateMessageDTO
from dto.ticket_dto import CreateTicketDTO
from dto.user_dto import RegisterUserDTO
from infrastructure.models import User
from services import ticket_service
from services.auth_service import AuthService
from services.ticket_service import TicketService
from services.user_service import UserService

router = APIRouter()


@router.post("", response_model=dict, status_code=HTTPStatus.CREATED)
async def create_ticket(
        type_ticket: str = Form(),
        tgchat_id: int = Form(),
        fullname: Optional[str] = Form(None),
        wish_group: Optional[str] = Form(None),
        message: Optional[str] = Form(None),
        photo: UploadFile = File(None),
        ticket_service: TicketService = Depends(get_ticket_service),
        #user=Depends(validate_auth_admin)
):
    try:
        dto = await CreateTicketDTO.from_form(
            type_ticket=type_ticket,
            tgchat_id=tgchat_id,
            fullname=fullname,
            wish_group=wish_group,
            message=message,
            photo=photo,
        )
        print(dto)
        await ticket_service.create(dto)
        return {"message": "Ticket created"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/{ticket_id}/cancel", response_model=dict, status_code=HTTPStatus.OK)
async def cancel_ticket(
        ticket_id: int,
        dto: CreateMessageDTO,
        ticket_service: TicketService = Depends(get_ticket_service),
        #user=Depends(validate_auth_admin)
):
    try:
        await ticket_service.cancel(ticket_id, dto)
        return {"message": "Ticket cancelled"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/{ticket_id}/accept", response_model=dict, status_code=HTTPStatus.OK)
async def accept_ticket(
        ticket_id: int,
        dto: CreateMessageDTO,
        ticket_service: TicketService = Depends(get_ticket_service),
        #user=Depends(validate_auth_admin)
):
    try:
        await ticket_service.accept(ticket_id, dto)
        return {"message": "Ticket accepted"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{tgchat_id}/active", response_model=None, status_code=HTTPStatus.OK)
async def get_active_ticket(
        tgchat_id: int,
        ticket_service: TicketService = Depends(get_ticket_service),
        #user=Depends(validate_auth_admin)
):
    try:
        return await ticket_service.get_active_by_tgchat_id(tgchat_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/open", response_model=None, status_code=HTTPStatus.OK)
async def get_all_open_tickets(
        ticket_service: TicketService = Depends(get_ticket_service),
        #user=Depends(validate_auth_admin)
):
    try:
        return await ticket_service.get_all_open()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
