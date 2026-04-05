# Job Tracker API

A REST API for tracking job applications, built with FastAPI.

## 🚀 Features

- User registration
- JWT authentication (login)
- Protected routes
- Get current authenticated user
- Create, read, update, and delete job applications
- Ownership-based access control
- Filter applications by status
- Search applications by company name
- Pagination support
- PostgreSQL database
- Dockerized environment
- Alembic database migrations

---

## 🧱 Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT (python-jose)
- Passlib (bcrypt)
- Docker & Docker Compose
- Alembic

---

## 📁 Project Structure

```bash
app/
├── main.py
├── config.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
├── dependencies.py
└── routers/
    ├── auth.py
    └── applications.py


alembic/
Dockerfile
docker-compose.yml
requirements.txt
```

---

## ⚙️ Environment Variables

Create .env from .env.example:
```bash
cp .env.example .env
```
Example:
```bash
DATABASE_URL=postgresql://postgres:postgres@db:5432/job_tracker_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🐳 Run with Docker
```bash
docker compose up --build
```
API will be available at:
```bash
http://127.0.0.1:8000/docs
```

---

## 🔐 Authentication Flow
Register a user
Log in via /auth/login
Receive JWT access token
Authorize in Swagger UI
Use protected endpoints

---

## 📌 API Endpoints
Auth
POST /auth/register
POST /auth/login
GET /auth/me
Applications
POST /applications
GET /applications
GET /applications/{application_id}
PUT /applications/{application_id}
DELETE /applications/{application_id}

--- 

## 🔎 Query Parameters
Filter by status
```bash
GET /applications?status=applied
```
Search by company name
```bash
GET /applications?search=google
```
Pagination
```bash
GET /applications?skip=0&limit=10
```

---

## 🧠 What I Learned
How JWT authentication works in FastAPI
How to protect routes using dependencies
How to work with PostgreSQL via SQLAlchemy
How to implement ownership-based access control
How to manage schema changes with Alembic
How to containerize a full backend system with Docker

---

## 💬 About the Project

This project started as a basic CRUD API but was refactored into a realistic job application tracking system.
It demonstrates backend architecture, authentication, database design, and production-like setup.