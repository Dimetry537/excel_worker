import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent.parent

class AuthJWT(BaseSettings):
    private_key_path: Path = BASE_DIR / ".certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / ".certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 1440

class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_pass: str

    oracle_user: str
    oracle_password: str
    oracle_host: str
    oracle_port: int
    oracle_service: str
    oracle_client: str

    db_host_test: str
    db_port_test: int
    db_name_test: str
    db_user_test: str
    db_pass_test: str

    cors_host: str
    cors_port: str
    celery_broker_url: str
    celery_result_backend: str

    admin_username: str
    admin_password: str

    admin_flower_username: str
    admin_flower_password: str

    admin_pg_password: str

    auth_jwt: AuthJWT = AuthJWT()

    model_config = SettingsConfigDict(
        env_file=(
            BASE_DIR / ".env.dev" if (BASE_DIR / ".env.dev").exists()
            else BASE_DIR / ".env.prod" if (BASE_DIR / ".env.prod").exists()
            else BASE_DIR / ".env"
        ),
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()
