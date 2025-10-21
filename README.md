# AtlasIQ Benelux-DE Web - Macro Dashboard MVP

**Professional web application for real-time macroeconomic and sectoral data analysis across Benelux + Germany**

## 🎯 Project Overview

AtlasIQ Web is a production-ready application that provides near-real-time macroeconomic and sectoral data for Netherlands, Belgium, Luxembourg, and Germany. Built with React + FastAPI, it features user authentication, automated data refresh, interactive dashboards, and risk scoring.

### Key Features

- 🔐 **User Authentication** - JWT-based auth with register/login
- 📊 **Real-time Dashboard** - Live macro/sectoral KPIs with WebSocket updates
- 🌍 **Multi-Country Support** - NL, BE, LU, DE with sector breakdowns
- 📈 **Risk Scoring** - 10-factor risk model with explainable breakdowns
- 🔄 **Auto Data Refresh** - Scheduled fetching from 7+ data sources
- 💾 **Data Export** - CSV/Excel export of charts and tables
- 🐳 **Docker Ready** - Full containerized deployment

### Tech Stack

#### Frontend

- **React 18** (TypeScript)
- **Vite** - Fast build tooling
- **TailwindCSS** + Headless UI - Responsive, accessible design
- **Recharts** - Interactive data visualizations
- **Socket.IO** - Real-time updates

#### Backend

- **FastAPI** - Modern Python async framework
- **SQLAlchemy 2.0** - Async ORM
- **PostgreSQL** - Time-series data storage
- **Redis** - Caching & pub/sub
- **APScheduler** - Background jobs
- **JWT** - Secure authentication

#### DevOps

- **Docker** + docker-compose
- **GitHub Actions** - CI/CD pipelines
- **Prometheus** - Metrics & monitoring
- **pytest** + **Playwright** - Comprehensive testing

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose (recommended)
- OR: Python 3.11+, Node.js 18+, PostgreSQL 15+, Redis 7+

### Run with Docker (Recommended)

```bash
# Clone the repository
cd atlasiq-web

# Copy environment template
cp .env.example .env

# Edit .env with your settings (all sensible defaults provided)
nano .env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Run Locally (Development)

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

---

## 📊 Data Sources

The application integrates data from multiple authoritative sources:

### 1. **Eurostat** (4 datasets)

- **BSD** - Business Structure & Dynamics
- **STS** - Short-term Statistics
- **GBS** - Globalisation in Business
- **PROM** - Production of Manufactured Goods

### 2. **ECB** (European Central Bank)

- Interest rates (EURIBOR)
- Exchange rates (EUR/USD)
- Monetary policy indicators

### 3. **World Bank**

- GDP & GDP growth
- Unemployment rates
- Inflation (CPI)
- FDI indicators

### 4. **OECD**

- Business confidence indices
- Productivity metrics
- Labor cost indices
- Industrial production

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                        │
│  - Auth UI  - Dashboard  - Charts  - Country Views          │
└────────────────────┬────────────────────────────────────────┘
                     │ REST API + WebSocket
┌────────────────────▼────────────────────────────────────────┐
│                  BACKEND (FastAPI)                          │
│  ┌──────────────┐  ┌───────────────┐  ┌─────────────────┐  │
│  │   Auth API   │  │   Data API    │  │  Dashboard API  │  │
│  └──────────────┘  └───────────────┘  └─────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Data Adapters (Modular)                    │  │
│  │  Eurostat │ ECB │ World Bank │ OECD                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │      Background Jobs (APScheduler)                   │  │
│  │  - Fetch data  - Process KPIs  - Risk scoring        │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  DATA LAYER                                 │
│  ┌───────────────┐  ┌──────────┐  ┌────────────────────┐  │
│  │  PostgreSQL   │  │  Redis   │  │  File Storage      │  │
│  │  (TimeSeries) │  │ (Cache)  │  │  (Logs, Exports)   │  │
│  └───────────────┘  └──────────┘  └────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Project Structure

```
atlasiq-web/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── config.py          # Configuration management
│   │   ├── database.py        # Database connection
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── api/               # API endpoints
│   │   │   ├── auth.py        # Authentication
│   │   │   ├── data.py        # Data queries
│   │   │   └── dashboard.py   # Dashboard endpoints
│   │   ├── adapters/          # Data source adapters
│   │   │   ├── base.py        # Base adapter interface
│   │   │   ├── eurostat.py
│   │   │   ├── ecb.py
│   │   │   ├── worldbank.py
│   │   │   └── oecd.py
│   │   ├── services/          # Business logic
│   │   │   ├── auth.py
│   │   │   ├── data_processor.py
│   │   │   └── risk_scorer.py
│   │   ├── tasks/             # Background jobs
│   │   │   └── scheduler.py
│   │   └── utils/             # Utilities
│   ├── alembic/               # Database migrations
│   ├── tests/                 # Backend tests
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── main.tsx           # App entry point
│   │   ├── App.tsx            # Root component
│   │   ├── components/        # Reusable components
│   │   ├── pages/             # Page components
│   │   │   ├── Login.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── CountryDetail.tsx
│   │   │   └── IndicatorExplorer.tsx
│   │   ├── services/          # API clients
│   │   ├── hooks/             # Custom React hooks
│   │   ├── utils/             # Utilities
│   │   └── types/             # TypeScript types
│   ├── public/
│   ├── tests/                 # Frontend tests
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── docker-compose.yml          # Docker orchestration
├── .env.example               # Environment template
├── .github/
│   └── workflows/
│       └── ci.yml             # CI/CD pipeline
└── README.md                  # This file
```

---

## 🔑 API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT tokens
- `POST /api/v1/auth/refresh` - Refresh access token

### Data

- `GET /api/v1/countries` - List supported countries
- `GET /api/v1/indicators` - List available indicators
- `GET /api/v1/data` - Query time-series data
- `POST /api/v1/fetch` - Trigger manual data fetch (admin)

### Dashboard

- `GET /api/v1/dashboard/summary` - Aggregate KPIs
- `GET /api/v1/dashboard/country/{code}` - Country details
- `GET /api/v1/dashboard/risk-scores` - Risk scores by sector

### Export

- `POST /api/v1/export/csv` - Export data to CSV
- `POST /api/v1/export/excel` - Export data to Excel

**Full API documentation**: http://localhost:8000/docs

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Tests

```bash
cd frontend
npm test
npm run test:e2e  # Playwright integration tests
```

### Run All Tests

```bash
# From root directory
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

---

## 📈 Monitoring & Observability

### Logs

```bash
# View all logs
docker-compose logs -f

# Backend logs only
docker-compose logs -f backend

# Frontend logs only
docker-compose logs -f frontend
```

### Metrics

Prometheus metrics available at:

- **Backend**: http://localhost:8000/metrics
- **Grafana**: http://localhost:3001 (if enabled)

### Health Checks

- **Backend**: http://localhost:8000/health
- **Database**: Check via backend health endpoint

---

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://atlasiq:password@postgres:5432/atlasiq

# Redis
REDIS_URL=redis://redis:6379/0

# JWT
JWT_SECRET=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Data Refresh
DATA_REFRESH_SCHEDULE="0 2 * * *"  # Daily at 2 AM
CACHE_TTL_SECONDS=3600

# API Rate Limits
RATE_LIMIT_PER_MINUTE=60

# External APIs (optional - use test mode if not provided)
EUROSTAT_API_KEY=optional
WORLD_BANK_API_KEY=optional
```

---

## 🚀 Deployment

### Production Deployment

1. **Update docker-compose.prod.yml**
2. **Set production environment variables**
3. **Enable HTTPS** (use nginx-proxy or Traefik)
4. **Run migrations**

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Scaling

```bash
# Scale backend workers
docker-compose up -d --scale backend=3

# Scale frontend
docker-compose up -d --scale frontend=2
```

---

## 📚 Documentation

- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc
- **User Guide**: [docs/USER_GUIDE.md](docs/USER_GUIDE.md)
- **Developer Guide**: [docs/DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md)
- **Architecture**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 🛠️ Development

### Adding a New Data Source

See [docs/DEVELOPER_GUIDE.md#adding-data-sources](docs/DEVELOPER_GUIDE.md) for step-by-step guide.

### Running in Development Mode

```bash
# Backend with auto-reload
cd backend
uvicorn app.main:app --reload

# Frontend with HMR
cd frontend
npm run dev
```

---

## 🔒 Security

- **JWT Authentication** with refresh tokens
- **Password Hashing** using bcrypt
- **HTTPS** enforced in production
- **Rate Limiting** on all endpoints
- **CORS** configured for frontend origin
- **SQL Injection** protection via SQLAlchemy
- **XSS** protection via React's built-in escaping

---

## 📊 Data Flow

1. **Scheduled Fetch** - APScheduler triggers data adapters
2. **Adapter Fetch** - Each adapter fetches from its API
3. **Parse & Normalize** - Convert to standard format
4. **Store** - Save to PostgreSQL with metadata
5. **Cache** - Cache processed KPIs in Redis
6. **Publish** - Notify frontend via WebSocket
7. **Display** - Frontend updates dashboard in real-time

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/atlasiq-web/issues)
- **Email**: support@atlasiq.example.com
- **Documentation**: [docs/](docs/)

---

## 🗺️ Roadmap

### Phase 1: MVP (Current)

- ✅ Basic auth & dashboard
- ✅ 4 countries, 3 sectors
- ✅ 7 data sources
- ✅ Risk scoring

### Phase 2: Portfolio Management

- Portfolio creation & tracking
- M&A deal simulation
- ROI/IRR calculations
- Scenario analysis

### Phase 3: Advanced Analytics

- Machine learning predictions
- Custom indicators
- Multi-portfolio comparison
- Advanced exports

### Phase 4: Enterprise Features

- Team collaboration
- Role-based access control
- Audit logging
- White-labeling

---

**Version**: 1.0.0-MVP
**Status**: 🚧 In Development
**Last Updated**: October 20, 2025

_Built with ❤️ for Private Equity & M&A professionals_
#   a t l a s i q - w e b  
 