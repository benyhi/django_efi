from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('flights/', include('flight.urls')),
    path('passengers/', include('passenger.urls')),
    path('reservations/', include('reservation.urls')),
    path('users/', include('user.urls')),
]
