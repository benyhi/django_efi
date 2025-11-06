#!/bin/bash#!/bin/bash



# Colores para output# Script de instalación para el proyecto Django Rest Framework

RED='\033[0;31m'# Ejecutar desde la raíz del proyecto

GREEN='\033[0;32m'

YELLOW='\033[1;33m'echo "=== Instalación del Proyecto Airline Management API ==="

BLUE='\033[0;34m'

NC='\033[0m' # No Color# Verificar Python

python --version

# Función para imprimir mensajes con coloresif [ $? -ne 0 ]; then

print_success() {    echo "Error: Python no está instalado o no está en el PATH"

    echo -e "${GREEN}✅ $1${NC}"    exit 1

}fi



print_error() {# Crear entorno virtual

    echo -e "${RED}❌ ERROR: $1${NC}"echo "Creando entorno virtual..."

}python -m venv env



print_warning() {# Activar entorno virtual

    echo -e "${YELLOW}⚠️  WARNING: $1${NC}"echo "Activando entorno virtual..."

}if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then

    # Windows

print_info() {    source env/Scripts/activate

    echo -e "${BLUE}📋 $1${NC}"else

}    # Linux/Mac

    source env/bin/activate

print_header() {fi

    echo -e "${BLUE}========================================${NC}"

    echo -e "${BLUE}   🛫 Airline Management System${NC}"# Instalar dependencias

    echo -e "${BLUE}   Instalador automático para Linux/macOS${NC}"echo "Instalando dependencias..."

    echo -e "${BLUE}========================================${NC}"pip install -r requirements.txt

    echo

}# Cambiar al directorio del proyecto Django

cd airline_managment

# Función para verificar si un comando existe

command_exists() {# Hacer migraciones

    command -v "$1" >/dev/null 2>&1echo "Creando migraciones..."

}python manage.py makemigrations



# Función para verificar Pythonecho "Aplicando migraciones..."

check_python() {python manage.py migrate

    if command_exists python3; then

        PYTHON_CMD="python3"# Crear superusuario

        PIP_CMD="pip3"echo "Creando superusuario..."

    elif command_exists python; thenecho "Por favor, ingresa los datos del administrador:"

        PYTHON_CMD="python"python manage.py createsuperuser

        PIP_CMD="pip"

    else# Mensaje de finalización

        print_error "Python no está instalado"echo ""

        print_info "Instala Python desde: https://www.python.org/downloads/"echo "=== Instalación completada ==="

        print_info "O usa tu gestor de paquetes:"echo ""

        print_info "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"echo "Para iniciar el servidor, ejecuta:"

        print_info "  macOS: brew install python3"echo "cd airline_managment"

        print_info "  CentOS/RHEL: sudo yum install python3 python3-pip"echo "python manage.py runserver"

        exit 1echo ""

    fiecho "URLs importantes:"

}echo "- Aplicación web: http://127.0.0.1:8000/"

echo "- Admin: http://127.0.0.1:8000/admin/"

# Función principalecho "- API: http://127.0.0.1:8000/api/v1/"

main() {echo "- Documentación API: http://127.0.0.1:8000/api/v1/docs/"

    print_headerecho "- ReDoc: http://127.0.0.1:8000/api/v1/redoc/"
    
    # Verificar Python
    check_python
    print_success "Python detectado: $($PYTHON_CMD --version)"
    
    # Verificar pip
    if ! command_exists $PIP_CMD; then
        print_error "pip no está disponible"
        exit 1
    fi
    print_success "pip detectado correctamente"
    
    # Verificar directorio del proyecto
    if [ ! -d "airline_managment" ]; then
        print_error "No se encontró el directorio del proyecto 'airline_managment'"
        print_info "Asegúrate de ejecutar este script desde la raíz del proyecto"
        exit 1
    fi
    print_success "Directorio del proyecto encontrado"
    
    # Crear entorno virtual
    echo
    print_info "🔧 Creando entorno virtual..."
    $PYTHON_CMD -m venv env
    if [ $? -ne 0 ]; then
        print_error "No se pudo crear el entorno virtual"
        exit 1
    fi
    print_success "Entorno virtual creado exitosamente"
    
    # Activar entorno virtual
    echo
    print_info "🔌 Activando entorno virtual..."
    source env/bin/activate
    if [ $? -ne 0 ]; then
        print_error "No se pudo activar el entorno virtual"
        exit 1
    fi
    print_success "Entorno virtual activado"
    
    # Actualizar pip
    echo
    print_info "📦 Actualizando pip..."
    python -m pip install --upgrade pip
    
    # Verificar requirements.txt
    if [ ! -f "requirements.txt" ]; then
        print_error "No se encontró el archivo requirements.txt"
        exit 1
    fi
    
    # Instalar dependencias
    echo
    print_info "📋 Instalando dependencias desde requirements.txt..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        print_error "Falló la instalación de dependencias"
        exit 1
    fi
    print_success "Dependencias instaladas correctamente"
    
    # Cambiar al directorio de Django
    cd airline_managment
    
    # Aplicar migraciones
    echo
    print_info "🗃️  Configurando base de datos (migraciones)..."
    python manage.py migrate
    if [ $? -ne 0 ]; then
        print_error "Falló al aplicar migraciones"
        exit 1
    fi
    print_success "Base de datos configurada correctamente"
    
    # Ejecutar tests
    echo
    print_info "🧪 Ejecutando tests para verificar instalación..."
    python manage.py test --verbosity=0
    if [ $? -ne 0 ]; then
        print_warning "Algunos tests fallaron, pero el sistema puede funcionar"
    else
        print_success "Todos los tests pasaron correctamente"
    fi
    
    # Poblar base de datos con datos de prueba (opcional)
    echo
    read -p "🌱 ¿Deseas poblar la base de datos con datos de prueba? (s/n): " seed_data
    if [[ $seed_data =~ ^[Ss]$ ]]; then
        print_info "📊 Poblando base de datos con datos de prueba..."
        python manage.py seed_data
    else
        # Crear superusuario (opcional) si no se pobló con datos
        read -p "👤 ¿Deseas crear un superusuario ahora? (s/n): " create_superuser
        if [[ $create_superuser =~ ^[Ss]$ ]]; then
            print_info "📝 Creando superusuario..."
            python manage.py createsuperuser
        fi
    fi
    
    # Información final
    echo
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}   🎉 INSTALACIÓN COMPLETADA${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo
    print_info "🚀 Para iniciar el servidor ejecuta:"
    echo "    cd airline_managment"
    echo "    source ../env/bin/activate"
    echo "    python manage.py runserver"
    echo
    print_info "📖 URLs importantes:"
    echo "    - API: http://127.0.0.1:8000/"
    echo "    - Swagger: http://127.0.0.1:8000/swagger/"
    echo "    - Admin: http://127.0.0.1:8000/admin/"
    echo
    print_info "📁 Archivos importantes:"
    echo "    - Colección Postman: Airline_Management_API.postman_collection.json"
    echo "    - Documentación: README.md"
    echo
    print_success "El proyecto está listo para usar!"
    echo
}

# Verificar si el script se ejecuta correctamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi