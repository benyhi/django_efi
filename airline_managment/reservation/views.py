from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Reservation, Seat
from .forms import ReservationForm, SeatForm

class ReservationListView(ListView):
    model = Reservation
    template_name = 'reservation/reservation_list.html'
    context_object_name = 'reservations'

class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation/reservation_form.html'
    success_url = reverse_lazy('reservation_list')

class ReservationUpdateView(UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation/reservation_form.html'
    success_url = reverse_lazy('reservation_list')

class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'reservation/reservation_delete.html'
    success_url = reverse_lazy('reservation_list')

class SeatListView(ListView):
    model = Seat
    template_name = 'seat/seat_list.html'
    context_object_name = 'seats'

class SeatCreateView(CreateView):
    model = Seat
    form_class = SeatForm
    template_name = 'seat/seat_form.html'
    success_url = reverse_lazy('seat_list')

class SeatUpdateView(UpdateView):
    model = Seat
    form_class = SeatForm
    template_name = 'seat/seat_form.html'
    success_url = reverse_lazy('seat_list')

class SeatDeleteView(DeleteView):
    model = Seat
    template_name = 'seat/seat_delete.html'
    success_url = reverse_lazy('seat_list')
