from django.db import models

# Create your models here.

class Passenger(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dni = models.CharField(max_length=8, unique=True, null=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    dni_type = models.CharField(max_length=10, choices=[
        ('dni', 'DNI'),
        ('passport', 'Pasaporte'),
    ], default='passport')

    def __str__(self):
        return f"Pasajero: {self.first_name} {self.last_name} "
    
