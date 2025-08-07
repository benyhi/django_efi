from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Flight, Plane
from .forms import FlightForm, PlaneForm

# Create your views here.

class FlightListView(ListView):
    model = Flight
    template_name = 'flight/flight_list.html'
    context_object_name = 'flights'

class FlightCreateView(CreateView):
    model = Flight
    form_class = FlightForm
    template_name = 'flight/flight_form.html'
    success_url = reverse_lazy('flight_list')

class FlightUpdateView(UpdateView):
    model = Flight
    form_class = FlightForm
    template_name = 'flight/flight_form.html'
    success_url = reverse_lazy('flight_list')

class FlightDeleteView(DeleteView):
    model = Flight
    template_name = 'flight/flight_delete.html'
    success_url = reverse_lazy('flight_list')

class PlaneListView(ListView):
    model = Plane
    template_name = 'plane/plane_list.html'
    context_object_name = 'planes'

class PlaneCreateView(CreateView):
    model = Plane
    form_class = PlaneForm
    template_name = 'plane/plane_form.html'
    success_url = reverse_lazy('plane_list')

class PlaneUpdateView(UpdateView):
    model = Plane
    form_class = PlaneForm
    template_name = 'plane/plane_form.html'
    success_url = reverse_lazy('plane_list')

class PlaneDeleteView(DeleteView):
    model = Plane
    template_name = 'plane/plane_delete.html'
    success_url = reverse_lazy('plane_list')

