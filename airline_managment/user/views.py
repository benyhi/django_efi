from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    UserProfileSerializer, ChangePasswordSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Vista personalizada para obtener tokens JWT"""
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            # Agregar información del usuario a la respuesta
            username = request.data.get('username')
            try:
                user = User.objects.get(username=username)
                response.data['user'] = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser
                }
            except User.DoesNotExist:
                pass
        return response


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Registrar nuevo usuario."""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Usuario registrado exitosamente',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Cerrar sesión (invalidar refresh token)."""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({'message': 'Sesión cerrada exitosamente'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Obtener perfil del usuario autenticado."""
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Actualizar perfil del usuario autenticado."""
    serializer = UserProfileSerializer(
        request.user, 
        data=request.data, 
        partial=request.method == 'PATCH'
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Cambiar contraseña del usuario autenticado."""
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Contraseña cambiada exitosamente'})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de usuarios (solo para administradores)."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    @action(detail=True, methods=['post'])
    def set_admin(self, request, pk=None):
        """Convertir usuario en administrador"""
        user = self.get_object()
        user.is_staff = True
        user.is_superuser = True
        user.save()
        
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def remove_admin(self, request, pk=None):
        """Remover privilegios de administrador"""
        user = self.get_object()
        user.is_staff = False
        user.is_superuser = False
        user.save()
        
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activar usuario"""
        user = self.get_object()
        user.is_active = True
        user.save()
        
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Desactivar usuario"""
        user = self.get_object()
        user.is_active = False
        user.save()
        
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def admins(self, request):
        """Listar usuarios administradores"""
        admins = User.objects.filter(is_staff=True)
        serializer = UserSerializer(admins, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active_users(self, request):
        """Listar usuarios activos"""
        active_users = User.objects.filter(is_active=True)
        serializer = UserSerializer(active_users, many=True)
        return Response(serializer.data)