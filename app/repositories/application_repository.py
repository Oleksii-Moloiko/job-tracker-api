from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from app.models import Application, ApplicationStatus


class ApplicationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> Application:
        application = Application(**kwargs)
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        return application

    def get_by_id_for_user(self, application_id: int, user_id: int) -> Application | None:
        return (
            self.db.query(Application)
            .filter(Application.id == application_id, Application.owner_id == user_id)
            .first()
        )

    def list_for_user(
        self,
        user_id: int,
        status_filter: ApplicationStatus | None = None,
        search: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        skip: int = 0,
        limit: int = 10,
    ) -> tuple[list[Application], int]:
        query = self.db.query(Application).filter(Application.owner_id == user_id)

        if status_filter:
            query = query.filter(Application.status == status_filter)

        if search:
            query = query.filter(
                or_(
                    Application.company_name.ilike(f"%{search}%"),
                    Application.position.ilike(f"%{search}%"),
                )
            )

        sortable_fields = {
            "created_at": Application.created_at,
            "updated_at": Application.updated_at,
            "company_name": Application.company_name,
            "position": Application.position,
            "status": Application.status,
        }

        sort_column = sortable_fields.get(sort_by, Application.created_at)

        if sort_order == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        total = query.count()
        items = query.offset(skip).limit(limit).all()

        return items, total

    def update(self, application: Application, **kwargs) -> Application:
        for field, value in kwargs.items():
            setattr(application, field, value)

        self.db.commit()
        self.db.refresh(application)
        return application

    def delete(self, application: Application) -> None:
        self.db.delete(application)
        self.db.commit()

    def get_status_counts(self, user_id: int):
        results = (
            self.db.query(
                Application.status,
                func.count(Application.id)
            )
            .filter(Application.owner_id == user_id)
            .group_by(Application.status)
            .all()
        )

        return {status: count for status, count in results}