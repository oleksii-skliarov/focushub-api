# FocusHub API

A RESTful task management backend service built with **FastAPI**, **SQLAlchemy 2.0**, and **JWT authentication**. Designed with clean layered architecture, automated test isolation via **Pytest**, and **Docker** containerization.

## Tech Stack

- **Language:** Python 3.12
- **Framework:** FastAPI, Uvicorn
- **Database & ORM:** SQLite, SQLAlchemy 2.0, Alembic
- **Validation & Settings:** Pydantic v2, `pydantic-settings`
- **Security:** OAuth2 Password Flow with JWT (`python-jose`), password hashing with `passlib[bcrypt]`
- **Testing:** Pytest, FastAPI `TestClient`
- **Containerization:** Docker

## Project Structure

```text
├── alembic/            # Database migrations
├── tests/              # Automated test suite with isolated DB fixtures
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_tasks.py
├── auth.py             # JWT token creation and user dependency validation
├── config.py           # Environment configuration via Pydantic BaseSettings
├── crud.py             # Database CRUD operations
├── database.py         # SQLAlchemy engine and session management
├── main.py             # FastAPI application and API route definitions
├── models.py           # SQLAlchemy ORM models (UserDB, TaskDB)
├── schemas.py          # Pydantic request/response schemas
├── Dockerfile          # Production container image configuration
├── .dockerignore
├── .env.example        # Environment variables template
└── requirements.txt
```

## Getting Started

### 1. Clone the repository

```bash
git clone [https://github.com/oleksii-skliarov/focushub-api.git](https://github.com/oleksii-skliarov/focushub-api.git)
cd focushub-api
```

### 2. Run Locally

Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux / macOS:
source .venv/bin/activate
```

Install dependencies and configure environment variables:

```bash
pip install -r requirements.txt
cp .env.example .env
```

Start the development server:

```bash
uvicorn main:app --reload
```

### 3. Run with Docker

Build and run the container without setting up a local Python environment:

```bash
docker build -t focushub-api .
docker run -d -p 8000:8000 --name focushub-container focushub-api
```

Once running, interactive API documentation (Swagger UI) is available at:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## Running Tests

The test suite uses isolated per-function SQLite database sessions via Pytest fixtures and FastAPI dependency overrides:

```bash
pytest -v
```

## API Endpoints

### Authentication & Users
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/users` | Register a new user | No |
| `POST` | `/token` | Obtain JWT access token (OAuth2 form) | No |
| `GET` | `/users/me` | Get current authenticated user profile | Yes |
| `GET` | `/users` | List all registered users | Yes |

### Tasks
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/tasks` | List tasks for current user (supports `limit`, `offset`, `completed`) | Yes |
| `GET` | `/tasks/{task_id}` | Get a specific task by ID | Yes |
| `POST` | `/tasks` | Create a new task | Yes |
| `PATCH` | `/tasks/{task_id}` | Update task title or completion status | Yes |
| `DELETE` | `/tasks/{task_id}` | Delete a task | Yes |