from django.urls import path
from .views import (
    ReservationListView, ReservationCreateView, ReservationUpdateView, ReservationDeleteView,
    SeatListView, SeatCreateView, SeatUpdateView, SeatDeleteView, TicketCreateView, TicketDeleteView, TicketListView, TicketUpdateView
)

urlpatterns = [
    path('', ReservationListView.as_view(), name='reservation_list'),
    path('create/', ReservationCreateView.as_view(), name='reservation_create'),
    path('update/<int:pk>/', ReservationUpdateView.as_view(), name='reservation_update'),
    path('delete/<int:pk>/', ReservationDeleteView.as_view(), name='reservation_delete'),

    path('seats/', SeatListView.as_view(), name='seat_list'),
    path('seats/create/', SeatCreateView.as_view(), name='seat_create'),
    path('seats/update/<int:pk>/', SeatUpdateView.as_view(), name='seat_update'),
    path('seats/delete/<int:pk>/', SeatDeleteView.as_view(), name='seat_delete'),

    path('tickets/', TicketListView.as_view(), name='ticket_list'),
    path('tickets/create/', TicketCreateView.as_view(), name='ticket_create'),
    path('tickets/update/<int:pk>/', TicketUpdateView.as_view(), name='ticket_update'),
    path('tickets/delete/<int:pk>/', TicketDeleteView.as_view(), name='ticket_delete'),
]