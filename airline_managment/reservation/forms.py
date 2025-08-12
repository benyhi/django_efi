from django import forms
from .models import Reservation, Seat

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'flight',
            'passenger',
            'seat',
            'code',
            'price',
            'status',
        ]
        widgets = {
            'flight': forms.Select(attrs={'class': 'form-control'}),
            'passenger': forms.Select(attrs={'class': 'form-control'}),
            'seat': forms.Select(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class SeatForm(forms.ModelForm):
    class Meta:
        model = Seat
        fields = [
            'plane',
            'number',
            'row',
            'column',
            'type',
            'status',
        ]
        widgets = {
            'flight': forms.Select(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'row': forms.NumberInput(attrs={'class': 'form-control'}),
            'column': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }