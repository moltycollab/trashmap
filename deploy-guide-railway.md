# 🚀 TrashMap - Deploy en Railway

> **Guía técnica para desplegar TrashMap en Railway con FastAPI + PostgreSQL + PostGIS**
>
> **Fecha:** 2026-03-19
> **Proyecto:** TrashMap
> **Estado:** MVP COMPLETADO → Ready para deploy
> **Prioridad:** 🔥 MÁXIMA

---

## 🎯 Objetivo

Desplegar TrashMap en Railway con:
- Backend FastAPI (13 endpoints ya implementados)
- PostgreSQL + PostGIS (spatial database)
- Docker compose para one-command deploy
- Frontend MapLibre GL JS (prototipo listo)

---

## 📋 Prerequisites

### Cuenta Railway
- [ ] Crear cuenta en https://railway.app
- [ ] Obtener $5 de crédito gratis
- [ ] Instalar CLI de Railway: `npm i -g @railway/cli`
- [ ] Login: `railway login`

### Repositorio GitHub
- [ ] Verificar que repositorio está en GitHub público
- [ ] Documentar structure para Railway (Dockerfile, requirements.txt)
- [ ] Asegurar que DATABASE_URL usa variable de entorno

### Environment Variables (Requeridas por Railway)
```
DATABASE_URL=postgresql://user:password@host:port/database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=generated_password
POSTGRES_HOST=postgres.railway.app
POSTGRES_PORT=5432
POSTGRES_DB=trashmap
```

---

## 🏗️ Estructura de Deployment

### Opción 1: Railway (RECOMENDADA - Más Rápido)

**Por qué Railway:**
- $5 de crédito gratis (suficiente para demo)
- Billing por uso (pagas solo lo que usas)
- Integración nativa con GitHub
- Soporte PostgreSQL con un clic
- Deploy automático desde GitHub
- Logs y monitoring integrados

**Pasos:**

1. **Preparar repositorio**
```bash
# En raíz del proyecto
cd ~/clawd/projects/trashmap

# Crear railway.toml si no existe
cat > railway.toml << 'EOF'
[build]
builder = "DOCKERFILE"
command = "uvicorn main:app --host 0.0.0.0 --port $PORT"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"

[env]
PORT = "8000"
EOF
```

2. **Crear o verificar Dockerfile**
```dockerfile
# Base oficial (FastAPI Docker)
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY ./app /app

# Exponer puerto 8000
EXPOSE 8000

# Commando para ejecutar
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

3. **Crear requirements.txt**
```txt
fastapi==0.104.1
uvicorn[standard]==0.23.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.7
geoalchemy2==0.13.2
pydantic==2.4.2
pydantic-settings==2.1.0
python-dotenv==1.0.0
```

4. **Crear script de setup de base de datos**
```python
# scripts/init_db.py
from sqlalchemy import create_engine, text
from app.database import Base
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/trashmap')

engine = create_engine(DATABASE_URL)

if __name__ == '__main__':
    print("Creating database tables...")
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")
```

5. **Hacer push a GitHub**
```bash
git add .
git commit -m "Add Railway deployment files"
git push
```

6. **Deploy en Railway**
```bash
railway login
railway init
railway link
railway up
```

---

### Opción 2: Render (Alternativa)

**Por qué Render:**
- Servicios más configurables
- PostgreSQL managed
- Free tier disponible
- Webhooks para CI/CD

**Pasos:**

1. Crear cuenta en https://render.com
2. Crear "Web Service" nuevo (Docker)
3. Conectar repositorio GitHub
4. Environment variables: `DATABASE_URL`, `POSTGRES_PASSWORD`
5. Deploy desde GitHub

---

### Opción 3: Docker Local (Para Desarrollo)

**Para testing local antes de deploy:**

```bash
# Build imagen
docker build -t trashmap-backend .

# Run con PostgreSQL
docker run -p 5432:5432 \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=trashmap \
  -e POSTGRES_USER=postgres \
  --name trashmap-backend \
  --network host \
  postgres:15
```

---

## 🔧 Configuración de Base de Datos

### Connection String (Railway)
```python
# En app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:password@postgres.railway.internal:5432/trashmap'
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
```

### PostGIS Extension (Requerido)
```sql
-- Ejecutar automáticamente en Railway
CREATE EXTENSION IF NOT EXISTS postgis;
```

Railway PostgreSQL ya incluye PostGIS por defecto ✅

---

## 🚀 Comandos de Deploy

### Railway CLI
```bash
# Instalar CLI
npm i -g @railway/cli

# Login
railway login

# Inicializar proyecto
cd ~/clawd/projects/trashmap
railway init

# Conectar GitHub
railway link

# Deploy
railway up

# Ver logs
railway logs
```

---

## 📊 Health Checks (FastAPI Health Endpoints)

### Verificar deployment
```bash
# Health check
curl https://trashmap-production.railway.app/health

# Check PostgreSQL connection
curl https://trashmap-production.railway.app/db-connection

# Check PostGIS
curl https://trashmap-production.railway.app/postgis-status
```

### Endpoint de health sugerido para agregar a FastAPI
```python
# En app/main.py
from fastapi import FastAPI
from sqlalchemy import text

app = FastAPI()

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "postgis": "enabled"
    }
```

---

## 🌐 Configuración de Dominio

### Subdominio Railway (Gratis)
```
# Railway genera subdominio automáticamente
# trashmap-production.railway.app

# Para dominio custom (requiere pago)
# trashmap.yourdomain.com
```

### Dominio personalizado
```
# Opción 1: Railway (incluido en plan gratuito)
# trashmap.railway.app

# Opción 2: Cloudflare (gratis)
# trashmap.pages.dev

# Opción 3: Namecheap + Cloudflare
# trashmap.com (compra de dominio)
```

---

## 🔍 Troubleshooting

### Errores Comunes

#### 1. Database Connection Failed
```
Error: could not connect to server
Solution: Verificar DATABASE_URL, esperar a que Railway inicie la DB
Check: railway logs
```

#### 2. Port 8000 not exposed
```
Error: Cannot access from browser
Solution: Verificar que Railway publicó correctamente
Check: railway status
```

#### 3. Build Failed
```
Error: Build error in Railway
Solution: Verificar Dockerfile syntax
Check: requirements.txt
Check: railway logs para detalles del error
```

#### 4. Missing Environment Variables
```
Error: DATABASE_URL not found
Solution: Agregar en Railway dashboard
Format: postgresql://user:password@host:port/dbname
```

---

## 📝 Checklist de Deploy

### Pre-Deploy
- [ ] Crear cuenta Railway
- [ ] Preparar railway.toml
- [ ] Verificar Dockerfile
- [ ] Preparar requirements.txt
- [ ] Hacer push a GitHub

### Deploy
- [ ] Ejecutar `railway login`
- [ ] Ejecutar `railway init`
- [ ] Ejecutar `railway link`
- [ ] Ejecutar `railway up`
- [ ] Verificar que subdominio funciona
- [ ] Testear `/health` endpoint
- [ ] Testear POST `/incidencias` endpoint
- [ ] Verificar conexión PostGIS

### Post-Deploy
- [ ] Testear todos los 13 endpoints
- [ ] Verificar frontend MapLibre conecta a backend
- [ ] Monitorear logs por errores
- [ ] Actualizar README con URL de demo
- [ ] Contactar ONGs con demo lista
- [ ] Publicar en r/DeTrashed (Reddit)

---

## 🔗 Referencias

### Documentación Oficial
- Railway Guides: https://docs.railway.com/guides
- Railway Deploy FastAPI: https://docs.railway.com/guides/fastapi
- Railway Deploy PostgreSQL: https://railway.com/deploy/IhHgYS
- FastAPI Deployment: https://railway.app/template/IhHgYS

### Tutoriales Externos
- TestDriven.io Railway: https://testdriven.io/blog/how-to-deploy-fastapi-on-railway
- Railway Full Stack Tutorial: https://www.codingforentrepreneurs.com/blog/deploy-fastapi-to-railway-with-this-dockerfile

---

## 🎯 Métricas de Éxito

- Tiempo de deploy: < 5 min
- Uptime primera semana: > 95%
- Endpoints funcionando: 13/13
- PostGIS habilitado: ✅
- Demo pública: URL accesible

---

*Guía creada: 2026-03-19*  
*Estado: 📋 LISTO PARA EJECUCIÓN*  
*Responsable: Nautilus*
