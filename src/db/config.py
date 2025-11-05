import os

from pydantic import BaseModel
from pathlib import Path
from pydantic_settings import BaseSettings

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

ORACLE_USER = os.environ.get("ORACLE_USER")
ORACLE_PASSWORD = os.environ.get("ORACLE_PASSWORD")
ORACLE_HOST = os.environ.get("ORACLE_HOST")
ORACLE_PORT = os.environ.get("ORACLE_PORT")
ORACLE_SERVICE = os.environ.get("ORACLE_SERVICE")
ORACLE_CLIENT = os.environ.get("ORACLE_CLIENT")

DB_HOST_TEST = os.environ.get("DB_HOST_TEST")
DB_PORT_TEST = os.environ.get("DB_PORT_TEST")
DB_NAME_TEST = os.environ.get("DB_NAME_TEST")
DB_USER_TEST = os.environ.get("DB_USER_TEST")
DB_PASS_TEST = os.environ.get("DB_PASS_TEST")

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / ".certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / ".certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expires: int = 15  # minutes

class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()

settings = Settings()
