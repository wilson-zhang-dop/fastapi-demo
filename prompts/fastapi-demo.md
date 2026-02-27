Design a production-ready FastAPI backend project with fully asynchronous request handling, following Domain-Driven Design (DDD) principles.

This project must be enterprise-grade, scalable, and suitable for microservice architecture.

Technical Stack:
- Python 3.11+
- FastAPI
- Async SQLAlchemy 2.0
- PostgreSQL
- Pydantic v2
- Uvicorn
- Alembic (database migrations)
- Dependency Injection
- Structured logging
- Docker
- Pytest (async testing)
- Environment-based configuration (.env)

Architecture Requirements:

1. Follow clean layered architecture with DDD concepts:
   - api (routers / controllers)
   - application (use cases / services)
   - domain (entities, aggregates, business rules)
   - infrastructure (database, external services)
   - repository (interfaces in domain, implementations in infrastructure)
   - db (engine, session management)
   - core (config, logging, security, exceptions, middleware)

2. Implement:
   - Repository Pattern (abstract base repository in domain layer)
   - Unit of Work Pattern
   - Dependency Injection for UoW and repositories
   - Centralized exception handling
   - Custom error response model
   - Logging middleware
   - Health check endpoint
   - Readiness and liveness endpoints

3. Fully async:
   - No blocking calls
   - Async DB session management
   - Proper transaction handling

4. RESTful API principles:
   - Resource-based naming
   - Correct HTTP methods
   - Proper status codes
   - Pagination support
   - Filtering example

Deliverables:

- Recommended project directory structure
- Example User aggregate
- Domain entity
- Repository interface
- SQLAlchemy implementation
- Unit of Work implementation
- Application service (use case layer)
- Router
- Async DB configuration
- Example .env configuration
- Alembic setup example
- Dockerfile
- docker-compose.yml
- Example pytest async test
- README structure overview

The code must follow:
- Clean Code principles
- SOLID principles
- Clear separation of concerns
- Production-ready standards
- Scalable microservice-friendly structure