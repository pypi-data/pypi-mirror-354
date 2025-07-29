from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum
from datetime import datetime
from typing import Optional


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class UserEventType(str, Enum):
    CREATED = "user.created"
    UPDATED = "user.updated"
    DELETED = "user.deleted"


class UserBase(BaseModel):
    """Base user model with common fields."""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None
    role: UserRole = UserRole.USER
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema for updating user information."""

    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    """User model as stored in the database."""

    id: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserEvent(BaseModel):
    """Schema for user-related events."""

    event_type: UserEventType
    user_id: str
    user_data: dict
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict = {}
