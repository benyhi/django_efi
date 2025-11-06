#!/bin/bash

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con colores
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ ERROR: $1${NC}"
}

print_info() {
    echo -e "${BLUE}📋 $1${NC}"
}

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   🛫 Airline Management System${NC}"
echo -e "${BLUE}   Iniciador rápido${NC}"
echo -e "${BLUE}========================================${NC}"

# Verificar si existe el entorno virtual
if [ ! -f "env/bin/activate" ]; then
    print_error "Entorno virtual no encontrado"
    print_info "Ejecuta primero: ./install.sh"
    exit 1
fi

# Activar entorno virtual
print_info "🔌 Activando entorno virtual..."
source env/bin/activate

# Cambiar al directorio de Django
cd airline_managment

# Aplicar migraciones (por si hay cambios)
print_info "🗃️  Verificando base de datos..."
python manage.py migrate --verbosity=0

# Mostrar información
echo
print_success "Sistema listo!"
print_info "🌐 El servidor se iniciará en: http://127.0.0.1:8000/"
echo
print_info "📖 URLs disponibles:"
echo "    - API Home: http://127.0.0.1:8000/"
echo "    - Swagger: http://127.0.0.1:8000/swagger/"
echo "    - Admin: http://127.0.0.1:8000/admin/"
echo
print_info "🔄 Presiona Ctrl+C para detener el servidor"
echo

# Iniciar servidor
print_info "🚀 Iniciando servidor Django..."
python manage.py runserver