from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.crypto import get_random_string
import random

from flight.models import Flight, Plane
from passenger.models import Passenger
from reservation.models import Reservation, Seat, Ticket


class Command(BaseCommand):
    help = 'Poblar la base de datos con datos de prueba para el sistema de aerolínea'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpiar todos los datos antes de crear nuevos',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🌱 Iniciando seed de datos de prueba...')
        )

        if options['clear']:
            self.clear_data()

        self.create_users()
        planes = self.create_planes()
        flights = self.create_flights(planes)
        passengers = self.create_passengers()
        self.create_reservations_and_tickets(flights, passengers)

        self.print_summary()

    def clear_data(self):
        """Limpiar todos los datos existentes"""
        self.stdout.write("🗑️  Limpiando datos existentes...")
        
        Ticket.objects.all().delete()
        Reservation.objects.all().delete()
        Seat.objects.all().delete()
        Flight.objects.all().delete()
        Plane.objects.all().delete()
        Passenger.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        self.stdout.write(self.style.WARNING("   ✅ Datos limpiados"))

    def create_users(self):
        """Crear usuarios de prueba"""
        self.stdout.write("👤 Creando usuarios...")
        
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
            self.stdout.write("   ✅ Admin creado: admin/admin123")
        
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
                self.stdout.write(f"   ✅ Usuario: {username}/{password}")

    def create_planes(self):
        """Crear aviones de prueba"""
        self.stdout.write("✈️  Creando aviones...")
        
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
                self.stdout.write(f"   ✅ {model} ({capacity} asientos)")
            planes.append(plane)
        
        return planes

    def create_flights(self, planes):
        """Crear vuelos de prueba"""
        self.stdout.write("🛫 Creando vuelos...")
        
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
                self.stdout.write(f"   ✅ {flight_num} {dep_city}→{arr_city} (${price})")
            flights.append(flight)
        
        return flights

    def create_passengers(self):
        """Crear pasajeros de prueba"""
        self.stdout.write("👥 Creando pasajeros...")
        
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
                self.stdout.write(f"   ✅ {first_name} {last_name} ({dni})")
            passengers.append(passenger)
        
        return passengers

    def create_reservations_and_tickets(self, flights, passengers):
        """Crear reservas y tickets de prueba"""
        self.stdout.write("🎫 Creando reservas y tickets...")
        
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
                
                reservations_created += 1
        
        self.stdout.write(f"   📊 {reservations_created} reservas, {tickets_created} tickets")

    def print_summary(self):
        """Imprimir resumen de datos creados"""
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS("🎉 SEED COMPLETADO EXITOSAMENTE"))
        self.stdout.write("=" * 50)
        
        self.stdout.write("\n📊 Resumen de datos creados:")
        self.stdout.write(f"   👤 Usuarios: {User.objects.count()}")
        self.stdout.write(f"   ✈️  Aviones: {Plane.objects.count()}")
        self.stdout.write(f"   🛫 Vuelos: {Flight.objects.count()}")
        self.stdout.write(f"   👥 Pasajeros: {Passenger.objects.count()}")
        self.stdout.write(f"   🪑 Asientos: {Seat.objects.count()}")
        self.stdout.write(f"   📝 Reservas: {Reservation.objects.count()}")
        self.stdout.write(f"   🎫 Tickets: {Ticket.objects.count()}")
        
        self.stdout.write(f"\n🔑 Credenciales de prueba:")
        self.stdout.write(f"   👨‍💼 Admin: admin/admin123")
        self.stdout.write(f"   👤 Usuario: testuser/test123")
        
        self.stdout.write(f"\n🌐 URLs importantes:")
        self.stdout.write(f"   🏠 Home: http://127.0.0.1:8000/")
        self.stdout.write(f"   📖 Swagger: http://127.0.0.1:8000/swagger/")
        self.stdout.write(f"   👨‍💼 Admin: http://127.0.0.1:8000/admin/")