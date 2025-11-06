from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from .models import Reservation, Seat, Ticket
from .serializers import (
    ReservationSerializer, ReservationDetailSerializer, ReservationListSerializer,
    ReservationCreateSerializer, SeatSerializer, SeatDetailSerializer,
    TicketSerializer
)


class ReservationViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de reservas."""
    queryset = Reservation.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'flight', 'passenger']
    search_fields = ['code', 'passenger__first_name', 'passenger__last_name', 'flight__flight_number']
    ordering_fields = ['date', 'price']
    ordering = ['-date']
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Seleccionar serializer según la acción"""
        if self.action == 'create':
            return ReservationCreateSerializer
        elif self.action == 'list':
            return ReservationListSerializer
        elif self.action == 'retrieve':
            return ReservationDetailSerializer
        return ReservationSerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Crear reserva con manejo de transacciones"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Verificar disponibilidad del asiento una vez más
        seat = serializer.validated_data['seat']
        if seat.status != 'available':
            return Response(
                {'error': 'El asiento ya no está disponible'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear la reserva
        reservation = serializer.save()
        
        seat.status = 'occupied'
        seat.save()
        
        response_serializer = ReservationDetailSerializer(reservation)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['patch'])
    def confirm(self, request, pk=None):
        """Confirmar una reserva"""
        reservation = self.get_object()
        if reservation.status != 'pending':
            return Response(
                {'error': 'Solo se pueden confirmar reservas pendientes'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reservation.status = 'confirmed'
        reservation.save()
        
        serializer = ReservationDetailSerializer(reservation)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        """Cancelar una reserva"""
        reservation = self.get_object()
        if reservation.status == 'cancelled':
            return Response(
                {'error': 'La reserva ya está cancelada'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            # Cambiar estado de la reserva
            reservation.status = 'cancelled'
            reservation.save()
            
            # Liberar el asiento
            seat = reservation.seat
            seat.status = 'available'
            seat.save()
            
            # Desactivar el ticket si existe
            if hasattr(reservation, 'ticket'):
                ticket = reservation.ticket
                ticket.status = 'inactive'
                ticket.save()
        
        serializer = ReservationDetailSerializer(reservation)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_flight(self, request):
        """Obtener reservas por vuelo"""
        flight_id = request.query_params.get('flight_id')
        if not flight_id:
            return Response(
                {'error': 'Parámetro flight_id es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reservations = Reservation.objects.filter(
            flight_id=flight_id
        ).order_by('seat__row', 'seat__column')
        
        serializer = ReservationListSerializer(reservations, many=True)
        return Response(serializer.data)


class SeatViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para consulta de asientos."""
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['plane', 'type', 'status']
    ordering_fields = ['row', 'column']
    ordering = ['row', 'column']
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SeatDetailSerializer
        return SeatSerializer
    
    @action(detail=False, methods=['get'])
    def available_by_flight(self, request):
        """Obtener asientos disponibles por vuelo"""
        flight_id = request.query_params.get('flight_id')
        if not flight_id:
            return Response(
                {'error': 'Parámetro flight_id es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from flight.models import Flight
            flight = Flight.objects.get(id=flight_id)
            available_seats = Seat.objects.filter(
                plane=flight.plane,
                status='available'
            ).order_by('row', 'column')
            
            serializer = SeatSerializer(available_seats, many=True)
            return Response(serializer.data)
        except Flight.DoesNotExist:
            return Response(
                {'error': 'Vuelo no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class TicketViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para consulta de boletos."""
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'reservation__flight']
    search_fields = ['bar_code', 'reservation__code']
    ordering_fields = ['date']
    ordering = ['-date']
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def by_barcode(self, request):
        """Buscar boleto por código de barras"""
        barcode = request.query_params.get('barcode')
        if not barcode:
            return Response(
                {'error': 'Parámetro barcode es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            ticket = Ticket.objects.get(bar_code=barcode)
            serializer = TicketSerializer(ticket)
            return Response(serializer.data)
        except Ticket.DoesNotExist:
            return Response(
                {'error': 'Boleto no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def by_reservation(self, request):
        """Buscar boleto por código de reserva"""
        reservation_code = request.query_params.get('reservation_code')
        if not reservation_code:
            return Response(
                {'error': 'Parámetro reservation_code es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            ticket = Ticket.objects.get(reservation__code=reservation_code)
            serializer = TicketSerializer(ticket)
            return Response(serializer.data)
        except Ticket.DoesNotExist:
            return Response(
                {'error': 'Boleto no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )