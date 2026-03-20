# TrashMap - Architecture

## Overview

TrashMap is a full-stack application for mapping and reporting illegal dumping sites. It enables communities to report, track, and visualize waste accumulation areas for collective action.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│                   (MapLibre GL JS)                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  Map View   │  │  Report    │  │  Statistics         │ │
│  │  - Markers  │  │  Form      │  │  - Charts           │ │
│  │  - Clusters │  │  - Upload  │  │  - Filters         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        BACKEND                              │
│                   (FastAPI + Uvicorn)                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   API Routes                        │   │
│  │  /health, /api/v1/incidencias, /api/v1/stats      │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐   │
│  │  Schemas    │  │  Services    │  │  Database     │   │
│  │  (Pydantic)│  │  (Business   │  │  (SQLAlchemy │   │
│  │             │  │   Logic)     │  │   + PostGIS) │   │
│  └──────────────┘  └──────────────┘  └───────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ SQL
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATABASE                                │
│                  (PostgreSQL + PostGIS)                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   Tables                             │   │
│  │  - incidencias (id, lat, lon, tipo, cantidad,       │   │
│  │                descripcion, fecha_reporte)          │   │
│  │  - tipo_basura (enum: plastico, papel, metal,      │   │
│  │                   organico, vidrio)                 │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Components

### Frontend (prototype/)
- **Technology:** MapLibre GL JS, Vanilla JavaScript, HTML, CSS
- **Purpose:** Interactive map with marker visualization
- **Features:**
  - Display incidence markers on map
  - Cluster markers for performance
  - Click marker to see details
  - Filter by waste type

### Backend (backend/)
- **Technology:** FastAPI, Uvicorn, SQLAlchemy, Pydantic
- **Purpose:** REST API for data management
- **Features:**
  - CRUD operations for incidences
  - Spatial queries (nearby incidences)
  - Statistics aggregation
  - Health check endpoints

### Database
- **Technology:** PostgreSQL + PostGIS
- **Purpose:** Spatial data storage
- **Schema:**
  ```sql
  CREATE TABLE incidencias (
      id SERIAL PRIMARY KEY,
      latitud FLOAT NOT NULL,
      longitud FLOAT NOT NULL,
      tipo_basura VARCHAR(50) NOT NULL,
      cantidad VARCHAR(20) NOT NULL,
      descripcion TEXT,
      fecha_reporte TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      GEOMETRY(POINT, 4326)
  );
  ```

## Deployment

### Development
```bash
# Local
docker-compose up -d

# Backend only
cd backend
uvicorn main:app --reload
```

### Production
- **Platform:** Railway
- **Database:** Railway PostgreSQL with PostGIS
- **Backend:** Docker container
- **Frontend:** GitHub Pages or Railway static

## Data Flow

1. **User reports incidence**
   - Frontend → POST /api/v1/incidencias
   - Backend validates → Stores in DB
   - Backend returns success

2. **User views map**
   - Frontend → GET /api/v1/incidencias
   - Backend queries DB → Returns list
   - Frontend renders markers

3. **User searches nearby**
   - Frontend → GET /api/v1/incidencias/cercanos?lat=X&lon=Y&radio=Z
   - Backend performs spatial query
   - Returns filtered results

## Security

- Input validation via Pydantic schemas
- SQL injection prevention via SQLAlchemy ORM
- CORS configuration for frontend access
- Environment variables for secrets

## Scalability

- **Horizontal:** Load balancer + multiple backend instances
- **Vertical:** Upgrade Railway plan for more resources
- **Database:** Add read replicas for heavy queries
- **Caching:** Redis for frequent queries (future)

## Future Enhancements

- User authentication (OAuth)
- Image uploads for incidences
- Real-time updates (WebSocket)
- Mobile app
- AI classification of waste type
- Community voting/prioritization
- Integration with municipal services
