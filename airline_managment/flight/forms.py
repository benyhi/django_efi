from django import forms
from .models import Flight, Plane

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = [
            'flight_number',
            'plane_id',
            'departure_city',
            'departure_date',
            'departure_time',
            'arrival_city',
            'arrival_date',
            'arrival_time',
        ]
        widgets = {
            'flight_number': forms.TextInput(attrs={'class': 'form-control'}),
            'plane_id': forms.Select(attrs={'class': 'form-control'}),
            'departure_city': forms.TextInput(attrs={'class': 'form-control'}),
            'departure_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'departure_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'arrival_city': forms.TextInput(attrs={'class': 'form-control'}),
            'arrival_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'arrival_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

class PlaneForm(forms.ModelForm):
    class Meta:
        model = Plane
        fields = [
            'plane_number',
            'model',
            'capacity',
        ]
        widgets = {
            'plane_number': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
        }