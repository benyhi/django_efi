from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Passenger
from .forms import PassengerForm

class PassengerListView(ListView):
    model = Passenger
    template_name = 'passenger/passenger_list.html'
    context_object_name = 'passengers'

class PassengerCreateView(CreateView):
    model = Passenger
    form_class = PassengerForm
    template_name = 'passenger/passenger_form.html'
    success_url = reverse_lazy('passenger_list')

class PassengerUpdateView(UpdateView):
    model = Passenger
    form_class = PassengerForm
    template_name = 'passenger/passenger_form.html'
    success_url = reverse_lazy('passenger_list')

class PassengerDeleteView(DeleteView):
    model = Passenger
    template_name = 'passenger/passenger_delete.html'
    success_url = reverse_lazy('passenger_list')
