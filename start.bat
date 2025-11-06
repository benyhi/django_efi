@echo off
echo ========================================
echo   🛫 Airline Management System
echo   Iniciador rapido
echo ========================================

:: Verificar si existe el entorno virtual
if not exist "env\Scripts\activate.bat" (
    echo ❌ ERROR: Entorno virtual no encontrado
    echo 📋 Ejecuta primero: install.bat
    pause
    exit /b 1
)

:: Activar entorno virtual
echo 🔌 Activando entorno virtual...
call env\Scripts\activate.bat

:: Cambiar al directorio de Django
cd airline_managment

:: Aplicar migraciones (por si hay cambios)
echo 🗃️  Verificando base de datos...
python manage.py migrate --verbosity=0

:: Mostrar información
echo.
echo ✅ Sistema listo!
echo 🌐 El servidor se iniciará en: http://127.0.0.1:8000/
echo.
echo 📖 URLs disponibles:
echo    - API Home: http://127.0.0.1:8000/
echo    - Swagger: http://127.0.0.1:8000/swagger/
echo    - Admin: http://127.0.0.1:8000/admin/
echo.
echo 🔄 Presiona Ctrl+C para detener el servidor
echo.

:: Iniciar servidor
echo 🚀 Iniciando servidor Django...
python manage.py runserver