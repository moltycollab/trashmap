#!/bin/bash
# TrashMap - Post-Deploy Verification Script
# Usage: ./verify-deploy.sh https://trashmap-api.onrender.com

BASE_URL="${1:-https://trashmap-api.onrender.com}"

echo "🔍 Verificando TrashMap API en: $BASE_URL"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS=0
FAIL=0

check() {
    local name="$1"
    local expected="$2"
    local actual="$3"
    
    if [[ "$actual" == *"$expected"* ]] || [[ "$expected" == "any" && -n "$actual" ]]; then
        echo -e "${GREEN}✅ PASS${NC}: $name"
        ((PASS++))
    else
        echo -e "${RED}❌ FAIL${NC}: $name"
        echo "   Esperado: $expected"
        echo "   Recibido: $actual"
        ((FAIL++))
    fi
}

# Test 1: Health check
echo "📋 Health Check"
health=$(curl -s "$BASE_URL/health" 2>/dev/null)
check "GET /health" "healthy" "$health"
echo ""

# Test 2: Get all reports
echo "📋 Reports Endpoint"
reports=$(curl -s "$BASE_URL/reports" 2>/dev/null)
check "GET /reports" "reports" "$reports"
count=$(echo "$reports" | grep -o '"id"' | wc -l)
echo "   Total reportes: $count"
echo ""

# Test 3: Statistics
echo "📋 Statistics"
stats=$(curl -s "$BASE_URL/stats" 2>/dev/null)
check "GET /stats" "total" "$stats"
echo ""

# Test 4: Cities
echo "📋 Cities"
cities=$(curl -s "$BASE_URL/stats/by-city" 2>/dev/null)
check "GET /stats/by-city" "city" "$cities"
echo ""

# Test 5: API Docs
echo "📋 API Documentation"
docs=$(curl -s "$BASE_URL/docs" 2>/dev/null)
check "GET /docs" "swagger" "$docs"
echo ""

# Summary
echo "========================================"
echo -e "Resultados: ${GREEN}$PASS passed${NC}, ${RED}$FAIL failed${NC}"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}🎉 Todos los checks pasaron! TrashMap está listo.${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  Algunos checks fallaron. Revisar logs.${NC}"
    exit 1
fi
