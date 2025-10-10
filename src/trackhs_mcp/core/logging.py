"""
Sistema de logging mejorado para Track HS MCP Connector
Incluye niveles, contexto, métricas y integración con MCP
"""

import logging
import json
import time
import uuid
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timezone
import asyncio
from contextvars import ContextVar

# Context variables para tracking de requests
request_id_var: ContextVar[Optional[str]] = ContextVar('request_id', default=None)
user_id_var: ContextVar[Optional[str]] = ContextVar('user_id', default=None)
session_id_var: ContextVar[Optional[str]] = ContextVar('session_id', default=None)

class LogLevel(Enum):
    """Niveles de logging personalizados"""
    TRACE = 5
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

class LogCategory(Enum):
    """Categorías de logs"""
    API_REQUEST = "api_request"
    API_RESPONSE = "api_response"
    MCP_TOOL = "mcp_tool"
    MCP_RESOURCE = "mcp_resource"
    MCP_PROMPT = "mcp_prompt"
    AUTHENTICATION = "authentication"
    PAGINATION = "pagination"
    ERROR = "error"
    PERFORMANCE = "performance"
    SECURITY = "security"

@dataclass
class LogContext:
    """Contexto de logging"""
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    tool_name: Optional[str] = None
    resource_uri: Optional[str] = None
    prompt_name: Optional[str] = None
    api_endpoint: Optional[str] = None
    http_method: Optional[str] = None
    response_code: Optional[int] = None
    duration_ms: Optional[float] = None
    additional_data: Optional[Dict[str, Any]] = None

@dataclass
class LogMetric:
    """Métrica de logging"""
    name: str
    value: Union[int, float, str]
    unit: Optional[str] = None
    tags: Optional[Dict[str, str]] = None
    timestamp: Optional[datetime] = None

class TrackHSLogger:
    """Logger personalizado para Track HS MCP Connector"""
    
    def __init__(self, name: str, mcp_client=None):
        self.logger = logging.getLogger(name)
        self.mcp_client = mcp_client
        self._setup_logger()
        self._metrics: List[LogMetric] = []
    
    def _setup_logger(self):
        """Configura el logger"""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def _get_context(self) -> LogContext:
        """Obtiene el contexto actual"""
        return LogContext(
            request_id=request_id_var.get(),
            user_id=user_id_var.get(),
            session_id=session_id_var.get()
        )
    
    def _format_message(self, message: str, context: LogContext, 
                       category: LogCategory, level: LogLevel) -> Dict[str, Any]:
        """Formatea el mensaje de log"""
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level.name,
            "category": category.value,
            "message": message,
            "context": asdict(context),
            "logger": self.logger.name
        }
        
        # Filtrar valores None del contexto
        log_entry["context"] = {k: v for k, v in log_entry["context"].items() if v is not None}
        
        return log_entry
    
    def _log_to_mcp(self, log_entry: Dict[str, Any]):
        """Envía log al cliente MCP si está disponible"""
        if self.mcp_client:
            try:
                # Enviar log al cliente MCP
                asyncio.create_task(self._send_mcp_log(log_entry))
            except Exception as e:
                # Fallback al logger estándar si MCP falla
                self.logger.error(f"Error enviando log a MCP: {str(e)}")
    
    async def _send_mcp_log(self, log_entry: Dict[str, Any]):
        """Envía log al cliente MCP"""
        try:
            if hasattr(self.mcp_client, 'send_log'):
                await self.mcp_client.send_log(
                    level=log_entry["level"],
                    message=log_entry["message"],
                    data=log_entry
                )
        except Exception as e:
            self.logger.error(f"Error en _send_mcp_log: {str(e)}")
    
    def log(self, level: LogLevel, message: str, category: LogCategory = LogCategory.MCP_TOOL,
            context: Optional[LogContext] = None, **kwargs):
        """Log principal con contexto"""
        ctx = context or self._get_context()
        ctx.additional_data = kwargs
        
        log_entry = self._format_message(message, ctx, category, level)
        
        # Log estándar
        if level.value >= LogLevel.INFO.value:
            self.logger.log(level.value, json.dumps(log_entry, ensure_ascii=False))
        
        # Log a MCP
        self._log_to_mcp(log_entry)
    
    def trace(self, message: str, **kwargs):
        """Log de nivel TRACE"""
        self.log(LogLevel.TRACE, message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log de nivel DEBUG"""
        self.log(LogLevel.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log de nivel INFO"""
        self.log(LogLevel.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log de nivel WARNING"""
        self.log(LogLevel.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log de nivel ERROR"""
        self.log(LogLevel.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log de nivel CRITICAL"""
        self.log(LogLevel.CRITICAL, message, **kwargs)
    
    def log_api_request(self, method: str, endpoint: str, params: Dict[str, Any] = None):
        """Log de request a API"""
        context = LogContext(
            api_endpoint=endpoint,
            http_method=method,
            additional_data={"params": params}
        )
        self.log(
            LogLevel.INFO,
            f"API Request: {method} {endpoint}",
            LogCategory.API_REQUEST,
            context
        )
    
    def log_api_response(self, method: str, endpoint: str, status_code: int, 
                        duration_ms: float, response_size: int = None):
        """Log de response de API"""
        context = LogContext(
            api_endpoint=endpoint,
            http_method=method,
            response_code=status_code,
            duration_ms=duration_ms,
            additional_data={"response_size": response_size}
        )
        self.log(
            LogLevel.INFO,
            f"API Response: {method} {endpoint} - {status_code} ({duration_ms}ms)",
            LogCategory.API_RESPONSE,
            context
        )
    
    def log_tool_execution(self, tool_name: str, params: Dict[str, Any], 
                          duration_ms: float, success: bool):
        """Log de ejecución de herramienta MCP"""
        context = LogContext(
            tool_name=tool_name,
            duration_ms=duration_ms,
            additional_data={"params": params, "success": success}
        )
        level = LogLevel.INFO if success else LogLevel.ERROR
        category = LogCategory.MCP_TOOL
        
        self.log(
            level,
            f"Tool execution: {tool_name} - {'SUCCESS' if success else 'FAILED'} ({duration_ms}ms)",
            category,
            context
        )
    
    def log_resource_access(self, resource_uri: str, access_type: str, 
                           duration_ms: float = None):
        """Log de acceso a recurso MCP"""
        context = LogContext(
            resource_uri=resource_uri,
            duration_ms=duration_ms,
            additional_data={"access_type": access_type}
        )
        self.log(
            LogLevel.INFO,
            f"Resource access: {resource_uri} ({access_type})",
            LogCategory.MCP_RESOURCE,
            context
        )
    
    def log_prompt_usage(self, prompt_name: str, args: Dict[str, Any], 
                        duration_ms: float = None):
        """Log de uso de prompt MCP"""
        context = LogContext(
            prompt_name=prompt_name,
            duration_ms=duration_ms,
            additional_data={"args": args}
        )
        self.log(
            LogLevel.INFO,
            f"Prompt usage: {prompt_name}",
            LogCategory.MCP_PROMPT,
            context
        )
    
    def log_authentication(self, user_id: str, success: bool, method: str = None):
        """Log de autenticación"""
        context = LogContext(
            user_id=user_id,
            additional_data={"success": success, "method": method}
        )
        level = LogLevel.INFO if success else LogLevel.WARNING
        self.log(
            level,
            f"Authentication: {user_id} - {'SUCCESS' if success else 'FAILED'}",
            LogCategory.AUTHENTICATION,
            context
        )
    
    def log_performance(self, operation: str, duration_ms: float, 
                       metrics: Dict[str, Any] = None):
        """Log de rendimiento"""
        context = LogContext(
            duration_ms=duration_ms,
            additional_data={"operation": operation, "metrics": metrics}
        )
        self.log(
            LogLevel.INFO,
            f"Performance: {operation} - {duration_ms}ms",
            LogCategory.PERFORMANCE,
            context
        )
    
    def log_security(self, event: str, details: Dict[str, Any] = None):
        """Log de seguridad"""
        context = LogContext(
            additional_data={"event": event, "details": details}
        )
        self.log(
            LogLevel.WARNING,
            f"Security event: {event}",
            LogCategory.SECURITY,
            context
        )
    
    def add_metric(self, name: str, value: Union[int, float, str], 
                  unit: str = None, tags: Dict[str, str] = None):
        """Agrega una métrica"""
        metric = LogMetric(
            name=name,
            value=value,
            unit=unit,
            tags=tags,
            timestamp=datetime.now(timezone.utc)
        )
        self._metrics.append(metric)
    
    def get_metrics(self) -> List[LogMetric]:
        """Obtiene todas las métricas"""
        return self._metrics.copy()
    
    def clear_metrics(self):
        """Limpia las métricas"""
        self._metrics.clear()

# Context managers para tracking
class RequestContext:
    """Context manager para tracking de requests"""
    
    def __init__(self, request_id: str = None, user_id: str = None, session_id: str = None):
        self.request_id = request_id or str(uuid.uuid4())
        self.user_id = user_id
        self.session_id = session_id
        self._tokens = []
    
    def __enter__(self):
        if self.request_id:
            self._tokens.append(request_id_var.set(self.request_id))
        if self.user_id:
            self._tokens.append(user_id_var.set(self.user_id))
        if self.session_id:
            self._tokens.append(session_id_var.set(self.session_id))
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        for token in self._tokens:
            token.delete()

class PerformanceTimer:
    """Context manager para medir rendimiento"""
    
    def __init__(self, logger: TrackHSLogger, operation: str):
        self.logger = logger
        self.operation = operation
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration_ms = (time.time() - self.start_time) * 1000
            self.logger.log_performance(self.operation, duration_ms)

# Funciones de conveniencia
def get_logger(name: str, mcp_client=None) -> TrackHSLogger:
    """Obtiene un logger personalizado"""
    return TrackHSLogger(name, mcp_client)

def log_api_call(logger: TrackHSLogger, method: str, endpoint: str, 
                 params: Dict[str, Any] = None):
    """Función de conveniencia para log de API calls"""
    logger.log_api_request(method, endpoint, params)

def log_tool_call(logger: TrackHSLogger, tool_name: str, params: Dict[str, Any], 
                  duration_ms: float, success: bool):
    """Función de conveniencia para log de tool calls"""
    logger.log_tool_execution(tool_name, params, duration_ms, success)
