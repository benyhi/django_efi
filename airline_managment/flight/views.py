from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Flight, Plane
from .forms import FlightForm, PlaneForm
from django.views import View
from .utils.generate_pdf import generar_pdf

# Create your views here.

class FlightListView(LoginRequiredMixin, ListView):
    model = Flight
    template_name = 'flight/flight_list.html'
    context_object_name = 'flights'

class FlightCreateView(LoginRequiredMixin, CreateView):
    model = Flight
    form_class = FlightForm
    template_name = 'flight/flight_form.html'
    success_url = reverse_lazy('flight_list')

class FlightUpdateView(LoginRequiredMixin, UpdateView):
    model = Flight
    form_class = FlightForm
    template_name = 'flight/flight_form.html'
    success_url = reverse_lazy('flight_list')

class FlightDeleteView(LoginRequiredMixin, DeleteView):
    model = Flight
    template_name = 'flight/flight_delete.html'
    success_url = reverse_lazy('flight_list')

class FlightReportPDFView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        vuelos_queryset = Flight.objects.all()
        return generar_pdf(request, vuelos_queryset)

class PlaneListView(LoginRequiredMixin, ListView):
    model = Plane
    template_name = 'plane/plane_list.html'
    context_object_name = 'planes'

class PlaneCreateView(LoginRequiredMixin, CreateView):
    model = Plane
    form_class = PlaneForm
    template_name = 'plane/plane_form.html'
    success_url = reverse_lazy('plane_list')

class PlaneUpdateView(LoginRequiredMixin, UpdateView):
    model = Plane
    form_class = PlaneForm
    template_name = 'plane/plane_form.html'
    success_url = reverse_lazy('plane_list')

class PlaneDeleteView(LoginRequiredMixin, DeleteView):
    model = Plane
    template_name = 'plane/plane_delete.html'
    success_url = reverse_lazy('plane_list')

