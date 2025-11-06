from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado que permite solo lectura a usuarios autenticados
    y escritura solo a administradores.
    """
    
    def has_permission(self, request, view):
        # Permitir acceso de lectura a cualquier usuario autenticado
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Permitir acceso de escritura solo a administradores
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permiso personalizado que permite acceso solo al propietario del objeto
    o a administradores.
    """
    
    def has_object_permission(self, request, view, obj):
        # Los administradores tienen acceso completo
        if request.user.is_staff:
            return True
        
        # El propietario del objeto tiene acceso
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Para pasajeros, verificar si el usuario es el mismo
        if hasattr(obj, 'passenger'):
            # Aquí podrías agregar lógica para vincular usuarios con pasajeros
            # Por ahora, permitir acceso si es el mismo usuario autenticado
            return True
        
        return False


class IsReservationOwnerOrAdmin(permissions.BasePermission):
    """
    Permiso personalizado para reservas - permite acceso solo al pasajero
    que hizo la reserva o a administradores.
    """
    
    def has_object_permission(self, request, view, obj):
        # Los administradores tienen acceso completo
        if request.user.is_staff:
            return True
        
        # Aquí podrías agregar lógica para verificar si el usuario autenticado
        # corresponde al pasajero de la reserva
        # Por ejemplo, si tienes un campo user en el modelo Passenger:
        # return obj.passenger.user == request.user
        
        # Por ahora, permitir acceso a usuarios autenticados
        return request.user.is_authenticated


class IsTicketOwnerOrAdmin(permissions.BasePermission):
    """
    Permiso personalizado para tickets - permite acceso solo al pasajero
    del ticket o a administradores.
    """
    
    def has_object_permission(self, request, view, obj):
        # Los administradores tienen acceso completo
        if request.user.is_staff:
            return True
        
        # Verificar si el usuario corresponde al pasajero del ticket
        # return obj.reservation.passenger.user == request.user
        
        # Por ahora, permitir acceso a usuarios autenticados
        return request.user.is_authenticated


class CanCancelReservation(permissions.BasePermission):
    """
    Permiso para cancelar reservas - solo el propietario o admin.
    """
    
    def has_object_permission(self, request, view, obj):
        # Solo permitir cancelación si la reserva no está cancelada
        if obj.status == 'cancelled':
            return False
        
        # Los administradores pueden cancelar cualquier reserva
        if request.user.is_staff:
            return True
        
        # El propietario puede cancelar su propia reserva
        # return obj.passenger.user == request.user
        
        # Por ahora, permitir a usuarios autenticados
        return request.user.is_authenticated


class CanCreateReservation(permissions.BasePermission):
    """
    Permiso para crear reservas - verificar que el vuelo esté disponible.
    """
    
    def has_permission(self, request, view):
        # Solo usuarios autenticados pueden crear reservas
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Verificar disponibilidad del asiento
        if hasattr(obj, 'seat') and obj.seat.status != 'available':
            return False
        
        # Verificar que el vuelo no esté cancelado
        if hasattr(obj, 'flight') and obj.flight.status == 'cancelled':
            return False
        
        return True