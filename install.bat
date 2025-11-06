@echo off@echo off

echo ========================================REM Script de instalación para Windows

echo   🛫 Airline Management SystemREM Ejecutar desde la raíz del proyecto

echo   Instalador automatico para Windows

echo ========================================echo === Instalación del Proyecto Airline Management API ===

echo.

REM Verificar Python

:: Verificar si Python esta instaladopython --version

python --version >nul 2>&1if errorlevel 1 (

if %errorlevel% neq 0 (    echo Error: Python no está instalado o no está en el PATH

    echo ❌ ERROR: Python no esta instalado o no esta en el PATH    pause

    echo 📋 Instala Python desde: https://www.python.org/downloads/    exit /b 1

    echo ⚠️  Asegurate de marcar "Add Python to PATH" durante la instalacion)

    pause

    exit /b 1REM Crear entorno virtual

)echo Creando entorno virtual...

python -m venv env

echo ✅ Python detectado correctamente

python --versionREM Activar entorno virtual

echo Activando entorno virtual...

:: Verificar si pip esta disponiblecall env\Scripts\activate.bat

pip --version >nul 2>&1

if %errorlevel% neq 0 (REM Instalar dependencias

    echo ❌ ERROR: pip no esta disponibleecho Instalando dependencias...

    pausepip install -r requirements.txt

    exit /b 1

)REM Cambiar al directorio del proyecto Django

cd airline_managment

echo ✅ pip detectado correctamente

REM Hacer migraciones

:: Crear directorio del proyecto si no existeecho Creando migraciones...

if not exist "airline_managment" (python manage.py makemigrations

    echo ❌ ERROR: No se encontro el directorio del proyecto 'airline_managment'

    echo 📁 Asegurate de ejecutar este script desde la raiz del proyectoecho Aplicando migraciones...

    pausepython manage.py migrate

    exit /b 1

)REM Crear superusuario

echo Creando superusuario...

echo 📁 Directorio del proyecto encontradoecho Por favor, ingresa los datos del administrador:

python manage.py createsuperuser

:: Crear entorno virtual

echo.REM Mensaje de finalización

echo 🔧 Creando entorno virtual...echo.

python -m venv envecho === Instalación completada ===

if %errorlevel% neq 0 (echo.

    echo ❌ ERROR: No se pudo crear el entorno virtualecho Para iniciar el servidor, ejecuta:

    pauseecho cd airline_managment

    exit /b 1echo python manage.py runserver

)echo.

echo URLs importantes:

echo ✅ Entorno virtual creado exitosamenteecho - Aplicación web: http://127.0.0.1:8000/

echo - Admin: http://127.0.0.1:8000/admin/

:: Activar entorno virtualecho - API: http://127.0.0.1:8000/api/v1/

echo.echo - Documentación API: http://127.0.0.1:8000/api/v1/docs/

echo 🔌 Activando entorno virtual...echo - ReDoc: http://127.0.0.1:8000/api/v1/redoc/

call env\Scripts\activate.bat

if %errorlevel% neq 0 (pause
    echo ❌ ERROR: No se pudo activar el entorno virtual
    pause
    exit /b 1
)

echo ✅ Entorno virtual activado

:: Actualizar pip
echo.
echo 📦 Actualizando pip...
python -m pip install --upgrade pip

:: Instalar dependencias
echo.
echo 📋 Instalando dependencias desde requirements.txt...
if not exist "requirements.txt" (
    echo ❌ ERROR: No se encontro el archivo requirements.txt
    pause
    exit /b 1
)

pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ ERROR: Fallo la instalacion de dependencias
    pause
    exit /b 1
)

echo ✅ Dependencias instaladas correctamente

:: Cambiar al directorio de Django
cd airline_managment

:: Aplicar migraciones
echo.
echo 🗃️  Configurando base de datos (migraciones)...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ❌ ERROR: Fallo al aplicar migraciones
    pause
    exit /b 1
)

echo ✅ Base de datos configurada correctamente

:: Ejecutar tests
echo.
echo 🧪 Ejecutando tests para verificar instalacion...
python manage.py test --verbosity=0
if %errorlevel% neq 0 (
    echo ⚠️  WARNING: Algunos tests fallaron, pero el sistema puede funcionar
) else (
    echo ✅ Todos los tests pasaron correctamente
)

:: Poblar base de datos con datos de prueba (opcional)
echo.
echo 🌱 ¿Deseas poblar la base de datos con datos de prueba? (s/n)
set /p seed_data=
if /i "%seed_data%"=="s" (
    echo 📊 Poblando base de datos con datos de prueba...
    python manage.py seed_data
) else (
    :: Crear superusuario (opcional) si no se pobló con datos
    echo 👤 ¿Deseas crear un superusuario ahora? (s/n)
    set /p create_superuser=
    if /i "%create_superuser%"=="s" (
        echo 📝 Creando superusuario...
        python manage.py createsuperuser
    )
)

:: Mostrar informacion final
echo.
echo ========================================
echo   🎉 INSTALACION COMPLETADA
echo ========================================
echo.
echo 🚀 Para iniciar el servidor ejecuta:
echo    cd airline_managment
echo    env\Scripts\activate
echo    python manage.py runserver
echo.
echo 📖 URLs importantes:
echo    - API: http://127.0.0.1:8000/
echo    - Swagger: http://127.0.0.1:8000/swagger/
echo    - Admin: http://127.0.0.1:8000/admin/
echo.
echo 📁 Archivos importantes:
echo    - Coleccion Postman: Airline_Management_API.postman_collection.json
echo    - Documentacion: README.md
echo.
echo ✅ El proyecto esta listo para usar!
echo.

pause