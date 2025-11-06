from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlightViewSet, PlaneViewSet

router = DefaultRouter()
router.register(r'flights', FlightViewSet)
router.register(r'planes', PlaneViewSet)

urlpatterns = [
    path('', include(router.urls)),
]