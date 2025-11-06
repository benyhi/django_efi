from rest_framework import serializers
from .models import Passenger
from django.core.validators import RegexValidator


class PassengerSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Passenger"""
    
    dni_validator = RegexValidator(
        regex=r'^\d{8}$',
        message="El DNI debe tener exactamente 8 dígitos."
    )
    
    class Meta:
        model = Passenger
        fields = [
            'id', 'first_name', 'last_name', 'dni', 'email', 
            'phone_number', 'birth_date', 'dni_type'
        ]
        read_only_fields = ['id']
    
    def validate_dni(self, value):
        """Validación personalizada para DNI"""
        if self.initial_data.get('dni_type') == 'dni':
            if not value.isdigit() or len(value) != 8:
                raise serializers.ValidationError("El DNI debe tener exactamente 8 dígitos.")
        return value
    
    def validate_email(self, value):
        """Validación para email único"""
        instance = self.instance
        if Passenger.objects.filter(email=value).exclude(
            pk=instance.pk if instance else None
        ).exists():
            raise serializers.ValidationError("Ya existe un pasajero con este email.")
        return value
    
    def validate_phone_number(self, value):
        """Validación para número de teléfono"""
        if value and not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("El número de teléfono debe contener solo dígitos, espacios, + y -.")
        return value


class PassengerDetailSerializer(PassengerSerializer):
    """Serializer detallado para el modelo Passenger con reservas"""
    reservations_count = serializers.SerializerMethodField()
    recent_reservations = serializers.SerializerMethodField()
    
    class Meta(PassengerSerializer.Meta):
        fields = PassengerSerializer.Meta.fields + ['reservations_count', 'recent_reservations']
    
    def get_reservations_count(self, obj):
        """Obtiene el número total de reservas del pasajero"""
        return obj.reservation_set.count()
    
    def get_recent_reservations(self, obj):
        """Obtiene las 5 reservas más recientes del pasajero"""
        from reservation.serializers import ReservationListSerializer
        recent_reservations = obj.reservation_set.order_by('-date')[:5]
        return ReservationListSerializer(recent_reservations, many=True).data


class PassengerListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de pasajeros"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Passenger
        fields = ['id', 'full_name', 'dni', 'email', 'dni_type']
    
    def get_full_name(self, obj):
        """Obtiene el nombre completo del pasajero"""
        return f"{obj.first_name} {obj.last_name}"