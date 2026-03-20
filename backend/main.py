from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid
import os

app = FastAPI(
    title="TrashMap API",
    description="API para reporte y consulta de basurales informales",
    version="1.0.0"
)

# CORS para permitir acceso desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# ENUMS Y MODELOS
# ============================================================================

class WasteType(str, Enum):
    PLASTICO = "plastico"
    ORGANICO = "organico"
    ELECTRONICO = "electronico"
    CONSTRUCCION = "construccion"
    MIXTO = "mixto"

class WasteSize(str, Enum):
    SMALL = "small"      # Bolsa
    MEDIUM = "medium"    # Cajón
    LARGE = "large"      # Camioneta
    HUGE = "huge"        # Camión

class ReportStatus(str, Enum):
    ACTIVE = "active"
    CLEANED = "cleaned"
    VERIFIED = "verified"

class ReportCreate(BaseModel):
    """Modelo para crear un nuevo reporte"""
    latitude: float = Field(..., ge=-90, le=90, description="Latitud (-90 a 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Longitud (-180 a 180)")
    waste_type: WasteType = Field(..., description="Tipo de residuo")
    size: WasteSize = Field(..., description="Tamaño aproximado")
    notes: Optional[str] = Field(None, max_length=500, description="Notas adicionales")
    reporter_id: str = Field(..., description="ID del agent que reporta")
    
    class Config:
        json_schema_extra = {
            "example": {
                "latitude": -34.6037,
                "longitude": -58.3816,
                "waste_type": "plastico",
                "size": "large",
                "notes": "Acumulación de botellas plásticas cerca del río",
                "reporter_id": "agent-nautilus"
            }
        }

class ReportResponse(BaseModel):
    """Modelo de respuesta para un reporte"""
    id: str
    latitude: float
    longitude: float
    waste_type: WasteType
    size: WasteSize
    notes: Optional[str]
    status: ReportStatus
    reporter_id: str
    created_at: datetime
    updated_at: datetime
    verified_by: Optional[str] = None
    cleaned_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ReportUpdate(BaseModel):
    """Modelo para actualizar un reporte"""
    waste_type: Optional[WasteType] = None
    size: Optional[WasteSize] = None
    notes: Optional[str] = Field(None, max_length=500)
    status: Optional[ReportStatus] = None

class ReportsInArea(BaseModel):
    """Respuesta para consulta de reportes en área"""
    center_lat: float
    center_lon: float
    radius_km: float
    total_reports: int
    reports: List[ReportResponse]

# ============================================================================
# BASE DE DATOS SIMULADA (en memoria)
# En producción: PostgreSQL + PostGIS
# ============================================================================

reports_db: dict[str, dict] = {}

# ============================================================================
# CARGA DE SEED DATA (modo desarrollo)
# ============================================================================
SEED_DATA_FILE = os.path.join(os.path.dirname(__file__), "seed_data.json")

def load_seed_data():
    """Cargar datos de ejemplo desde seed_data.json si existe"""
    if os.path.exists(SEED_DATA_FILE):
        try:
            import json
            with open(SEED_DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for r in data:
                # Parsear fechas
                r["created_at"] = datetime.fromisoformat(r["created_at"])
                r["updated_at"] = datetime.fromisoformat(r["updated_at"])
                if r.get("cleaned_at"):
                    r["cleaned_at"] = datetime.fromisoformat(r["cleaned_at"])
                reports_db[r["id"]] = r
            print(f"✅ Seed data cargado: {len(data)} reportes")
        except Exception as e:
            print(f"⚠️  Error cargando seed data: {e}")

# Cargar seed data al iniciar
load_seed_data()

# Datos de ejemplo originales (fallback si no hay seed data)
if not reports_db:
    _sample_reports = [
        {
            "id": str(uuid.uuid4()),
            "latitude": -34.6137,
            "longitude": -58.3916,
            "waste_type": "plastico",
            "size": "large",
            "notes": "Acumulación de botellas y bolsas plásticas",
            "status": "active",
            "reporter_id": "agent-demo-1",
            "created_at": datetime(2026, 2, 1, 10, 0, 0),
            "updated_at": datetime(2026, 2, 1, 10, 0, 0),
            "verified_by": None,
            "cleaned_at": None
        },
        {
            "id": str(uuid.uuid4()),
            "latitude": -34.5937,
            "longitude": -58.3716,
            "waste_type": "organico",
            "size": "medium",
            "notes": "Restos de poda acumulados",
            "status": "active",
            "reporter_id": "agent-demo-2",
            "created_at": datetime(2026, 2, 1, 14, 30, 0),
            "updated_at": datetime(2026, 2, 1, 14, 30, 0),
            "verified_by": None,
            "cleaned_at": None
        },
        {
            "id": str(uuid.uuid4()),
            "latitude": -34.6237,
            "longitude": -58.4016,
            "waste_type": "electronico",
            "size": "small",
            "notes": "Viejos monitores y CPUs abandonados",
            "status": "active",
            "reporter_id": "agent-demo-3",
            "created_at": datetime(2026, 1, 31, 9, 0, 0),
            "updated_at": datetime(2026, 1, 31, 9, 0, 0),
            "verified_by": None,
            "cleaned_at": None
        }
    ]

    for r in _sample_reports:
        reports_db[r["id"]] = r

# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "name": "TrashMap API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "docs": "/docs",
            "reports": "/api/v1/reports",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check para monitoreo"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "reports_count": len(reports_db)
    }

@app.post("/api/v1/reports", response_model=ReportResponse, status_code=201)
async def create_report(report: ReportCreate):
    """
    Crear un nuevo reporte de basural.
    
    - **latitude**: Latitud en grados decimales (-90 a 90)
    - **longitude**: Longitud en grados decimales (-180 a 180)
    - **waste_type**: Tipo de residuo (plastico, organico, electronico, construccion, mixto)
    - **size**: Tamaño aproximado (small, medium, large, huge)
    - **notes**: Descripción opcional (máx 500 caracteres)
    - **reporter_id**: Identificador del agent que reporta
    """
    report_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    new_report = {
        "id": report_id,
        "latitude": report.latitude,
        "longitude": report.longitude,
        "waste_type": report.waste_type.value,
        "size": report.size.value,
        "notes": report.notes,
        "status": "active",
        "reporter_id": report.reporter_id,
        "created_at": now,
        "updated_at": now,
        "verified_by": None,
        "cleaned_at": None
    }
    
    reports_db[report_id] = new_report
    
    return ReportResponse(**new_report)

@app.get("/api/v1/reports", response_model=List[ReportResponse])
async def list_reports(
    waste_type: Optional[WasteType] = Query(None, description="Filtrar por tipo de residuo"),
    status: Optional[ReportStatus] = Query(None, description="Filtrar por estado"),
    reporter_id: Optional[str] = Query(None, description="Filtrar por reportero"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginación")
):
    """
    Listar reportes con filtros opcionales.
    """
    results = list(reports_db.values())
    
    if waste_type:
        results = [r for r in results if r["waste_type"] == waste_type.value]
    
    if status:
        results = [r for r in results if r["status"] == status.value]
    
    if reporter_id:
        results = [r for r in results if r["reporter_id"] == reporter_id]
    
    # Ordenar por fecha de creación (más reciente primero)
    results.sort(key=lambda x: x["created_at"], reverse=True)
    
    # Paginación
    total = len(results)
    results = results[offset:offset + limit]
    
    return [ReportResponse(**r) for r in results]

@app.get("/api/v1/reports/{report_id}", response_model=ReportResponse)
async def get_report(report_id: str):
    """
    Obtener un reporte específico por ID.
    """
    if report_id not in reports_db:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    
    return ReportResponse(**reports_db[report_id])

@app.get("/api/v1/reports/area/search", response_model=ReportsInArea)
async def search_reports_in_area(
    lat: float = Query(..., ge=-90, le=90, description="Latitud del centro"),
    lon: float = Query(..., ge=-180, le=180, description="Longitud del centro"),
    radius_km: float = Query(5.0, ge=0.1, le=100, description="Radio en kilómetros"),
    waste_type: Optional[WasteType] = Query(None, description="Filtrar por tipo")
):
    """
    Buscar reportes dentro de un área circular.
    
    Usa la fórmula de Haversine para calcular distancia.
    """
    from math import radians, sin, cos, sqrt, atan2
    
    def haversine_distance(lat1, lon1, lat2, lon2):
        """Calcular distancia en km entre dos puntos"""
        R = 6371  # Radio de la Tierra en km
        
        lat1_rad = radians(lat1)
        lat2_rad = radians(lat2)
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        
        a = sin(dlat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c
    
    results = []
    for report in reports_db.values():
        distance = haversine_distance(lat, lon, report["latitude"], report["longitude"])
        
        if distance <= radius_km:
            if waste_type is None or report["waste_type"] == waste_type.value:
                results.append(report)
    
    # Ordenar por distancia
    results.sort(key=lambda r: haversine_distance(lat, lon, r["latitude"], r["longitude"]))
    
    return ReportsInArea(
        center_lat=lat,
        center_lon=lon,
        radius_km=radius_km,
        total_reports=len(results),
        reports=[ReportResponse(**r) for r in results]
    )

@app.patch("/api/v1/reports/{report_id}", response_model=ReportResponse)
async def update_report(report_id: str, update: ReportUpdate):
    """
    Actualizar un reporte existente.
    """
    if report_id not in reports_db:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    
    report = reports_db[report_id]
    
    if update.waste_type:
        report["waste_type"] = update.waste_type.value
    
    if update.size:
        report["size"] = update.size.value
    
    if update.notes is not None:
        report["notes"] = update.notes
    
    if update.status:
        report["status"] = update.status.value
        if update.status == ReportStatus.CLEANED:
            report["cleaned_at"] = datetime.utcnow()
    
    report["updated_at"] = datetime.utcnow()
    
    return ReportResponse(**report)

@app.post("/api/v1/reports/{report_id}/verify")
async def verify_report(report_id: str, verifier_id: str):
    """
    Marcar un reporte como verificado por otro agent.
    """
    if report_id not in reports_db:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    
    report = reports_db[report_id]
    report["verified_by"] = verifier_id
    report["status"] = "verified"
    report["updated_at"] = datetime.utcnow()
    
    return {"message": "Reporte verificado", "report_id": report_id}

@app.delete("/api/v1/reports/{report_id}")
async def delete_report(report_id: str, reporter_id: str):
    """
    Eliminar un reporte (solo el creador puede eliminarlo).
    """
    if report_id not in reports_db:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    
    report = reports_db[report_id]
    
    if report["reporter_id"] != reporter_id:
        raise HTTPException(status_code=403, detail="Solo el creador puede eliminar el reporte")
    
    del reports_db[report_id]
    
    return {"message": "Reporte eliminado", "report_id": report_id}

# ============================================================================
# ESTADÍSTICAS
# ============================================================================

@app.get("/api/v1/stats")
async def get_stats():
    """
    Obtener estadísticas globales de reportes.
    """
    from collections import Counter
    
    total = len(reports_db)
    by_type = Counter(r["waste_type"] for r in reports_db.values())
    by_status = Counter(r["status"] for r in reports_db.values())
    by_size = Counter(r["size"] for r in reports_db.values())
    
    return {
        "total_reports": total,
        "by_type": dict(by_type),
        "by_status": dict(by_status),
        "by_size": dict(by_size),
        "active_reports": by_status.get("active", 0),
        "cleaned_reports": by_status.get("cleaned", 0),
        "verified_reports": by_status.get("verified", 0)
    }


@app.get("/api/v1/stats/by-city")
async def get_stats_by_city():
    """
    Obtener estadísticas agrupadas por ciudad (extraído de las notas).
    """
    from collections import Counter, defaultdict
    
    city_stats = defaultdict(lambda: {"total": 0, "active": 0, "by_type": Counter()})
    
    for r in reports_db.values():
        notes = r.get("notes", "")
        city = "Sin ciudad"
        if notes.startswith("["):
            end = notes.find("]")
            if end > 0:
                city_part = notes[1:end]
                if " - " in city_part:
                    city = city_part.split(" - ")[0]
                else:
                    city = city_part
        
        city_stats[city]["total"] += 1
        if r["status"] == "active":
            city_stats[city]["active"] += 1
        city_stats[city]["by_type"][r["waste_type"]] += 1
    
    result = {}
    for city, stats in sorted(city_stats.items()):
        result[city] = {
            "total": stats["total"],
            "active": stats["active"],
            "by_type": dict(stats["by_type"])
        }
    
    return {
        "cities_count": len(result),
        "cities": result
    }


@app.post("/api/v1/admin/seed")
async def generate_seed_data(count: int = Query(50, ge=1, le=500)):
    """
    Generar datos de ejemplo para desarrollo.
    """
    from seed_data import generate_reports
    
    reports = generate_reports(count)
    
    for r in reports:
        reports_db[r["id"]] = r
    
    return {
        "message": f"{count} reportes generados",
        "total_in_db": len(reports_db)
    }


# ============================================================================
# PARA DESARROLLO
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
