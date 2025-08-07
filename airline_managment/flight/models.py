from django.db import models

# Create your models here.

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    plane_id = models.ForeignKey('Plane', on_delete=models.CASCADE)
    departure_city = models.CharField(max_length=100)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    arrival_city = models.CharField(max_length=100)
    arrival_date = models.DateField()
    arrival_time = models.TimeField()

    def __str__(self):
        return f"{self.flight_number}: desde {self.departure_city} a {self.arrival_city}"
    
class Plane(models.Model):
    plane_number = models.CharField(max_length=10)
    model = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.plane_number} - {self.model}"