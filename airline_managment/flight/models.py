import math
from django.db import models
from django.forms import ValidationError
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
    
    def clean(self):
        if self.capacity and self.capacity > 500:
            raise ValidationError({'capacity': 'La capacidad máxima permitida es 500 pasajeros.'})
        if self.columns is not None and self.columns > 9:
            raise ValidationError({'columns': 'El máximo de columnas permitido es 9.'})
        if self.rows and self.columns and self.capacity != self.rows * self.columns:
            raise ValidationError({
                'capacity': 'La capacidad debe ser igual a filas x columnas.'
            })
        
    def save(self, *args, **kwargs):
        if self.capacity > 500:
            self.capacity = 500
        if (not self.rows or not self.columns or self.columns > 9) and self.capacity:
            self.rows, self.columns = self._calculate_rows_columns(self.capacity)
        elif self.rows and self.columns:
            self.capacity = self.rows * self.columns
        super().save(*args, **kwargs)

    @staticmethod
    def _calculate_rows_columns(capacity):
        max_columns = 9
        for columns in range(max_columns, 0, -1):
            if capacity % columns == 0:
                rows = capacity // columns
                return rows, columns
        columns = max_columns
        rows = math.ceil(capacity / columns)
        return rows, columns
    


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