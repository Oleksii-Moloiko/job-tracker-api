# 🚀 Job Tracker API
![CI](https://github.com/Oleksii-Moloiko/job-tracker-api/actions/workflows/ci.yml/badge.svg)

Production-ready backend service for tracking job applications.

Built with FastAPI, PostgreSQL, and modern backend practices including JWT authentication, refresh tokens, and CI/CD.

---

## ✨ Features

### 🔐 Authentication
- JWT access tokens
- Refresh tokens with rotation
- Token revocation (logout)
- Secure password hashing

### 📦 Applications Management
- Create, update, delete applications
- Ownership-based access control
- Filtering by status
- Search by company
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

### ❤️ Health Monitoring
- `/health`
- `/health/live`
- `/health/ready`

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

# 👨‍💻 Author

### Oleksii Moloiko