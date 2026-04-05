# Job Tracker API

A production-like REST API for tracking job applications, built with FastAPI.

---

## 🚀 Overview

This project is a backend service that allows users to manage job applications.

It includes authentication, protected routes, database persistence, and a Dockerized environment, making it easy to run on any machine.

---

## ✨ Features

- User registration
- JWT authentication (login)
- Protected API routes
- Get current authenticated user
- Full CRUD for job applications
- Ownership-based access control (users only see their own data)
- Filtering by status
- Search by company name
- Pagination support
- PostgreSQL database
- Dockerized environment (API + DB)
- Alembic database migrations

---

## 🧱 Tech Stack

- **FastAPI** — backend framework
- **PostgreSQL** — relational database
- **SQLAlchemy** — ORM
- **Pydantic** — validation
- **JWT (python-jose)** — authentication
- **Passlib (bcrypt)** — password hashing
- **Docker & Docker Compose** — containerization
- **Alembic** — database migrations

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
```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/job_tracker_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🐳 Run the Project

Start everything with a single command:
```bash
docker compose up --build
```
API documentation will be available at:
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
- POST /auth/register
- POST /auth/login
- GET /auth/me
Applications
- POST /applications
- GET /applications
- GET /applications/{application_id}
- PUT /applications/{application_id}
- DELETE /applications/{application_id}

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

## 🧠 Key Concepts Demonstrated
- JWT-based authentication and authorization
- Dependency-based route protection in FastAPI
- ORM modeling and relationships with SQLAlchemy
- Ownership-based data isolation
Database migrations with Alembic
- Dockerized backend environment
- API design beyond basic CRUD

---

## 💬 About the Project

This project started as a simple CRUD API but was refactored into a more realistic system for tracking job applications.

The focus was on building a production-like backend with proper authentication, database design, and infrastructure setup.

---

## 🚀 Future Improvements
- Add automated tests (pytest)
- Role-based access (admin/user)
- Refresh tokens
- Rate limiting
- Logging and monitoring

---

