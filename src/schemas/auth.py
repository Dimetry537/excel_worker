from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class RoleRead(RoleBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role_names: List[str] = []

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role_names: Optional[List[str]] = None

class UserRead(UserBase):
    id: int
    is_active: bool
    roles: List[RoleRead] = []

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
