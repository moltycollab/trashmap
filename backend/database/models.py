from sqlalchemy import create_engine, Column, String, DateTime, Text, Numeric, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from geoalchemy2 import Geography
import os
from datetime import datetime
from typing import Optional

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://trashmap:trashmap@localhost:5432/trashmap"
)

# Create engine
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Report(Base):
    """Modelo SQLAlchemy para reportes de basurales"""
    __tablename__ = "reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    
    # Coordenadas
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    location = Column(Geography(geometry_type='POINT', srid=4326), nullable=False)
    
    # Detalles del reporte
    waste_type = Column(String(20), nullable=False, index=True)
    size = Column(String(10), nullable=False)
    notes = Column(Text, nullable=True)
    
    # Estado
    status = Column(String(20), default='active', nullable=False, index=True)
    
    # Metadata
    reporter_id = Column(String(100), nullable=False, index=True)
    verified_by = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    cleaned_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Report(id={self.id}, type={self.waste_type}, status={self.status})>"
    
    def to_dict(self):
        """Convertir a diccionario para respuesta API"""
        return {
            "id": str(self.id),
            "latitude": float(self.latitude),
            "longitude": float(self.longitude),
            "waste_type": self.waste_type,
            "size": self.size,
            "notes": self.notes,
            "status": self.status,
            "reporter_id": self.reporter_id,
            "verified_by": self.verified_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "cleaned_at": self.cleaned_at.isoformat() if self.cleaned_at else None
        }

# Índice adicional para búsqueda geográfica
Index('idx_reports_location', Report.location, postgresql_using='GIST')

def get_db():
    """Dependency para obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Inicializar base de datos (crear tablas)"""
    Base.metadata.create_all(bind=engine)

def search_reports_in_area_db(
    db,
    lat: float,
    lon: float,
    radius_km: float,
    waste_type: Optional[str] = None
):
    """
    Buscar reportes dentro de un área usando PostGIS.
    Más eficiente que la implementación en memoria (usa índices espaciales).
    """
    from sqlalchemy import text
    
    query = """
        SELECT 
            id,
            latitude,
            longitude,
            waste_type,
            size,
            notes,
            status,
            reporter_id,
            created_at,
            ST_Distance(
                location::geometry,
                ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geometry
            ) as distance_meters
        FROM reports
        WHERE ST_DWithin(
            location::geometry,
            ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geometry,
            :radius_meters
        )
        AND status != 'cleaned'
    """
    
    params = {
        "lat": lat,
        "lon": lon,
        "radius_meters": radius_km * 1000
    }
    
    if waste_type:
        query += " AND waste_type = :waste_type"
        params["waste_type"] = waste_type
    
    query += " ORDER BY distance_meters"
    
    result = db.execute(text(query), params)
    
    reports = []
    for row in result:
        reports.append({
            "id": str(row.id),
            "latitude": float(row.latitude),
            "longitude": float(row.longitude),
            "waste_type": row.waste_type,
            "size": row.size,
            "notes": row.notes,
            "status": row.status,
            "reporter_id": row.reporter_id,
            "created_at": row.created_at.isoformat() if row.created_at else None,
            "distance_meters": float(row.distance_meters)
        })
    
    return reports

if __name__ == "__main__":
    # Crear tablas si no existen
    init_db()
    print("✅ Base de datos inicializada correctamente")
