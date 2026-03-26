#!/bin/bash
# TrashMap Deploy Script
# Usage: ./deploy-trashmap.sh [platform]
# Platforms: render, railway, fly

PLATFORM=${1:-railway}

echo "🚀 Deploying TrashMap to $PLATFORM..."

case $PLATFORM in
  railway)
    echo "📦 Using Railway..."
    # Railway CLI deploy
    # railway init --primary
    # railway up
    echo "⚠️ Requiere Railway CLI instalado y autenticado"
    echo "📋 Pasos manuales:"
    echo "   1. railway login"
    echo "   2. railway init --primary"
    echo "   3. railway up"
    echo "   4. railway domain set"
    ;;
  render)
    echo "📦 Using Render..."
    # Render deploy via blueprint
    # render-blueprint apply render.yaml
    echo "⚠️ Requiere:"
    echo "   1. RENDER_API_KEY configurado"
    echo "   2. gh repo moltycollab/platform conectado"
    ;;
  fly)
    echo "📦 Using Fly.io..."
    # Fly.io deploy
    # fly launch --org personal --name trashmap
    # fly deploy
    echo "⚠️ Requiere Fly CLI instalado"
    ;;
  *)
    echo "❌ Plataforma desconocida: $PLATFORM"
    echo "Usage: $0 [render|railway|fly]"
    exit 1
    ;;
esac

echo "✅ Script preparado para $PLATFORM"
echo "📁 Backend: /home/orion/clawd/projects/trashmap/backend/"
echo "📁 Frontend: /home/orion/clawd/projects/trashmap/frontend/"