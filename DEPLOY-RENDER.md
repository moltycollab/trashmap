# 🚀 TrashMap - Deploy a Render (GRATIS)

**Fecha:** 2026-03-24  
**Estado:** ✅ LISTO PARA DEPLOY  
**Costo:** $0 (FREE tier)  

---

## ✅ Prerequisites

- [x] Repo en GitHub: `https://github.com/moltycollab/trashmap`
- [x] Backend completo en `backend/`
- [x] Frontend en `prototype/`
- [x] `render.yaml` configurado

---

## 🎯 Deploy Backend a Render (Web Service)

### Paso 1: Crear cuenta Render

1. Ir a **https://render.com**
2. Click **"Get Started"** → Sign up with **GitHub**
3. Confirmar email
4. ✅ Listo (NO necesita tarjeta de crédito)

### Paso 2: Crear PostgreSQL Database

1. En Render Dashboard → **"New +"** → **"PostgreSQL"**
2. Configurar:
   - **Name:** `trashmap-db`
   - **Database:** `trashmap`
   - **Region:** closest to your users
3. Click **"Create Database"**
4. Esperar ~1 minuto hasta que esté listo
5. **COPIAR** el valor de `Internal Connection URL`

### Paso 3: Crear Web Service (Backend)

1. **"New +"** → **"Web Service"**
2. Conectar tu GitHub repo `moltycollab/trashmap`
3. Configurar:
   | Campo | Valor |
   |-------|-------|
   | **Name** | `trashmap-api` |
   | **Region** | (default) |
   | **Branch** | `main` |
   | **Root Directory** | `backend` |
   | **Runtime** | `Python` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
   | **Plan** | `Free` |

4. **Environment Variables** → Add:
   ```
   DATABASE_URL = [pegar Internal Connection URL de PostgreSQL]
   SECRET_KEY = trashmap-secret-$(openssl rand -hex 32)
   ALLOWED_ORIGINS = *
   ```

5. Click **"Create Web Service"**
6. Esperar deploy (~2-3 minutos)

### Paso 4: Verificar Backend

1. Ir a `https://trashmap-api.onrender.com/health`
2. Debería retornar `{"status":"healthy"}`
3. Ir a `https://trashmap-api.onrender.com/docs` para API docs

---

## 🌐 Deploy Frontend a GitHub Pages (GRATIS)

### Paso 1: Preparar Frontend

1. Editar `prototype/index.html`
2. Cambiar `API_BASE` al URL del backend:
   ```javascript
   const API_BASE = "https://trashmap-api.onrender.com";
   ```
3. Commit y push a GitHub

### Paso 2: Habilitar GitHub Pages

1. Ir a `https://github.com/moltycollab/trashmap/settings/pages`
2. **Source:** Deploy from branch
3. **Branch:** `gh-pages` (crear si no existe) `/ (root)`
4. Click **Save**
5. Esperar ~2 minutos
6. URL: `https://moltycollab.github.io/trashmap`

---

## 🔗 URLs Finales

| Servicio | URL |
|----------|-----|
| Backend API | `https://trashmap-api.onrender.com` |
| API Docs | `https://trashmap-api.onrender.com/docs` |
| Frontend | `https://moltycollab.github.io/trashmap` |

---

## ❓ Troubleshooting

### "Build failed"
- Revisar Build Logs en Render dashboard
- Asegurar que `requirements.txt` tiene todas las dependencias

### "Database connection error"
- Verificar `DATABASE_URL` está correcto
- PostgreSQL toma ~1 min en inicializar

### "CORS error"
- Asegurar `ALLOWED_ORIGINS=*` en environment variables

---

## ⏱️ Tiempo Total

- Crear cuenta Render: 3 min
- PostgreSQL: 2 min
- Backend deploy: 3 min
- Frontend prep: 5 min
- **Total: ~15 minutos**

---

*Nota: Render free tier pone el servicio en "sleep" después de 15 min de inactividad. Se activa automáticamente cuando alguien lo llama. Para producción 24/7, considerar plan paid ($7/mo).*
