from django.urls import path
from .views import (
    ReservationListView, ReservationCreateView, ReservationUpdateView, ReservationDeleteView,
    SeatListView, SeatCreateView, SeatUpdateView, SeatDeleteView
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
]