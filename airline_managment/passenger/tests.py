from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Passenger
import json
from datetime import date


class PassengerAPITestCase(APITestCase):
    """Tests para los endpoints de Passenger"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = APIClient()
        
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Crear usuario admin para tests de eliminación
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        # Generar token JWT
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        # Configurar autenticación
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Crear pasajero de prueba
        self.passenger = Passenger.objects.create(
            first_name='Juan',
            last_name='Pérez',
            email='juan.perez@example.com',
            phone_number='123456789',
            birth_date=date(1990, 5, 15),
            dni='12345678',  # 8 dígitos exactos
            dni_type='dni'
        )

    def test_get_passengers_list(self):
        """Test para obtener lista de pasajeros"""
        url = reverse('passenger-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['full_name'], 'Juan Pérez')
        self.assertEqual(response.data['results'][0]['dni'], '12345678')

    def test_get_passenger_detail(self):
        """Test para obtener detalle de un pasajero"""
        url = reverse('passenger-detail', kwargs={'pk': self.passenger.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Juan')
        self.assertEqual(response.data['email'], 'juan.perez@example.com')
        self.assertEqual(response.data['dni'], '12345678')

    def test_create_passenger(self):
        """Test para crear un nuevo pasajero"""
        url = reverse('passenger-list')
        data = {
            'first_name': 'María',
            'last_name': 'García',
            'email': 'maria.garcia@example.com',
            'phone_number': '987654321',
            'birth_date': '1985-08-20',
            'dni': '87654321',  # 8 dígitos válidos
            'dni_type': 'dni'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Passenger.objects.count(), 2)
        self.assertEqual(response.data['first_name'], 'María')
        self.assertEqual(response.data['email'], 'maria.garcia@example.com')

    def test_create_passenger_invalid_data(self):
        """Test para crear pasajero con datos inválidos"""
        url = reverse('passenger-list')
        data = {
            'first_name': '',  # Campo requerido vacío
            'last_name': 'García',
            'email': 'invalid-email',  # Email inválido
            'phone_number': '987654321',
            'birth_date': '1985-08-20',
            'dni': '1234567',  # DNI inválido (7 dígitos)
            'dni_type': 'dni'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data['errors'])
        self.assertIn('email', response.data['errors'])

    def test_update_passenger(self):
        """Test para actualizar un pasajero"""
        url = reverse('passenger-detail', kwargs={'pk': self.passenger.pk})
        data = {
            'first_name': 'Juan Carlos',  # Cambio de nombre
            'last_name': 'Pérez',
            'email': 'juancarlos.perez@example.com',  # Cambio de email
            'phone_number': '123456789',
            'birth_date': '1990-05-15',
            'dni': '12345678',
            'dni_type': 'dni'
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.passenger.refresh_from_db()
        self.assertEqual(self.passenger.first_name, 'Juan Carlos')
        self.assertEqual(self.passenger.email, 'juancarlos.perez@example.com')

    def test_partial_update_passenger(self):
        """Test para actualización parcial de un pasajero"""
        url = reverse('passenger-detail', kwargs={'pk': self.passenger.pk})
        data = {
            'phone_number': '111222333',
            'dni_type': 'dni'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.passenger.refresh_from_db()
        self.assertEqual(self.passenger.phone_number, '111222333')
        self.assertEqual(self.passenger.dni_type, 'dni')
        # Verificar que otros campos no cambiaron
        self.assertEqual(self.passenger.first_name, 'Juan')

    def test_delete_passenger(self):
        """Test para eliminar un pasajero"""
        # Usar token de admin para eliminación
        refresh = RefreshToken.for_user(self.admin_user)
        admin_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')
        
        url = reverse('passenger-detail', kwargs={'pk': self.passenger.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Passenger.objects.count(), 0)

    def test_passengers_without_authentication(self):
        """Test para verificar que se requiere autenticación"""
        self.client.credentials()  # Remover autenticación
        url = reverse('passenger-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_passenger_filtering_by_email(self):
        """Test para filtrado de pasajeros por email"""
        # Crear pasajero adicional
        Passenger.objects.create(
            first_name='Ana',
            last_name='López',
            email='ana.lopez@example.com',
            phone_number='555666777',
            birth_date=date(1992, 3, 10),
            dni='23456789',  # 8 dígitos válidos
            dni_type='dni'
        )
        
        url = reverse('passenger-list')
        response = self.client.get(url, {'search': 'juan.perez@example.com'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['email'], 'juan.perez@example.com')

    def test_passenger_filtering_by_name(self):
        """Test para filtrado de pasajeros por nombre"""
        # Crear pasajero adicional
        Passenger.objects.create(
            first_name='Ana',
            last_name='López',
            email='ana.lopez@example.com',
            phone_number='555666777',
            birth_date=date(1992, 3, 10),
            dni='34567890',  # 8 dígitos válidos
            dni_type='dni'
        )
        
        url = reverse('passenger-list')
        response = self.client.get(url, {'search': 'Juan'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['full_name'], 'Juan Pérez')

    def test_passenger_search(self):
        """Test para búsqueda de pasajeros"""
        # Crear pasajeros adicionales
        Passenger.objects.create(
            first_name='Ana',
            last_name='López',
            email='ana.lopez@example.com',
            phone_number='555666777',
            birth_date=date(1992, 3, 10),
            dni='45678901',  # 8 dígitos válidos
            dni_type='dni'
        )
        Passenger.objects.create(
            first_name='Carlos',
            last_name='Pérez',
            email='carlos.perez@example.com',
            phone_number='444555666',
            birth_date=date(1988, 7, 25),
            dni='56789012',  # 8 dígitos válidos
            dni_type='dni'
        )
        
        url = reverse('passenger-list')
        response = self.client.get(url, {'search': 'Pérez'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Juan Pérez y Carlos Pérez

    def test_duplicate_passport_number(self):
        """Test para verificar que no se permiten números de DNI duplicados"""
        url = reverse('passenger-list')
        data = {
            'first_name': 'María',
            'last_name': 'García',
            'email': 'maria.garcia@example.com',
            'phone_number': '987654321',
            'birth_date': '1985-08-20',
            'dni': '12345678',  # Mismo número de DNI (8 dígitos)
            'dni_type': 'dni'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dni', response.data['errors'])

    def test_duplicate_email(self):
        """Test para verificar que no se permiten emails duplicados"""
        url = reverse('passenger-list')
        data = {
            'first_name': 'María',
            'last_name': 'García',
            'email': 'juan.perez@example.com',  # Mismo email
            'phone_number': '987654321',
            'birth_date': '1985-08-20',
            'dni': '67890123',  # DNI válido de 8 dígitos
            'dni_type': 'dni'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data['errors'])
