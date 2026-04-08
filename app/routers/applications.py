from typing import Literal

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models import ApplicationStatus, User
from app.repositories.application_repository import ApplicationRepository
from app.schemas import (
    AnalyticsSummary,
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate,
    PaginatedApplicationResponse,
)
from app.services.application_service import ApplicationService

router = APIRouter(prefix="/applications", tags=["Applications"])


def get_application_service(db: Session = Depends(get_db)) -> ApplicationService:
    repository = ApplicationRepository(db)
    return ApplicationService(repository)


@router.post("", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(
    application: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service),
):
    return service.create_application(application, current_user)


@router.get("", response_model=PaginatedApplicationResponse)
def get_applications(
    status_filter: ApplicationStatus | None = Query(default=None, alias="status"),
    search: str | None = Query(default=None, min_length=1, max_length=100),
    sort_by: Literal["created_at", "updated_at", "company_name", "position", "status"] = Query(default="created_at"),
    sort_order: Literal["asc", "desc"] = Query(default="desc"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service),
):
    return service.get_applications(
        current_user=current_user,
        status_filter=status_filter,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        skip=skip,
        limit=limit,
    )


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service),
):
    return service.get_application(application_id, current_user)


@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: int,
    application_data: ApplicationUpdate,
    current_user: User = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service),
):
    return service.update_application(application_id, application_data, current_user)


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service),
):
    service.delete_application(application_id, current_user)
    return None


@router.get("/analytics/summary", response_model=AnalyticsSummary)
def get_analytics(
    current_user: User = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service),
):
    return service.get_analytics(current_user)