from datetime import timedelta, datetime, timezone
import jwt
import bcrypt
from typing import Dict

from src.db.config import settings
from src.models.user import User

PRIVATE_KEY = settings.auth_jwt.private_key_path.read_text()
PUBLIC_KEY = settings.auth_jwt.public_key_path.read_text()
ALGORITHM = settings.auth_jwt.algorithm

def encode_jwt(
    payload: Dict,
    private_key: str = PRIVATE_KEY,
    algorithm: str = ALGORITHM
) -> str:
    return jwt.encode(payload, private_key, algorithm=algorithm)

def decode_jwt(
    token: str | bytes,
    public_key: str = PUBLIC_KEY,
    algorithm: str = ALGORITHM
) -> Dict:
    return jwt.decode(token, public_key, algorithms=[algorithm])

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def create_access_token(user: User) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.auth_jwt.access_token_expire_minutes)
    payload = {
        "sub": str(user.id),
        "exp": expire,
        "type": "access",
        "roles": [role.name for role in user.roles]
    }
    return encode_jwt(payload)

def create_refresh_token(user: User) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.auth_jwt.refresh_token_expire_minutes)
    payload = {
        "sub": str(user.id),
        "exp": expire,
        "type": "refresh"
    }
    return encode_jwt(payload)
