# TrashMap Backend

> API REST para TrashMap - Reporte y consulta de basurales informales

**Tecnología:** FastAPI + Python 3.12  
**Estado:** ✅ MVP funcional (datos en memoria)  
**Próximo paso:** PostgreSQL + PostGIS

---

## 🚀 Quick Start

### Instalación

```bash
cd projects/trashmap/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install fastapi uvicorn pydantic
```

### Ejecutar

```bash
# Desarrollo con auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Producción
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Documentación Interactiva

Una vez corriendo:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📡 Endpoints

### Health & Info
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Info de la API |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger UI |

### Reportes
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/reports` | Crear reporte |
| GET | `/api/v1/reports` | Listar reportes |
| GET | `/api/v1/reports/{id}` | Obtener reporte |
| PATCH | `/api/v1/reports/{id}` | Actualizar reporte |
| DELETE | `/api/v1/reports/{id}` | Eliminar reporte |
| GET | `/api/v1/reports/area/search` | Buscar en área |
| POST | `/api/v1/reports/{id}/verify` | Verificar reporte |

### Estadísticas
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/stats` | Estadísticas globales |

---

## 📋 Ejemplos de Uso

### Crear Reporte

```bash
curl -X POST "http://localhost:8000/api/v1/reports" \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": -34.6037,
    "longitude": -58.3816,
    "waste_type": "plastico",
    "size": "large",
    "notes": "Acumulación cerca del río",
    "reporter_id": "agent-nautilus"
  }'
```

### Listar Reportes

```bash
# Todos
curl "http://localhost:8000/api/v1/reports"

# Filtrados por tipo
curl "http://localhost:8000/api/v1/reports?waste_type=plastico"

# Paginados
curl "http://localhost:8000/api/v1/reports?limit=10&offset=0"
```

### Buscar en Área

```bash
# Buscar en radio de 5km desde Buenos Aires
curl "http://localhost:8000/api/v1/reports/area/search?lat=-34.6037&lon=-58.3816&radius_km=5"
```

### Estadísticas

```bash
curl "http://localhost:8000/api/v1/stats"
```

---

## 🗄️ Modelo de Datos

### Reporte

```json
{
  "id": "uuid",
  "latitude": -34.6037,
  "longitude": -58.3816,
  "waste_type": "plastico|organico|electronico|construccion|mixto",
  "size": "small|medium|large|huge",
  "notes": "string (opcional)",
  "status": "active|cleaned|verified",
  "reporter_id": "string",
  "created_at": "2026-02-02T12:00:00",
  "updated_at": "2026-02-02T12:00:00",
  "verified_by": "string|null",
  "cleaned_at": "datetime|null"
}
```

---

## 🔮 Roadmap Backend

### v1.1 (Próximo)
- [ ] PostgreSQL + PostGIS
- [ ] Migraciones con Alembic
- [ ] Autenticación JWT
- [ ] Rate limiting

### v1.2
- [ ] Upload de fotos (S3/MinIO)
- [ ] Notificaciones realtime (WebSockets)
- [ ] Cache con Redis
- [ ] Tests automatizados

### v1.3
- [ ] Exportar GeoJSON/KML
- [ ] Integración OpenStreetMap
- [ ] Dashboard admin

---

## 🔒 Seguridad

- CORS configurado para desarrollo
- Validación de inputs con Pydantic
- Solo creador puede eliminar reporte
- En producción: JWT + HTTPS + Rate limiting

---

*Creado: 2026-02-03*  
*Responsable: Nautilus*
