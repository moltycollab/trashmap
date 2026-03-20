#!/bin/bash
# 🚀 TrashMap Deployment Script
# Deploy TrashMap backend to Render (free tier)

set -e  # Exit on error

echo "🦞 TrashMap Deployment Script"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if user is logged into GitHub
echo -e "${BLUE}1. Verificando GitHub...${NC}"
if ! gh auth status &> /dev/null; then
    echo "❌ No estás logueado en GitHub"
    echo "   Ejecuta: gh auth login"
    exit 1
fi
echo -e "${GREEN}✓ GitHub autenticado${NC}"
echo ""

# Create GitHub repository for TrashMap
echo -e "${BLUE}2. Creando repositorio GitHub para TrashMap...${NC}"
REPO_NAME="trashmap-demo"

if gh repo view "$REPO_NAME" &> /dev/null; then
    echo "⚠️  Repo $REPO_NAME ya existe"
    read -p "¿Deseas usar el repo existente? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        read -p "Nuevo nombre: " REPO_NAME
    fi
else
    gh repo create "$REPO_NAME" --public --description "TrashMap - Plataforma de reporte de basurales informales en Venezuela" --source=. --remote=origin
fi
echo -e "${GREEN}✓ Repo $REPO_NAME creado${NC}"
echo ""

# Initialize git if not already done
echo -e "${BLUE}3. Verificando git...${NC}"
if [ ! -d .git ]; then
    git init
    git add .
    git commit -m "Initial TrashMap commit"
else
    git add .
    git commit -m "Update: $(date -u +"%Y-%m-%d %H:%M:%S UTC")"
fi
echo -e "${GREEN}✓ Git inicializado${NC}"
echo ""

# Ask for Render deployment
echo -e "${BLUE}4. Preparando para Render...${NC}"
echo ""
echo "Render URL objetivo: $REPO_NAME.onrender.com"
echo ""
read -p "¿Deseas desplegar ahora a Render? (y/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}🔄 Desplegando a Render...${NC}"

    # Create .render.yaml for Render deployment
    cat > .render.yaml << 'EOF'
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
EOF

    git add .render.yaml
    git commit -m "Add Render deployment configuration"
    git push origin main

    echo ""
    echo -e "${GREEN}✓ Despliegue iniciado a Render${NC}"
    echo ""
    echo "⚠️  TIEMPO DE ESPERA:"
    echo "   - Render toma 3-5 minutos para detectar el push"
    echo "   - Build toma 2-3 minutos"
    echo "   - Total: aprox 5-8 minutos"
    echo ""
    echo "📍 Para verificar:"
    echo "   https://dashboard.render.com"
    echo ""
else
    echo "✓ Configuración guardada en git"
    echo ""
    echo "Para desplegar manualmente:"
    echo "1. Ve a https://dashboard.render.com"
    echo "2. Click en 'New' > 'Web Service'"
    echo "3. Conecta tu repo de GitHub"
    echo "4. Configura:"
    echo "   - Build command: pip install -r requirements.txt"
    echo "   - Start command: uvicorn main:app --host 0.0.0.0 --port $PORT"
    echo "   - Root directory: backend"
fi

echo ""
echo -e "${GREEN}🎉 ¡Listo!${NC}"
echo ""
echo "Próximos pasos:"
echo "1. Verifica que el deploy fue exitoso en dashboard.render.com"
echo "2. Prueba el health check: curl https://$REPO_NAME.onrender.com/health"
echo "3. Configura frontend para conectar a tu API"
echo ""
