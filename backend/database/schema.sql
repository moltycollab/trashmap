-- TrashMap Database Schema
-- PostgreSQL + PostGIS

-- Habilitar extensión PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;

-- Tabla de reportes
CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location GEOGRAPHY(POINT, 4326) NOT NULL,  -- PostGIS point
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    waste_type VARCHAR(20) NOT NULL CHECK (waste_type IN ('plastico', 'organico', 'electronico', 'construccion', 'mixto')),
    size VARCHAR(10) NOT NULL CHECK (size IN ('small', 'medium', 'large', 'huge')),
    notes TEXT,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'cleaned', 'verified')),
    reporter_id VARCHAR(100) NOT NULL,
    verified_by VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    cleaned_at TIMESTAMP WITH TIME ZONE
);

-- Índices para búsquedas eficientes
CREATE INDEX idx_reports_location ON reports USING GIST(location);
CREATE INDEX idx_reports_waste_type ON reports(waste_type);
CREATE INDEX idx_reports_status ON reports(status);
CREATE INDEX idx_reports_reporter ON reports(reporter_id);
CREATE INDEX idx_reports_created_at ON reports(created_at DESC);

-- Índice compuesto para búsqueda geográfica + tipo
CREATE INDEX idx_reports_location_type ON reports USING GIST(location) INCLUDE (waste_type, status);

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_reports_updated_at 
    BEFORE UPDATE ON reports 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Función para buscar reportes dentro de un radio (km)
CREATE OR REPLACE FUNCTION search_reports_in_area(
    center_lat DECIMAL,
    center_lon DECIMAL,
    radius_km DECIMAL,
    filter_type VARCHAR(20) DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    latitude DECIMAL,
    longitude DECIMAL,
    waste_type VARCHAR,
    size VARCHAR,
    notes TEXT,
    status VARCHAR,
    reporter_id VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE,
    distance_meters DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        r.id,
        r.latitude,
        r.longitude,
        r.waste_type,
        r.size,
        r.notes,
        r.status,
        r.reporter_id,
        r.created_at,
        ST_Distance(
            r.location::geometry,
            ST_SetSRID(ST_MakePoint(center_lon, center_lat), 4326)::geometry
        )::DECIMAL as distance_meters
    FROM reports r
    WHERE ST_DWithin(
        r.location::geometry,
        ST_SetSRID(ST_MakePoint(center_lon, center_lat), 4326)::geometry,
        radius_km * 1000  -- Convertir km a metros
    )
    AND (filter_type IS NULL OR r.waste_type = filter_type)
    AND r.status != 'cleaned'  -- Opcional: excluir limpios por defecto
    ORDER BY distance_meters;
END;
$$ LANGUAGE plpgsql;

-- Vista para estadísticas
CREATE VIEW report_stats AS
SELECT 
    COUNT(*) as total_reports,
    COUNT(*) FILTER (WHERE status = 'active') as active_reports,
    COUNT(*) FILTER (WHERE status = 'cleaned') as cleaned_reports,
    COUNT(*) FILTER (WHERE status = 'verified') as verified_reports,
    COUNT(*) FILTER (WHERE created_at > CURRENT_TIMESTAMP - INTERVAL '30 days') as reports_last_30_days,
    COUNT(DISTINCT reporter_id) as unique_reporters
FROM reports;

-- Vista para conteo por tipo
CREATE VIEW reports_by_type AS
SELECT 
    waste_type,
    COUNT(*) as count,
    COUNT(*) FILTER (WHERE status = 'active') as active,
    COUNT(*) FILTER (WHERE status = 'cleaned') as cleaned
FROM reports
GROUP BY waste_type;

-- Comentarios para documentación
COMMENT ON TABLE reports IS 'Reportes de basurales informales';
COMMENT ON COLUMN reports.location IS 'Coordenadas geográficas (PostGIS Point)';
COMMENT ON COLUMN reports.waste_type IS 'Tipo de residuo: plastico, organico, electronico, construccion, mixto';
COMMENT ON COLUMN reports.size IS 'Tamaño estimado: small, medium, large, huge';
COMMENT ON COLUMN reports.status IS 'Estado: active, cleaned, verified';
