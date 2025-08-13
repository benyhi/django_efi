from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Reservation, Seat, Ticket
from .forms import ReservationForm, SeatForm, TicketForm

class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservation/reservation_list.html'
    context_object_name = 'reservations'

class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation/reservation_form.html'
    success_url = reverse_lazy('reservation_list')

class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation/reservation_form.html'
    success_url = reverse_lazy('reservation_list')

class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'reservation/reservation_delete.html'
    success_url = reverse_lazy('reservation_list')

class SeatListView(LoginRequiredMixin, ListView):
    model = Seat
    template_name = 'seat/seat_list.html'
    context_object_name = 'seats'

class SeatCreateView(LoginRequiredMixin, CreateView):
    model = Seat
    form_class = SeatForm
    template_name = 'seat/seat_form.html'
    success_url = reverse_lazy('seat_list')

class SeatUpdateView(LoginRequiredMixin, UpdateView):
    model = Seat
    form_class = SeatForm
    template_name = 'seat/seat_form.html'
    success_url = reverse_lazy('seat_list')

class SeatDeleteView(LoginRequiredMixin, DeleteView):
    model = Seat
    template_name = 'seat/seat_delete.html'
    success_url = reverse_lazy('seat_list')

class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'ticket/ticket_list.html'
    context_object_name = 'tickets'

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'ticket/ticket_form.html'
    success_url = reverse_lazy('ticket_list')

class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'ticket/ticket_form.html'
    success_url = reverse_lazy('ticket_list')

class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = 'ticket/ticket_delete.html'
    success_url = reverse_lazy('ticket_list')
