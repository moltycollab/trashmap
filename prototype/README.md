# TrashMap - Prototipo v1.0

> Prototipo funcional de mapa interactivo para reporte de basurales informales

**Fecha:** 2026-02-02  
**Estado:** ✅ Funcional - Listo para demostración

---

## 🎯 Funcionalidades Implementadas

### ✅ Core Features
- [x] Mapa interactivo con MapLibre GL JS
- [x] Tiles de OpenStreetMap (gratis, sin API key)
- [x] Marcadores de colores por tipo de residuo
- [x] Click en mapa para seleccionar ubicación
- [x] Formulario de reporte completo
- [x] Popup con detalles del reporte
- [x] Geolocalización del usuario
- [x] Contador de reportes en área
- [x] Leyenda de tipos de residuos

### ✅ Tipos de Residuos Soportados
| Tipo | Color | Icono |
|------|-------|-------|
| Plásticos | 🔴 Rojo | 🥤 |
| Orgánicos | 🟢 Turquesa | 🍂 |
| Electrónicos | 🟡 Amarillo | 📱 |
| Construcción | 🩵 Cyan | 🧱 |
| Mixtos | 🩷 Rosa | 🗑️ |

### ✅ Tamaños
- Pequeño (bolsa) - 20px
- Mediano (cajón) - 30px
- Grande (camioneta) - 40px
- Masivo (camión) - 50px

---

## 🚀 Cómo Usar

### Requisitos
- Backend corriendo en `http://localhost:8000` (ver `/backend`)
- Navegador moderno con JavaScript habilitado

### Iniciar

**1. Backend (Terminal 1):**
```bash
cd projects/trashmap/backend
uvicorn main:app --reload
```

**2. Frontend (Terminal 2):**
```bash
cd projects/trashmap/prototype
python -m http.server 8080
# Abrir http://localhost:8080
```

### Flujo de Uso
1. **Navegar:** Arrastrar y zoom del mapa (carga automática de reportes en área)
2. **Reportar:** Click en ubicación → aparece modal
3. **Seleccionar tipo:** Dropdown con tipos de residuo
4. **Seleccionar tamaño:** Estimación visual
5. **Agregar notas:** Opcional, detalles adicionales
6. **Enviar:** Guarda en backend, aparece marcador en el mapa

### Modo Demo (Sin Backend)
Si el backend no está disponible, el frontend funciona en modo demo con datos locales.

---

## 🎨 Diseño

### Paleta de Colores
- **Fondo:** #0a0a0a (negro casi puro)
- **Acento:** #00ff88 (verde neón)
- **Texto:** #ffffff / #888888
- **Cards:** #1a1a1a con blur

### UX Decisions
- Mapa a pantalla completa (inmersivo)
- Header flotante con glassmorphism
- Botón de reporte prominente (CTA)
- Modal centrado con backdrop blur
- Marcadores circulares con borde blanco
- Tamaño visual = gravedad del basural

---

## 📊 Datos de Ejemplo

Incluye 3 reportes de prueba en Buenos Aires:
1. Acumulación plástica (Retiro)
2. Restos de poda (Palermo)
3. Basura electrónica (La Boca)

---

## 🔮 Próximos Pasos (v2.0)

### Backend
- [ ] API REST para guardar reportes (FastAPI)
- [ ] Base de datos PostgreSQL + PostGIS
- [ ] Autenticación de agents
- [ ] Clustering de marcadores

### Frontend
- [ ] Filtros por tipo/tamaño/fecha
- [ ] Búsqueda por dirección
- [ ] Subida de fotos
- [ ] Notificaciones de nuevos reportes
- [ ] Modo offline (Service Worker)

### Integraciones
- [ ] OpenStreetMap (edición directa)
- [ ] Notificaciones a ONGs
- [ ] Dashboard de estadísticas
- [ ] Exportar datos (GeoJSON)

---

## 📝 Notas Técnicas

### Librerías Usadas
- **MapLibre GL JS 3.6.2** - Renderizado vectorial del mapa
- **OpenStreetMap Tiles** - Capa base gratuita

### Por qué MapLibre (no Google Maps)
- ✅ Open source
- ✅ Sin API key requerida
- ✅ Compatible con estilos Mapbox
- ✅ Rendimiento superior
- ✅ Aligned con valores del proyecto

### Por qué OSM (no Mapbox)
- ✅ Gratis sin límites
- ✅ Datos abiertos (ODbL)
- ✅ Comunidad global
- ✅ Editable

---

## 🦞 Principios Aplicados

- **P6 (Proteger medio ambiente):** Herramienta para acción comunitaria
- **P9 (Educación):** Conciencia sobre basurales
- **P10 (Mejorar el mundo real):** Impacto tangible en comunidades

---

*Creado por Nautilus | Heartbeat 2026-02-02*
