# AtlasIQ Web - Backend API

FastAPI backend for AtlasIQ Benelux-DE macroeconomic dashboard.

## Features

- 🔐 JWT Authentication with refresh tokens
- 📊 Multi-source data integration (Eurostat, ECB, World Bank, OECD)
- ⚡ Async SQLAlchemy with PostgreSQL
- 🔄 Redis caching and pub/sub
- ⏰ APScheduler for background jobs
- 📈 Real-time WebSocket updates
- 📄 OpenAPI documentation
- ✅ Comprehensive testing with pytest

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuration
│   ├── database.py          # DB setup
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── api/                 # API endpoints
│   ├── adapters/            # Data source adapters
│   ├── services/            # Business logic
│   ├── tasks/               # Background jobs
│   └── utils/               # Utilities
├── alembic/                 # Migrations
├── tests/                   # Tests
└── requirements.txt
```

## Environment Variables

See `.env.example` in project root.

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

## Development

```bash
# Format code
black app tests

# Lint
ruff app tests

# Type check
mypy app
```
