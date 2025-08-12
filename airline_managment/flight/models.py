from django.db import models

# Create your models here.

class Plane(models.Model):
    model = models.CharField(max_length=100)
    capacity = models.IntegerField()
    rows = models.IntegerField()
    columns = models.IntegerField()

    def __str__(self):
        return f"{self.model} - {self.capacity} pasajeros"

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    plane = models.ForeignKey(Plane, on_delete=models.CASCADE, related_name='flights')
    departure_city = models.CharField(max_length=100)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    arrival_city = models.CharField(max_length=100)
    arrival_date = models.DateField()
    arrival_time = models.TimeField()
    duration = models.DurationField()
    status = models.CharField(max_length=20, choices=[
        ('on_time', 'A tiempo'),
        ('delayed', 'Retrasado'),
        ('cancelled', 'Cancelado'),
    ])
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.flight_number}: desde {self.departure_city} a {self.arrival_city}"