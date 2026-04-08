from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import setup_logging
from app.routers.applications import router as applications_router
from app.routers.auth import router as auth_router
from app.routers.health import router as health_router


setup_logging()

app = FastAPI(
    title="Job Tracker API",
    description="Production-style API for tracking job applications and hiring pipeline progress.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Job Tracker API is running"}


app.include_router(auth_router)
app.include_router(applications_router)
app.include_router(health_router)