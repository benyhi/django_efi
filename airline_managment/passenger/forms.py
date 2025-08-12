from django import forms
from .models import Passenger

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = [
            'first_name',
            'last_name',
            'dni',
            'email',
            'phone_number',
            'birth_date',
            'dni_type',
        ]
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'dni': 'DNI',
            'email': 'Correo electrónico',
            'phone_number': 'Teléfono',
            'birth_date': 'Fecha de nacimiento',
            'dni_type': 'Tipo de DNI',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dni_type': forms.Select(attrs={'class': 'form-control'}),
        }
