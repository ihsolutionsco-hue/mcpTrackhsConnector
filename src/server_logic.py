"""
Lógica del servidor MCP para TrackHS
Separación de responsabilidades siguiendo mejores prácticas
"""

import os
from typing import Any, Dict, Optional

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.server.middleware.timing import TimingMiddleware

from tools import TOOLS
from utils.api_client import TrackHSAPIClient
from utils.exceptions import TrackHSError
from utils.logger import get_logger


def create_api_client() -> Optional[TrackHSAPIClient]:
    """
    Crea y configura el cliente API de TrackHS

    Returns:
        Cliente API configurado o None si no hay credenciales
    """
    logger = get_logger(__name__)

    try:
        username = os.getenv("TRACKHS_USERNAME")
        password = os.getenv("TRACKHS_PASSWORD")
        api_url = os.getenv("TRACKHS_API_URL", "https://ihmvacations.trackhs.com")

        if not username or not password:
            logger.warning(
                "Credenciales de TrackHS no configuradas",
                extra={
                    "username_configured": bool(username),
                    "password_configured": bool(password),
                },
            )
            return None

        api_client = TrackHSAPIClient(
            base_url=api_url, username=username, password=password, timeout=30
        )

        logger.info(
            "Cliente API TrackHS configurado",
            extra={"api_url": api_url, "username": username},
        )

        return api_client

    except Exception as api_error:
        logger.error(
            "Error configurando cliente API",
            extra={
                "error_type": type(api_error).__name__,
                "error_message": str(api_error),
            },
        )
        raise


def create_mcp_server() -> FastMCP:
    """
    Crea y configura el servidor MCP

    Returns:
        Servidor MCP configurado
    """
    logger = get_logger(__name__)

    try:
        mcp_server = FastMCP(
            name="TrackHS API",
            version="2.0.0",
            strict_input_validation=False,  # CRÍTICO: Permite coerción de tipos
            mask_error_details=True,
        )

        # Agregar timing middleware para monitoreo de rendimiento
        mcp_server.add_middleware(TimingMiddleware())

        logger.info("Servidor MCP configurado")
        return mcp_server

    except Exception as mcp_error:
        logger.error(
            "Error configurando servidor MCP",
            extra={
                "error_type": type(mcp_error).__name__,
                "error_message": str(mcp_error),
            },
        )
        raise


def register_tools(mcp_server: FastMCP, api_client: TrackHSAPIClient) -> Dict[str, Any]:
    """
    Registra todas las herramientas MCP en el servidor

    Args:
        mcp_server: Servidor MCP donde registrar las herramientas
        api_client: Cliente API para las herramientas

    Returns:
        Diccionario con las herramientas registradas
    """
    logger = get_logger(__name__)
    tools = {}

    try:
        for tool_class in TOOLS:
            # Crear instancia de la herramienta
            tool_instance = tool_class(api_client)

            # Registrar herramienta en MCP
            register_single_tool(mcp_server, tool_instance)

            # Guardar referencia
            tools[tool_instance.name] = tool_instance

            logger.info(
                f"Herramienta registrada: {tool_instance.name}",
                extra={
                    "tool_name": tool_instance.name,
                    "tool_class": tool_class.__name__,
                },
            )

        logger.info(
            f"Total de herramientas registradas: {len(tools)}",
            extra={"tool_count": len(tools)},
        )

        return tools

    except Exception as tool_error:
        logger.error(
            "Error registrando herramientas",
            extra={
                "error_type": type(tool_error).__name__,
                "error_message": str(tool_error),
            },
        )
        raise


def register_single_tool(mcp_server: FastMCP, tool_instance: Any) -> None:
    """
    Registra una herramienta individual en el servidor MCP

    Args:
        mcp_server: Servidor MCP donde registrar la herramienta
        tool_instance: Instancia de la herramienta
    """
    logger = get_logger(__name__)

    def tool_wrapper(**kwargs) -> Dict[str, Any]:
        """Wrapper para ejecutar la herramienta"""
        try:
            return tool_instance.execute(**kwargs)
        except TrackHSError as trackhs_error:
            # Re-lanzar errores de TrackHS como ToolError
            raise ToolError(str(trackhs_error))
        except Exception as unexpected_error:
            # Log error inesperado
            logger.error(
                f"Error inesperado en herramienta {tool_instance.name}",
                extra={
                    "tool_name": tool_instance.name,
                    "error_type": type(unexpected_error).__name__,
                    "error_message": str(unexpected_error),
                    "input_params": kwargs,
                },
            )
            raise ToolError(f"Error interno: {str(unexpected_error)}")

    # Registrar en FastMCP
    mcp_server.tool(name=tool_instance.name, description=tool_instance.description)(
        tool_wrapper
    )
