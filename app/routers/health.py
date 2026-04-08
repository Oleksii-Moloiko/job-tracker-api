from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "status": "ok",
        "service": "job-tracker-api",
    }


@router.get("/live", status_code=status.HTTP_200_OK)
def liveness_check():
    return {
        "status": "ok",
    }


@router.get("/ready", status_code=status.HTTP_200_OK)
def readiness_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {
        "status": "ready",
        "database": "ok",
    }