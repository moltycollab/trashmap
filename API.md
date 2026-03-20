# TrashMap API Documentation

## Base URL
```
Production: https://trashmap-api.railway.app
Local: http://localhost:8000
```

## Authentication
Currently open. Add auth in future versions.

## Endpoints

### Health Check

**GET** `/health`

Check if API is running.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-03-19T12:00:00Z"
}
```

### Incidences

#### List All Incidences

**GET** `/api/v1/incidencias`

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| skip | int | Number to skip (pagination) |
| limit | int | Limit results |
| tipo | string | Filter by type (plastico, papel, metal, organico, vidrio) |

**Response:**
```json
{
  "total": 50,
  "incidencias": [
    {
      "id": 1,
      "latitud": 10.4806,
      "longitud": -66.9036,
      "tipo_basura": "plastico",
      "cantidad": "alta",
      "descripcion": "Basural en calle principal",
      "fecha_reporte": "2026-03-19T10:00:00Z"
    }
  ]
}
```

#### Create Incidence

**POST** `/api/v1/incidencias`

**Body:**
```json
{
  "latitud": 10.4806,
  "longitud": -66.9036,
  "tipo_basura": "plastico",
  "cantidad": "media",
  "descripcion": "Reporte de ejemplo"
}
```

**Response:**
```json
{
  "id": 51,
  "latitud": 10.4806,
  "longitud": -66.9036,
  "tipo_basura": "plastico",
  "cantidad": "media",
  "descripcion": "Reporte de ejemplo",
  "fecha_reporte": "2026-03-19T16:00:00Z"
}
```

#### Get Incidence by ID

**GET** `/api/v1/incidencias/{id}`

**Response:**
```json
{
  "id": 1,
  "latitud": 10.4806,
  "longitud": -66.9036,
  "tipo_basura": "plastico",
  "cantidad": "alta",
  "descripcion": "Basural en calle principal",
  "fecha_reporte": "2026-03-19T10:00:00Z"
}
```

#### Update Incidence

**PUT** `/api/v1/incidencias/{id}`

**Body:**
```json
{
  "descripcion": "Nueva descripción",
  "cantidad": "baja"
}
```

#### Delete Incidence

**DELETE** `/api/v1/incidencias/{id}`

**Response:**
```json
{
  "message": "Incidence deleted successfully"
}
```

#### Get Nearby Incidences

**GET** `/api/v1/incidencias/cercanos`

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| lat | float | Latitude |
| lon | float | Longitude |
| radio_km | float | Radius in kilometers (default: 5) |

**Response:**
```json
{
  "total": 10,
  "incidencias": [...]
}
```

### Statistics

#### Get Stats

**GET** `/api/v1/stats`

**Response:**
```json
{
  "total_incidencias": 50,
  "por_tipo": {
    "plastico": 25,
    "papel": 10,
    "metal": 5,
    "organico": 8,
    "vidrio": 2
  },
  "por_cantidad": {
    "alta": 15,
    "media": 20,
    "baja": 15
  }
}
```

### Database

#### PostGIS Status

**GET** `/postgis-status`

**Response:**
```json
{
  "postgis_version": "3.4.0",
  "status": "connected"
}
```

## Error Responses

**400 Bad Request**
```json
{
  "detail": "Invalid request parameters"
}
```

**404 Not Found**
```json
{
  "detail": "Incidence not found"
}
```

**500 Internal Server Error**
```json
{
  "detail": "Internal server error"
}
```

---

## Example: Using cURL

```bash
# Health check
curl https://trashmap-api.railway.app/health

# List incidences
curl https://trashmap-api.railway.app/api/v1/incidencias

# Create incidence
curl -X POST https://trashmap-api.railway.app/api/v1/incidencias \
  -H "Content-Type: application/json" \
  -d '{
    "latitud": 10.4806,
    "longitud": -66.9036,
    "tipo_basura": "plastico",
    "cantidad": "media",
    "descripcion": "Test reporte"
  }'

# Get nearby
curl "https://trashmap-api.railway.app/api/v1/incidencias/cercanos?lat=10.4806&lon=-66.9036&radio_km=5"
```
