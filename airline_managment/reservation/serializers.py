from rest_framework import serializers
from .models import Reservation, Seat, Ticket
import uuid


class SeatSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Seat"""
    plane_model = serializers.CharField(source='plane.model', read_only=True)
    
    class Meta:
        model = Seat
        fields = ['id', 'plane', 'plane_model', 'number', 'row', 'column', 'type', 'status']
        read_only_fields = ['id']
        ref_name = 'ReservationSeat'


class SeatDetailSerializer(SeatSerializer):
    """Serializer detallado para el modelo Seat con información del avión"""
    plane_details = serializers.SerializerMethodField()
    
    class Meta(SeatSerializer.Meta):
        fields = SeatSerializer.Meta.fields + ['plane_details']
    
    def get_plane_details(self, obj):
        """Obtiene detalles del avión"""
        if obj.plane:
            return {
                'id': obj.plane.id,
                'model': obj.plane.model,
                'capacity': obj.plane.capacity,
                'rows': obj.plane.rows,
                'columns': obj.plane.columns
            }
        return None


class TicketSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Ticket"""
    passenger_name = serializers.CharField(source='reservation.passenger.first_name', read_only=True)
    flight_number = serializers.CharField(source='reservation.flight.flight_number', read_only=True)
    
    class Meta:
        model = Ticket
        fields = ['id', 'reservation', 'date', 'bar_code', 'status', 'passenger_name', 'flight_number']
        read_only_fields = ['id', 'date', 'bar_code']


class ReservationSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Reservation"""
    passenger_name = serializers.CharField(source='passenger.first_name', read_only=True)
    flight_number = serializers.CharField(source='flight.flight_number', read_only=True)
    seat_number = serializers.CharField(source='seat.number', read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'flight', 'passenger', 'seat', 'code', 'date', 
            'price', 'status', 'passenger_name', 'flight_number', 'seat_number'
        ]
        read_only_fields = ['id', 'code', 'date']
    
    def validate(self, data):
        """Validación para asegurar que el asiento esté disponible"""
        seat = data.get('seat')
        flight = data.get('flight')
        
        if seat and flight:
            # Verificar que el asiento pertenezca al avión del vuelo
            if seat.plane != flight.plane:
                raise serializers.ValidationError({
                    'seat': 'El asiento no pertenece al avión de este vuelo.'
                })
            
            # Verificar que el asiento esté disponible
            if seat.status != 'available':
                raise serializers.ValidationError({
                    'seat': 'El asiento seleccionado no está disponible.'
                })
            
            # Verificar que no exista otra reserva para este asiento en este vuelo
            existing_reservation = Reservation.objects.filter(
                flight=flight,
                seat=seat
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if existing_reservation.exists():
                raise serializers.ValidationError({
                    'seat': 'Ya existe una reserva para este asiento en este vuelo.'
                })
        
        return data
    
    def create(self, validated_data):
        """Crear reserva con código único"""
        validated_data['code'] = str(uuid.uuid4())[:8].upper()
        return super().create(validated_data)


class ReservationDetailSerializer(ReservationSerializer):
    """Serializer detallado para el modelo Reservation"""
    passenger = serializers.SerializerMethodField()
    flight = serializers.SerializerMethodField()
    seat = SeatSerializer(read_only=True)
    ticket = TicketSerializer(read_only=True)
    
    class Meta(ReservationSerializer.Meta):
        fields = ReservationSerializer.Meta.fields + ['ticket']
    
    def get_passenger(self, obj):
        """Obtiene información del pasajero"""
        return {
            'id': obj.passenger.id,
            'full_name': f"{obj.passenger.first_name} {obj.passenger.last_name}",
            'dni': obj.passenger.dni,
            'email': obj.passenger.email
        }
    
    def get_flight(self, obj):
        """Obtiene información del vuelo"""
        return {
            'id': obj.flight.id,
            'flight_number': obj.flight.flight_number,
            'departure_city': obj.flight.departure_city,
            'arrival_city': obj.flight.arrival_city,
            'departure_date': obj.flight.departure_date,
            'departure_time': obj.flight.departure_time,
            'price': obj.flight.price
        }


class ReservationListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de reservas"""
    passenger_full_name = serializers.SerializerMethodField()
    flight_route = serializers.SerializerMethodField()
    seat_number = serializers.CharField(source='seat.number', read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'code', 'date', 'status', 'price',
            'passenger_full_name', 'flight_route', 'seat_number'
        ]
    
    def get_passenger_full_name(self, obj):
        """Obtiene el nombre completo del pasajero"""
        return f"{obj.passenger.first_name} {obj.passenger.last_name}"
    
    def get_flight_route(self, obj):
        """Obtiene la ruta del vuelo"""
        return f"{obj.flight.departure_city} → {obj.flight.arrival_city}"


class ReservationCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear reservas"""
    
    class Meta:
        model = Reservation
        fields = ['flight', 'passenger', 'seat', 'price']
    
    def validate(self, data):
        """Validación completa para creación de reserva"""
        seat = data.get('seat')
        flight = data.get('flight')
        
        if seat and flight:
            # Verificar que el asiento pertenezca al avión del vuelo
            if seat.plane != flight.plane:
                raise serializers.ValidationError({
                    'seat': 'El asiento no pertenece al avión de este vuelo.'
                })
            
            # Verificar que el asiento esté disponible
            if seat.status != 'available':
                raise serializers.ValidationError({
                    'seat': 'El asiento seleccionado no está disponible.'
                })
            
            # Verificar que no exista otra reserva para este asiento en este vuelo
            if Reservation.objects.filter(flight=flight, seat=seat).exists():
                raise serializers.ValidationError({
                    'seat': 'Ya existe una reserva para este asiento en este vuelo.'
                })
        
        return data
    
    def create(self, validated_data):
        """Crear reserva con código único"""
        validated_data['code'] = str(uuid.uuid4())[:8].upper()
        return super().create(validated_data)