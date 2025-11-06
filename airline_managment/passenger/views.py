from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from .models import Passenger
from .serializers import (
    PassengerSerializer, PassengerDetailSerializer, PassengerListSerializer
)
from reservation.models import Reservation
from reservation.serializers import ReservationListSerializer


class PassengerViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de pasajeros"""
    queryset = Passenger.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['dni_type']
    search_fields = ['first_name', 'last_name', 'dni', 'email']
    ordering_fields = ['first_name', 'last_name', 'dni']
    ordering = ['first_name', 'last_name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PassengerListSerializer
        elif self.action == 'retrieve':
            return PassengerDetailSerializer
        return PassengerSerializer
    
    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def reservations(self, request, pk=None):
        passenger = self.get_object()
        reservations = Reservation.objects.filter(
            passenger=passenger
        ).order_by('-date')
        
        # Aplicar paginación
        page = self.paginate_queryset(reservations)
        if page is not None:
            serializer = ReservationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ReservationListSerializer(reservations, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def active_reservations(self, request, pk=None):
        """Obtener reservas activas de un pasajero"""
        passenger = self.get_object()
        active_reservations = Reservation.objects.filter(
            passenger=passenger,
            status__in=['confirmed', 'pending']
        ).order_by('-date')
        
        serializer = ReservationListSerializer(active_reservations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search_by_dni(self, request):
        """Buscar pasajero por DNI"""
        dni = request.query_params.get('dni')
        if not dni:
            return Response(
                {'error': 'Parámetro dni es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            passenger = Passenger.objects.get(dni=dni)
            serializer = PassengerDetailSerializer(passenger)
            return Response(serializer.data)
        except Passenger.DoesNotExist:
            return Response(
                {'error': 'Pasajero no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def search_by_email(self, request):
        """Buscar pasajero por email"""
        email = request.query_params.get('email')
        if not email:
            return Response(
                {'error': 'Parámetro email es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            passenger = Passenger.objects.get(email=email)
            serializer = PassengerDetailSerializer(passenger)
            return Response(serializer.data)
        except Passenger.DoesNotExist:
            return Response(
                {'error': 'Pasajero no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )