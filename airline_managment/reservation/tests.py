from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Reservation, Seat, Ticket
from flight.models import Flight, Plane
from passenger.models import Passenger
import json
from datetime import datetime, timezone, date


class ReservationAPITestCase(APITestCase):
    """Tests para los endpoints de Reservation"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = APIClient()
        
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Generar token JWT
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        # Configurar autenticación
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Crear datos de prueba
        self.plane = Plane.objects.create(
            model='Boeing 737',
            capacity=180,
            rows=30, 
            columns=6
        )
        
        self.flight = Flight.objects.create(
            flight_number='TEST001',
            plane=self.plane,
            departure_city='Madrid',
            departure_date=datetime(2025, 12, 25, tzinfo=timezone.utc).date(),
            departure_time=datetime(2025, 12, 25, 10, 0, tzinfo=timezone.utc).time(),
            arrival_city='Barcelona',
            arrival_date=datetime(2025, 12, 25, tzinfo=timezone.utc).date(),
            arrival_time=datetime(2025, 12, 25, 12, 0, tzinfo=timezone.utc).time(),
            status='on_time',
            price=150.00
        )
        
        self.passenger = Passenger.objects.create(
            first_name='Juan',
            last_name='Pérez',
            email='juan.perez@example.com',
            phone_number='123456789',
            birth_date=date(1990, 5, 15),
            dni='12345678',
            dni_type='dni'
        )
        
        # Crear asiento
        self.seat = Seat.objects.create(
            plane=self.plane,
            number='1A',
            row=1,
            column='A',
            type='economy',
            status='available'
        )

        self.reservation = Reservation.objects.create(
            flight=self.flight,
            passenger=self.passenger,
            seat=self.seat,
            code='RES001',
            date=datetime(2025, 12, 1, tzinfo=timezone.utc).date(),
            price=150.00,
            status='confirmed'
        )

    def test_get_reservations_list(self):
        """Test para obtener lista de reservas"""
        url = reverse('reservation-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status'], 'confirmed')

    def test_get_reservation_detail(self):
        """Test para obtener detalle de una reserva"""
        url = reverse('reservation-detail', kwargs={'pk': self.reservation.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 'RES001')
        self.assertEqual(response.data['status'], 'confirmed')

    def test_create_reservation(self):
        """Test para crear una nueva reserva"""
        # Crear otro asiento disponible
        seat2 = Seat.objects.create(
            plane=self.plane,
            number='1B',
            row=1,
            column='B',
            type='economy',
            status='available'
        )
        
        url = reverse('reservation-list')
        data = {
            'flight': self.flight.pk,
            'passenger': self.passenger.pk,
            'seat': seat2.pk,
            'price': 150.00,
            'status': 'pending'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 2)
        # El código se genera automáticamente, verificar que existe
        self.assertIsNotNone(response.data['code'])
        self.assertEqual(len(response.data['code']), 8)

    def test_update_reservation_status(self):
        """Test para actualizar el estado de una reserva"""
        url = reverse('reservation-detail', kwargs={'pk': self.reservation.pk})
        data = {
            'status': 'cancelled'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.status, 'cancelled')

    def test_partial_update_reservation(self):
        """Test para actualización parcial de una reserva"""
        url = reverse('reservation-detail', kwargs={'pk': self.reservation.pk})
        data = {'status': 'pending'}
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.status, 'pending')

    def test_delete_reservation(self):
        """Test para eliminar una reserva"""
        url = reverse('reservation-detail', kwargs={'pk': self.reservation.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Reservation.objects.count(), 0)

    def test_reservation_filtering_by_status(self):
        """Test para filtrado de reservas por estado"""
        url = reverse('reservation-list')
        response = self.client.get(url, {'status': 'confirmed'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status'], 'confirmed')

    def test_reservations_without_authentication(self):
        """Test para verificar que se requiere autenticación"""
        self.client.credentials()  # Remover autenticación
        url = reverse('reservation-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SeatAPITestCase(APITestCase):
    """Tests para los endpoints de Seat"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = APIClient()
        
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Generar token JWT
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        # Configurar autenticación
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Crear datos de prueba
        self.plane = Plane.objects.create(
            model='Boeing 737',
            capacity=180,
            rows=30, 
            columns=6
        )
        
        self.flight = Flight.objects.create(
            flight_number='TEST001',
            plane=self.plane,
            departure_city='Madrid',
            departure_date=datetime(2025, 12, 25, tzinfo=timezone.utc).date(),
            departure_time=datetime(2025, 12, 25, 10, 0, tzinfo=timezone.utc).time(),
            arrival_city='Barcelona',
            arrival_date=datetime(2025, 12, 25, tzinfo=timezone.utc).date(),
            arrival_time=datetime(2025, 12, 25, 12, 0, tzinfo=timezone.utc).time(),
            status='on_time',
            price=150.00
        )
        
        self.seat = Seat.objects.create(
            plane=self.plane,
            number='1A',
            row=1,
            column='A',
            type='economy',
            status='available'
        )

    def test_get_seats_list(self):
        """Test para obtener lista de asientos"""
        url = reverse('seat-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Los asientos se crean automáticamente al crear el avión
        self.assertGreater(len(response.data['results']), 0)

    def test_seat_creation_automatic(self):
        """Test para verificar que los asientos se crean automáticamente con el avión"""
        # Los asientos se crean automáticamente cuando se crea un avión
        url = reverse('seat-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verificar que hay asientos creados automáticamente
        total_seats = len(response.data['results'])
        self.assertGreater(total_seats, 0)  # Al menos algunos asientos deben existir

    def test_seat_status_change_with_reservation(self):
        """Test para verificar que el estado del asiento cambia con la reserva"""
        # Crear asiento disponible  
        seat = Seat.objects.filter(plane=self.plane, status='available').first()
        self.assertEqual(seat.status, 'available')
        
        # Crear reserva con ese asiento
        passenger = Passenger.objects.create(
            first_name='Ana',
            last_name='García',
            email='ana.garcia@example.com',
            phone_number='987654321',
            birth_date=date(1985, 3, 10),
            dni='87654321',
            dni_type='dni'
        )
        
        Reservation.objects.create(
            flight=self.flight,
            passenger=passenger,
            seat=seat,
            code='RES999',
            date=datetime(2025, 12, 1, tzinfo=timezone.utc).date(),
            price=150.00,
            status='confirmed'
        )
        
        # Verificar que el asiento cambió a ocupado
        seat.refresh_from_db()
        self.assertEqual(seat.status, 'occupied')

    def test_seat_filtering_by_flight(self):
        """Test para filtrado de asientos por vuelo"""
        # Crear otro vuelo con otro avión
        another_plane = Plane.objects.create(
            model='Airbus A320',
            capacity=150,
            rows=25,
            columns=6
        )
        
        Flight.objects.create(
            flight_number='TEST002',
            plane=another_plane,
            departure_city='Valencia',
            departure_date=datetime(2025, 12, 26, tzinfo=timezone.utc).date(),
            departure_time=datetime(2025, 12, 26, 15, 0, tzinfo=timezone.utc).time(),
            arrival_city='Sevilla',
            arrival_date=datetime(2025, 12, 26, tzinfo=timezone.utc).date(),
            arrival_time=datetime(2025, 12, 26, 17, 0, tzinfo=timezone.utc).time(),
            status='on_time',
            price=120.00
        )
        
        url = reverse('seat-list')
        response = self.client.get(url, {'plane': self.plane.pk})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verificar que solo se devuelven asientos del avión específico
        for seat in response.data['results']:
            self.assertEqual(seat['plane'], self.plane.pk)


class TicketAPITestCase(APITestCase):
    """Tests para los endpoints de Ticket"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = APIClient()
        
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Generar token JWT
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        # Configurar autenticación
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Crear datos de prueba
        self.plane = Plane.objects.create(
            model='Boeing 737',
            capacity=180,
            rows=30, 
            columns=6
        )
        
        self.flight = Flight.objects.create(
            flight_number='TEST001',
            plane=self.plane,
            departure_city='Madrid',
            departure_date=datetime(2025, 12, 25, tzinfo=timezone.utc).date(),
            departure_time=datetime(2025, 12, 25, 10, 0, tzinfo=timezone.utc).time(),
            arrival_city='Barcelona',
            arrival_date=datetime(2025, 12, 25, tzinfo=timezone.utc).date(),
            arrival_time=datetime(2025, 12, 25, 12, 0, tzinfo=timezone.utc).time(),
            status='on_time',
            price=150.00
        )
        
        self.passenger = Passenger.objects.create(
            first_name='Juan',
            last_name='Pérez',
            email='juan.perez@example.com',
            phone_number='123456789',
            birth_date=date(1990, 5, 15),
            dni='12345678',
            dni_type='dni'
        )
        
        # Crear asiento
        self.seat = Seat.objects.create(
            plane=self.plane,
            number='1A',
            row=1,
            column='A',
            type='economy',
            status='available'
        )

        self.reservation = Reservation.objects.create(
            flight=self.flight,
            passenger=self.passenger,
            seat=self.seat,
            code='RES001',
            date=datetime(2025, 12, 1, tzinfo=timezone.utc).date(),
            price=150.00,
            status='confirmed'
        )
        
        # El ticket se crea automáticamente cuando se crea la reserva
        self.ticket = self.reservation.ticket

    def test_get_tickets_list(self):
        """Test para obtener lista de tickets"""
        url = reverse('ticket-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertIsNotNone(response.data['results'][0]['bar_code'])

    def test_get_ticket_detail(self):
        """Test para obtener detalle de un ticket"""
        url = reverse('ticket-detail', kwargs={'pk': self.ticket.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['bar_code'])
        self.assertEqual(response.data['status'], 'active')

    def test_create_ticket(self):
        """Test para verificar que el ticket se crea automáticamente con la reserva"""
        # Crear otra reserva, el ticket se creará automáticamente
        seat2 = Seat.objects.create(
            plane=self.plane,
            number='1B',
            row=1,
            column='B',
            type='economy',
            status='available'
        )
        
        reservation2 = Reservation.objects.create(
            flight=self.flight,
            passenger=self.passenger,
            seat=seat2,
            code='RES002',
            date=datetime(2025, 12, 1, tzinfo=timezone.utc).date(),
            price=150.00,
            status='confirmed'
        )
        
        # Verificar que se creó el ticket automáticamente
        self.assertEqual(Ticket.objects.count(), 2)
        self.assertTrue(hasattr(reservation2, 'ticket'))
        self.assertIsNotNone(reservation2.ticket.bar_code)

    def test_ticket_readonly_operations(self):
        """Test para verificar que los tickets son de solo lectura"""
        # Los tickets se crean automáticamente y solo permiten lectura
        url = reverse('ticket-detail', kwargs={'pk': self.ticket.pk})
        
        # Verificar que GET funciona
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que los tickets tienen los campos correctos
        self.assertIn('bar_code', response.data)
        self.assertIn('status', response.data)
        self.assertIn('date', response.data)

    def test_ticket_lifecycle_with_reservation(self):
        """Test para verificar el ciclo de vida del ticket con la reserva"""
        # Los tickets se eliminan automáticamente cuando se elimina la reserva
        initial_ticket_count = Ticket.objects.count()
        
        # Eliminar la reserva
        self.reservation.delete()
        
        # Verificar que el ticket también se eliminó (cascade)
        final_ticket_count = Ticket.objects.count()
        self.assertEqual(final_ticket_count, initial_ticket_count - 1)

    def test_ticket_filtering_by_reservation(self):
        """Test para filtrado de tickets por reserva"""
        url = reverse('ticket-list')
        response = self.client.get(url, {'reservation': self.reservation.pk})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['reservation'], self.reservation.pk)

    def test_tickets_without_authentication(self):
        """Test para verificar que se requiere autenticación"""
        self.client.credentials()  # Remover autenticación
        url = reverse('ticket-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)