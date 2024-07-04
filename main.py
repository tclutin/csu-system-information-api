from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.auth_handler import router as auth_router
from api.user_handler import router as user_router
from api.department_handler import router as department_router
from api.specialty_handler import router as specialty_router
from api.group_handler import router as group_router
from api.faq_handler import router as faq_router
from api.student_handler import router as student_router
from api.upload_handler import router as upload_router
from api.ticket_handler import router as ticket_router

from config.config import settings
from infrastructure.models import Base

from infrastructure.postgres import postgres_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with postgres_client.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await postgres_client.dispose()


main_app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем доступ со всех доменов
    allow_credentials=True,  # Разрешаем отправку куки и заголовков аутентификации
    allow_methods=["*"],  # Разрешаем все HTTP-методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

main_app.include_router(auth_router, prefix="/auth", tags=["auth"])
main_app.include_router(user_router, prefix="/users", tags=["user"])
main_app.include_router(faq_router, prefix="/faqs", tags=["faq"])
main_app.include_router(group_router, prefix="/groups", tags=["group"])
main_app.include_router(student_router, prefix="/students", tags=["student"])
main_app.include_router(department_router, prefix="/departments", tags=["department"])
main_app.include_router(specialty_router, prefix="/specialties", tags=["specialty"])

main_app.include_router(ticket_router, prefix="/tickets", tags=["ticket"])
main_app.include_router(upload_router, prefix="/uploads", tags=["uploads"])

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.http_host,
        port=settings.http_port,
        reload=True
    )
