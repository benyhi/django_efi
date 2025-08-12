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
        widgets = {
            'flight_number': forms.TextInput(attrs={'class': 'form-control'}),
            'plane': forms.Select(attrs={'class': 'form-control'}),
            'departure_city': forms.TextInput(attrs={'class': 'form-control'}),
            'departure_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'departure_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'arrival_city': forms.TextInput(attrs={'class': 'form-control'}),
            'arrival_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'arrival_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'duration': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
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
        widgets = {
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'rows': forms.NumberInput(attrs={'class': 'form-control'}),
            'columns': forms.NumberInput(attrs={'class': 'form-control'}),
        }