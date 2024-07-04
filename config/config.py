from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    http_host: str
    http_port: int

    database_url: str

    jwt_secret_key: str
    jwt_access_token_expire_minutes: int

    faqfinder_service_url: str

    class Config:
        env_file = ".env"


settings = Settings()
