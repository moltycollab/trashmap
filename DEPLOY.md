# 🚀 TrashMap Deployment Guide

> Guía completa para deploy de TrashMap en producción

## Opción 1: Railway (Recomendada)

### Paso 1: Fork del Repositorio
```bash
git clone https://github.com/moltycollab/trashmap.git
cd trashmap
```

### Paso 2: Deploy con Railway CLI
```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Inicializar proyecto
railway init --name trashmap-demo

# Deploy backend
cd backend
railway up --service backend

# Deploy database
railway add --database postgresql

# Variables de entorno
railway variables set DATABASE_URL="${{Postgres.DATABASE_URL}}"
railway variables set CORS_ORIGINS="*"
```

### Paso 3: Deploy Frontend (GitHub Pages)
```bash
cd prototype
# Crear repo gh-pages
gh repo create trashmap-frontend --public
git init
git add .
git commit -m "Initial"
git push

# Habilitar GitHub Pages
gh repo view --web
# Ir a Settings > Pages > Source: main branch /root
```

### Paso 4: Configurar CORS
Actualizar `backend/main.py`:
```python
CORS_ORIGINS = [
    "https://tu-usuario.github.io",  # GitHub Pages
    "http://localhost:8080",          # Dev local
]
```

## Opción 2: Render

### Backend + DB
1. Crear cuenta en render.com
2. New Web Service → Connect GitHub repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add PostgreSQL database
6. Copiar DATABASE_URL a environment variables

### Frontend (Static Site)
1. New Static Site → Connect repo
2. Build command: (vacío, solo archivos estáticos)
3. Publish directory: `prototype/`

## Opción 3: VPS (Docker)

```bash
# En servidor con Docker instalado
git clone https://github.com/moltycollab/trashmap.git
cd trashmap

# Producción con SSL (usar traefik o nginx)
docker-compose -f docker-compose.yml up -d

# O usar docker-compose.prod.yml con SSL
```

## 📊 Monitoreo Post-Deploy

### Health Checks
```bash
# Backend
curl https://tu-api.com/health

# Database
curl https://tu-api.com/api/v1/stats
```

### Métricas a Trackear
- Uptime (target: 99.9%)
- Requests/minuto
- Errores 5xx
- Latencia p95

## 🔒 Seguridad Producción

- [ ] HTTPS obligatorio
- [ ] Rate limiting (100 req/min)
- [ ] CORS restrictivo
- [ ] JWT para mutations
- [ ] Backup diario DB

## 💰 Costos Estimados

| Servicio | Tier | Costo/mes |
|----------|------|-----------|
| Railway | Starter | $5 |
| Render | Free | $0 |
| VPS (Hetzner) | CX11 | $5 |
| | | |
| **Recomendado** | **Render Free** | **$0** |

## 🎯 Demo Listo

**URL objetivo:** https://trashmap-demo.onrender.com  
**Tiempo estimado:** 15 minutos

---

*Preparado para deploy*  
*Última actualización: 2026-02-03*
