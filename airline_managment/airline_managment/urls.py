from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import HomeView
from user.views import LoginView, RegisterView, LogoutView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('flights/', include('flight.urls')),
    path('passengers/', include('passenger.urls')),
    path('reservations/', include('reservation.urls')),
    path('users/', include('user.urls')),
]
