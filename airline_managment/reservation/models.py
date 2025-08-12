from django.db import models

# Create your models here.

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
        return f"Asiento {self.number} en vuelo {self.flight}"
    
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
