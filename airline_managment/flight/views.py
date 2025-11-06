from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from datetime import datetime

from .models import Flight, Plane
from .serializers import (
    FlightSerializer, FlightDetailSerializer, FlightListSerializer,
    PlaneSerializer
)
from reservation.models import Seat
from reservation.serializers import SeatSerializer


class FlightViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de vuelos"""
    queryset = Flight.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['departure_city', 'arrival_city', 'departure_date', 'status']
    search_fields = ['flight_number', 'departure_city', 'arrival_city']
    ordering_fields = ['departure_date', 'departure_time', 'price']
    ordering = ['departure_date', 'departure_time']
    
    def get_serializer_class(self):
        """Seleccionar serializer según la acción"""
        if self.action == 'list':
            return FlightListSerializer
        elif self.action == 'retrieve':
            return FlightDetailSerializer
        return FlightSerializer
    
    def get_permissions(self):
        """Configurar permisos según la acción"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Buscar vuelos por origen, destino y fecha"""
        origin = request.query_params.get('origin')
        destination = request.query_params.get('destination')
        date = request.query_params.get('date')
        
        queryset = self.get_queryset()
        
        if origin:
            queryset = queryset.filter(departure_city__icontains=origin)
        if destination:
            queryset = queryset.filter(arrival_city__icontains=destination)
        if date:
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
                queryset = queryset.filter(departure_date=date_obj)
            except ValueError:
                return Response(
                    {'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Aplicar paginación
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FlightListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = FlightListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def available_seats(self, request, pk=None):
        """Obtener asientos disponibles para un vuelo específico"""
        flight = self.get_object()
        available_seats = Seat.objects.filter(
            plane=flight.plane,
            status='available'
        ).order_by('row', 'column')
        
        serializer = SeatSerializer(available_seats, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def seat_map(self, request, pk=None):
        """Obtener mapa de asientos para un vuelo"""
        flight = self.get_object()
        all_seats = Seat.objects.filter(plane=flight.plane).order_by('row', 'column')
        
        # Organizar asientos por filas
        seat_map = {}
        for seat in all_seats:
            if seat.row not in seat_map:
                seat_map[seat.row] = []
            seat_map[seat.row].append({
                'id': seat.id,
                'number': seat.number,
                'column': seat.column,
                'type': seat.type,
                'status': seat.status
            })
        
        return Response({
            'flight_id': flight.id,
            'plane_model': flight.plane.model,
            'total_capacity': flight.plane.capacity,
            'seat_map': seat_map
        })


class PlaneViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de aviones"""
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['model']
    ordering_fields = ['model', 'capacity']
    ordering = ['model']
    
    def get_permissions(self):
        """Configurar permisos según la acción"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def seats(self, request, pk=None):
        """Obtener todos los asientos de un avión"""
        plane = self.get_object()
        seats = Seat.objects.filter(plane=plane).order_by('row', 'column')
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def layout(self, request, pk=None):
        """Obtener layout de asientos de un avión"""
        plane = self.get_object()
        
        return Response({
            'plane_id': plane.id,
            'model': plane.model,
            'capacity': plane.capacity,
            'rows': plane.rows,
            'columns': plane.columns,
            'layout': {
                'total_seats': plane.capacity,
                'rows': plane.rows,
                'columns_per_row': plane.columns
            }
        })
    
    @action(detail=True, methods=['get'])
    def flights(self, request, pk=None):
        """Obtener vuelos programados para un avión"""
        plane = self.get_object()
        flights = Flight.objects.filter(plane=plane).order_by('departure_date', 'departure_time')
        serializer = FlightListSerializer(flights, many=True)
        return Response(serializer.data)