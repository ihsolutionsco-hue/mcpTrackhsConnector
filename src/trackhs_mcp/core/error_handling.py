"""
Manejo robusto de errores para Track HS MCP Connector
Basado en la especificación de la API y mejores prácticas de MCP
"""

import json
import traceback
from typing import Dict, Any, Optional, Union, List
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timezone
import asyncio
from .logging import get_logger

logger = get_logger(__name__)

class ErrorType(Enum):
    """Tipos de errores del sistema"""
    API_ERROR = "api_error"
    AUTHENTICATION_ERROR = "authentication_error"
    VALIDATION_ERROR = "validation_error"
    NETWORK_ERROR = "network_error"
    TIMEOUT_ERROR = "timeout_error"
    RATE_LIMIT_ERROR = "rate_limit_error"
    MCP_ERROR = "mcp_error"
    INTERNAL_ERROR = "internal_error"
    CONFIGURATION_ERROR = "configuration_error"

class ErrorSeverity(Enum):
    """Niveles de severidad de errores"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class TrackHSError:
    """Error personalizado de Track HS"""
    error_type: ErrorType
    message: str
    details: Optional[Dict[str, Any]] = None
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
    timestamp: Optional[datetime] = None
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    retry_after: Optional[int] = None
    suggested_action: Optional[str] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)

@dataclass
class APIErrorResponse:
    """Respuesta de error de la API según especificación RFC 7807"""
    type: str
    title: str
    status: int
    detail: str
    code: Optional[str] = None
    validation_messages: Optional[List[str]] = None
    instance: Optional[str] = None

class TrackHSErrorHandler:
    """Manejador de errores para Track HS MCP Connector"""
    
    def __init__(self):
        self.error_counts: Dict[str, int] = {}
        self.retry_strategies: Dict[ErrorType, Dict[str, Any]] = {
            ErrorType.NETWORK_ERROR: {"max_retries": 3, "backoff_factor": 2},
            ErrorType.TIMEOUT_ERROR: {"max_retries": 2, "backoff_factor": 1.5},
            ErrorType.RATE_LIMIT_ERROR: {"max_retries": 5, "backoff_factor": 2},
            ErrorType.API_ERROR: {"max_retries": 1, "backoff_factor": 1},
        }
    
    def parse_api_error(self, response_data: Dict[str, Any], status_code: int) -> TrackHSError:
        """Parsea error de la API según especificación RFC 7807"""
        try:
            api_error = APIErrorResponse(
                type=response_data.get("type", "about:blank"),
                title=response_data.get("title", "API Error"),
                status=status_code,
                detail=response_data.get("detail", "Unknown error"),
                code=response_data.get("code"),
                validation_messages=response_data.get("validation_messages"),
                instance=response_data.get("instance")
            )
            
            # Determinar tipo de error basado en status code
            if status_code == 401:
                error_type = ErrorType.AUTHENTICATION_ERROR
                severity = ErrorSeverity.HIGH
                suggested_action = "Verificar credenciales de autenticación"
            elif status_code == 403:
                error_type = ErrorType.AUTHENTICATION_ERROR
                severity = ErrorSeverity.HIGH
                suggested_action = "Verificar permisos de acceso"
            elif status_code == 400:
                error_type = ErrorType.VALIDATION_ERROR
                severity = ErrorSeverity.MEDIUM
                suggested_action = "Revisar parámetros de la solicitud"
            elif status_code == 422:
                error_type = ErrorType.VALIDATION_ERROR
                severity = ErrorSeverity.MEDIUM
                suggested_action = "Corregir datos de entrada según validation_messages"
            elif status_code == 429:
                error_type = ErrorType.RATE_LIMIT_ERROR
                severity = ErrorSeverity.MEDIUM
                suggested_action = "Esperar antes de realizar más solicitudes"
            elif status_code >= 500:
                error_type = ErrorType.API_ERROR
                severity = ErrorSeverity.HIGH
                suggested_action = "Reintentar más tarde o contactar soporte"
            else:
                error_type = ErrorType.API_ERROR
                severity = ErrorSeverity.MEDIUM
                suggested_action = "Revisar la solicitud y reintentar"
            
            return TrackHSError(
                error_type=error_type,
                message=f"{api_error.title}: {api_error.detail}",
                details={
                    "api_error": api_error.__dict__,
                    "status_code": status_code,
                    "response_data": response_data
                },
                severity=severity,
                suggested_action=suggested_action
            )
            
        except Exception as e:
            logger.error(f"Error parsing API error: {str(e)}")
            return TrackHSError(
                error_type=ErrorType.API_ERROR,
                message=f"Error parsing API response: {str(e)}",
                details={"original_response": response_data, "parse_error": str(e)},
                severity=ErrorSeverity.MEDIUM
            )
    
    def handle_network_error(self, exception: Exception) -> TrackHSError:
        """Maneja errores de red"""
        error_message = str(exception)
        
        if "timeout" in error_message.lower():
            error_type = ErrorType.TIMEOUT_ERROR
            severity = ErrorSeverity.MEDIUM
            suggested_action = "Verificar conectividad y reintentar"
        elif "connection" in error_message.lower():
            error_type = ErrorType.NETWORK_ERROR
            severity = ErrorSeverity.HIGH
            suggested_action = "Verificar conectividad a internet y configuración de red"
        else:
            error_type = ErrorType.NETWORK_ERROR
            severity = ErrorSeverity.MEDIUM
            suggested_action = "Reintentar la operación"
        
        return TrackHSError(
            error_type=error_type,
            message=f"Network error: {error_message}",
            details={"exception_type": type(exception).__name__, "traceback": traceback.format_exc()},
            severity=severity,
            suggested_action=suggested_action
        )
    
    def handle_validation_error(self, field: str, value: Any, constraint: str) -> TrackHSError:
        """Maneja errores de validación"""
        return TrackHSError(
            error_type=ErrorType.VALIDATION_ERROR,
            message=f"Validation error for field '{field}': {constraint}",
            details={"field": field, "value": value, "constraint": constraint},
            severity=ErrorSeverity.LOW,
            suggested_action=f"Corregir el valor del campo '{field}' según las restricciones"
        )
    
    def handle_mcp_error(self, error: Exception, context: str) -> TrackHSError:
        """Maneja errores específicos de MCP"""
        return TrackHSError(
            error_type=ErrorType.MCP_ERROR,
            message=f"MCP error in {context}: {str(error)}",
            details={"context": context, "exception_type": type(error).__name__, "traceback": traceback.format_exc()},
            severity=ErrorSeverity.MEDIUM,
            suggested_action="Verificar configuración MCP y reintentar"
        )
    
    def handle_internal_error(self, error: Exception, context: str) -> TrackHSError:
        """Maneja errores internos del sistema"""
        return TrackHSError(
            error_type=ErrorType.INTERNAL_ERROR,
            message=f"Internal error in {context}: {str(error)}",
            details={"context": context, "exception_type": type(error).__name__, "traceback": traceback.format_exc()},
            severity=ErrorSeverity.HIGH,
            suggested_action="Contactar soporte técnico"
        )
    
    def should_retry(self, error: TrackHSError) -> bool:
        """Determina si un error debe ser reintentado"""
        if error.error_type not in self.retry_strategies:
            return False
        
        error_key = f"{error.error_type.value}_{error.request_id or 'unknown'}"
        current_retries = self.error_counts.get(error_key, 0)
        max_retries = self.retry_strategies[error.error_type]["max_retries"]
        
        return current_retries < max_retries
    
    def get_retry_delay(self, error: TrackHSError) -> float:
        """Calcula el delay para reintento"""
        if error.error_type not in self.retry_strategies:
            return 1.0
        
        error_key = f"{error.error_type.value}_{error.request_id or 'unknown'}"
        current_retries = self.error_counts.get(error_key, 0)
        backoff_factor = self.retry_strategies[error.error_type]["backoff_factor"]
        
        return backoff_factor ** current_retries
    
    def increment_retry_count(self, error: TrackHSError):
        """Incrementa el contador de reintentos"""
        error_key = f"{error.error_type.value}_{error.request_id or 'unknown'}"
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1
    
    def reset_retry_count(self, error: TrackHSError):
        """Resetea el contador de reintentos"""
        error_key = f"{error.error_type.value}_{error.request_id or 'unknown'}"
        self.error_counts.pop(error_key, None)
    
    def format_error_response(self, error: TrackHSError) -> Dict[str, Any]:
        """Formatea error para respuesta MCP"""
        response = {
            "error": True,
            "error_type": error.error_type.value,
            "message": error.message,
            "severity": error.severity.value,
            "timestamp": error.timestamp.isoformat(),
        }
        
        if error.details:
            response["details"] = error.details
        
        if error.suggested_action:
            response["suggested_action"] = error.suggested_action
        
        if error.retry_after:
            response["retry_after"] = error.retry_after
        
        if error.request_id:
            response["request_id"] = error.request_id
        
        return response
    
    def log_error(self, error: TrackHSError, context: str = ""):
        """Registra error en el sistema de logging"""
        log_message = f"TrackHS Error [{error.error_type.value}]: {error.message}"
        
        if context:
            log_message = f"{context} - {log_message}"
        
        if error.severity == ErrorSeverity.CRITICAL:
            logger.critical(log_message, error_type=error.error_type.value, details=error.details)
        elif error.severity == ErrorSeverity.HIGH:
            logger.error(log_message, error_type=error.error_type.value, details=error.details)
        elif error.severity == ErrorSeverity.MEDIUM:
            logger.warning(log_message, error_type=error.error_type.value, details=error.details)
        else:
            logger.info(log_message, error_type=error.error_type.value, details=error.details)

# Funciones de conveniencia
def handle_api_error(response_data: Dict[str, Any], status_code: int) -> TrackHSError:
    """Función de conveniencia para manejar errores de API"""
    handler = TrackHSErrorHandler()
    return handler.parse_api_error(response_data, status_code)

def handle_network_error(exception: Exception) -> TrackHSError:
    """Función de conveniencia para manejar errores de red"""
    handler = TrackHSErrorHandler()
    return handler.handle_network_error(exception)

def handle_validation_error(field: str, value: Any, constraint: str) -> TrackHSError:
    """Función de conveniencia para manejar errores de validación"""
    handler = TrackHSErrorHandler()
    return handler.handle_validation_error(field, value, constraint)

def format_error_for_mcp(error: TrackHSError) -> Dict[str, Any]:
    """Función de conveniencia para formatear error para MCP"""
    handler = TrackHSErrorHandler()
    return handler.format_error_response(error)

# Decorador para manejo automático de errores
def error_handler(context: str = ""):
    """Decorador para manejo automático de errores"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            handler = TrackHSErrorHandler()
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                error = handler.handle_internal_error(e, context or func.__name__)
                handler.log_error(error, context)
                return handler.format_error_response(error)
        return wrapper
    return decorator
