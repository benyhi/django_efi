from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class APIResponse:
    """Clase para generar respuestas estandarizadas de la API"""
    
    @staticmethod
    def success(data=None, message="Operación exitosa", status_code=status.HTTP_200_OK):
        """Respuesta exitosa"""
        response_data = {
            'success': True,
            'message': message,
            'status_code': status_code
        }
        
        if data is not None:
            response_data['data'] = data
        
        return Response(response_data, status=status_code)
    
    @staticmethod
    def error(message="Error en la operación", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        """Respuesta de error"""
        response_data = {
            'success': False,
            'message': message,
            'status_code': status_code
        }
        
        if errors:
            response_data['errors'] = errors
        
        return Response(response_data, status=status_code)
    
    @staticmethod
    def validation_error(errors, message="Error de validación"):
        """Respuesta de error de validación"""
        return APIResponse.error(
            message=message,
            errors=errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    @staticmethod
    def not_found(message="Recurso no encontrado"):
        """Respuesta de recurso no encontrado"""
        return APIResponse.error(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    @staticmethod
    def unauthorized(message="No autorizado"):
        """Respuesta de no autorizado"""
        return APIResponse.error(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    @staticmethod
    def forbidden(message="Prohibido"):
        """Respuesta de prohibido"""
        return APIResponse.error(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN
        )
    
    @staticmethod
    def server_error(message="Error interno del servidor"):
        """Respuesta de error del servidor"""
        return APIResponse.error(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def custom_exception_handler(exc, context):
    """Manejador personalizado de excepciones para DRF"""
    # Llamar al manejador por defecto de DRF
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'success': False,
            'message': 'Error en la operación',
            'status_code': response.status_code,
            'errors': response.data
        }
        
        # Personalizar mensajes según el tipo de error
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            custom_response_data['message'] = 'Error de validación'
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            custom_response_data['message'] = 'No autorizado'
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            custom_response_data['message'] = 'Prohibido'
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            custom_response_data['message'] = 'Recurso no encontrado'
        elif response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            custom_response_data['message'] = 'Método no permitido'
        elif response.status_code >= 500:
            custom_response_data['message'] = 'Error interno del servidor'
            # Log del error del servidor
            logger.error(f"Server error: {exc}", exc_info=True)
        
        response.data = custom_response_data
    
    return response


class ValidationMixin:
    """Mixin para validaciones comunes"""
    
    def validate_required_fields(self, data: Dict[str, Any], required_fields: list) -> Dict[str, Any]:
        """Validar campos requeridos"""
        errors = {}
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == '':
                errors[field] = f'Este campo es requerido.'
        return errors
    
    def validate_positive_number(self, value: Any, field_name: str) -> str:
        """Validar que un número sea positivo"""
        try:
            num_value = float(value)
            if num_value <= 0:
                return f'{field_name} debe ser un número positivo.'
        except (ValueError, TypeError):
            return f'{field_name} debe ser un número válido.'
        return ''
    
    def validate_date_range(self, start_date, end_date) -> str:
        """Validar rango de fechas"""
        if start_date and end_date:
            if start_date > end_date:
                return 'La fecha de inicio no puede ser posterior a la fecha de fin.'
        return ''
    
    def validate_email_format(self, email: str) -> str:
        """Validar formato de email"""
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return 'Formato de email inválido.'
        return ''


class PaginationMixin:
    """Mixin para paginación estandarizada"""
    
    def get_paginated_response(self, data, page, page_size, total_count):
        """Generar respuesta paginada estandarizada"""
        total_pages = (total_count + page_size - 1) // page_size
        
        return {
            'results': data,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total_pages': total_pages,
                'total_count': total_count,
                'has_next': page < total_pages,
                'has_previous': page > 1,
                'next_page': page + 1 if page < total_pages else None,
                'previous_page': page - 1 if page > 1 else None
            }
        }


class FilterMixin:
    """Mixin para filtros comunes"""
    
    def apply_date_filter(self, queryset, date_field, start_date=None, end_date=None):
        """Aplicar filtro de fecha"""
        if start_date:
            filter_kwargs = {f'{date_field}__gte': start_date}
            queryset = queryset.filter(**filter_kwargs)
        
        if end_date:
            filter_kwargs = {f'{date_field}__lte': end_date}
            queryset = queryset.filter(**filter_kwargs)
        
        return queryset
    
    def apply_search_filter(self, queryset, search_fields, search_term):
        """Aplicar filtro de búsqueda"""
        if search_term:
            from django.db.models import Q
            search_query = Q()
            
            for field in search_fields:
                search_query |= Q(**{f'{field}__icontains': search_term})
            
            queryset = queryset.filter(search_query)
        
        return queryset


# Códigos de error personalizados
class ErrorCodes:
    # Errores generales
    INVALID_INPUT = 'INVALID_INPUT'
    RESOURCE_NOT_FOUND = 'RESOURCE_NOT_FOUND'
    UNAUTHORIZED = 'UNAUTHORIZED'
    FORBIDDEN = 'FORBIDDEN'
    
    # Errores de vuelos
    FLIGHT_NOT_FOUND = 'FLIGHT_NOT_FOUND'
    FLIGHT_NUMBER_EXISTS = 'FLIGHT_NUMBER_EXISTS'
    FLIGHT_CANCELLED = 'FLIGHT_CANCELLED'
    
    # Errores de asientos
    SEAT_NOT_AVAILABLE = 'SEAT_NOT_AVAILABLE'
    SEAT_NOT_FOUND = 'SEAT_NOT_FOUND'
    
    # Errores de reservas
    RESERVATION_NOT_FOUND = 'RESERVATION_NOT_FOUND'
    RESERVATION_ALREADY_CONFIRMED = 'RESERVATION_ALREADY_CONFIRMED'
    RESERVATION_ALREADY_CANCELLED = 'RESERVATION_ALREADY_CANCELLED'
    
    # Errores de pasajeros
    PASSENGER_NOT_FOUND = 'PASSENGER_NOT_FOUND'
    DNI_ALREADY_EXISTS = 'DNI_ALREADY_EXISTS'
    EMAIL_ALREADY_EXISTS = 'EMAIL_ALREADY_EXISTS'