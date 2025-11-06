from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView, UserViewSet,
    register, logout, profile, update_profile, change_password
)

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    # Autenticación JWT
    path('login', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', register, name='register'),
    path('logout', logout, name='logout'),
    
    # Perfil de usuario
    path('profile', profile, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
    path('change-password/', change_password, name='change_password'),
    
    # Gestión de usuarios (admin)
    path('', include(router.urls)),
]