# API Endpoints Documentation

## Descripción General
Esta API REST fue desarrollada con Django Rest Framework para gestionar un sistema de aerolíneas. La API sigue principios REST y utiliza autenticación JWT.

## Estructura de URLs Base
Todas las URLs de la API están bajo el prefijo `/api/v1/`

## Autenticación
La API utiliza JWT (JSON Web Tokens) para autenticación. Todos los endpoints requieren autenticación excepto el registro y login.

### Endpoints de Autenticación
```
POST /api/v1/auth/login/        - Iniciar sesión
POST /api/v1/auth/refresh/      - Renovar token
POST /api/v1/auth/register/     - Registrar usuario
POST /api/v1/auth/logout/       - Cerrar sesión
GET  /api/v1/auth/profile/      - Obtener perfil
PUT  /api/v1/auth/profile/update/ - Actualizar perfil
POST /api/v1/auth/change-password/ - Cambiar contraseña
```

## Gestión de Vuelos

### Endpoints de Vuelos
```
GET    /api/v1/flights/flights/                    - Listar vuelos
POST   /api/v1/flights/flights/                    - Crear vuelo (admin)
GET    /api/v1/flights/flights/{id}/               - Detalle de vuelo
PUT    /api/v1/flights/flights/{id}/               - Actualizar vuelo (admin)
DELETE /api/v1/flights/flights/{id}/               - Eliminar vuelo (admin)
GET    /api/v1/flights/flights/search/             - Buscar vuelos
GET    /api/v1/flights/flights/{id}/available_seats/ - Asientos disponibles
GET    /api/v1/flights/flights/{id}/seat_map/      - Mapa de asientos
```

#### Buscar Vuelos
**Query Parameters:**
- `origin`: Ciudad de origen
- `destination`: Ciudad de destino  
- `date`: Fecha de salida (YYYY-MM-DD)

**Ejemplo:**
```
GET /api/v1/flights/flights/search/?origin=Madrid&destination=Barcelona&date=2024-12-01
```

### Endpoints de Aviones
```
GET    /api/v1/flights/planes/              - Listar aviones
POST   /api/v1/flights/planes/              - Crear avión (admin)
GET    /api/v1/flights/planes/{id}/         - Detalle de avión
PUT    /api/v1/flights/planes/{id}/         - Actualizar avión (admin)
DELETE /api/v1/flights/planes/{id}/         - Eliminar avión (admin)
GET    /api/v1/flights/planes/{id}/seats/   - Asientos del avión
GET    /api/v1/flights/planes/{id}/layout/  - Layout del avión
GET    /api/v1/flights/planes/{id}/flights/ - Vuelos del avión
```

## Gestión de Pasajeros

### Endpoints de Pasajeros
```
GET    /api/v1/passengers/passengers/                     - Listar pasajeros
POST   /api/v1/passengers/passengers/                     - Registrar pasajero
GET    /api/v1/passengers/passengers/{id}/                - Detalle de pasajero
PUT    /api/v1/passengers/passengers/{id}/                - Actualizar pasajero
DELETE /api/v1/passengers/passengers/{id}/                - Eliminar pasajero (admin)
GET    /api/v1/passengers/passengers/{id}/reservations/   - Reservas del pasajero
GET    /api/v1/passengers/passengers/{id}/active_reservations/ - Reservas activas
GET    /api/v1/passengers/passengers/search_by_dni/       - Buscar por DNI
GET    /api/v1/passengers/passengers/search_by_email/     - Buscar por email
```

## Sistema de Reservas

### Endpoints de Reservas
```
GET    /api/v1/reservations/reservations/              - Listar reservas
POST   /api/v1/reservations/reservations/              - Crear reserva
GET    /api/v1/reservations/reservations/{id}/         - Detalle de reserva
PUT    /api/v1/reservations/reservations/{id}/         - Actualizar reserva
DELETE /api/v1/reservations/reservations/{id}/         - Cancelar reserva
PATCH  /api/v1/reservations/reservations/{id}/confirm/ - Confirmar reserva
PATCH  /api/v1/reservations/reservations/{id}/cancel/  - Cancelar reserva
GET    /api/v1/reservations/reservations/by_flight/    - Reservas por vuelo
```

### Endpoints de Asientos
```
GET /api/v1/reservations/seats/                        - Listar asientos
GET /api/v1/reservations/seats/{id}/                   - Detalle de asiento
GET /api/v1/reservations/seats/available_by_flight/    - Asientos disponibles por vuelo
```

### Endpoints de Boletos
```
GET /api/v1/reservations/tickets/                      - Listar tickets
GET /api/v1/reservations/tickets/{id}/                 - Detalle de ticket
GET /api/v1/reservations/tickets/by_barcode/           - Buscar por código de barras
GET /api/v1/reservations/tickets/by_reservation/       - Buscar por código de reserva
```

## Gestión de Usuarios (Admin)

### Endpoints de Usuarios
```
GET    /api/v1/auth/users/                    - Listar usuarios (admin)
POST   /api/v1/auth/users/                    - Crear usuario (admin)
GET    /api/v1/auth/users/{id}/               - Detalle de usuario (admin)
PUT    /api/v1/auth/users/{id}/               - Actualizar usuario (admin)
DELETE /api/v1/auth/users/{id}/               - Eliminar usuario (admin)
POST   /api/v1/auth/users/{id}/set_admin/     - Hacer administrador (admin)
POST   /api/v1/auth/users/{id}/remove_admin/  - Quitar administrador (admin)
POST   /api/v1/auth/users/{id}/activate/      - Activar usuario (admin)
POST   /api/v1/auth/users/{id}/deactivate/    - Desactivar usuario (admin)
GET    /api/v1/auth/users/admins/             - Listar administradores (admin)
GET    /api/v1/auth/users/active_users/       - Listar usuarios activos (admin)
```

## Reportes

### Endpoints de Reportes
```
GET /api/v1/reports/passengers-by-flight/              - Pasajeros por vuelo (admin)
GET /api/v1/reports/active-reservations-by-passenger/  - Reservas activas por pasajero
GET /api/v1/reports/flight-statistics/                 - Estadísticas de vuelos (admin)
GET /api/v1/reports/reservation-statistics/            - Estadísticas de reservas (admin)
GET /api/v1/reports/passenger-statistics/              - Estadísticas de pasajeros (admin)
```

## Documentación Interactiva

### Swagger UI
```
GET /api/v1/docs/      - Documentación Swagger UI
GET /api/v1/redoc/     - Documentación ReDoc
```

## Formatos de Respuesta

### Respuesta Exitosa
```json
{
    "success": true,
    "message": "Operación exitosa",
    "status_code": 200,
    "data": {
        // Datos de respuesta
    }
}
```

### Respuesta de Error
```json
{
    "success": false,
    "message": "Error en la operación",
    "status_code": 400,
    "errors": {
        "field": ["Error description"]
    }
}
```

## Filtros y Búsqueda

### Parámetros de Query Comunes
- `page`: Número de página (paginación)
- `page_size`: Tamaño de página
- `search`: Término de búsqueda
- `ordering`: Campo de ordenamiento

### Ejemplos de Filtros
```
GET /api/v1/flights/flights/?departure_city=Madrid
GET /api/v1/reservations/reservations/?status=confirmed
GET /api/v1/passengers/passengers/?search=Juan&page=2
```

## Códigos de Estado HTTP

- `200`: OK - Operación exitosa
- `201`: Created - Recurso creado exitosamente
- `400`: Bad Request - Error en la solicitud
- `401`: Unauthorized - No autenticado
- `403`: Forbidden - Sin permisos
- `404`: Not Found - Recurso no encontrado
- `500`: Internal Server Error - Error del servidor

## Permisos

### Niveles de Permisos
1. **Usuario Autenticado**: Puede ver y crear sus propios recursos
2. **Administrador**: Acceso completo a todos los recursos

### Operaciones por Rol
- **Usuarios**: Crear reservas, ver vuelos, gestionar su perfil
- **Administradores**: Gestionar vuelos, aviones, usuarios, acceso a reportes