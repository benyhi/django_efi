#!/usr/bin/env python
"""
Archivo seed para poblar la base de datos con datos de prueba.

Ejecutar desde el directorio airline_managment/:
python seed_data.py

Este script creará:
- Usuarios (admin y normales)
- Aviones con diferentes capacidades
- Vuelos programados
- Pasajeros de prueba
- Reservas y asientos ocupados
- Tickets generados
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airline_managment.settings')
django.setup()

from django.contrib.auth.models import User
from flight.models import Flight, Plane
from passenger.models import Passenger
from reservation.models import Reservation, Seat, Ticket


def create_users():
    """Crear usuarios de prueba"""
    print("🔧 Creando usuarios...")
    
    # Admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@airline.com',
            'first_name': 'Admin',
            'last_name': 'System',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"   ✅ Admin creado: admin/admin123")
    
    # Regular users
    users_data = [
        ('testuser', 'test@example.com', 'Test', 'User', 'test123'),
        ('john_doe', 'john@example.com', 'John', 'Doe', 'john123'),
        ('maria_garcia', 'maria@example.com', 'Maria', 'García', 'maria123'),
    ]
    
    for username, email, first_name, last_name, password in users_data:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            }
        )
        if created:
            user.set_password(password)
            user.save()
            print(f"   ✅ Usuario creado: {username}/{password}")
    
    return admin_user


def create_planes():
    """Crear aviones de prueba"""
    print("✈️  Creando aviones...")
    
    planes_data = [
        ('Boeing 737-800', 180, 30, 6),
        ('Airbus A320', 150, 25, 6),
        ('Boeing 787', 242, 42, 9),
        ('Embraer E190', 100, 25, 4),
        ('ATR 72', 70, 18, 4),
    ]
    
    planes = []
    for model, capacity, rows, columns in planes_data:
        plane, created = Plane.objects.get_or_create(
            model=model,
            defaults={
                'capacity': capacity,
                'rows': rows,
                'columns': columns
            }
        )
        if created:
            print(f"   ✅ Avión creado: {model} ({capacity} asientos)")
        planes.append(plane)
    
    return planes


def create_flights(planes):
    """Crear vuelos de prueba"""
    print("🛫 Creando vuelos...")
    
    base_date = timezone.now().date()
    
    flights_data = [
        # Vuelos nacionales
        ('AA001', 'Madrid', 'Barcelona', 0, '08:00', 1.5, 'on_time', 85.00),
        ('AA002', 'Barcelona', 'Madrid', 0, '10:30', 1.5, 'on_time', 89.00),
        ('AA003', 'Madrid', 'Valencia', 1, '14:15', 1.0, 'delayed', 65.00),
        ('AA004', 'Valencia', 'Madrid', 1, '16:45', 1.0, 'on_time', 67.00),
        ('AA005', 'Madrid', 'Sevilla', 2, '09:20', 1.25, 'on_time', 75.00),
        
        # Vuelos internacionales
        ('IB101', 'Madrid', 'París', 0, '11:30', 2.5, 'on_time', 185.00),
        ('IB102', 'París', 'Madrid', 0, '15:45', 2.5, 'boarding', 189.00),
        ('IB201', 'Barcelona', 'Roma', 1, '13:20', 2.0, 'on_time', 165.00),
        ('IB301', 'Madrid', 'Londres', 2, '07:15', 2.75, 'on_time', 210.00),
        ('LH501', 'Madrid', 'Frankfurt', 3, '16:30', 3.0, 'on_time', 195.00),
        
        # Vuelos de larga distancia
        ('AA801', 'Madrid', 'Nueva York', 1, '22:45', 8.5, 'on_time', 485.00),
        ('AA802', 'Barcelona', 'Buenos Aires', 5, '23:15', 12.0, 'on_time', 695.00),
    ]
    
    flights = []
    for i, (flight_num, dep_city, arr_city, day_offset, dep_time, duration, status, price) in enumerate(flights_data):
        # Calcular fechas y horas
        dep_date = base_date + timedelta(days=day_offset)
        dep_datetime = datetime.strptime(dep_time, '%H:%M').time()
        
        arr_datetime = (datetime.combine(dep_date, dep_datetime) + 
                       timedelta(hours=int(duration), minutes=int((duration % 1) * 60)))
        arr_date = arr_datetime.date()
        arr_time = arr_datetime.time()
        
        # Seleccionar avión basado en el tipo de vuelo
        if price > 400:  # Larga distancia
            plane = planes[2]  # Boeing 787
        elif price > 150:  # Internacional
            plane = planes[1] if i % 2 == 0 else planes[0]  # Airbus A320 o Boeing 737
        else:  # Nacional
            plane = planes[3] if price < 70 else planes[4]  # Embraer o ATR
        
        flight, created = Flight.objects.get_or_create(
            flight_number=flight_num,
            defaults={
                'plane': plane,
                'departure_city': dep_city,
                'arrival_city': arr_city,
                'departure_date': dep_date,
                'departure_time': dep_datetime,
                'arrival_date': arr_date,
                'arrival_time': arr_time,
                'status': status,
                'price': price
            }
        )
        if created:
            print(f"   ✅ Vuelo creado: {flight_num} {dep_city}→{arr_city} (${price})")
        flights.append(flight)
    
    return flights


def create_passengers():
    """Crear pasajeros de prueba"""
    print("👥 Creando pasajeros...")
    
    passengers_data = [
        ('12345678', 'Carlos', 'Rodríguez', 'carlos.rodriguez@email.com', '+34600123456', '1985-03-15'),
        ('87654321', 'Ana', 'Martínez', 'ana.martinez@email.com', '+34600987654', '1990-07-22'),
        ('11223344', 'Miguel', 'López', 'miguel.lopez@email.com', '+34600111222', '1978-11-08'),
        ('44332211', 'Laura', 'González', 'laura.gonzalez@email.com', '+34600444333', '1992-05-30'),
        ('55667788', 'David', 'Sánchez', 'david.sanchez@email.com', '+34600555666', '1987-12-12'),
        ('99887766', 'Elena', 'Fernández', 'elena.fernandez@email.com', '+34600999888', '1983-09-18'),
        ('13579246', 'Roberto', 'Jiménez', 'roberto.jimenez@email.com', '+34600135792', '1995-01-25'),
        ('24681357', 'Carmen', 'Ruiz', 'carmen.ruiz@email.com', '+34600246813', '1989-04-03'),
    ]
    
    passengers = []
    for dni, first_name, last_name, email, phone, birth_date in passengers_data:
        passenger, created = Passenger.objects.get_or_create(
            dni=dni,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone_number': phone,
                'birth_date': birth_date,
                'dni_type': 'dni'
            }
        )
        if created:
            print(f"   ✅ Pasajero creado: {first_name} {last_name} ({dni})")
        passengers.append(passenger)
    
    return passengers


def create_reservations_and_tickets(flights, passengers):
    """Crear reservas y tickets de prueba"""
    print("🎫 Creando reservas y tickets...")
    
    import random
    from django.utils.crypto import get_random_string
    
    reservations_created = 0
    tickets_created = 0
    
    # Crear reservas para algunos vuelos
    for flight in flights[:8]:  # Solo primeros 8 vuelos
        # Obtener asientos disponibles para este vuelo
        available_seats = Seat.objects.filter(
            plane=flight.plane,
            status='available'
        )[:random.randint(2, 6)]  # Entre 2 y 6 reservas por vuelo
        
        for seat in available_seats:
            passenger = random.choice(passengers)
            
            # Verificar que no exista ya una reservación para este asiento
            if Reservation.objects.filter(seat=seat).exists():
                continue
            
            # Crear reservación con código único
            reservation_code = f"RES{flight.flight_number}{get_random_string(4, '0123456789')}"
            reservation = Reservation.objects.create(
                flight=flight,
                passenger=passenger,
                seat=seat,
                code=reservation_code,
                status=random.choice(['confirmed', 'pending', 'confirmed', 'confirmed']),  # Más confirmadas
                price=flight.price + random.uniform(-20, 50),  # Variación de precio
            )
            
            # Ocupar el asiento
            seat.status = 'occupied'
            seat.save()
            
            # Crear ticket si la reserva está confirmada
            if reservation.status == 'confirmed':
                ticket, ticket_created = Ticket.objects.get_or_create(
                    reservation=reservation,
                    defaults={
                        'bar_code': get_random_string(12, '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                        'status': 'active',
                        'date': reservation.date
                    }
                )
                if ticket_created:
                    tickets_created += 1
                    print(f"   🎫 Ticket creado: {ticket.bar_code}")
            
            reservations_created += 1
            print(f"   ✅ Reserva creada: {flight.flight_number} - {passenger.first_name} {passenger.last_name}")
    
    print(f"   📊 Total: {reservations_created} reservas, {tickets_created} tickets")


def main():
    """Función principal para ejecutar el seed"""
    print("=" * 50)
    print("🌱 INICIANDO SEED DE DATOS DE PRUEBA")
    print("=" * 50)
    
    try:
        # Verificar si ya existen datos
        if User.objects.filter(username='admin').exists():
            print("⚠️  Los datos ya existen. ¿Deseas continuar? (s/n)")
            response = input().lower()
            if response != 's' and response != 'si':
                print("❌ Operación cancelada")
                return
        
        # Crear datos
        admin_user = create_users()
        planes = create_planes()
        flights = create_flights(planes)
        passengers = create_passengers()
        create_reservations_and_tickets(flights, passengers)
        
        print("\n" + "=" * 50)
        print("🎉 SEED COMPLETADO EXITOSAMENTE")
        print("=" * 50)
        print("\n📊 Resumen de datos creados:")
        print(f"   👤 Usuarios: {User.objects.count()}")
        print(f"   ✈️  Aviones: {Plane.objects.count()}")
        print(f"   🛫 Vuelos: {Flight.objects.count()}")
        print(f"   👥 Pasajeros: {Passenger.objects.count()}")
        print(f"   🪑 Asientos: {Seat.objects.count()}")
        print(f"   📝 Reservas: {Reservation.objects.count()}")
        print(f"   🎫 Tickets: {Ticket.objects.count()}")
        
        print(f"\n🔑 Credenciales de prueba:")
        print(f"   👨‍💼 Admin: admin/admin123")
        print(f"   👤 Usuario: testuser/test123")
        
        print(f"\n🌐 URLs importantes:")
        print(f"   🏠 Home: http://127.0.0.1:8000/")
        print(f"   📖 Swagger: http://127.0.0.1:8000/swagger/")
        print(f"   👨‍💼 Admin: http://127.0.0.1:8000/admin/")
        
    except Exception as e:
        print(f"❌ Error durante el seed: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()