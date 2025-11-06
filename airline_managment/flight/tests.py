from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Flight, Plane
from passenger.models import Passenger
import json
from datetime import datetime, timezone


class FlightAPITestCase(APITestCase):
    """Tests para los endpoints de Flight"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = APIClient()
        
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()
        
        # Generar token JWT para usuario normal
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        # Generar token JWT para usuario admin
        admin_refresh = RefreshToken.for_user(self.admin_user)
        self.admin_token = str(admin_refresh.access_token)
        
        # Configurar autenticación (usuario normal por defecto)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Crear avión de prueba
        self.plane = Plane.objects.create(
            model='Boeing 737',
            capacity=180,
            rows=30,
            columns=6
        )
        
        # Crear vuelo de prueba
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

    def test_get_flights_list(self):
        """Test para obtener lista de vuelos"""
        url = reverse('flight-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['flight_number'], 'TEST001')

    def test_get_flight_detail(self):
        """Test para obtener detalle de un vuelo"""
        url = reverse('flight-detail', kwargs={'pk': self.flight.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['flight_number'], 'TEST001')
        self.assertEqual(response.data['departure_city'], 'Madrid')

    def test_create_flight(self):
        """Test para crear un nuevo vuelo"""
        # Usar token de admin para creación
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        url = reverse('flight-list')
        data = {
            'flight_number': 'TEST002',
            'plane': self.plane.pk,
            'departure_city': 'Valencia',
            'arrival_city': 'Sevilla',
            'departure_date': '2025-12-26',
            'departure_time': '14:00:00',
            'arrival_date': '2025-12-26',
            'arrival_time': '16:00:00',
            'status': 'on_time',
            'price': 120.00
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Flight.objects.count(), 2)
        self.assertEqual(response.data['flight_number'], 'TEST002')

    def test_update_flight(self):
        """Test para actualizar un vuelo"""
        # Usar token de admin para actualización
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        url = reverse('flight-detail', kwargs={'pk': self.flight.pk})
        data = {
            'flight_number': 'TEST001',
            'plane': self.plane.pk,
            'departure_city': 'Madrid',
            'arrival_city': 'Valencia',  # Cambio de destino
            'departure_date': '2025-12-25',
            'departure_time': '10:00:00',
            'arrival_date': '2025-12-25',
            'arrival_time': '12:00:00',
            'status': 'on_time',
            'price': 180.00  # Cambio de precio
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.flight.refresh_from_db()
        self.assertEqual(self.flight.arrival_city, 'Valencia')
        self.assertEqual(float(self.flight.price), 180.00)

    def test_partial_update_flight(self):
        """Test para actualización parcial de un vuelo"""
        # Usar token de admin para actualización
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        url = reverse('flight-detail', kwargs={'pk': self.flight.pk})
        data = {'price': 200.00}
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.flight.refresh_from_db()
        self.assertEqual(float(self.flight.price), 200.00)

    def test_delete_flight(self):
        """Test para eliminar un vuelo"""
        # Usar token de admin para eliminación
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        url = reverse('flight-detail', kwargs={'pk': self.flight.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Flight.objects.count(), 0)

    def test_flights_without_authentication(self):
        """Test para verificar que se requiere autenticación"""
        self.client.credentials()  # Remover autenticación
        url = reverse('flight-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_flight_filtering(self):
        """Test para filtrado de vuelos"""
        # Crear vuelo adicional
        Flight.objects.create(
            flight_number='TEST003',
            plane=self.plane,
            departure_city='Barcelona',
            departure_date=datetime(2025, 12, 27, tzinfo=timezone.utc).date(),
            departure_time=datetime(2025, 12, 27, 15, 0, tzinfo=timezone.utc).time(),
            arrival_city='Madrid',
            arrival_date=datetime(2025, 12, 27, tzinfo=timezone.utc).date(),
            arrival_time=datetime(2025, 12, 27, 17, 0, tzinfo=timezone.utc).time(),
            price=160.00
        )
        
        url = reverse('flight-list')
        response = self.client.get(url, {'departure_city': 'Madrid'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['departure_city'], 'Madrid')


class PlaneAPITestCase(APITestCase):
    """Tests para los endpoints de Plane"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = APIClient()
        
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()
        
        # Generar token JWT para usuario normal
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        # Generar token JWT para usuario admin
        admin_refresh = RefreshToken.for_user(self.admin_user)
        self.admin_token = str(admin_refresh.access_token)
        
        # Configurar autenticación (usuario normal por defecto)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Crear avión de prueba
        self.plane = Plane.objects.create(
            model='Airbus A320',
            capacity=150,
            rows=25,
            columns=6
        )

    def test_get_planes_list(self):
        """Test para obtener lista de aviones"""
        url = reverse('plane-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['model'], 'Airbus A320')

    def test_get_plane_detail(self):
        """Test para obtener detalle de un avión"""
        url = reverse('plane-detail', kwargs={'pk': self.plane.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['model'], 'Airbus A320')
        self.assertEqual(response.data['capacity'], 150)

    def test_create_plane(self):
        """Test para crear un nuevo avión"""
        # Usar token de admin para creación
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        url = reverse('plane-list')
        data = {
            'model': 'Boeing 777',
            'capacity': 300,
            'rows': 50,
            'columns': 6
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Plane.objects.count(), 2)
        self.assertEqual(response.data['model'], 'Boeing 777')

    def test_update_plane(self):
        """Test para actualizar un avión"""
        # Usar token de admin para actualización
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        url = reverse('plane-detail', kwargs={'pk': self.plane.pk})
        data = {
            'model': 'Airbus A320',
            'capacity': 162,  # 27 * 6 = 162
            'rows': 27,
            'columns': 6
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.plane.refresh_from_db()
        self.assertEqual(self.plane.capacity, 162)
        self.assertEqual(self.plane.rows, 27)

    def test_partial_update_plane(self):
        """Test para actualización parcial de un avión"""
        # Usar token de admin para actualización
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        url = reverse('plane-detail', kwargs={'pk': self.plane.pk})
        data = {'capacity': 144, 'rows': 24}  # 24 * 6 (columns originales) = 144
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.plane.refresh_from_db()
        self.assertEqual(self.plane.capacity, 144)

    def test_delete_plane(self):
        """Test para eliminar un avión"""
        # Usar token de admin para eliminación
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        url = reverse('plane-detail', kwargs={'pk': self.plane.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Plane.objects.count(), 0)

    def test_plane_filtering(self):
        """Test para filtrado de aviones"""
        # Crear avión adicional
        Plane.objects.create(
            model='Boeing 787',
            capacity=250,
            rows=42,
            columns=6
        )
        
        url = reverse('plane-list')
        response = self.client.get(url, {'search': 'Airbus A320'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['model'], 'Airbus A320')

    def test_planes_without_authentication(self):
        """Test para verificar que se requiere autenticación"""
        self.client.credentials()  # Remover autenticación
        url = reverse('plane-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
