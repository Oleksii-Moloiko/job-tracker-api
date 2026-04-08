# 🚀 Job Tracker API
![CI](https://github.com/Oleksii-Moloiko/job-tracker-api/actions/workflows/ci.yml/badge.svg)

Production-style backend API for tracking job applications, managing hiring pipelines, and analyzing job search performance.

Built with FastAPI, PostgreSQL, and modern backend practices including JWT authentication, refresh tokens, and CI/CD.

---

## ✨ Features

### 📊 Analytics

- Applications count by status
- Hiring funnel metrics
- Conversion rates (applied → interview → offer)

Example:

```json
{
  "total": 120,
  "applied": 80,
  "interview": 15,
  "offer": 3,
  "conversion_to_interview": 0.1875,
  "conversion_to_offer": 0.0375
}
```

### 🔐 Authentication
- JWT access tokens
- Refresh tokens with rotation
- Token revocation (logout)
- Secure password hashing

### 📦 Applications Management
- Create, update, delete applications
- Ownership-based access control
- Filtering by status
- Search by company and position
- Sorting (created_at, updated_at, etc.)
- Typed filtering using enums
- Pagination support

### 🧠 Domain Model
- Strong typing with enums (`ApplicationStatus`)
- Clean data validation with Pydantic

### ⚙️ Infrastructure
- PostgreSQL database
- Alembic migrations
- Environment-based configuration

### 🧪 Testing & Quality
- Pytest test suite
- Auth flow fully tested
- GitHub Actions CI pipeline

## ❤️ Health Endpoints

- `/health` – basic service status
- `/health/live` – liveness probe
- `/health/ready` – readiness check (DB connection)
---
## 📌 Key Highlights

- Clean layered architecture (router/service/repository)
- JWT authentication with refresh token rotation
- Flexible querying (filtering, search, sorting, pagination)
- Hiring funnel analytics
- Fully tested authentication flow
- CI pipeline with GitHub Actions

---

## 📡 API Endpoints

### Auth
- POST /auth/register
- POST /auth/login
- GET /auth/me
- POST /auth/refresh
- POST /auth/logout

### Applications
- GET /applications
- POST /applications
- GET /applications/{id}
- PUT /applications/{id}
- DELETE /applications/{id}

### Analytics
- GET /applications/analytics/summary

### Health
- GET /health
- GET /health/live
- GET /health/ready

---
## 🛠 Tech Stack

- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **Alembic**
- **Pydantic v2**
- **JWT (python-jose)**
- **Pytest**
- **GitHub Actions**

---

## 📁 Project Structure

```bash
app/
├── routers/ # API endpoints
├── models/ # SQLAlchemy models
├── schemas/ # Pydantic schemas
├── auth.py # JWT + security logic
├── dependencies.py # DI (auth, db)
├── config.py # settings
├── database.py # DB connection
└── core/
└── exceptions.py

alembic/ # DB migrations
tests/ # test suite
```

---

## 🏗 Architecture

The project follows a layered architecture:

Request → Router → Service → Repository → Database

- **Routers** – handle HTTP requests and responses  
- **Services** – contain business logic  
- **Repositories** – handle database access  
- **Models** – define ORM entities  
- **Schemas** – validate request/response data  

This separation improves maintainability, testability, and scalability.

---
## ⚙️ Setup

### 1. Clone repo
```bash
git clone https://github.com/YOUR_USERNAME/job-tracker-api.git
cd job-tracker-api
```

### 2. Create virtual environment
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup environment
Create .env file:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/job_tracker_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 5.Run migrations
```bash
alembic upgrade head
```

### 6. Run app
```bash
uvicorn app.main:app --reload
```

# 📖 API Docs

Available at:
```
http://127.0.0.1:8000/docs
```

# 🔐 Auth Flow
### Login
```
POST /auth/login
```

Returns:
```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer"
}
```

### Refresh
```
POST /auth/refresh
```
```json
{
  "refresh_token": "..."
}
```

### Logout
```
POST /auth/logout
```
```json
{
  "refresh_token": "..."
}
```

# 🧪 Run Tests
```bash
pytest -v
```

# ⚡ CI

GitHub Actions pipeline:

- installs dependencies
- runs migrations
- executes tests

# 📌 Future Improvements
- Rate limiting (login protection)
- Role-based access control
- Application history tracking
- Background jobs (notifications)
- Docker production setup

---

## 💡 About This Project

This project was built to demonstrate real-world backend development skills, including:

- API design best practices
- authentication flows with token rotation
- clean architecture patterns
- database migrations and persistence
- observability via logging
- production-style features like analytics and health checks

---

# 👨‍💻 Author

### Oleksii Moloiko

---
## 📸 API Preview

![Swagger UI](./docs/swagger.png)