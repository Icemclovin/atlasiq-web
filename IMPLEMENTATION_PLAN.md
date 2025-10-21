# 🚀 AtlasIQ Web MVP - Implementation Plan

## 📋 Executive Summary

This document outlines the complete implementation plan for AtlasIQ Web MVP - a professional web application for real-time macroeconomic and sectoral data analysis across Benelux + Germany.

**Status**: 🏗️ **Foundation Created**
**Next Steps**: Complete backend implementation, then frontend

---

## ✅ What Has Been Created

### 1. Project Structure

- ✅ Root `README.md` with comprehensive documentation
- ✅ `.env.example` with 100+ configuration options
- ✅ `docker-compose.yml` with PostgreSQL, Redis, Backend, Frontend, Worker
- ✅ Backend folder structure defined
- ✅ Frontend folder structure defined
- ✅ `requirements.txt` with 50+ Python dependencies

### 2. Documentation

- ✅ Architecture overview
- ✅ API endpoint specification
- ✅ Data source integration plan
- ✅ Security guidelines
- ✅ Deployment instructions

---

## 🔨 Implementation Phases

### Phase 1: Backend Core (Priority: HIGH)

#### 1.1 Configuration & Database Setup

**Files to Create:**

```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py              # Pydantic settings from environment
│   ├── database.py            # Async SQLAlchemy setup
│   └── dependencies.py        # FastAPI dependencies
```

**Key Features:**

- Pydantic Settings management
- Async database session factory
- Connection pooling
- Health check endpoints

#### 1.2 Database Models

**Files to Create:**

```
backend/app/models/
├── __init__.py
├── user.py                    # User model
├── indicator.py               # IndicatorValue model (time-series)
├── data_source.py             # DataSource metadata
├── fetch_log.py               # FetchLog for tracking
└── export.py                  # Export history
```

**Schema Design:**

```sql
-- users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    is_admin BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- indicator_values table (time-series)
CREATE TABLE indicator_values (
    id SERIAL PRIMARY KEY,
    country VARCHAR(2) NOT NULL,        -- NL, BE, LU, DE
    sector VARCHAR(10),                 -- C, G, J or NULL for country-level
    indicator_code VARCHAR(100) NOT NULL,
    indicator_name VARCHAR(255),
    date DATE NOT NULL,
    value NUMERIC,
    unit VARCHAR(50),
    source VARCHAR(50) NOT NULL,       -- eurostat, ecb, worldbank, oecd
    raw_metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(country, sector, indicator_code, date, source)
);
CREATE INDEX idx_indicator_country_date ON indicator_values(country, indicator_code, date);
CREATE INDEX idx_indicator_sector ON indicator_values(sector);

-- data_sources table
CREATE TABLE data_sources (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    api_base_url VARCHAR(500),
    is_active BOOLEAN DEFAULT true,
    last_fetch_at TIMESTAMP,
    last_fetch_status VARCHAR(50),
    config JSONB
);

-- fetch_logs table
CREATE TABLE fetch_logs (
    id SERIAL PRIMARY KEY,
    source_name VARCHAR(100) NOT NULL,
    dataset VARCHAR(100),
    status VARCHAR(50) NOT NULL,       -- success, failed, partial
    records_fetched INTEGER,
    error_message TEXT,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    duration_seconds INTEGER
);

-- exports table
CREATE TABLE exports (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    export_type VARCHAR(50) NOT NULL,  -- csv, excel, pdf
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500),
    status VARCHAR(50) NOT NULL,       -- pending, completed, failed
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
);
```

#### 1.3 Authentication System

**Files to Create:**

```
backend/app/
├── auth/
│   ├── __init__.py
│   ├── jwt.py                 # JWT token creation/validation
│   ├── password.py            # Password hashing
│   └── dependencies.py        # get_current_user, require_admin
├── schemas/
│   ├── __init__.py
│   ├── user.py                # UserCreate, UserLogin, UserResponse
│   └── token.py               # Token, TokenData
└── api/v1/
    └── auth.py                # Auth endpoints
```

**Endpoints:**

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login (returns access + refresh token)
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user info

#### 1.4 Data Adapters (Modular Pattern)

**Files to Create:**

```
backend/app/adapters/
├── __init__.py
├── base.py                    # BaseAdapter (abstract interface)
├── eurostat.py                # EurostatAdapter
├── ecb.py                     # ECBAdapter
├── worldbank.py               # WorldBankAdapter
└── oecd.py                    # OECDAdapter
```

**BaseAdapter Interface:**

```python
class BaseAdapter(ABC):
    """Base adapter for data sources"""

    @abstractmethod
    async def discover(self) -> List[str]:
        """List available datasets"""
        pass

    @abstractmethod
    async def fetch(self, dataset: str, params: dict) -> bytes:
        """Fetch raw data from API"""
        pass

    @abstractmethod
    def parse(self, raw_data: bytes) -> pd.DataFrame:
        """Parse raw data to DataFrame"""
        pass

    @abstractmethod
    def normalize(self, df: pd.DataFrame) -> List[dict]:
        """Normalize to standard schema"""
        pass

    @abstractmethod
    async def store(self, records: List[dict]):
        """Store to database"""
        pass
```

#### 1.5 Background Jobs & Scheduler

**Files to Create:**

```
backend/app/tasks/
├── __init__.py
├── scheduler.py               # APScheduler setup
├── fetch_jobs.py              # Data fetch jobs
└── worker.py                  # Background worker process
```

**Jobs:**

- `fetch_all_sources()` - Fetch from all 7 sources
- `compute_risk_scores()` - Calculate risk indicators
- `clean_old_exports()` - Delete expired exports
- `update_cache()` - Refresh Redis cache

#### 1.6 API Endpoints

**Files to Create:**

```
backend/app/api/v1/
├── __init__.py
├── router.py                  # Main API router
├── auth.py                    # Authentication endpoints
├── data.py                    # Data query endpoints
├── dashboard.py               # Dashboard endpoints
├── indicators.py              # Indicator metadata
├── countries.py               # Country endpoints
└── export.py                  # Export endpoints
```

**Key Endpoints:**

- `GET /api/v1/countries` - List supported countries
- `GET /api/v1/indicators` - List available indicators
- `GET /api/v1/data` - Query time-series data with filters
- `GET /api/v1/dashboard/summary` - Aggregate KPIs
- `GET /api/v1/dashboard/country/{code}` - Country details
- `POST /api/v1/export/csv` - Export to CSV
- `POST /api/v1/fetch` - Manual fetch trigger (admin)

---

### Phase 2: Frontend (Priority: HIGH)

#### 2.1 React App Setup

**Files to Create:**

```
frontend/
├── package.json
├── vite.config.ts
├── tailwind.config.js
├── tsconfig.json
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── vite-env.d.ts
│   └── index.css
```

#### 2.2 Authentication Flow

**Files to Create:**

```
frontend/src/
├── pages/
│   ├── Login.tsx
│   ├── Register.tsx
│   └── ForgotPassword.tsx
├── contexts/
│   └── AuthContext.tsx
├── services/
│   └── auth.ts
└── utils/
    └── localStorage.ts
```

#### 2.3 Main Dashboard

**Files to Create:**

```
frontend/src/pages/
├── Dashboard.tsx              # Main dashboard
├── CountryDetail.tsx          # Country-specific view
└── IndicatorExplorer.tsx      # Indicator search/filter
```

**Dashboard Components:**

- KPI Summary Cards (GDP, unemployment, inflation)
- Country selector dropdown
- Sector breakdown table
- Time-series charts (1y, 3y, 5y toggles)
- Last update timestamp
- Refresh button

#### 2.4 Reusable Components

**Files to Create:**

```
frontend/src/components/
├── layout/
│   ├── Navbar.tsx
│   ├── Sidebar.tsx
│   └── Footer.tsx
├── charts/
│   ├── LineChart.tsx
│   ├── BarChart.tsx
│   └── PieChart.tsx
├── tables/
│   ├── DataTable.tsx
│   └── SortableTable.tsx
├── forms/
│   ├── Input.tsx
│   ├── Select.tsx
│   └── Button.tsx
└── ui/
    ├── Card.tsx
    ├── Badge.tsx
    ├── Modal.tsx
    └── Spinner.tsx
```

#### 2.5 API Integration

**Files to Create:**

```
frontend/src/services/
├── api.ts                     # Axios instance
├── auth.ts                    # Auth API calls
├── data.ts                    # Data API calls
├── dashboard.ts               # Dashboard API calls
└── websocket.ts               # WebSocket client
```

---

### Phase 3: Testing (Priority: MEDIUM)

#### 3.1 Backend Tests

**Files to Create:**

```
backend/tests/
├── conftest.py                # Pytest fixtures
├── test_auth.py               # Auth tests
├── test_data_api.py           # Data API tests
├── test_adapters.py           # Adapter tests
├── test_models.py             # Model tests
└── test_services.py           # Service tests
```

#### 3.2 Frontend Tests

**Files to Create:**

```
frontend/tests/
├── setup.ts
├── Login.test.tsx
├── Dashboard.test.tsx
└── components/
    ├── Card.test.tsx
    └── DataTable.test.tsx
```

#### 3.3 Integration Tests

**Files to Create:**

```
tests/e2e/
├── playwright.config.ts
├── auth.spec.ts
├── dashboard.spec.ts
└── data-export.spec.ts
```

---

### Phase 4: DevOps & Deployment (Priority: MEDIUM)

#### 4.1 Docker Configuration

**Files to Create:**

```
backend/Dockerfile
frontend/Dockerfile
docker-compose.prod.yml
.dockerignore
```

#### 4.2 CI/CD Pipeline

**Files to Create:**

```
.github/workflows/
├── ci.yml                     # Lint, test, build
├── deploy-staging.yml
└── deploy-prod.yml
```

#### 4.3 Monitoring

**Files to Create:**

```
monitoring/
├── prometheus.yml
├── grafana/
│   └── dashboards/
└── alerts.yml
```

---

## 📊 Estimated Effort

| Phase           | Components               | Estimated Hours | Priority |
| --------------- | ------------------------ | --------------- | -------- |
| Backend Core    | Config, DB, Models, Auth | 16-20h          | HIGH     |
| Data Adapters   | 4 adapters + base        | 12-16h          | HIGH     |
| API Endpoints   | 15+ endpoints            | 12-16h          | HIGH     |
| Background Jobs | Scheduler, jobs          | 8-12h           | MEDIUM   |
| Frontend Setup  | React, routing, auth     | 12-16h          | HIGH     |
| Dashboard UI    | Pages, components        | 16-20h          | HIGH     |
| Charts & Viz    | Recharts integration     | 8-12h           | MEDIUM   |
| Testing         | Backend + frontend + e2e | 16-20h          | MEDIUM   |
| Docker & CI/CD  | Deployment setup         | 8-12h           | MEDIUM   |
| Documentation   | User + dev guides        | 8-12h           | LOW      |

**Total Estimated: 116-176 hours (3-4 weeks for 1 developer)**

---

## 🚀 Quick Start (Current State)

The project foundation has been created. To continue:

### Option 1: Complete Backend First

```bash
cd atlasiq-web/backend

# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Implement core modules (see Phase 1)
# - app/config.py
# - app/database.py
# - app/models/
# - app/api/
# - app/adapters/

# 4. Run migrations
alembic upgrade head

# 5. Start server
uvicorn app.main:app --reload
```

### Option 2: Use Docker (Recommended)

```bash
cd atlasiq-web

# 1. Copy environment file
cp .env.example .env

# 2. Edit .env (set passwords, etc.)
nano .env

# 3. Build and start
docker-compose up --build

# Services will be available at:
# - Backend: http://localhost:8000
# - Frontend: http://localhost:3000
# - PostgreSQL: localhost:5432
# - Redis: localhost:6379
```

---

## 📝 Next Immediate Steps

### Step 1: Backend Core Implementation

1. Create `app/config.py` with Pydantic Settings
2. Create `app/database.py` with async SQLAlchemy setup
3. Create all models in `app/models/`
4. Create Alembic migration scripts
5. Implement JWT authentication in `app/auth/`

### Step 2: Data Adapters

1. Implement `BaseAdapter` in `app/adapters/base.py`
2. Implement `EurostatAdapter` with BSD, STS, GBS, PROM
3. Implement `ECBAdapter` for interest rates
4. Implement `WorldBankAdapter` for GDP, unemployment
5. Implement `OECDAdapter` for business indicators

### Step 3: API Endpoints

1. Create `/auth/*` endpoints (register, login, refresh)
2. Create `/data` endpoint with filters
3. Create `/dashboard/*` endpoints
4. Create `/export/*` endpoints
5. Add OpenAPI documentation

### Step 4: Frontend

1. Set up Vite + React + TypeScript
2. Configure Tailwind CSS
3. Implement authentication flow
4. Build dashboard page
5. Integrate charts (Recharts)

---

## 🎯 Success Criteria

Before considering MVP complete, ensure:

- ✅ User can register and login
- ✅ Dashboard displays KPIs for NL, BE, LU, DE
- ✅ At least 5 KPIs per country visible
- ✅ Sector breakdown shows risk scores
- ✅ Data can be exported to CSV
- ✅ Scheduled fetch job runs successfully
- ✅ UI shows last fetch timestamp
- ✅ API documentation at `/docs` is complete
- ✅ All tests pass
- ✅ Docker setup works out of the box

---

## 💡 Development Tips

1. **Start Simple**: Get one data source working end-to-end first (e.g., Eurostat BSD)
2. **Test Early**: Write tests as you go, not at the end
3. **Use Mocks**: Mock external APIs during development to avoid rate limits
4. **Cache Aggressively**: Use Redis for everything that doesn't change frequently
5. **Document**: Add docstrings and comments as you write code
6. **Security First**: Never commit secrets, always use `.env`

---

## 📚 Resources

- **FastAPI**: https://fastapi.tiangolo.com
- **SQLAlchemy**: https://docs.sqlalchemy.org/en/20/
- **React**: https://react.dev
- **Vite**: https://vitejs.dev
- **Tailwind CSS**: https://tailwindcss.com
- **Recharts**: https://recharts.org

---

**Ready to build? Start with Phase 1, Task 1.1: Configuration & Database Setup!** 🚀
