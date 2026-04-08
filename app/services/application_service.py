import logging

from fastapi import status

from app.core.exceptions import AppException
from app.models import ApplicationStatus, User
from app.repositories.application_repository import ApplicationRepository
from app.schemas import ApplicationCreate, ApplicationUpdate

logger = logging.getLogger(__name__)


class ApplicationService:
    def __init__(self, repository: ApplicationRepository):
        self.repository = repository

    def create_application(self, application_data: ApplicationCreate, current_user: User):
        logger.info("Creating application for user_id=%s", current_user.id)

        return self.repository.create(
            company_name=application_data.company_name,
            position=application_data.position,
            status=application_data.status,
            notes=application_data.notes,
            applied_at=application_data.applied_at,
            owner_id=current_user.id,
        )

    def get_applications(
        self,
        current_user: User,
        status_filter: ApplicationStatus | None = None,
        search: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        skip: int = 0,
        limit: int = 10,
    ):
        logger.info(
            "Fetching applications for user_id=%s with status=%s search=%s sort_by=%s sort_order=%s skip=%s limit=%s",
            current_user.id,
            status_filter,
            search,
            sort_by,
            sort_order,
            skip,
            limit,
        )

        allowed_sort_fields = {"created_at", "updated_at", "company_name", "position", "status"}
        allowed_sort_orders = {"asc", "desc"}

        if sort_by not in allowed_sort_fields:
            raise AppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                code="invalid_sort_by",
                message=f"Invalid sort_by value. Allowed values: {', '.join(sorted(allowed_sort_fields))}",
            )

        if sort_order not in allowed_sort_orders:
            raise AppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                code="invalid_sort_order",
                message="Invalid sort_order value. Allowed values: asc, desc",
            )

        items, total = self.repository.list_for_user(
            user_id=current_user.id,
            status_filter=status_filter,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order,
            skip=skip,
            limit=limit,
        )

        return {
            "items": items,
            "total": total,
            "skip": skip,
            "limit": limit,
        }

    def get_application(self, application_id: int, current_user: User):
        logger.info("Fetching application_id=%s for user_id=%s", application_id, current_user.id)

        application = self.repository.get_by_id_for_user(application_id, current_user.id)
        if not application:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                code="application_not_found",
                message="Application not found",
            )
        return application

    def update_application(self, application_id: int, application_data: ApplicationUpdate, current_user: User):
        logger.info("Updating application_id=%s for user_id=%s", application_id, current_user.id)

        application = self.get_application(application_id, current_user)
        update_data = application_data.model_dump(exclude_unset=True)
        return self.repository.update(application, **update_data)

    def delete_application(self, application_id: int, current_user: User):
        logger.info("Deleting application_id=%s for user_id=%s", application_id, current_user.id)

        application = self.get_application(application_id, current_user)
        self.repository.delete(application)

    def get_analytics(self, current_user: User):
        logger.info("Fetching analytics for user_id=%s", current_user.id)

        counts = self.repository.get_status_counts(current_user.id)

        total = sum(counts.values())

        saved = counts.get(ApplicationStatus.SAVED, 0)
        applied = counts.get(ApplicationStatus.APPLIED, 0)
        interview = counts.get(ApplicationStatus.INTERVIEW, 0)
        offer = counts.get(ApplicationStatus.OFFER, 0)
        rejected = counts.get(ApplicationStatus.REJECTED, 0)

        conversion_to_interview = interview / applied if applied > 0 else 0
        conversion_to_offer = offer / applied if applied > 0 else 0

        return {
            "total": total,
            "saved": saved,
            "applied": applied,
            "interview": interview,
            "offer": offer,
            "rejected": rejected,
            "conversion_to_interview": conversion_to_interview,
            "conversion_to_offer": conversion_to_offer,
        }