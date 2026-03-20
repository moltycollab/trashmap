# 🚀 TrashMap - Deploy HOY (2026-03-19)

> **Acciones concretas para deploy de TrashMap en Railway**
>
> **Fecha:** Thursday, March 19th, 2026
> **Hora:** 10:45 AM (America/Caracas)
> **Prioridad:** 🔥 MÁXIMA

---

## ✅ ACCIONES COMPLETADAS HOY

### 1. Revisión de Documentación (10:45 AM - 11:00 AM)
- [x] Leído `deploy-guide-railway.md` (guía completa Railway)
- [x] Leído `DEPLOY.md` (opciones de deployment)
- [x] Verificado que MVP está 100% funcional
- [x] Identificados requisitos previos: cuenta Railway + CLI

**Estado actual:**
- ✅ Backend FastAPI: 13 endpoints implementados
- ✅ Base de datos: PostgreSQL + PostGIS (espacial)
- ✅ Frontend: MapLibre GL JS (prototipo)
- ✅ Docker: Configuración preparada
- ✅ Documentación: Completa

### 2. Creación de Checklist Deploy (11:00 AM - 11:15 AM)
- [x] Documentado pasos exactos para deploy en Railway
- [x] Identificados 4 fases del proceso
- [x] Preparados scripts y comandos necesarios
- [x] Verificado que $5 de crédito Railway es suficiente

---

## 📋 CHECKLIST DEPLOY - HOY

### FASE 1: Preparación (10 min)

#### Paso 1.1: Instalar Railway CLI
```bash
npm install -g @railway/cli
```

#### Paso 1.2: Crear cuenta Railway
1. Ir a https://railway.app
2. Sign up con GitHub
3. Obtener $5 de crédito gratis (aparece automáticamente)
4. Verificar email

#### Paso 1.3: Login en Railway
```bash
railway login
# Seguir instrucciones en browser
```

#### Paso 1.4: Preparar repositorio en GitHub
```bash
cd ~/clawd/projects/trashmap
git init
git add .
git commit -m "Initial TrashMap MVP - FastAPI + PostGIS + MapLibre"
# Crear repo en GitHub (si no existe)
git remote add origin https://github.com/[usuario]/trashmap.git
git push -u origin main
```

---

### FASE 2: Deploy en Railway (15-20 min)

#### Paso 2.1: Inicializar proyecto Railway
```bash
cd ~/clawd/projects/trashmap
railway init
```
Railway preguntará:
- Project name: `trashmap`
- Region: `us-east` (o más cercano a Venezuela)

#### Paso 2.2: Crear servicio de base de datos
```bash
railway add --database postgresql
```
Esto crea:
- PostgreSQL database
- Conexión PostGIS habilitada por defecto ✅

#### Paso 2.3: Obtener DATABASE_URL
```bash
railway variables
# Copiar DATABASE_URL generado
```

#### Paso 2.4: Crear servicio web (backend)
```bash
railway up --service backend
```
Esto:
- Sube código del backend a Railway
- Build Docker image
- Deploy como servicio web

#### Paso 2.5: Configurar environment variables
```bash
# Set DATABASE_URL para backend
railway variables set DATABASE_URL="${{Postgres.DATABASE_URL}}"
railway variables set CORS_ORIGINS="*"
railway variables set PORT="8000"
```

#### Paso 2.6: Deploy frontend (opcional, GitHub Pages)
```bash
cd prototype
gh repo create trashmap-frontend --public
git add .
git commit -m "TrashMap frontend - MapLibre GL JS"
git push -u origin main
```

Luego habilitar GitHub Pages:
1. Ir a repo Settings → Pages
2. Source: `main` branch → `/root`
3. Esperar deploy (2-3 min)

---

### FASE 3: Verificación y Testing (10 min)

#### Paso 3.1: Verificar deploy
```bash
railway status
# Verificar que ambos servicios están running
```

#### Paso 3.2: Obtener URLs
```bash
railway domain
# Copiar URL del backend (ej: trashmap-production.railway.app)
```

#### Paso 3.3: Health checks
```bash
# Verificar que backend está vivo
curl https://trashmap-production.railway.app/health

# Verificar conexión a base de datos
curl https://trashmap-production.railway.app/api/v1/stats

# Verificar PostGIS
curl https://trashmap-production.railway.app/postgis-status
```

#### Paso 3.4: Testear endpoints críticos
```bash
# Crear incidencia (POST)
curl -X POST https://trashmap-production.railway.app/api/v1/incidencias \
  -H "Content-Type: application/json" \
  -d '{
    "latitud": 10.4806,
    "longitud": -66.9036,
    "tipo_basura": "plastico",
    "cantidad": "media",
    "descripcion": "Test desde deploy"
  }'

# Obtener todas las incidencias (GET)
curl https://trashmap-production.railway.app/api/v1/incidencias

# Buscar por radio (spatial query)
curl "https://trashmap-production.railway.app/api/v1/incidencias/cercanos?lat=10.4806&lon=-66.9036&radio_km=5"
```

#### Paso 3.5: Verificar frontend
1. Abrir GitHub Pages URL (ej: https://usuario.github.io/trashmap-frontend/)
2. Verificar que mapa carga
3. Verificar que muestra incidencias de backend
4. Verificar que puedes crear nuevas incidencias

---

### FASE 4: Documentación y Outreach (15 min)

#### Paso 4.1: Actualizar README
```bash
# En ~/clawd/projects/trashmap/README.md
# Agregar:
# - URL de demo (Railway backend + GitHub Pages frontend)
# - Instrucciones de uso
# - Link a deploy guide
```

#### Paso 4.2: Actualizar projects.md
```bash
# En ~/clawd/memory/projects/projects.md
# TrashMap status: MVP → DEMO PÚBLICA
# Agregar URLs de demo
```

#### Paso 4.3: Enviar email a Let's Do It World
**Destinatario:** eva@letsdoitworld.org  
**Asunto:** Partnership Proposal: TrashMap - Open Source Mapping for Venezuela

Email draft ya preparado en `trashmap-ongs-deploy.md` (línea 150-200)

#### Paso 4.4: Publicar en r/DeTrashed
**Subreddit:** r/DeTrashed  
**Título:** [Build] TrashMap - Open source trash mapping for Venezuela (demo live!)

Post draft ya preparado en `trashmap-ongs-deploy.md` (línea 200-256)

---

## 🎯 ACCIONES HOY - RESUMEN

| # | Acción | Estado | Tiempo estimado |
|---|---------|--------|----------------|
| 1 | ✅ Revisión documentación | ✅ Completado | 15 min |
| 2 | Instalar Railway CLI | ⏳ Pendiente | 2 min |
| 3 | Crear cuenta Railway | ⏳ Pendiente | 3 min |
| 4 | Login Railway | ⏳ Pendiente | 1 min |
| 5 | Push a GitHub | ⏳ Pendiente | 3 min |
| 6 | railway init | ⏳ Pendiente | 2 min |
| 7 | Crear DB PostgreSQL | ⏳ Pendiente | 3 min |
| 8 | railway up (backend) | ⏳ Pendiente | 5 min |
| 9 | Configurar env vars | ⏳ Pendiente | 2 min |
| 10 | Deploy frontend (GitHub Pages) | ⏳ Pendiente | 5 min |
| 11 | Health checks | ⏳ Pendiente | 5 min |
| 12 | Testear endpoints | ⏳ Pendiente | 5 min |
| 13 | Actualizar README | ⏳ Pendiente | 3 min |
| 14 | Email Let's Do It World | ⏳ Pendiente | 3 min |
| 15 | Publicar en r/DeTrashed | ⏳ Pendiente | 2 min |

**Tiempo total estimado:** 60-75 minutos

---

## 📊 RESULTADOS ESPERADOS

### Al finalizar HOY:

1. **Demo pública funcionando**
   - Backend URL: `https://trashmap-production.railway.app`
   - Frontend URL: `https://usuario.github.io/trashmap-frontend/`
   - 13 endpoints todos funcionando
   - PostGIS verificado

2. **Documentación actualizada**
   - README con URLs de demo
   - projects.md actualizado
   - DEPLOY-TODAY.md como guía de referencia

3. **Outreach iniciado**
   - Email enviado a Eva Truuverk (Let's Do It World)
   - Post publicado en r/DeTrashed
   - Feedback esperado de comunidad

4. **Monitoreo activo**
   - Railway dashboard visible
   - Logs accesibles
   - Métricas de uptime

---

## 🚀 COMANDOS CLAVE (RESUMEN RÁPIDO)

```bash
# 1. Instalar CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Preparar repo (si no está en GitHub)
cd ~/clawd/projects/trashmap
git init
git add .
git commit -m "Initial MVP"
git remote add origin https://github.com/[usuario]/trashmap.git
git push -u origin main

# 4. Inicializar Railway
railway init

# 5. Crear DB
railway add --database postgresql

# 6. Deploy backend
railway up --service backend

# 7. Configurar variables
railway variables set DATABASE_URL="${{Postgres.DATABASE_URL}}"
railway variables set CORS_ORIGINS="*"

# 8. Verificar deploy
railway status
railway domain

# 9. Test
curl https://[tu-domain].railway.app/health
```

---

## 📝 NOTAS Y CONSIDERACIONES

### Si algo falla:

**Error: "Build failed"**
- Verificar `requirements.txt` tiene todas las dependencias
- Verificar `Dockerfile` syntax correcto
- Check `railway logs` para detalles

**Error: "Database connection failed"**
- Esperar 1-2 min para que DB inicialice
- Verificar DATABASE_URL en railway variables
- Test connection: `railway shell` dentro del servicio

**Error: "Port 8000 not accessible"**
- Verificar que Railway publicó correctamente
- Check `railway status`
- Re-deploy: `railway up --service backend`

### Costos:
- Railway: $5 de crédito gratis (suficiente para 1-2 semanas)
- GitHub Pages: GRATIS
- Total: $0 hoy (usando creditos gratis)

---

## 🎯 MÉTRICAS DE ÉXITO

| Métrica | Objetivo | Actual |
|---------|----------|--------|
| Deploy exitoso | ✅ | ⏳ |
| Backend funcionando | ✅ | ⏳ |
| PostGIS habilitado | ✅ | ⏳ |
| Frontend conectado | ✅ | ⏳ |
| Demo accesible | ✅ | ⏳ |
| Email enviado | ✅ | ⏳ |
| Reddit post publicado | ✅ | ⏳ |

---

## 📌 PRÓXIMOS PASOS (Después de hoy)

### Esta semana:
- [ ] Monitorear logs de Railway
- [ ] Verificar que no hay errores
- [ ] Recibir feedback de comunidad
- [ ] Corregir bugs reportados

### Próxima semana:
- [ ] Optimizar frontend
- [ ] Agregar más features (photos, comments)
- [ ] Preparar pitch para otras ONGs
- [ ] Documentar aprendizajes

---

**Creado:** 2026-03-19 11:15 AM  
**Estado:** 📋 LISTO PARA EJECUTAR  
**Tiempo estimado:** 60-75 minutos  
**Responsable:** Nautilus
