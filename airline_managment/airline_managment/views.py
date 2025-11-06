from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Count, Q
from datetime import datetime, date

from flight.models import Flight
from passenger.models import Passenger
from reservation.models import Reservation
from reservation.serializers import ReservationListSerializer
from passenger.serializers import PassengerListSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def passengers_by_flight(request):
    """
    Endpoint para obtener listado de pasajeros por vuelo
    Query param: flight_id (requerido)
    """
    flight_id = request.query_params.get('flight_id')
    if not flight_id:
        return Response(
            {'error': 'Parámetro flight_id es requerido'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        flight = Flight.objects.get(id=flight_id)
        reservations = Reservation.objects.filter(
            flight=flight,
            status__in=['confirmed', 'pending']
        ).select_related('passenger', 'seat').order_by('seat__row', 'seat__column')
        
        passengers_data = []
        for reservation in reservations:
            passengers_data.append({
                'reservation_id': reservation.id,
                'reservation_code': reservation.code,
                'passenger': {
                    'id': reservation.passenger.id,
                    'full_name': f"{reservation.passenger.first_name} {reservation.passenger.last_name}",
                    'dni': reservation.passenger.dni,
                    'email': reservation.passenger.email,
                    'dni_type': reservation.passenger.dni_type
                },
                'seat': {
                    'number': reservation.seat.number,
                    'row': reservation.seat.row,
                    'column': reservation.seat.column,
                    'type': reservation.seat.type
                },
                'status': reservation.status,
                'price': reservation.price
            })
        
        return Response({
            'flight': {
                'id': flight.id,
                'flight_number': flight.flight_number,
                'departure_city': flight.departure_city,
                'arrival_city': flight.arrival_city,
                'departure_date': flight.departure_date,
                'departure_time': flight.departure_time
            },
            'total_passengers': len(passengers_data),
            'passengers': passengers_data
        })
        
    except Flight.DoesNotExist:
        return Response(
            {'error': 'Vuelo no encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def active_reservations_by_passenger(request):
    """
    Endpoint para obtener reservas activas de un pasajero
    Query param: passenger_id (requerido)
    """
    passenger_id = request.query_params.get('passenger_id')
    if not passenger_id:
        return Response(
            {'error': 'Parámetro passenger_id es requerido'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        passenger = Passenger.objects.get(id=passenger_id)
        active_reservations = Reservation.objects.filter(
            passenger=passenger,
            status__in=['confirmed', 'pending']
        ).select_related('flight', 'seat').order_by('flight__departure_date', 'flight__departure_time')
        
        serializer = ReservationListSerializer(active_reservations, many=True)
        
        return Response({
            'passenger': {
                'id': passenger.id,
                'full_name': f"{passenger.first_name} {passenger.last_name}",
                'dni': passenger.dni,
                'email': passenger.email
            },
            'total_active_reservations': active_reservations.count(),
            'reservations': serializer.data
        })
        
    except Passenger.DoesNotExist:
        return Response(
            {'error': 'Pasajero no encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def flight_statistics(request):
    """
    Endpoint para obtener estadísticas de vuelos
    """
    today = date.today()
    
    # Estadísticas generales
    total_flights = Flight.objects.count()
    flights_today = Flight.objects.filter(departure_date=today).count()
    upcoming_flights = Flight.objects.filter(departure_date__gt=today).count()
    past_flights = Flight.objects.filter(departure_date__lt=today).count()
    
    # Vuelos por estado
    flights_by_status = Flight.objects.values('status').annotate(
        count=Count('id')
    ).order_by('status')
    
    # Vuelos más populares (con más reservas)
    popular_flights = Flight.objects.annotate(
        reservations_count=Count('reservation')
    ).filter(reservations_count__gt=0).order_by('-reservations_count')[:5]
    
    popular_flights_data = []
    for flight in popular_flights:
        popular_flights_data.append({
            'id': flight.id,
            'flight_number': flight.flight_number,
            'route': f"{flight.departure_city} → {flight.arrival_city}",
            'departure_date': flight.departure_date,
            'reservations_count': flight.reservations_count,
            'available_seats': flight.plane.capacity - flight.reservations_count
        })
    
    return Response({
        'general_statistics': {
            'total_flights': total_flights,
            'flights_today': flights_today,
            'upcoming_flights': upcoming_flights,
            'past_flights': past_flights
        },
        'flights_by_status': list(flights_by_status),
        'popular_flights': popular_flights_data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def reservation_statistics(request):
    """
    Endpoint para obtener estadísticas de reservas
    """
    today = date.today()
    
    # Estadísticas generales
    total_reservations = Reservation.objects.count()
    reservations_today = Reservation.objects.filter(date=today).count()
    
    # Reservas por estado
    reservations_by_status = Reservation.objects.values('status').annotate(
        count=Count('id')
    ).order_by('status')
    
    # Ingresos totales
    total_revenue = Reservation.objects.filter(
        status__in=['confirmed']
    ).aggregate(total=Count('price'))['total'] or 0
    
    # Ocupación promedio
    total_capacity = sum([flight.plane.capacity for flight in Flight.objects.all()])
    occupied_seats = Reservation.objects.filter(status='confirmed').count()
    occupancy_rate = (occupied_seats / total_capacity * 100) if total_capacity > 0 else 0
    
    return Response({
        'general_statistics': {
            'total_reservations': total_reservations,
            'reservations_today': reservations_today,
            'total_revenue': total_revenue,
            'occupancy_rate': round(occupancy_rate, 2)
        },
        'reservations_by_status': list(reservations_by_status)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def passenger_statistics(request):
    """
    Endpoint para obtener estadísticas de pasajeros
    """
    # Estadísticas generales
    total_passengers = Passenger.objects.count()
    
    # Pasajeros por tipo de documento
    passengers_by_dni_type = Passenger.objects.values('dni_type').annotate(
        count=Count('id')
    ).order_by('dni_type')
    
    # Pasajeros más frecuentes
    frequent_passengers = Passenger.objects.annotate(
        reservations_count=Count('reservation')
    ).filter(reservations_count__gt=0).order_by('-reservations_count')[:10]
    
    frequent_passengers_data = []
    for passenger in frequent_passengers:
        frequent_passengers_data.append({
            'id': passenger.id,
            'full_name': f"{passenger.first_name} {passenger.last_name}",
            'dni': passenger.dni,
            'email': passenger.email,
            'total_reservations': passenger.reservations_count
        })
    
    return Response({
        'general_statistics': {
            'total_passengers': total_passengers
        },
        'passengers_by_dni_type': list(passengers_by_dni_type),
        'frequent_passengers': frequent_passengers_data
    })