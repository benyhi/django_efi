from django.urls import path
from .views import (
    FlightListView, FlightCreateView, FlightUpdateView, FlightDeleteView,
    PlaneListView, PlaneCreateView, PlaneUpdateView, PlaneDeleteView, FlightReportPDFView
)

urlpatterns = [
    path('', FlightListView.as_view(), name='flight_list'),
    path('create/', FlightCreateView.as_view(), name='flight_create'),
    path('update/<int:pk>/', FlightUpdateView.as_view(), name='flight_update'),
    path('delete/<int:pk>/', FlightDeleteView.as_view(), name='flight_delete'),
    path('report/pdf/', FlightReportPDFView.as_view(), name='flight_report'),

    path('planes/', PlaneListView.as_view(), name='plane_list'),
    path('planes/create/', PlaneCreateView.as_view(), name='plane_create'),
    path('planes/update/<int:pk>/', PlaneUpdateView.as_view(), name='plane_update'),
    path('planes/delete/<int:pk>/', PlaneDeleteView.as_view(), name='plane_delete'),
]