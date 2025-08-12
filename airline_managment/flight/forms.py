from django import forms
from .models import Flight, Plane

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = [
            'flight_number',
            'plane',
            'departure_city',
            'departure_date',
            'departure_time',
            'arrival_city',
            'arrival_date',
            'arrival_time',
            'duration',
            'status',
            'price',
        ]
        labels = {
            'flight_number': 'Número de Vuelo',
            'plane': 'Aeronave',
            'departure_city': 'Ciudad de Salida',
            'departure_date': 'Fecha de Salida',
            'departure_time': 'Hora de Salida',
            'arrival_city': 'Ciudad de Llegada',
            'arrival_date': 'Fecha de Llegada',
            'arrival_time': 'Hora de Llegada',
            'duration': 'Duración',
            'status': 'Estado',
            'price': 'Precio',
        }
        widgets = {
            'flight_number': forms.TextInput(attrs={'class': 'form-control'}),
            'plane': forms.Select(attrs={'class': 'form-control'}),
            'departure_city': forms.TextInput(attrs={'class': 'form-control'}),
            'departure_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'departure_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'arrival_city': forms.TextInput(attrs={'class': 'form-control'}),
            'arrival_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'arrival_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PlaneForm(forms.ModelForm):
    class Meta:
        model = Plane
        fields = [
            'model',
            'capacity',
            'rows',
            'columns',
        ]
        labels = {
            'model': 'Modelo',
            'capacity': 'Capacidad',
            'rows': 'Filas',
            'columns': 'Columnas',
        }
        widgets = {
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'rows': forms.NumberInput(attrs={'class': 'form-control'}),
            'columns': forms.NumberInput(attrs={'class': 'form-control'}),
        }