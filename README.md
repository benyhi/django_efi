# 🛫 Airline Management System# 🛫 Airline Management System# 🛫 Airline Management System - API REST# 🛫 Airline Management System - API REST# Airline Management System - Django Rest Framework



API REST para gestión de aerolíneas con Django REST Framework. Permite administrar vuelos, reservas, pasajeros y asientos.



## 🚀 Stack TecnológicoAPI REST para gestión de aerolíneas con Django REST Framework. Permite administrar vuelos, reservas, pasajeros y asientos.



- **Backend**: Django 5.2.4 + DRF 3.15.2

- **Autenticación**: JWT con blacklist

- **Base de datos**: SQLite## 🚀 Stack TecnológicoSistema de gestión de aerolíneas desarrollado con Django REST Framework (DRF) que permite administrar vuelos, pasajeros, reservas, asientos y boletos de manera eficiente y profesional.

- **Documentación**: Swagger/OpenAPI

- **Tests**: 70+ tests automatizados



## ⚡ Instalación Rápida- **Backend**: Django 5.2.4 + DRF 3.15.2



**Windows:**- **Autenticación**: JWT con blacklist

```cmd

install.bat- **Base de datos**: SQLite## 🚀 Características principalesSistema de gestión de aerolíneas desarrollado con Django REST Framework (DRF) que permite administrar vuelos, pasajeros, reservas, asientos y boletos de manera eficiente y profesional.Un sistema completo de gestión de aerolíneas desarrollado con Django Rest Framework que proporciona una API REST robusta para la gestión de vuelos, pasajeros, reservas y boletos.

```

- **Documentación**: Swagger/OpenAPI

**Linux/macOS:**

```bash- **Tests**: 70+ tests automatizados

chmod +x install.sh && ./install.sh

```



**Ejecución:**## ⚡ Instalación Rápida- **Gestión de Vuelos**: Crear, actualizar, listar y eliminar vuelos

```cmd

start.bat        # Windows

./start.sh       # Linux/macOS

```**Windows:**- **Administración de Aviones**: Gestión completa de la flota de aviones



## 📋 Endpoints Principales```cmd



### Autenticacióninstall.bat- **Sistema de Reservas**: Reservar, confirmar y cancelar reservas de vuelos## 🚀 Características principales## 🚀 Características Principales

- `POST /auth/login/` - Iniciar sesión

- `POST /auth/register/` - Registrar usuario```

- `POST /auth/logout/` - Cerrar sesión

- **Gestión de Pasajeros**: Registro y administración de información de pasajeros

### Vuelos

- `GET /flights/` - Listar vuelos**Linux/macOS:**

- `POST /flights/` - Crear vuelo (admin)

- `GET /flights/search/` - Buscar vuelos```bash- **Control de Asientos**: Asignación automática y manual de asientos



### Reservaschmod +x install.sh && ./install.sh

- `GET /reservations/` - Listar reservas

- `POST /reservations/` - Crear reserva```- **Boletos Electrónicos**: Generación y validación de tickets con códigos de barras

- `PATCH /reservations/{id}/confirm/` - Confirmar reserva



### Pasajeros

- `GET /passengers/` - Listar pasajeros**Ejecución:**- **Autenticación JWT**: Sistema seguro de autenticación con tokens- **Gestión de Vuelos**: Crear, actualizar, listar y eliminar vuelos### ✅ Funcionalidades Implementadas

- `POST /passengers/` - Registrar pasajero

```cmd

## 🌱 Datos de Prueba

start.bat        # Windows- **Documentación API**: Swagger/OpenAPI integrado para documentación automática

**Poblar base de datos automáticamente:**

```bash./start.sh       # Linux/macOS

cd airline_managment

python manage.py seed_data```- **Reportes PDF**: Generación de reportes de vuelos en formato PDF- **Administración de Aviones**: Gestión completa de la flota de aviones

```



**Credenciales incluidas:**

- Admin: `admin/admin123`## 📋 Endpoints Principales

- Usuario: `testuser/test123`



**Datos incluidos:**

- 5 aviones diferentes (Boeing, Airbus, etc.)### Autenticación## 🏗️ Arquitectura técnica- **Sistema de Reservas**: Reservar, confirmar y cancelar reservas de vuelos#### Gestión de Vuelos (API)

- 12 vuelos programados (nacionales e internacionales)

- 8 pasajeros de prueba- `POST /auth/login/` - Iniciar sesión

- Reservas y tickets activos

- `POST /auth/register/` - Registrar usuario

## 📁 Estructura del Proyecto

- `POST /auth/logout/` - Cerrar sesión

```

airline_managment/- **Backend**: Django 5.2.4 + Django REST Framework 3.15.2- **Gestión de Pasajeros**: Registro y administración de información de pasajeros- ✅ Listar todos los vuelos disponibles

├── flight/         # Vuelos y aviones

├── passenger/      # Gestión de pasajeros### Vuelos

├── reservation/    # Reservas, asientos y tickets

├── user/          # Autenticación y usuarios- `GET /flights/` - Listar vuelos- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)

└── manage.py      # Django CLI

```- `POST /flights/` - Crear vuelo (admin)



## 📖 Documentación API- `GET /flights/search/` - Buscar vuelos- **Autenticación**: JWT con tokens de refresco y blacklist- **Control de Asientos**: Asignación automática y manual de asientos- ✅ Obtener detalle de un vuelo



- **Swagger**: http://127.0.0.1:8000/swagger/

- **Admin**: http://127.0.0.1:8000/admin/

- **Postman**: `Airline_Management_API.postman_collection.json`### Reservas- **Documentación**: drf-yasg (Swagger/OpenAPI)



## 🧪 Testing- `GET /reservations/` - Listar reservas



```bash- `POST /reservations/` - Crear reserva- **Testing**: 70+ tests automatizados con cobertura completa- **Boletos Electrónicos**: Generación y validación de tickets con códigos de barras- ✅ Filtrar vuelos por origen, destino y fecha

cd airline_managment

python manage.py test- `PATCH /reservations/{id}/confirm/` - Confirmar reserva

```

- **PDF Generation**: WeasyPrint para reportes

---

*Desarrollado con Django REST Framework*### Pasajeros

- `GET /passengers/` - Listar pasajeros- **Autenticación JWT**: Sistema seguro de autenticación con tokens- ✅ Crear, editar y eliminar vuelos (solo administradores)

- `POST /passengers/` - Registrar pasajero

## 📋 Endpoints principales

## 📁 Estructura del Proyecto

- **Documentación API**: Swagger/OpenAPI integrado para documentación automática- ✅ Consultar asientos disponibles por vuelo

```

airline_managment/### Autenticación

├── flight/         # Vuelos y aviones

├── passenger/      # Gestión de pasajeros- `POST /auth/login/` - Iniciar sesión- **Reportes PDF**: Generación de reportes de vuelos en formato PDF- ✅ Visualizar mapa de asientos

├── reservation/    # Reservas, asientos y tickets

├── user/          # Autenticación y usuarios- `POST /auth/register/` - Registrar usuario

└── manage.py      # Django CLI

```- `POST /auth/logout/` - Cerrar sesión



## 📖 Documentación API- `POST /auth/token/refresh/` - Renovar token



- **Swagger**: http://127.0.0.1:8000/swagger/## 🏗️ Arquitectura técnica#### Gestión de Pasajeros (API)

- **Admin**: http://127.0.0.1:8000/admin/

- **Postman**: `Airline_Management_API.postman_collection.json`### Gestión de Vuelos



## 🧪 Testing- `GET /flights/` - Listar vuelos- ✅ Registrar un pasajero



```bash- `POST /flights/` - Crear vuelo (admin)

cd airline_managment

python manage.py test- `GET /flights/{id}/` - Detalle de vuelo- **Backend**: Django 5.2.4 + Django REST Framework 3.15.2- ✅ Consultar información de un pasajero

```

- `PUT/PATCH /flights/{id}/` - Actualizar vuelo (admin)

---

*Desarrollado con Django REST Framework*- `DELETE /flights/{id}/` - Eliminar vuelo (admin)- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)- ✅ Listar reservas asociadas a un pasajero

- `GET /flights/search/` - Buscar vuelos

- **Autenticación**: JWT con tokens de refresco y blacklist- ✅ Búsqueda por DNI y email

### Aviones

- `GET /planes/` - Listar aviones- **Documentación**: drf-yasg (Swagger/OpenAPI)- ✅ Validaciones de datos únicos

- `POST /planes/` - Crear avión (admin)

- `GET /planes/{id}/seats/` - Ver asientos del avión- **Testing**: 70+ tests automatizados con cobertura completa



### Reservas- **PDF Generation**: WeasyPrint para reportes#### Sistema de Reservas (API)

- `GET /reservations/` - Listar reservas

- `POST /reservations/` - Crear reserva- ✅ Crear una reserva para un pasajero en un vuelo

- `PATCH /reservations/{id}/confirm/` - Confirmar reserva

- `PATCH /reservations/{id}/cancel/` - Cancelar reserva## 📋 Endpoints principales- ✅ Seleccionar asiento disponible



### Pasajeros- ✅ Cambiar estado de una reserva (confirmar, cancelar)

- `GET /passengers/` - Listar pasajeros

- `POST /passengers/` - Registrar pasajero### Autenticación- ✅ Validaciones de disponibilidad en tiempo real

- `GET /passengers/{id}/reservations/` - Reservas del pasajero

- `POST /auth/login/` - Iniciar sesión

## 🛠️ Instalación rápida

- `POST /auth/register/` - Registrar usuario#### Gestión de Aviones y Asientos (API)

### Opción 1: Script automático (Recomendado)

- `POST /auth/logout/` - Cerrar sesión- ✅ Listar aviones registrados

1. **Windows**:

   ```cmd- `POST /auth/token/refresh/` - Renovar token- ✅ Obtener layout de asientos de un avión

   # Doble clic en install.bat o ejecutar en terminal

   install.bat- ✅ Verificar disponibilidad de un asiento en un vuelo

   ```

### Gestión de Vuelos- ✅ Gestión automática de asientos por avión

2. **Linux/macOS**:

   ```bash- `GET /flights/` - Listar vuelos

   chmod +x install.sh

   ./install.sh- `POST /flights/` - Crear vuelo (admin)#### Boletos (API)

   ```

- `GET /flights/{id}/` - Detalle de vuelo- ✅ Generar boleto automáticamente al confirmar reserva

### 🚀 Ejecución rápida

- `PUT/PATCH /flights/{id}/` - Actualizar vuelo (admin)- ✅ Consultar información de un boleto por código de barras

Una vez instalado, usa los scripts de inicio rápido:

- `DELETE /flights/{id}/` - Eliminar vuelo (admin)- ✅ Búsqueda por código de reserva

**Windows**:

```cmd- `GET /flights/search/` - Buscar vuelos

start.bat

```#### Reportes (API)



**Linux/macOS**:### Aviones- ✅ Endpoint para obtener listado de pasajeros por vuelo

```bash

chmod +x start.sh- `GET /planes/` - Listar aviones- ✅ Endpoint para obtener reservas activas de un pasajero

./start.sh

```- `POST /planes/` - Crear avión (admin)- ✅ Estadísticas de vuelos, reservas y pasajeros



### Opción 2: Instalación manual- `GET /planes/{id}/seats/` - Ver asientos del avión



1. **Clonar el repositorio**:#### Autenticación y Seguridad

   ```bash

   git clone https://github.com/benyhi/django_efi.git### Reservas- ✅ Autenticación JWT (JSON Web Tokens)

   cd django_efi

   ```- `GET /reservations/` - Listar reservas- ✅ Registro y login de usuarios



2. **Crear entorno virtual**:- `POST /reservations/` - Crear reserva- ✅ Gestión de permisos por roles (Usuario/Administrador)

   ```bash

   python -m venv env- `PATCH /reservations/{id}/confirm/` - Confirmar reserva- ✅ Renovación automática de tokens

   

   # Windows- `PATCH /reservations/{id}/cancel/` - Cancelar reserva

   env\Scripts\activate

   #### Documentación

   # Linux/macOS

   source env/bin/activate### Pasajeros- ✅ Documentación interactiva con Swagger UI

   ```

- `GET /passengers/` - Listar pasajeros- ✅ Documentación alternativa con ReDoc

3. **Instalar dependencias**:

   ```bash- `POST /passengers/` - Registrar pasajero- ✅ Esquemas de API auto-generados

   pip install -r requirements.txt

   ```- `GET /passengers/{id}/reservations/` - Reservas del pasajero



4. **Configurar base de datos**:## 🏗️ Arquitectura

   ```bash

   cd airline_managment## 🛠️ Instalación rápida

   python manage.py migrate

   ```### Patrón Service-Repository



5. **Crear superusuario**:### Opción 1: Script automático (Recomendado)El proyecto implementa el patrón Service-Repository para una arquitectura limpia y mantenible:

   ```bash

   python manage.py createsuperuser

   ```

1. **Windows**:```

6. **Ejecutar servidor**:

   ```bash   ```bash┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐

   python manage.py runserver

   ```   # Ejecutar como administrador│    ViewSets     │ -> │    Services     │ -> │  Repositories   │



## 🧪 Testing   .\install.bat│   (API Views)   │    │ (Business Logic)│    │ (Data Access)   │



Ejecutar la suite completa de tests (70 tests):   ```└─────────────────┘    └─────────────────┘    └─────────────────┘



```bash```

cd airline_managment

python manage.py test2. **Linux/macOS**:

```

   ```bash### Tecnologías Utilizadas

Ejecutar tests con cobertura:

```bash   chmod +x install.sh- **Django 5.2.4**: Framework web principal

python manage.py test --verbosity=2

```   ./install.sh- **Django Rest Framework**: API REST



## 📖 Documentación de la API   ```- **Django Rest Framework SimpleJWT**: Autenticación JWT



Una vez ejecutando el servidor, accede a:- **drf-yasg**: Documentación Swagger



- **Swagger UI**: http://127.0.0.1:8000/swagger/### Opción 2: Instalación manual- **django-filter**: Filtros avanzados

- **ReDoc**: http://127.0.0.1:8000/redoc/

- **JSON Schema**: http://127.0.0.1:8000/swagger.json/- **django-cors-headers**: Soporte CORS



## 🔐 Autenticación1. **Clonar el repositorio**:



El sistema usa JWT (JSON Web Tokens) para autenticación:   ```bash## 📁 Estructura del Proyecto



1. **Registro/Login**: Obtén tokens de acceso y refresco   git clone https://github.com/benyhi/django_efi.git

2. **Autorización**: Include `Authorization: Bearer <access_token>` en headers

3. **Renovación**: Usa el refresh token cuando el access token expire   cd django_efi```

4. **Logout**: El refresh token se añade a blacklist

   ```airline_managment/

### Ejemplo de uso:

├── airline_managment/          # Configuración principal

```bash

# 1. Registrar usuario2. **Crear entorno virtual**:│   ├── settings.py            # Configuraciones de Django y DRF

curl -X POST http://127.0.0.1:8000/auth/register/ \

  -H "Content-Type: application/json" \   ```bash│   ├── urls.py               # URLs principales

  -d '{"username": "usuario", "email": "test@test.com", "password": "pass123"}'

   python -m venv env│   ├── api_urls.py           # URLs de la API

# 2. Hacer petición autenticada

curl -X GET http://127.0.0.1:8000/flights/ \   │   ├── api_reports.py        # Endpoints de reportes

  -H "Authorization: Bearer <your_access_token>"

```   # Windows│   ├── permissions.py        # Permisos personalizados



## 📁 Estructura del proyecto   env\Scripts\activate│   ├── utils.py             # Utilidades y manejo de errores



```   │   ├── repositories/        # Repositorios base

airline_managment/

├── airline_managment/          # Configuración principal   # Linux/macOS│   └── services/           # Servicios base

│   ├── settings.py            # Configuración Django

│   ├── urls.py               # URLs principales   source env/bin/activate├── flight/                  # App de vuelos

│   └── views.py              # Vista home

├── flight/                   # App de vuelos   ```│   ├── models.py           # Modelos: Flight, Plane

│   ├── models.py            # Modelos Flight, Plane

│   ├── views.py             # ViewSets REST API│   ├── serializers.py      # Serializers de DRF

│   ├── serializers.py       # Serializers DRF

│   └── tests.py             # Tests automatizados3. **Instalar dependencias**:│   ├── api_views.py        # ViewSets y APIViews

├── passenger/               # App de pasajeros

├── reservation/            # App de reservas   ```bash│   ├── repositories.py     # Repositorios específicos

├── user/                  # App de usuarios

├── static/               # Archivos estáticos   pip install -r requirements.txt│   └── services.py         # Servicios específicos

└── templates/           # Templates HTML

```   ```├── passenger/              # App de pasajeros



## 🚦 Estados del sistema│   ├── models.py          # Modelos: Passenger



### Estados de vuelos:4. **Configurar base de datos**:│   ├── serializers.py     # Serializers de DRF

- `on_time` - A tiempo

- `delayed` - Retrasado   ```bash│   ├── api_views.py       # ViewSets y APIViews

- `cancelled` - Cancelado

- `boarding` - Abordando   cd airline_managment│   ├── repositories.py    # Repositorios específicos

- `departed` - Despegado

   python manage.py migrate│   └── services.py        # Servicios específicos

### Estados de reservas:

- `pending` - Pendiente   ```├── reservation/           # App de reservas

- `confirmed` - Confirmada

- `cancelled` - Cancelada│   ├── models.py         # Modelos: Reservation, Seat, Ticket



### Estados de asientos:5. **Crear superusuario**:│   ├── serializers.py    # Serializers de DRF

- `available` - Disponible

- `occupied` - Ocupado   ```bash│   ├── api_views.py      # ViewSets y APIViews

- `blocked` - Bloqueado

   python manage.py createsuperuser│   ├── repositories.py   # Repositorios específicos

## 📊 Colección de Postman

   ```│   └── services.py       # Servicios específicos

Se incluye una colección completa de Postman en `Airline_Management_API.postman_collection.json` con todos los endpoints configurados y ejemplos de uso.

└── user/                 # App de usuarios

## 🤝 Contribución

6. **Ejecutar servidor**:    ├── serializers.py    # Serializers de usuarios

1. Fork el proyecto

2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)   ```bash    ├── api_views.py      # Vistas de autenticación

3. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)

4. Push a la rama (`git push origin feature/nueva-funcionalidad`)   python manage.py runserver    └── api_urls.py       # URLs de autenticación

5. Crea un Pull Request

   ``````

## 📝 Licencia



Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🧪 Testing## 🚀 Instalación Rápida

## 👨‍💻 Desarrolladores



- **Equipo de desarrollo**: Sistema de gestión de aerolíneas

- **Tecnologías**: Django, DRF, JWT, Swagger, WeasyPrintEjecutar la suite completa de tests (70 tests):### Opción 1: Script Automático

- **Versión**: 2.0.0



---

```bash#### Windows:

*Desarrollado con ❤️ usando Django REST Framework*
cd airline_managment```bash

python manage.py testinstall.bat

``````



Ejecutar tests con cobertura:#### Linux/Mac:

```bash```bash

python manage.py test --verbosity=2chmod +x install.sh

```./install.sh

```

## 📖 Documentación de la API

### Opción 2: Instalación Manual

Una vez ejecutando el servidor, accede a:

1. **Clonar el repositorio**:

- **Swagger UI**: http://127.0.0.1:8000/swagger/```bash

- **ReDoc**: http://127.0.0.1:8000/redoc/git clone <url-del-repositorio>

- **JSON Schema**: http://127.0.0.1:8000/swagger.json/cd django_efi

```

## 🔐 Autenticación

2. **Crear entorno virtual**:

El sistema usa JWT (JSON Web Tokens) para autenticación:```bash

# Windows

1. **Registro/Login**: Obtén tokens de acceso y refrescopython -m venv env

2. **Autorización**: Include `Authorization: Bearer <access_token>` en headersenv\Scripts\activate

3. **Renovación**: Usa el refresh token cuando el access token expire

4. **Logout**: El refresh token se añade a blacklist# Linux/Mac

python3 -m venv env

### Ejemplo de uso:source env/bin/activate

```

```bash

# 1. Registrar usuario3. **Instalar dependencias**:

curl -X POST http://127.0.0.1:8000/auth/register/ \```bash

  -H "Content-Type: application/json" \pip install -r requirements.txt

  -d '{"username": "usuario", "email": "test@test.com", "password": "pass123"}'```



# 2. Hacer petición autenticada4. **Configurar base de datos**:

curl -X GET http://127.0.0.1:8000/flights/ \```bash

  -H "Authorization: Bearer <your_access_token>"cd airline_managment

```python manage.py makemigrations

python manage.py migrate

## 📁 Estructura del proyecto```



```5. **Crear superusuario**:

airline_managment/```bash

├── airline_managment/          # Configuración principalpython manage.py createsuperuser

│   ├── settings.py            # Configuración Django```

│   ├── urls.py               # URLs principales

│   └── views.py              # Vista home6. **Ejecutar servidor**:

├── flight/                   # App de vuelos```bash

│   ├── models.py            # Modelos Flight, Planepython manage.py runserver

│   ├── views.py             # ViewSets REST API```

│   ├── serializers.py       # Serializers DRF

│   └── tests.py             # Tests automatizados## 🌐 URLs Importantes

├── passenger/               # App de pasajeros

├── reservation/            # App de reservas- **Aplicación Web**: http://127.0.0.1:8000/

├── user/                  # App de usuarios- **Panel Admin**: http://127.0.0.1:8000/admin/

├── static/               # Archivos estáticos- **API Base**: http://127.0.0.1:8000/api/v1/

└── templates/           # Templates HTML- **Documentación Swagger**: http://127.0.0.1:8000/api/v1/docs/

```- **Documentación ReDoc**: http://127.0.0.1:8000/api/v1/redoc/



## 🚦 Estados del sistema## 📚 Documentación Detallada



### Estados de vuelos:- [**API Endpoints**](API_ENDPOINTS.md) - Documentación completa de todos los endpoints

- `on_time` - A tiempo- [**Guía de Instalación**](SETUP_GUIDE.md) - Instrucciones detalladas de instalación

- `delayed` - Retrasado- [**Guía de Migración**](MIGRATION_GUIDE.md) - Detalles del refactor a DRF

- `cancelled` - Cancelado

- `boarding` - Abordando## 🔐 Autenticación

- `departed` - Despegado

### Registro de Usuario

### Estados de reservas:```bash

- `pending` - PendientePOST /api/v1/auth/register/

- `confirmed` - ConfirmadaContent-Type: application/json

- `cancelled` - Cancelada

{

### Estados de asientos:    "username": "usuario",

- `available` - Disponible    "password": "contraseña123",

- `occupied` - Ocupado    "password_confirm": "contraseña123",

- `blocked` - Bloqueado    "email": "usuario@email.com",

    "first_name": "Nombre",

## 📊 Colección de Postman    "last_name": "Apellido"

}

Se incluye una colección completa de Postman en `Airline_Management_API.postman_collection.json` con todos los endpoints configurados y ejemplos de uso.```



## 🤝 Contribución### Login

```bash

1. Fork el proyectoPOST /api/v1/auth/login/

2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)Content-Type: application/json

3. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)

4. Push a la rama (`git push origin feature/nueva-funcionalidad`){

5. Crea un Pull Request    "username": "usuario",

    "password": "contraseña123"

## 📝 Licencia}

```

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

### Usar Token en Requests

## 👨‍💻 Desarrolladores```bash

Authorization: Bearer <access_token>

- **Equipo de desarrollo**: Sistema de gestión de aerolíneas```

- **Tecnologías**: Django, DRF, JWT, Swagger, WeasyPrint

- **Versión**: 2.0.0## 📊 Ejemplos de Uso de la API



---### Buscar Vuelos

```bash

*Desarrollado con ❤️ usando Django REST Framework*GET /api/v1/flights/flights/search/?origin=Madrid&destination=Barcelona&date=2024-12-01
Authorization: Bearer <token>
```

### Crear Reserva
```bash
POST /api/v1/reservations/reservations/
Authorization: Bearer <token>
Content-Type: application/json

{
    "flight_id": 1,
    "passenger_id": 1,
    "seat_id": 15,
    "price": 150.00
}
```

### Obtener Asientos Disponibles
```bash
GET /api/v1/reservations/seats/available_by_flight/?flight_id=1
Authorization: Bearer <token>
```

## 🔒 Sistema de Permisos

### Roles de Usuario
- **Usuario Autenticado**: Puede crear reservas, ver vuelos, gestionar su perfil
- **Administrador**: Acceso completo a gestión de vuelos, aviones, usuarios y reportes

### Permisos por Endpoint
- **Lectura**: Usuarios autenticados
- **Escritura de vuelos/aviones**: Solo administradores
- **Gestión de usuarios**: Solo administradores
- **Reportes avanzados**: Solo administradores

## 📈 Reportes Disponibles

### Para Administradores
```bash
# Pasajeros por vuelo
GET /api/v1/reports/passengers-by-flight/?flight_id=1

# Estadísticas de vuelos
GET /api/v1/reports/flight-statistics/

# Estadísticas de reservas
GET /api/v1/reports/reservation-statistics/
```

### Para Usuarios
```bash
# Reservas activas de un pasajero
GET /api/v1/reports/active-reservations-by-passenger/?passenger_id=1
```

## 🧪 Testing

```bash
# Ejecutar tests
python manage.py test

# Ejecutar tests con coverage
coverage run manage.py test
coverage report
```

## 🚀 Consideraciones Técnicas

### Validaciones Implementadas
- ✅ Validaciones en serializers y services
- ✅ Manejo de errores con respuestas HTTP apropiadas (400, 401, 404, 500)
- ✅ Validaciones de disponibilidad de asientos en tiempo real
- ✅ Validaciones de unicidad (DNI, email, número de vuelo)

### Buenas Prácticas
- ✅ Principios REST respetados
- ✅ Código documentado y limpio
- ✅ Separación de responsabilidades
- ✅ Manejo centralizado de errores
- ✅ Respuestas API estandarizadas

### Seguridad
- ✅ Autenticación JWT con expiración
- ✅ CORS configurado apropiadamente
- ✅ Validaciones en múltiples capas
- ✅ Permisos granulares por endpoint

## 📝 Próximas Mejoras

- [ ] Tests unitarios y de integración completos
- [ ] Caching con Redis
- [ ] Rate limiting
- [ ] Monitoreo con Sentry
- [ ] Optimización de queries
- [ ] Frontend React/Vue

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

Desarrollado como parte del refactor a Django Rest Framework del sistema de gestión de aerolíneas.

---

⭐ Si este proyecto te resulta útil, ¡no olvides darle una estrella!

## Instalación

1. **Clona el repositorio**

   ```sh
   git clone https://github.com/benyhi/django_efi.git
   cd django_efi
   ```

2. **Crea y activa un entorno virtual (opcional pero recomendado)**

   ```sh
   python -m venv env
   # En Windows:
   env\Scripts\activate
   # En macOS/Linux:
   source env/bin/activate
   ```

3. **Instala las dependencias**

   ```sh
   pip install -r requirements.txt
   ```

4. **Aplica las migraciones**

   ```sh
   cd airline_managment
   python manage.py migrate
   ```

5. **Crea un superusuario (opcional, para acceder al panel de administración)**

   ```sh
   python manage.py createsuperuser
   ```

6. **Ejecuta el servidor de desarrollo**

   ```sh
   python manage.py runserver
   ```

7. **Accede a la aplicación**

   - Abre tu navegador y ve a: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Estructura del Proyecto

- `airline_managment/` - Código fuente principal
  - `flight/` - Gestión de vuelos y aviones
  - `passenger/` - Gestión de pasajeros
  - `reservation/` - Gestión de reservas, asientos y tickets
  - `user/` - Gestión de usuarios y autenticación
  - `templates/` - Plantillas HTML base
  - `static/` - Archivos estáticos (CSS, JS)
- `requirements.txt` - Dependencias del proyecto

## Funcionalidades

- CRUD de vuelos, aviones, pasajeros, reservas, asientos, tickets y usuarios
- Autenticación y registro de usuarios
- Reporte PDF de vuelos y pasajeros
- Panel de administración de Django

## Notas

- El sistema usa SQLite por defecto.
- Para cambiar la configuración, edita [`airline_managment/airline_managment/settings.py`](airline_managment/airline_managment/settings.py).
- Los estilos están en [`airline_managment/static/styles/forms.css`](airline_managment/static/styles/forms.css).

## Licencia

Este proyecto es solo para fines educativos.

---

DOCUMENTACION TECNICA - Sistema de Gestión de Aerolínea

1. TECNOLOGÍAS USADAS
---------------------
- Python 3.10+
- Django 4.x
- SQLite (base de datos por defecto)
- Bootstrap 5 (interfaz)
- FontAwesome (iconos)

2. ESTRUCTURA DEL PROYECTO
--------------------------
- airline_managment/ (carpeta principal)
  - flight/ (vuelos y aviones)
  - passenger/ (pasajeros)
  - reservation/ (reservas, asientos, tickets)
  - user/ (usuarios y autenticación)
  - templates/ (HTML)
  - static/ (CSS, JS)
- requirements.txt (dependencias)

3. FUNCIONALIDADES
------------------
- CRUD de vuelos, aviones, pasajeros, reservas, asientos, tickets y usuarios.
- Autenticación de usuarios (login/logout).
- Panel de administración Django.
- Reportes PDF de vuelos y pasajeros.
- Página de inicio con acceso rápido a cada módulo.

4. MODELOS PRINCIPALES
----------------------
- Plane: datos de aviones.
- Flight: datos de vuelos.
- Passenger: datos de pasajeros.
- Reservation: reservas de asientos.
- Seat: asientos disponibles.
- Ticket: tickets generados.
- User: usuarios del sistema.

5. USO BÁSICO
-------------
- Instalar dependencias: `pip install -r requirements.txt`
- Migrar base de datos: `python manage.py migrate`
- Crear superusuario: `python manage.py createsuperuser`
- Ejecutar servidor: `python manage.py runserver`
- Acceder vía navegador: `http://127.0.0.1:8000/`

6. PERSONALIZACIÓN
------------------
- Editar estilos en `static/styles/forms.css`
- Modificar plantillas en `templates/`
- Cambiar configuración en `settings.py`

7. SEGURIDAD
------------
- Formularios protegidos con CSRF.
- Permisos para usuarios staff y clientes.
