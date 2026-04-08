import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_password,
    verify_password,
)
from app.config import settings
from app.core.exceptions import AppException
from app.dependencies import get_current_user, get_db
from app.models import RefreshToken, User
from app.schemas import (
    RefreshTokenRequest,
    TokenResponse,
    UserCreate,
    UserResponse,
)


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()

    if existing_user:
        raise AppException(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="user_already_exists",
            message="User with this email or username already exists",
        )

    user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info("User registered: email=%s", user.email)


    return user


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.warning("Failed login attempt for email=%s", form_data.username)
        raise AppException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="invalid_credentials",
            message="Invalid email or password",
        )

    access_token = create_access_token({"sub": str(user.id), "email": user.email})
    refresh_token = create_refresh_token({"sub": str(user.id), "email": user.email})

    refresh_token_expires_at = datetime.utcnow() + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    db_refresh_token = RefreshToken(
        token=refresh_token,
        user_id=user.id,
        expires_at=refresh_token_expires_at,
        is_revoked=False,
    )
    db.add(db_refresh_token)
    db.commit()
    logger.info("User login success: user_id=%s", user.id)


    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    payload: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    decoded_payload = decode_refresh_token(payload.refresh_token)

    if not decoded_payload:
        raise AppException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="invalid_refresh_token",
            message="Invalid refresh token",
        )

    stored_token = db.query(RefreshToken).filter(
        RefreshToken.token == payload.refresh_token
    ).first()

    if not stored_token or stored_token.is_revoked:
        raise AppException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="refresh_token_revoked",
            message="Refresh token is revoked or not found",
        )

    if stored_token.expires_at < datetime.utcnow():
        raise AppException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="refresh_token_expired",
            message="Refresh token has expired",
        )

    user = db.query(User).filter(User.id == stored_token.user_id).first()
    if not user:
        raise AppException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="user_not_found",
            message="User not found",
        )

    stored_token.is_revoked = True

    new_access_token = create_access_token({"sub": str(user.id), "email": user.email})
    new_refresh_token = create_refresh_token({"sub": str(user.id), "email": user.email})

    new_refresh_token_expires_at = datetime.utcnow() + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    db_refresh_token = RefreshToken(
        token=new_refresh_token,
        user_id=user.id,
        expires_at=new_refresh_token_expires_at,
        is_revoked=False,
    )
    db.add(db_refresh_token)
    db.commit()
    logger.info("Refreshing tokens for user_id=%s", user.id)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    payload: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    stored_token = db.query(RefreshToken).filter(
        RefreshToken.token == payload.refresh_token
    ).first()

    if stored_token:
        stored_token.is_revoked = True
        db.commit()
        logger.info("User logout: user_id=%s", stored_token.user_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)