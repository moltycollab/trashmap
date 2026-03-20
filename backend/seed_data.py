"""
Seed data para TrashMap - Datos de ejemplo para Venezuela
Ejecutar: python seed_data.py
"""

import os
import uuid
from datetime import datetime, timedelta
import random

# Intentar importar sqlalchemy
try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from database.models import Report, Base, init_db
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    print("⚠️  SQLAlchemy no instalado. Usando modo JSON.")

# ============================================================================
# DATOS DE EJEMPLO - VENEZUELA
# ============================================================================

VENEZUELA_LOCATIONS = [
    # Caracas
    {"lat": 10.4806, "lon": -66.9036, "city": "Caracas", "zone": "Parque Central"},
    {"lat": 10.5000, "lon": -66.9167, "city": "Caracas", "zone": "Chacao"},
    {"lat": 10.4667, "lon": -66.8833, "city": "Caracas", "zone": "La Candelaria"},
    {"lat": 10.5167, "lon": -66.9333, "city": "Caracas", "zone": "Altamira"},
    {"lat": 10.4500, "lon": -66.8500, "city": "Caracas", "zone": "Petare"},
    {"lat": 10.5333, "lon": -66.9500, "city": "Caracas", "zone": "Los Palos Grandes"},
    {"lat": 10.4333, "lon": -66.9000, "city": "Caracas", "zone": "El Valle"},
    {"lat": 10.4833, "lon": -66.9667, "city": "Caracas", "zone": "La Florida"},
    {"lat": 10.4667, "lon": -66.9500, "city": "Caracas", "zone": "Las Mercedes"},
    {"lat": 10.5000, "lon": -66.8667, "city": "Caracas", "zone": "San Agustín"},
    # Valencia
    {"lat": 10.1621, "lon": -68.0078, "city": "Valencia", "zone": "Centro"},
    {"lat": 10.1833, "lon": -68.0167, "city": "Valencia", "zone": "San Diego"},
    {"lat": 10.1500, "lon": -67.9833, "city": "Valencia", "zone": "Naguanagua"},
    # Maracaibo
    {"lat": 10.6427, "lon": -71.6125, "city": "Maracaibo", "zone": "Centro"},
    {"lat": 10.6667, "lon": -71.6000, "city": "Maracaibo", "zone": "Bella Vista"},
    {"lat": 10.6167, "lon": -71.6333, "city": "Maracaibo", "zone": "Las Delicias"},
    # Barquisimeto
    {"lat": 10.0647, "lon": -69.3301, "city": "Barquisimeto", "zone": "Centro"},
    {"lat": 10.0833, "lon": -69.3167, "city": "Barquisimeto", "zone": "Cabudare"},
    # Mérida
    {"lat": 8.5897, "lon": -71.1561, "city": "Mérida", "zone": "Centro"},
    {"lat": 8.6000, "lon": -71.1333, "city": "Mérida", "zone": "Tabay"},
]

WASTE_TYPES = ["plastico", "organico", "electronico", "construccion", "mixto"]
SIZES = ["small", "medium", "large", "huge"]
STATUSES = ["active", "active", "active", "active", "cleaned", "verified"]  # Más activos

NOTES_BY_TYPE = {
    "plastico": [
        "Acumulación de botellas PET y bolsas plásticas cerca de la acera",
        "Botellas plásticas y envases de comida en zona de quioscos",
        "Bolsas plásticas dispersas en área de mercado",
        "Envases de plástico junto a contenedor desbordado",
        "Microplásticos visibles en cauce de agua cercano",
    ],
    "organico": [
        "Restos de comida y cáscaras junto a mercado informal",
        "Vegetación podada sin recolectar en parque",
        "Residuos orgánicos en bolsas rotas",
        "Comida vencida en área de bodegones",
        "Restos de frutas junto a frutería",
    ],
    "electronico": [
        "Monitores CRT y CPUs abandonados en esquina",
        "Electrodomésticos averiados junto a acera",
        "Cables y componentes electrónicos en lote baldío",
        "Celulares y tablets rotos en basurero ilegal",
        "Baterías y cargadores desechados sin tratamiento",
    ],
    "construccion": [
        "Escombros de demolición sin retirar por 2 semanas",
        "Material de construcción sobrante en acera",
        "Cemento y ladrillos en vía pública",
        "Metales y madera de obra abandonados",
        "Trozos de tubería y cables de construcción",
    ],
    "mixto": [
        "Basura variada acumulada en esquina - necesita atención urgente",
        "Mezcla de residuos domésticos e industriales",
        "Contenedor desbordado con todo tipo de residuos",
        "Basurero informal en lote baldío - difícil acceso",
        "Acumulación diversa junto a parada de autobús",
    ],
}

REPORTER_IDS = [
    "agent-cleanup-crew",
    "agent-eco-warrior",
    "agent-venezuela-green",
    "agent-community-hub",
    "agent-city-watch",
    "agent-nature-guard",
    "agent-recycle-hero",
    "agent-earth-ally",
]


def generate_reports(count=50):
    """Generar reportes de ejemplo"""
    reports = []
    
    for i in range(count):
        loc = random.choice(VENEZUELA_LOCATIONS)
        waste_type = random.choice(WASTE_TYPES)
        size = random.choice(SIZES)
        status = random.choice(STATUSES)
        
        # Offset pequeño para no superponer
        lat_offset = random.uniform(-0.01, 0.01)
        lon_offset = random.uniform(-0.01, 0.01)
        
        # Fecha aleatoria en los últimos 30 días
        days_ago = random.randint(0, 30)
        created = datetime.utcnow() - timedelta(days=days_ago, hours=random.randint(0, 23))
        
        notes = random.choice(NOTES_BY_TYPE[waste_type])
        # Agregar info de ciudad
        notes = f"[{loc['city']} - {loc['zone']}] {notes}"
        
        report = {
            "id": str(uuid.uuid4()),
            "latitude": round(loc["lat"] + lat_offset, 8),
            "longitude": round(loc["lon"] + lon_offset, 8),
            "waste_type": waste_type,
            "size": size,
            "notes": notes,
            "status": status,
            "reporter_id": random.choice(REPORTER_IDS),
            "created_at": created,
            "updated_at": created,
            "verified_by": "agent-verifier" if status == "verified" else None,
            "cleaned_at": created + timedelta(days=1) if status == "cleaned" else None,
        }
        
        reports.append(report)
    
    return reports


def seed_database():
    """Insertar datos en PostgreSQL"""
    if not DB_AVAILABLE:
        print("❌ SQLAlchemy no disponible")
        return False
    
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://trashmap:trashmap@localhost:5432/trashmap"
    )
    
    try:
        engine = create_engine(DATABASE_URL)
        init_db()
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Limpiar datos existentes
        session.query(Report).delete()
        session.commit()
        
        # Generar e insertar reportes
        reports = generate_reports(50)
        
        for r in reports:
            report = Report(
                id=uuid.UUID(r["id"]),
                latitude=r["latitude"],
                longitude=r["longitude"],
                waste_type=r["waste_type"],
                size=r["size"],
                notes=r["notes"],
                status=r["status"],
                reporter_id=r["reporter_id"],
                verified_by=r["verified_by"],
                created_at=r["created_at"],
                updated_at=r["updated_at"],
                cleaned_at=r["cleaned_at"],
            )
            session.add(report)
        
        session.commit()
        print(f"✅ {len(reports)} reportes insertados en la base de datos")
        
        # Estadísticas
        for wt in WASTE_TYPES:
            count = session.query(Report).filter_by(waste_type=wt).count()
            print(f"   • {wt}: {count} reportes")
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        return False


def seed_json():
    """Generar archivo JSON para modo sin base de datos"""
    import json
    
    reports = generate_reports(50)
    
    # Convertir datetime a string
    for r in reports:
        r["created_at"] = r["created_at"].isoformat()
        r["updated_at"] = r["updated_at"].isoformat()
        if r["cleaned_at"]:
            r["cleaned_at"] = r["cleaned_at"].isoformat()
    
    output_file = os.path.join(os.path.dirname(__file__), "seed_data.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(reports, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {len(reports)} reportes generados en {output_file}")
    return True


if __name__ == "__main__":
    print("🗑️  TrashMap - Generador de datos de ejemplo")
    print("=" * 50)
    
    # Intentar DB primero, fallback a JSON
    if not seed_database():
        print("\n📄 Generando archivo JSON como alternativa...")
        seed_json()
    
    print("\n🚀 Listo para visualizar en TrashMap!")
