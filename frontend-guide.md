# 🎨 TrashMap Frontend Integration Guide

> Guía para conectar frontend con backend desplegado

---

## 📋 Resumen

- **Backend:** `https://trashmap-demo.onrender.com`
- **Health Check:** `https://trashmap-demo.onrender.com/health`
- **API Base:** `https://trashmap-demo.onrender.com/api/v1`

---

## 🚀 Frontend Ready Options

### Opción 1: MapLibre + Mapbox GL JS (Recomendado)

**Ventajas:**
- Open-source, gratuito
- Controles y temas personalizados
- Fuerte comunidad

**Requisitos:**
- Mapbox token gratuito (500x500px)

**Ejemplo básico:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>TrashMap - Venezuela</title>
    <link rel='stylesheet' href='https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css' />
    <script src='https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js'></script>
    <style>
        #map { height: 100vh; }
    </style>
</head>
<body>
    <div id='map'></div>

    <script>
        // Initialize map
        const map = new maplibregl.Map({
            container: 'map',
            style: 'https://demotiles.maplibre.org/style.json',
            center: [-66.9036, 7.1197], // Caracas center
            zoom: 10
        });

        // Add navigation controls
        map.addControl(new maplibregl.NavigationControl());

        // Load reports from API
        async function loadReports() {
            try {
                const response = await fetch('https://trashmap-demo.onrender.com/api/v1/reports');
                const reports = await response.json();

                reports.forEach(report => {
                    const marker = new maplibregl.Marker()
                        .setLngLat([report.longitude, report.latitude])
                        .setPopup(new maplibregl.Popup().setHTML(`
                            <h3>${report.waste_type}</h3>
                            <p>${report.description || 'Sin descripción'}</p>
                            <small>Tamaño: ${report.size}</small>
                        `))
                        .addTo(map);
                });
            } catch (error) {
                console.error('Error loading reports:', error);
            }
        }

        loadReports();
    </script>
</body>
</html>
```

---

### Opción 2: Leaflet + OpenStreetMap (Gratis, sin token)

**Ventajas:**
- Totalmente gratuito
- Sin API keys
- Fácil de usar

**Requisitos:**
- Ninguno

**Ejemplo básico:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>TrashMap - Venezuela</title>
    <link rel='stylesheet' href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css' />
    <script src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'></script>
    <style>
        #map { height: 100vh; }
    </style>
</head>
<body>
    <div id='map'></div>

    <script>
        const map = L.map('map').setView([-66.9036, 7.1197], 10);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap'
        }).addTo(map);

        async function loadReports() {
            try {
                const response = await fetch('https://trashmap-demo.onrender.com/api/v1/reports');
                const reports = await response.json();

                reports.forEach(report => {
                    L.marker([report.latitude, report.longitude])
                        .addTo(map)
                        .bindPopup(`
                            <b>${report.waste_type}</b><br>
                            ${report.description || 'Sin descripción'}<br>
                            <small>${report.size}</small>
                        `);
                });
            } catch (error) {
                console.error('Error loading reports:', error);
            }
        }

        loadReports();
    </script>
</body>
</html>
```

---

### Opción 3: Next.js + MapLibre (Moderno)

**Ventajas:**
- SSR, SEO friendly
- TypeScript support
- Great developer experience

**Setup:**
```bash
npx create-next-app@latest trashmap-frontend
cd trashmap-frontend
npm install maplibre-gl
```

---

## 📝 Crear Nuevo Reporte

### Credenciales de autenticación

Para crear reportes, el backend debe tener endpoint de autenticación. Configura:

**En Render Variables de Entorno:**
```bash
AUTH_TOKEN=tu-token-seguro-aqui
CORS_ORIGINS=https://trashmap-demo.onrender.com,https://tu-usuario.github.io
```

**En frontend:**
```javascript
async function createReport(report) {
    const response = await fetch('https://trashmap-demo.onrender.com/api/v1/reports', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
        },
        body: JSON.stringify(report)
    });

    return response.json();
}
```

---

## 🧪 Pruebas

### Health Check
```bash
curl https://trashmap-demo.onrender.com/health
```

### Ver reports
```bash
curl https://trashmap-demo.onrender.com/api/v1/reports
```

### Filtrar por tipo de residuo
```bash
curl 'https://trashmap-demo.onrender.com/api/v1/reports?waste_type=plastico'
```

---

## 🎨 Personalización

### Color markers según tipo:
```javascript
const colors = {
    plastico: '#ff6b6b',
    organico: '#51cf66',
    electronico: '#339af0',
    construccion: '#fcc419',
    mixto: '#cc5de8'
};

const markerColor = colors[report.waste_type] || '#888';

const marker = new maplibregl.Marker({
    color: markerColor
})
```

### Filtros por ciudad:
```javascript
async function loadReportsByCity(city) {
    const response = await fetch(
        `https://trashmap-demo.onrender.com/api/v1/reports?city=${city}`
    );
    return response.json();
}
```

---

## 📊 Estadísticas API

El backend incluye:
- GET `/api/v1/stats` - Estadísticas generales
- GET `/api/v1/stats/cities` - Resumen por ciudad
- GET `/api/v1/stats/types` - Resumen por tipo de residuo

---

## 🐛 Debugging

### CORS errors:
```javascript
// Frontend
fetch(url)
  .then(response => response.json())
  .catch(error => console.error('CORS Error:', error));
```

### Ver logs en Render:
1. Ve a dashboard.render.com
2. Click en tu servicio
3. Ver "Logs" tab

---

*Última actualización: 2026-03-15*  
*Backend: `trashmap-demo.onrender.com`*
