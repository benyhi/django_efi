from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from .views import (
    passengers_by_flight, active_reservations_by_passenger,
    flight_statistics, reservation_statistics, passenger_statistics
)

# Configuración de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Airline Management API",
        default_version='v1',
        description="API para sistema de gestión de aerolíneas",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@airline.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Documentación API
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    # Endpoints de las apps
    path('auth/', include('user.urls')),
    path('', include('flight.urls')),
    path('', include('passenger.urls')),
    path('', include('reservation.urls')),
    
    # Endpoints de reportes
    path('reports/passengers-by-flight/', passengers_by_flight, name='passengers_by_flight'),
    path('reports/active-reservations-by-passenger/', active_reservations_by_passenger, name='active_reservations_by_passenger'),
    path('reports/flight-statistics/', flight_statistics, name='flight_statistics'),
    path('reports/reservation-statistics/', reservation_statistics, name='reservation_statistics'),
    path('reports/passenger-statistics/', passenger_statistics, name='passenger_statistics'),
]