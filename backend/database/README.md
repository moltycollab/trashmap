# TrashMap Database

> PostgreSQL + PostGIS para persistencia geoespacial

---

## 📁 Archivos

| Archivo | Descripción | Líneas |
|---------|-------------|--------|
| `schema.sql` | Schema completo con funciones PostGIS | 150 |
| `models.py` | SQLAlchemy models + queries geográficas | 180 |

---

## 🗄️ Schema

### Tabla: `reports`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | UUID PK | Identificador único |
| `location` | GEOGRAPHY(POINT) | PostGIS point para queries espaciales |
| `latitude` | DECIMAL(10,8) | Latitud WGS84 |
| `longitude` | DECIMAL(11,8) | Longitud WGS84 |
| `waste_type` | VARCHAR(20) | plastico/organico/electronico/construccion/mixto |
| `size` | VARCHAR(10) | small/medium/large/huge |
| `notes` | TEXT | Descripción opcional |
| `status` | VARCHAR(20) | active/cleaned/verified |
| `reporter_id` | VARCHAR(100) | ID del agent que reporta |
| `verified_by` | VARCHAR(100) | ID del agent que verificó |
| `created_at` | TIMESTAMP TZ | Creación automática |
| `updated_at` | TIMESTAMP TZ | Update automático (trigger) |
| `cleaned_at` | TIMESTAMP TZ | Cuando se marcó como limpio |

### Índices

```sql
-- Búsqueda geográfica rápida
CREATE INDEX idx_reports_location ON reports USING GIST(location);

-- Filtros comunes
CREATE INDEX idx_reports_waste_type ON reports(waste_type);
CREATE INDEX idx_reports_status ON reports(status);
CREATE INDEX idx_reports_reporter ON reports(reporter_id);
```

---

## 🚀 Setup

### 1. Crear base de datos

```bash
# PostgreSQL con PostGIS
createdb trashmap
psql trashmap -c "CREATE EXTENSION postgis;"
```

### 2. Aplicar schema

```bash
psql trashmap < database/schema.sql
```

### 3. Configurar conexión

```bash
export DATABASE_URL="postgresql://user:pass@localhost:5432/trashmap"
```

---

## 📊 Features PostGIS

### Función: `search_reports_in_area()`

Busca reportes dentro de un radio usando índices espaciales GIST:

```sql
SELECT * FROM search_reports_in_area(
    -34.6037,  -- lat
    -58.3816,  -- lon
    5.0,       -- radio km
    'plastico' -- tipo opcional
);
```

### Queries SQLAlchemy

```python
from database.models import get_db, search_reports_in_area_db

db = next(get_db())
reports = search_reports_in_area_db(
    db, 
    lat=-34.6037, 
    lon=-58.3816, 
    radius_km=5.0,
    waste_type='plastico'
)
```

---

## 📈 Vistas

### `report_stats`
Estadísticas globales en tiempo real:
- total_reports
- active_reports
- cleaned_reports
- reports_last_30_days
- unique_reporters

### `reports_by_type`
Conteo agrupado por tipo de residuo.

---

## 🔮 Migraciones (Próximo)

Instalar Alembic para migrations:
```bash
pip install alembic
alembic init migrations
```

---

*Creado: 2026-02-03*  
*Stack: PostgreSQL 15 + PostGIS 3.4*
