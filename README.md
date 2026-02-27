# FastAPI DDD Demo

Production-ready FastAPI backend following **Domain-Driven Design** principles with fully asynchronous request handling.

## Architecture

```
src/app/
├── api/                    # Presentation layer
│   ├── dependencies.py     # FastAPI dependency injection
│   ├── router.py           # Central router aggregator
│   ├── schemas.py          # Pydantic request/response schemas
│   └── v1/
│       ├── health.py       # Health, readiness, liveness probes
│       └── users.py        # User resource endpoints
├── application/            # Use-case / service layer
│   └── user_service.py     # Orchestrates user business operations
├── core/                   # Cross-cutting concerns
│   ├── config.py           # Environment-based settings (Pydantic)
│   ├── exceptions.py       # Custom exceptions & global handlers
│   ├── logging.py          # Structured logging (structlog)
│   ├── middleware.py        # Request logging, CORS
│   └── security.py         # Hashing, JWT helpers
├── db/                     # Database engine & session
│   ├── base.py             # SQLAlchemy declarative base
│   └── session.py          # Async engine + session factory
├── domain/                 # Domain layer (pure business logic)
│   ├── base.py             # Base entity
│   ├── uow.py              # Abstract Unit of Work
│   └── user/
│       ├── entity.py       # User aggregate root
│       └── repository.py   # Abstract repository interface
└── infrastructure/         # Adapters / implementations
    ├── persistence/
    │   ├── user_model.py   # SQLAlchemy ORM model
    │   └── user_repository.py  # Repository implementation
    └── uow.py              # SQLAlchemy Unit of Work
```

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 16+
- Docker & Docker Compose (optional)

### Running with Docker

```bash
cp .env.example .env
docker compose up --build
```

The API will be available at `http://localhost:8000`.

### Running locally

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -e ".[dev]"

# Set up the database
cp .env.example .env
# Edit .env with your local PostgreSQL credentials
alembic upgrade head

# Run the server
uvicorn app.main:app --reload --app-dir src
```

### Running tests

```bash
pytest --cov=app tests/
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/health` | Liveness probe |
| `GET` | `/api/v1/ready` | Readiness probe (DB check) |
| `GET` | `/api/v1/users` | List users (paginated, filterable) |
| `GET` | `/api/v1/users/{id}` | Get user by ID |
| `POST` | `/api/v1/users` | Create user |
| `PATCH` | `/api/v1/users/{id}` | Update user |
| `POST` | `/api/v1/users/{id}/deactivate` | Deactivate user |
| `DELETE` | `/api/v1/users/{id}` | Delete user |

## Database Migrations

```bash
# Generate a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1
```

## Design Principles

- **DDD**: Domain entities encapsulate business rules; infrastructure is an adapter
- **Repository Pattern**: Abstract interfaces in domain, concrete implementations in infrastructure
- **Unit of Work**: Transactional consistency across aggregates
- **Dependency Injection**: Wired via FastAPI's `Depends()` for testability
- **SOLID**: Single responsibility per layer, open for extension, programming to interfaces
- **Clean Architecture**: Dependencies point inward — domain has zero external imports

## Environment Configuration

All settings are loaded from environment variables (with `.env` fallback). See `.env.example` for the full list.
