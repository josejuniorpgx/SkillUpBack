# Leadership Feedback Survey API

API for collecting anonymous leadership feedback. Allows managers to create 3-question surveys with 1-5 scale ratings for their teams.

## 🚀 Tech Stack

- **FastAPI** + SQLAlchemy + Alembic
- **SQLite** (database)
- **Poetry** (dependency management)

## 🛠️ Quick Setup

### 1. Install Poetry
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. Setup Project
```bash
# Clone and install
git clone <repo-url>
cd skillupback
poetry install
poetry shell

# Setup environment variables
cp .env.example .env

# Create required files
touch app/__init__.py app/database/__init__.py app/core/__init__.py
mkdir -p scripts && touch scripts/__init__.py
```

### 3. Setup Database
```bash
# Create and apply migrations
poetry run alembic revision --autogenerate -m "Initial migration"
poetry run alembic upgrade head

# Insert predefined questions
poetry run python scripts/seed_data.py
```

### 4. Run Server
```bash
poetry run uvicorn app.main:app --reload --port 8000
```

## 📖 Documentation

- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔗 Key Endpoints

- `POST /api/v1/surveys` - Create survey
- `GET /api/v1/survey/{token}` - Get survey by token
- `POST /api/v1/survey/{token}/response` - Submit responses
- `GET /api/v1/surveys/{id}/analytics` - Get results

## 📋 Predefined Questions

1. How effectively does your manager communicate expectations?
2. How well does your manager support your professional development?
3. How would you rate your manager's overall leadership effectiveness?

## 🗄️ Database Commands

```bash
# Reset database (⚠️ deletes all data)
poetry run python scripts/init_db.py reset

# Seed only
poetry run python scripts/init_db.py seed
```