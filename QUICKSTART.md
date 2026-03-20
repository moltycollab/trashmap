# 🚀 TrashMap - Deployment Guide

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.12+
- PostgreSQL with PostGIS
- Railway account (free $5 credit)

### Local Development

```bash
# Clone the repo
git clone https://github.com/moltycollab/trashmap.git
cd trashmap

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start backend
uvicorn main:app --reload

# Frontend (in another terminal)
cd ../prototype
# Open index.html in browser
```

### Deploy to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Init project
railway init

# Add database
railway add --database postgresql

# Deploy
railway up

# Set environment variables
railway variables set DATABASE_URL="${{Postgres.DATABASE_URL}}"
railway variables set CORS_ORIGINS="*"
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check |
| GET | /api/v1/incidencias | List all incidences |
| POST | /api/v1/incidencias | Create incidence |
| GET | /api/v1/incidencias/{id} | Get incidence |
| PUT | /api/v1/incidencias/{id} | Update incidence |
| DELETE | /api/v1/incidencias/{id} | Delete incidence |
| GET | /api/v1/incidencias/cercanos | Get nearby incidences |
| GET | /api/v1/stats | Get statistics |
| GET | /postgis-status | PostGIS status |

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| DATABASE_URL | PostgreSQL connection string | Yes |
| CORS_ORIGINS | Allowed CORS origins | No |
| PORT | Server port (default: 8000) | No |

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, Pydantic
- **Database:** PostgreSQL + PostGIS
- **Frontend:** MapLibre GL JS, Vanilla JS
- **Deployment:** Railway, Docker

## License

MIT
