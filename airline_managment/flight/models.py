from django.db import models
from reservation.models import Seat
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
import string

class Plane(models.Model):
    model = models.CharField(max_length=100)
    capacity = models.IntegerField()
    rows = models.IntegerField()
    columns = models.IntegerField()

    def __str__(self):
        return f"{self.model} - {self.capacity} pasajeros"

# --- Señal para crear asientos automáticamente ---

@receiver(post_save, sender=Plane)
def create_seats_for_plane(sender, instance, created, **kwargs):
    if created:
        # Evitar duplicados
        if Seat.objects.filter(plane=instance).exists():
            return
        # Crear asientos según filas y columnas
        for row in range(1, instance.rows + 1):
            for col in range(1, instance.columns + 1):
                col_letter = string.ascii_uppercase[col - 1]
                Seat.objects.create(
                    plane=instance,
                    number=f"{row}{col_letter}",
                    row=row,
                    column=col_letter,
                    type='economy',
                    status='available'
                )

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    plane = models.ForeignKey(Plane, on_delete=models.CASCADE, related_name='flights')
    departure_city = models.CharField(max_length=100)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    arrival_city = models.CharField(max_length=100)
    arrival_date = models.DateField()
    arrival_time = models.TimeField()
    duration = models.DurationField(default=timedelta())
    status = models.CharField(max_length=20, choices=[
        ('on_time', 'A tiempo'),
        ('delayed', 'Retrasado'),
        ('cancelled', 'Cancelado'),
    ])
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.flight_number}: desde {self.departure_city} a {self.arrival_city}"