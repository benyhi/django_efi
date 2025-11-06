from rest_framework import serializers
from .models import Flight, Plane
from reservation.models import Seat


class PlaneSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Plane"""
    
    class Meta:
        model = Plane
        fields = '__all__'
        
    def validate_capacity(self, value):
        """Validación personalizada para la capacidad"""
        if value > 500:
            raise serializers.ValidationError("La capacidad máxima permitida es 500 pasajeros.")
        return value
    
    def validate_columns(self, value):
        """Validación personalizada para las columnas"""
        if value > 9:
            raise serializers.ValidationError("El máximo de columnas permitido es 9.")
        return value
    
    def validate(self, data):
        """Validación a nivel de objeto"""
        capacity = data.get('capacity')
        rows = data.get('rows')
        columns = data.get('columns')
        
        if capacity and rows and columns:
            if capacity != rows * columns:
                raise serializers.ValidationError({
                    'capacity': 'La capacidad debe ser igual a filas x columnas.'
                })
        
        return data


class SeatSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Seat"""
    plane_model = serializers.CharField(source='plane.model', read_only=True)
    
    class Meta:
        model = Seat
        fields = ['id', 'plane', 'plane_model', 'number', 'row', 'column', 'type', 'status']
        read_only_fields = ['id']
        ref_name = 'FlightSeat'


class FlightSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Flight"""
    plane_model = serializers.CharField(source='plane.model', read_only=True)
    plane_capacity = serializers.IntegerField(source='plane.capacity', read_only=True)
    available_seats = serializers.SerializerMethodField()
    
    class Meta:
        model = Flight
        fields = [
            'id', 'flight_number', 'plane', 'plane_model', 'plane_capacity',
            'departure_city', 'departure_date', 'departure_time',
            'arrival_city', 'arrival_date', 'arrival_time',
            'duration', 'status', 'price', 'available_seats'
        ]
        read_only_fields = ['id', 'duration']
    
    def get_available_seats(self, obj):
        """Obtiene el número de asientos disponibles para el vuelo"""
        if obj.plane:
            available_seats = Seat.objects.filter(
                plane=obj.plane,
                status='available'
            ).count()
            return available_seats
        return 0
    
    def validate_flight_number(self, value):
        """Validación para número de vuelo único"""
        instance = self.instance
        if Flight.objects.filter(flight_number=value).exclude(
            pk=instance.pk if instance else None
        ).exists():
            raise serializers.ValidationError("Ya existe un vuelo con este número.")
        return value
    
    def validate(self, data):
        """Validación de fechas y horarios"""
        departure_date = data.get('departure_date')
        departure_time = data.get('departure_time')
        arrival_date = data.get('arrival_date')
        arrival_time = data.get('arrival_time')
        
        if departure_date and arrival_date:
            if departure_date > arrival_date:
                raise serializers.ValidationError({
                    'arrival_date': 'La fecha de llegada no puede ser anterior a la fecha de salida.'
                })
            
            if departure_date == arrival_date and departure_time and arrival_time:
                if departure_time >= arrival_time:
                    raise serializers.ValidationError({
                        'arrival_time': 'La hora de llegada debe ser posterior a la hora de salida.'
                    })
        
        return data


class FlightDetailSerializer(FlightSerializer):
    """Serializer detallado para el modelo Flight con información de avión y asientos"""
    plane = PlaneSerializer(read_only=True)
    seats = SeatSerializer(source='plane.seat_set', many=True, read_only=True)
    
    class Meta(FlightSerializer.Meta):
        fields = FlightSerializer.Meta.fields + ['seats']


class FlightListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de vuelos"""
    plane_model = serializers.CharField(source='plane.model', read_only=True)
    available_seats = serializers.SerializerMethodField()
    
    class Meta:
        model = Flight
        fields = [
            'id', 'flight_number', 'plane_model',
            'departure_city', 'departure_date', 'departure_time',
            'arrival_city', 'arrival_date', 'arrival_time',
            'status', 'price', 'available_seats'
        ]
    
    def get_available_seats(self, obj):
        """Obtiene el número de asientos disponibles para el vuelo"""
        if obj.plane:
            available_seats = Seat.objects.filter(
                plane=obj.plane,
                status='available'
            ).count()
            return available_seats
        return 0