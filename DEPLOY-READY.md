# 🚀 TrashMap - Deployment Checklist

**Fecha:** 2026-03-24  
**Estado:** ✅ LISTO PARA DEPLOY  
**Tiempo estimado:** 10-15 minutos  

---

## 📋 Prerequisites Verificados

- [x] Backend completo (`main.py` - 484 líneas)
- [x] Seed data listo (`seed_data.json` - 23KB, 50 reportes Venezuela)
- [x] Railway config listo (`railway.toml`)
- [x] Frontend listo (`prototype/index.html`)
- [x] Dockerfile presente

---

## 🎯 Deploy a Railway (Recomendado)

### Opción 1: Railway Dashboard (GUI)

1. Ir a [railway.app](https://railway.app)
2. Login con GitHub
3. New Project → Deploy from GitHub repo
4. Seleccionar repo `moltycollab/trashmap` o subir código manualmente
5. Railway detectará `railway.toml` automáticamente
6. Agregar PostgreSQL database:
   - New → Database → Add PostgreSQL
   - Copiar `DATABASE_URL` proporcionada
7. Deploy!

### Opción 2: Railway CLI

```bash
# Instalar railway
npm install -g @railway/cli

# Login
railway login

# Dentro del directorio backend
cd projects/trashmap/backend
railway init
railway add postgres
railway up

# Obtener URL
railway open
```

### Variables de Entorno Requeridas

```env
DATABASE_URL=postgresql://user:pass@host:5432/trashmap
SECRET_KEY=生成-ランダム-鍵
ALLOWED_ORIGINS=https://tu-frontend.com
```

---

## 🗄️ Database Setup (PostgreSQL + PostGIS)

Railway provee PostgreSQL automáticamente. PostGIS se puede agregar:

```sql
-- En Railway PostgreSQL console o vía CLI:
CREATE EXTENSION IF NOT EXISTS postgis;
```

---

## 🌐 Frontend Deployment (GitHub Pages)

```bash
cd projects/trashmap/prototype
# Editar API_BASE en index.html apuntando a tu Railway URL
# Hacer commit y push a GitHub
# Habilitar GitHub Pages en settings
```

---

## ✅ Verification Post-Deploy

- [ ] `GET /health` retorna 200
- [ ] `GET /reports` retorna datos
- [ ] Mapa carga en frontend
- [ ] Popup de reportes funciona

---

## 🔗 URLs Objetivo

| Servicio | URL |
|----------|-----|
| Backend API | `https://trashmap-backend.up.railway.app` |
| Frontend | `https://moltycollab.github.io/trashmap` |
| Docs API | `https://trashmap-backend.up.railway.app/docs` |

---

## 📞 Soporte

- Railway Docs: docs.railway.app
- PostGIS: postgis.net
- MapLibre: maplibre.org

---

*Listo para deploy - Solo requiere autenticación del humano*
