# AtlasIQ Web Backend - Quick Start Guide

## ✅ Backend Core Implementation Complete!

The backend foundation is now fully implemented with:

### 🏗️ **What's Implemented**

1. **Configuration Management** (`app/config.py`)

   - Pydantic Settings with environment variables
   - Database, Redis, JWT configuration
   - Supported countries (NL, BE, LU, DE)
   - Data source settings

2. **Database Layer** (`app/database.py`)

   - Async SQLAlchemy setup
   - Connection pooling
   - Session management
   - Health checks

3. **Database Models** (`app/models/`)

   - ✅ `User` - Authentication & authorization
   - ✅ `IndicatorValue` - Time-series macro data
   - ✅ `DataSource` - External API configuration
   - ✅ `FetchLog` - Data fetch tracking
   - ✅ `Export` - File export tracking

4. **Authentication** (`app/auth/`)

   - ✅ Password hashing (bcrypt)
   - ✅ JWT access tokens
   - ✅ JWT refresh tokens
   - ✅ FastAPI dependencies for auth

5. **Pydantic Schemas** (`app/schemas/`)

   - ✅ User registration/login
   - ✅ Token responses
   - ✅ Indicator queries

6. **API Endpoints** (`app/api/v1/`)

   - ✅ `POST /api/v1/auth/register` - User registration
   - ✅ `POST /api/v1/auth/login` - Authentication
   - ✅ `POST /api/v1/auth/refresh` - Token refresh
   - ✅ `GET /api/v1/auth/me` - Get current user
   - ✅ `POST /api/v1/auth/logout` - Logout

7. **FastAPI Application** (`app/main.py`)
   - ✅ CORS middleware
   - ✅ GZip compression
   - ✅ Health check endpoint
   - ✅ OpenAPI documentation
   - ✅ Lifespan management

---

## 🚀 **How to Run**

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+ (optional for now)

### Step 1: Setup Environment

```powershell
cd C:\Users\ASUS\Desktop\parfumai\atlasiq-web\backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

```powershell
# Copy environment file
cp .env.development .env

# Edit .env with your settings (database URL, etc.)
notepad .env
```

### Step 3: Setup Database

```powershell
# Option A: Using Docker (Recommended)
cd ..
docker-compose up -d postgres redis

# Option B: Local PostgreSQL
# Create database manually:
# psql -U postgres -c "CREATE DATABASE atlasiq_db;"
# psql -U postgres -c "CREATE USER atlasiq WITH PASSWORD 'atlasiq_secure_2025';"
# psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE atlasiq_db TO atlasiq;"
```

### Step 4: Test Backend Core

```powershell
# Run test suite
python test_backend_core.py
```

Expected output:

```
🧪 ATLASIQ BACKEND CORE - TEST SUITE
============================================================
TEST 1: Configuration
✓ App Name: AtlasIQ Web
✓ Environment: development
✅ Configuration loaded successfully

TEST 2: Database Connection
✓ Database tables created
✅ Database connection is healthy

TEST 3: User Model
✓ Created test user (ID: 1)
✅ User model tests passed

TEST 4: JWT Authentication
✓ Access token created
✓ Access token verified
✅ JWT authentication tests passed

✅ ALL TESTS PASSED!
```

### Step 5: Start Backend Server

```powershell
# Start with auto-reload (development)
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at:

- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

---

## 📚 **API Documentation**

### Authentication Endpoints

#### 1. Register User

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe",
  "organization": "ACME Corp"
}
```

#### 2. Login

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

Response:

```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "is_admin": false
  }
}
```

#### 3. Get Current User

```http
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

#### 4. Refresh Token

```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGc..."
}
```

---

## 🗄️ **Database Schema**

### Tables Created

1. **users**

   - `id` (PK), `email` (unique), `hashed_password`
   - `full_name`, `organization`
   - `is_active`, `is_admin`
   - `created_at`, `updated_at`, `last_login_at`

2. **indicator_values**

   - `id` (PK), `country_code`, `sector`, `indicator_code`
   - `date`, `period_type`, `value`, `unit`
   - `source`, `source_dataset`, `metadata`
   - Indexed for fast time-series queries

3. **data_sources**

   - `id` (PK), `name`, `source_type`, `api_base_url`
   - `is_active`, `is_healthy`
   - Statistics tracking

4. **fetch_logs**

   - Tracks all data fetch operations
   - Performance metrics
   - Error logging

5. **exports**
   - User export tracking
   - File metadata
   - Expiration management

---

## 🧪 **Testing**

### Test with cURL

```powershell
# Register user
curl -X POST http://localhost:8000/api/v1/auth/register `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"test@example.com\",\"password\":\"Test123456!\"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"test@example.com\",\"password\":\"Test123456!\"}'

# Health check
curl http://localhost:8000/health
```

### Test with Python

```python
import requests

# Register
response = requests.post(
    "http://localhost:8000/api/v1/auth/register",
    json={
        "email": "test@example.com",
        "password": "Test123456!"
    }
)
print(response.json())

# Login
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    json={
        "email": "test@example.com",
        "password": "Test123456!"
    }
)
tokens = response.json()
access_token = tokens["access_token"]

# Get current user
response = requests.get(
    "http://localhost:8000/api/v1/auth/me",
    headers={"Authorization": f"Bearer {access_token}"}
)
print(response.json())
```

---

## 📁 **Project Structure**

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 ✅ FastAPI application
│   ├── config.py               ✅ Configuration
│   ├── database.py             ✅ Database setup
│   │
│   ├── models/                 ✅ SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── indicator.py
│   │   ├── data_source.py
│   │   └── export.py
│   │
│   ├── schemas/                ✅ Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── indicator.py
│   │
│   ├── auth/                   ✅ Authentication
│   │   ├── __init__.py
│   │   ├── security.py
│   │   └── dependencies.py
│   │
│   └── api/                    ✅ API endpoints
│       └── v1/
│           ├── __init__.py
│           └── auth.py
│
├── .env.development            ✅ Environment config
├── requirements.txt            ✅ Dependencies
└── test_backend_core.py        ✅ Test suite
```

---

## ✅ **Phase 1 Complete!**

### What's Working

- ✅ Configuration management
- ✅ Database models & migrations
- ✅ User authentication (register, login, refresh)
- ✅ JWT token generation & verification
- ✅ Password hashing (bcrypt)
- ✅ FastAPI application with CORS
- ✅ OpenAPI documentation
- ✅ Health checks

### Next Phase: Data Adapters

- [ ] BaseAdapter interface
- [ ] EurostatAdapter (BSD, STS, GBS, PROM)
- [ ] ECBAdapter (interest rates, FX)
- [ ] WorldBankAdapter (GDP, unemployment)
- [ ] OECDAdapter (business confidence)

---

## 🐛 **Troubleshooting**

### Database connection failed

```powershell
# Check if PostgreSQL is running
docker ps

# Or start it
docker-compose up -d postgres

# Verify connection
psql -U atlasiq -d atlasiq_db -h localhost
```

### Import errors

```powershell
# Make sure you're in the backend directory
cd C:\Users\ASUS\Desktop\parfumai\atlasiq-web\backend

# And virtual environment is activated
.\venv\Scripts\activate
```

### Module not found

```powershell
# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📞 **Support**

- Interactive API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health
- Configuration: Check `.env` file

**Backend Core is Ready! 🎉**
