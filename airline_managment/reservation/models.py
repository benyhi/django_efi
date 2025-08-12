from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class Reservation(models.Model):
    flight = models.ForeignKey('flight.Flight', on_delete=models.CASCADE)
    passenger = models.ForeignKey('passenger.Passenger', on_delete=models.CASCADE)
    seat = models.OneToOneField('Seat', on_delete=models.CASCADE)
    code = models.CharField(max_length=20, unique=True)
    date = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('confirmed', 'Confirmado'),
        ('cancelled', 'Cancelado'),
        ('pending', 'Pendiente')
    ], default='pending')

    def __str__(self):
        return f"Reservacion de {self.passenger} - Vuelo: {self.flight} - Asiento: {self.seat}"
    
class Seat(models.Model):
    plane = models.ForeignKey('flight.Plane', on_delete=models.CASCADE)
    number = models.CharField(max_length=5)
    row = models.IntegerField()
    column = models.CharField(max_length=2)
    type = models.CharField(max_length=20, choices=[
        ('economy', 'Economy'),
        ('business', 'Business'),
        ('first_class', 'First Class')
    ], default='economy')
    status = models.CharField(max_length=20, choices=[
        ('available', 'Disponible'),
        ('reserved', 'Reservado'),
        ('occupied', 'Ocupado')
    ], default='available')

    def __str__(self):
        return f"Asiento {self.number} en avion {self.plane}"
    
class Ticket(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    bar_code = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Activo'),
        ('inactive', 'Inactivo')
    ], default='active')

    def __str__(self):
        return f"Ticket para {self.reservation} - Código de barras: {self.bar_code}"

# --- Señal para crear un ticket al ingresar una reserva ---

@receiver(post_save, sender=Reservation)
def create_ticket_for_reservation(sender, instance, created, **kwargs):
    if created:
        if not hasattr(instance, 'ticket'):
            Ticket.objects.create(
                reservation=instance,
                bar_code=str(uuid.uuid4()),
                status='active'
            )

# --- Señal para cambiar estado de asiento a ocupado al crear reserva ---

@receiver(post_save, sender=Reservation)
def set_seat_occupied(sender, instance, created, **kwargs):
    if created and instance.seat.status != 'occupied':
        instance.seat.status = 'occupied'
        instance.seat.save()