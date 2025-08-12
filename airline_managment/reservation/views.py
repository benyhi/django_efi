from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Reservation, Seat, Ticket
from .forms import ReservationForm, SeatForm, TicketForm

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

class TicketListView(ListView):
    model = Ticket
    template_name = 'ticket/ticket_list.html'
    context_object_name = 'tickets'

class TicketCreateView(CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'ticket/ticket_form.html'
    success_url = reverse_lazy('ticket_list')

class TicketUpdateView(UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'ticket/ticket_form.html'
    success_url = reverse_lazy('ticket_list')

class TicketDeleteView(DeleteView):
    model = Ticket
    template_name = 'ticket/ticket_delete.html'
    success_url = reverse_lazy('ticket_list')
