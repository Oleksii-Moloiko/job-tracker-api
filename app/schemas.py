from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models import ApplicationStatus


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class ApplicationCreate(BaseModel):
    company_name: str = Field(min_length=1, max_length=100)
    position: str = Field(min_length=1, max_length=100)
    status: ApplicationStatus = ApplicationStatus.SAVED
    notes: str | None = Field(default=None, max_length=1000)
    applied_at: datetime | None = None


class ApplicationUpdate(BaseModel):
    company_name: str | None = Field(default=None, min_length=1, max_length=100)
    position: str | None = Field(default=None, min_length=1, max_length=100)
    status: ApplicationStatus | None = None
    notes: str | None = Field(default=None, max_length=1000)
    applied_at: datetime | None = None


class ApplicationResponse(BaseModel):
    id: int
    company_name: str
    position: str
    status: ApplicationStatus
    notes: str | None
    applied_at: datetime | None
    created_at: datetime
    updated_at: datetime
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class PaginatedApplicationResponse(BaseModel):
    items: list[ApplicationResponse]
    total: int
    skip: int
    limit: int