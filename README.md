# Sistema de Gestión de Aerolínea (EFI Django)

Este proyecto es un sistema de gestión de vuelos, pasajeros, reservas, asientos, tickets y usuarios, desarrollado con Django.

## Requisitos

- Python 3.10+
- [pip](https://pip.pypa.io/en/stable/)
- [Git](https://git-scm.com/)
- (Opcional) [Virtualenv](https://virtualenv.pypa.io/en/latest/)

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
