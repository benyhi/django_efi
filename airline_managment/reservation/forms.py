from django import forms
from .models import Reservation, Seat, Ticket

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
        labels = {
            'flight': 'Vuelo',
            'passenger': 'Pasajero',
            'seat': 'Asiento',
            'code': 'Código de Reserva',
            'price': 'Precio',
            'status': 'Estado',
        }
        widgets = {
            'flight': forms.Select(attrs={'class': 'form-control'}),
            'passenger': forms.Select(attrs={'class': 'form-control'}),
            'seat': forms.Select(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['seat'].queryset = Seat.objects.none()

        if 'flight' in self.data:
            try:
                flight_id = int(self.data.get('flight'))
                flight = Reservation._meta.get_field('flight').related_model.objects.get(pk=flight_id)
                plane = flight.plane
                self.fields['seat'].queryset = Seat.objects.filter(
                    plane=plane, status='available'
                )
            except (ValueError, TypeError, Reservation._meta.get_field('flight').related_model.DoesNotExist):
                pass
        elif self.instance.pk:
            plane = self.instance.flight.plane
            self.fields['seat'].queryset = Seat.objects.filter(
                plane=plane, status='available'
            ) | Seat.objects.filter(pk=self.instance.seat.pk)

    def clean_seat(self):
        seat = self.cleaned_data.get('seat')
        if Reservation.objects.filter(seat=seat).exists():
            raise forms.ValidationError("Este asiento ya está reservado.")
        return seat
    
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if Reservation.objects.filter(code=code).exists():
            raise forms.ValidationError("Este código de reserva ya está en uso.")
        return code

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
        labels = {
            'plane': 'Aeronave',
            'number': 'Número',
            'row': 'Fila',
            'column': 'Columna',
            'type': 'Tipo',
            'status': 'Estado',
        }
        widgets = {
            'plane': forms.Select(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'row': forms.NumberInput(attrs={'class': 'form-control'}),
            'column': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'reservation',
            'bar_code',
            'status',
        ]
        labels = {
            'reservation': 'Reserva',
            'bar_code': 'Código de Barras',
            'status': 'Estado',
        }
        widgets = {
            'reservation': forms.Select(attrs={'class': 'form-control'}),
            'bar_code': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
