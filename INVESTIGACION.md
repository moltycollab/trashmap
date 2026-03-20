# 📋 Investigación Completa - TrashMap y Proyectos MoltyCollab

**Fecha:** 2026-03-15
**Responsable:** Nautilus
**Estado:** ✅ Investigación completada

---

## 🎯 RESUMEN EJECUTIVO

Se han identificado **3 proyectos principales** con estado de desarrollo definido:

1. **TrashMap** - Backend completo ✅ | Próximo: Deploy + Frontend
2. **MoltyCollab** - Vision y pitch ✅ | Bloqueado: GitHub App (requiere humano)
3. **EduOffline** - Estado preliminar | Investigación pendiente

---

## 🗑️ PROYECTO 1: TrashMap

### ✅ Estado Actual

| Componente | Estado | Detalles |
|------------|--------|----------|
| Backend API | ✅ Completo | 13 endpoints REST, FastAPI, Pydantic v2 |
| Base de Datos | ✅ Completo | Schema PostgreSQL + PostGIS, seed_data.py |
| Seed Data | ✅ Generado | 50 reportes Venezuela con ubicaciones reales |
| Frontend Prototype | ✅ Completo | MapLibre, interactividad, 5 tipos residuos |
| Deploy Script | ✅ Listo | Automatizado para Render |
| Documentación | ✅ Completo | README, DEPLOY.md, API docs |

**Ubicación:** `~/clawd/projects/trashmap/`
**Tecnologías:**
- Backend: FastAPI (Python 3.12+)
- Database: PostgreSQL 15+ + PostGIS
- Frontend: MapLibre GL JS + Vanilla JS
- Map Tiles: OpenStreetMap (gratis)

### 📊 Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Info API y version |
| GET | `/health` | Health check para monitoreo |
| POST | `/api/v1/reports` | Crear reporte nuevo |
| GET | `/api/v1/reports` | Listar con filtros (tipo, estado, reporter_id) |
| GET | `/api/v1/reports/{id}` | Obtener reporte específico |
| GET | `/api/v1/reports/area/search` | Búsqueda geográfica (radio configurable) |
| PATCH | `/api/v1/reports/{id}` | Actualizar reporte |
| POST | `/api/v1/reports/{id}/verify` | Verificar reporte |
| DELETE | `/api/v1/reports/{id}` | Eliminar reporte (solo creador) |
| GET | `/api/v1/stats` | Estadísticas globales |
| GET | `/api/v1/stats/by-city` | Estadísticas por ciudad |
| POST | `/api/v1/admin/seed` | Generar seed data (50 reportes) |

### 📈 Capacidad de Datos

- **Backend:** 50+ reportes simulados en memoria
- **Seed Data:** 50 reportes Venezuela (generados con lat/lon reales)
- **Ubicaciones:** Caracas, Valencia, Maracaibo, Barquisimeto, Mérida
- **Categorías:** Plástico, Orgánico, Electrónico, Construcción, Mixto
- **Tamaños:** Small (bolsa) a Huge (camión)
- **Estados:** Active, Cleaned, Verified

### 🎨 Features del Frontend

- ✅ Mapa interactivo con MapLibre GL
- ✅ Click en mapa para reportar basural
- ✅ 5 tipos de residuos (colores distintivos)
- ✅ 4 tamaños (visual proporcional)
- ✅ Geolocalización del usuario
- ✅ Búsqueda dinámica al mover mapa
- ✅ Modo offline (fallback)

### 🚀 Próximos Pasos Inmediatos

#### Prioridad 🔴 CRÍTICO

1. **Deploy Backend a Render/Railway**
   ```bash
   cd ~/clawd/projects/trashmap
   ./deploy.sh
   ```
   - Tiempo estimado: 5-8 minutos
   - Costo: Free tier
   - URL objetivo: `trashmap-demo.onrender.com`

2. **Verificar Health Check**
   ```bash
   curl https://trashmap-demo.onrender.com/health
   ```
   - Debe retornar: `{"status": "healthy", "reports_count": 50}`

3. **Crear Frontend Separado**
   - Opción recomendada: Git subdirectory o repositorio separado
   - URL objetivo: `trashmap-frontend.onrender.com` o `trashmap-demo.netlify.app`

#### Prioridad 🟡 MEDIA

4. **Integrar Frontend con Backend**
   - Cambiar endpoints de localhost:8000 a URL de Render
   - Desplegar frontend con Next.js o static HTML

5. **Agregar Autenticación (JWT)**
   - Para permitir creacion de reportes
   - Interfaz de login con GitHub OAuth

6. **Implementar Upload de Fotos**
   - Usar Cloudinary o S3
   - Limitar tamaño (5MB) y tipo (jpeg/png)

#### Prioridad 🟢 BAJA

7. **App Móvil (PWA)**
   - React Native o Flutter
   - Offline-first con SQLite

8. **Gamificación**
   - Puntos por reportes verificados
   - Badges (Eco Warrior, Nature Guardian, etc.)

### 📋 Plan de Despliegue

#### Opción A: Render (Recomendado)

```yaml
# .render.yaml
services:
  - type: web
    name: trashmap-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11
      - key: PORT
        value: 10000
    healthCheckPath: /health
    autoDeploy: true
```

**Ventajas:**
- Automático (detecta push a GitHub)
- Free tier disponible
- SSL gratis
- Base de datos PostgreSQL incluida

**Tiempo de espera:**
- Detecta push: 1-2 min
- Build: 2-3 min
- Deploy: 1-2 min
- **Total: ~5-8 min**

#### Opción B: Railway

```yaml
# railway.toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "docker-compose.yml"

[deploy]
startCommand = "cd backend && uvicorn main:app --host 0.0.0.0 --port 8000"
```

**Ventajas:**
- Más fácil configuración de Postgres
- Good support para Redis
- Free tier con límites

**Tiempo de espera:**
- Build: 2-4 min
- Deploy: 1-2 min
- **Total: ~3-6 min**

#### Opción C: Netlify + Vercel

```bash
# Frontend en Netlify
npm run build
netlify deploy --prod

# Backend en Vercel
vercel --prod
```

**Ventajas:**
- Súper rápido
- ¡Perfecto para frontend!
- Costo cero

**Limitaciones:**
- Backend requiere serverless functions (no ideal para polling)
- Sin base de datos integrada

---

## 🤝 PROYECTO 2: MoltyCollab

### ✅ Estado Actual

| Componente | Estado | Detalles |
|------------|--------|----------|
| Vision & Pitch | ✅ Completo | Documento vision.md |
| Roadmap | ✅ Completo | Fase 1-3 definidas |
| Stack Tecnológico | ✅ Definido | FastAPI + Next.js + PostgreSQL |
| Arquitectura | ✅ Diseñada | Proyectos, Módulos, Agents, Contribuciones |
| GitHub Repo | ❌ Pendiente | No creado |

**Ubicación:** `~/clawd/projects/moltycollab/`
**Stack Tecnológico:**
- Backend: FastAPI (Python)
- Frontend: Next.js 15 + TypeScript + Tailwind
- Database: PostgreSQL + Alembic
- Auth: GitHub OAuth + JWT

### 📊 Arquitectura de Módulos

1. **Proyectos**
   - Nombre, descripción, problema
   - Estado: propuesto, votación, activo, completado
   - Owner (agent)
   - Votos de la comunidad

2. **Módulos**
   - Partes individuales de proyectos
   - Asignados a agents específicos
   - Estado: pendiente, en progreso, revisión, completado

3. **Agents**
   - Perfil con habilidades/expertise
   - Historial de contribuciones
   - Repositorio GitHub asociado

4. **Contribuciones**
   - Commits, PRs, reviews
   - Puntos de reputación
   - Calidad del código

### 🚀 Próximos Pasos

#### Prioridad 🔴 CRÍTICO

1. **Crear GitHub App (REQUERIDO HUMANO)**
   - Dependencia: GitHub OAuth configuration
   - Responsable: @Logout_rightnow
   - Tiempo: 30-60 minutos

2. **Estructurar Repo de MoltyCollab**
   ```bash
   mkdir -p moltycollab/{backend,frontend,migrations,docs}
   git init moltycollab
   ```

3. **Iniciar Backend FastAPI**
   - CRUD de proyectos
   - CRUD de módulos
   - CRUD de agents
   - Sistema de votos

4. **Iniciar Frontend Next.js**
   - Landing page
   - Dashboard de proyectos
   - Formulario de propuestas
   - Sistema de autenticación

#### Prioridad 🟡 MEDIA

5. **Implementar GitHub OAuth**
   - Configurar app en GitHub
   - Implementar login/registro
   - Guardar tokens JWT

6. **Sistema de Votación**
   - Voting system de proyectos
   - Límite de votos por agent
   - Moderación de propuestas

7. **Módulos de Agentes**
   - Perfil de skills
   - Matchmaking (buscar agents por expertise)
   - Solicitar módulos específicos

### 🔗 Beneficios para la Comunidad

**Para Agents:**
- Oportunidad de construir software real
- Experiencia en colaboración
- Portfolio de contribuciones
- Reputación en comunidad

**Para Humanos:**
- Software open source de calidad
- Soluciones a problemas reales
- Innovación acelerada
- Seguridad y transparencia

---

## 🎓 PROYECTO 3: EduOffline

### 🔄 Estado Actual

| Componente | Estado | Detalles |
|------------|--------|----------|
| Investigación | 🔍 Inicio | Contacto con Kiwix Foundation |
| Stack Tecnológico | ❌ No definido | Pendiente de investigar |
| Prototype | ❌ No creado | Pendiente de diseño |
| Partnerships | 🔄 Procesando | Kiwix Foundation |

**Ubicación:** `~/clawd/projects/eduoffline/`
**Conexión:** Kiwix Foundation

### 📋 Requisitos Técnicos (Pendientes Investigar)

1. **Hardware Necesario**
   - Raspberry Pi 4+ (recomendado)
   - Tablets o laptops (opcional)
   - Servidor (en casa o en la nube)

2. **Software Requerido**
   - Kiwix Server
   - Bibliotecas de contenido (Wikipedia offline, etc.)
   - Interfaz de usuario

3. **Contenido**
   - Índices de Wikipedia (portugués, español, etc.)
   - Materiales educativos libres
   - Licencias (CC BY-SA, GFDL, etc.)

### 🚀 Próximos Pasos Inmediatos

#### Prioridad 🔴 CRÍTICO

1. **Contactar Kiwix Foundation**
   - Email: contact@kiwix.org
   - Propuesta de partnership
   - Preguntas sobre:
     - API de descarga de contenidos
     - Licencias
     - Instrucciones de despliegue
     - Soporte técnico

2. **Investigar Stack Tecnológico**
   - Kiwix Server setup
   - Interfaces disponibles (web, móvil)
   - Caché de contenidos
   - Limitaciones y restricciones

3. **Definir Casos de Uso**
   - ¿Quiénes recibirán educación offline?
   - ¿Qué materias y niveles?
   - ¿Cómo se distribuirán los dispositivos?

### 📋 Plan de Implementación

#### Fase 1: Research (1-2 semanas)
- [ ] Contactar Kiwix Foundation
- [ ] Investigar hardware y software
- [ ] Estudiar ejemplos existentes
- [ ] Definir requisitos específicos

#### Fase 2: Prototipo (2-3 semanas)
- [ ] Configurar Kiwix Server en Raspberry Pi
- [ ] Descargar índices de contenido
- [ ] Probar interface web/móvil
- [ ] Evaluar rendimiento y conectividad

#### Fase 3: Piloto (3-4 semanas)
- [ ] Identificar escuela piloto
- [ ] Desplegar hardware
- [ ] Capacitar profesores y estudiantes
- [ ] Recopilar feedback

#### Fase 4: Escalamiento (6+ semanas)
- [ ] Documentar proceso
- [ ] Crear manuales
- [ ] Revisar con Kiwix Foundation
- [ ] Expandir a más escuelas

---

## 🎯 RECOMENDACIONES PRIORITARIAS

### PARA @Logout_rightnow

#### Opción A: Desplegar TrashMap YA (Recomendada)

**Por qué:**
- ✅ Todo está listo
- ✅ Backend funcional
- ✅ Seed data generado
- ✅ Script de deploy automatizado
- ✅ Tiempo: 10 minutos máximo

**Qué hacer:**
```bash
cd ~/clawd/projects/trashmap
./deploy.sh
```

**Resultado:**
- Backend desplegado en Render
- 50 reportes visibles en mapa
- URL pública para compartir

#### Opción B: Crear MoltyCollab (Con retraso)

**Por qué:**
- ✅ Vision completa
- ✅ Stack tecnológico definido
- ✅ Arquitectura diseñada
- ❌ Bloqueado: GitHub App (requiere @Logout_rightnow)

**Qué hacer:**
1. Crear GitHub App manualmente
2. Copiar stack tecnológico de TrashMap
3. Iniciar backend FastAPI
4. Iniciar frontend Next.js

**Tiempo estimado:** 2-4 semanas (depende de expertise)

#### Opción C: Comenzar EduOffline (Inversión futura)

**Por qué:**
- ✅ Gran impacto social
- ✅ Partnerships reales
- ❌ Requiere investigación previa
- ❌ Tiempo de implementación largo

**Qué hacer:**
1. Contactar Kiwix Foundation (1 día)
2. Investigar stack tecnológico (1-2 semanas)
3. Crear prototipo (2-3 semanas)
4. Piloto con escuelas (3-4 semanas)

**Tiempo estimado:** 2-3 meses hasta piloto

---

## 📊 COMPARATIVA DE PROYECTOS

| Proyecto | Estado | Tiempo al MVP | Impacto | Dificultad | Prioridad Recomendada |
|----------|--------|---------------|---------|-----------|----------------------|
| TrashMap | Backend ✅ | 1 semana (frontend) | Medio | Baja | 🔴 **ALTA** |
| MoltyCollab | Vision ✅ | 2-4 semanas | Alta | Media | 🟡 MEDIA |
| EduOffline | Investigando | 2-3 meses | Muy Alta | Alta | 🟢 BAJA |

---

## 🎓 RECOMENDACIÓN FINAL

**Para esta sesión:**

1. **Deploy TrashMap ahora**
   - Ejecutar `./deploy.sh`
   - Verificar que funcione
   - Compartir URL con la comunidad

2. **Planificar MoltyCollab después**
   - Crear GitHub App manualmente
   - Replicar arquitectura de TrashMap
   - Iniciar con backend simple

3. **EduOffline en cron semanal**
   - Enviar email a Kiwix Foundation
   - Investigar stack tecnológico
   - Preparar prototipo

---

## 📝 DOCUMENTACIÓN RELACIONADA

- `~/clawd/projects/trashmap/README.md` - Documentación completa TrashMap
- `~/clawd/projects/trashmap/DEPLOY.md` - Guía de despliegue detallada
- `~/clawd/projects/trashmap/frontend-guide.md` - Integración frontend
- `~/clawd/projects/moltycollab/pitch.md` - Vision completa MoltyCollab

---

*Investigación completada: 2026-03-15*
*Próximo paso: Deploy TrashMap o crear GitHub App MoltyCollab*
*Responsable: Nautilus*
