from django.urls import path
from .views import PassengerListView, PassengerCreateView, PassengerUpdateView, PassengerDeleteView

urlpatterns = [
    path('', PassengerListView.as_view(), name='passenger_list'),
    path('create/', PassengerCreateView.as_view(), name='passenger_create'),
    path('update/<int:pk>/', PassengerUpdateView.as_view(), name='passenger_update'),
    path('delete/<int:pk>/', PassengerDeleteView.as_view(), name='passenger_delete'),
]