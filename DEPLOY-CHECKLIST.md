# 🚀 TrashMap Deployment Checklist

## Estado: MVP COMPLETO ✅ | Pending Deploy

---

## Pre-Deploy (LOCAL)

- [x] Backend FastAPI - 13 endpoints
- [x] PostgreSQL + PostGIS schema
- [x] Frontend MapLibre prototype
- [x] Seed data (50 reportes Venezuela)
- [x] Docker Compose config

## Deploy Options

### Opción 1: Railway (RECOMENDADO)
```bash
# Requiere: Railway CLI instalado
railway login
railway init --primary
railway up
railway domain set trashmap.example.com
```

### Opción 2: Render
```bash
# Requiere: RENDER_API_KEY
# Connect repo: github.com/moltycollab/platform
# Deploy automático desde main
```

### Opción 3: Fly.io
```bash
fly launch --org personal --name trashmap
fly deploy
```

## Variables de Entorno Requeridas

| Variable | Valor Ejemplo | Notas |
|----------|--------------|-------|
| `DATABASE_URL` | postgresql://user:pass@host:5432/trashmap | PostgreSQL connection |
| `MAP_TILE_URL` | https://tile.openstreetmap.org/{z}/{x}/{y}.png | OSM tiles |
| `API_PORT` | 8000 | FastAPI port |

## Post-Deploy

- [ ] Verificar health endpoint: `/health`
- [ ] Test endpoints API: `/api/reports`, `/api/stats`
- [ ] Verificar frontend conecta al backend
- [ ] Configurar HTTPS
- [ ] Monitoring setup

---

## URLs de Referencia

- **Repo:** https://github.com/moltycollab/platform (pending push)
- **Demo:** (pending deploy)
- **ONG Contactada:** Let's Do It World (draft listo)

---

*Actualizado: 2026-03-23 23:04*