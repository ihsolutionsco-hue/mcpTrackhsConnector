"""
Lógica del servidor MCP para TrackHS
Separación de responsabilidades siguiendo mejores prácticas
"""

import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from fastmcp import FastMCP

# Cargar variables de entorno desde .env
load_dotenv()
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
            logger.error(
                "CREDENCIALES DE TRACKHS NO CONFIGURADAS",
                extra={
                    "username_configured": bool(username),
                    "password_configured": bool(password),
                    "error_type": "missing_credentials",
                    "solution": "Configure TRACKHS_USERNAME y TRACKHS_PASSWORD en variables de entorno o archivo .env",
                },
            )
            print("\n" + "=" * 60)
            print("ERROR: CREDENCIALES DE TRACKHS NO CONFIGURADAS")
            print("=" * 60)
            print("Para usar el servidor MCP de TrackHS, necesitas configurar:")
            print("1. TRACKHS_USERNAME - Tu usuario de TrackHS")
            print("2. TRACKHS_PASSWORD - Tu contraseña de TrackHS")
            print("\nOpciones de configuración:")
            print("a) Variables de entorno:")
            print("   set TRACKHS_USERNAME=tu_usuario")
            print("   set TRACKHS_PASSWORD=tu_contrasena")
            print("\nb) Archivo .env (recomendado):")
            print("   Copia env.example como .env y configura las credenciales")
            print("=" * 60)
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
        # Importar dinámicamente la lista de herramientas para permitir monkeypatching en tests
        try:
            import tools as tools_module  # type: ignore

            tool_classes = getattr(tools_module, "TOOLS", TOOLS)
        except Exception:
            tool_classes = TOOLS

        for tool_class in tool_classes:
            # Crear instancia de la herramienta
            tool_instance = tool_class(api_client)

            # Registrar herramienta en MCP
            register_single_tool(mcp_server, tool_instance)

            # Guardar referencia
            tools[tool_instance.name] = tool_instance

            safe_tool_class_name = getattr(
                tool_class, "__name__", getattr(tool_class, "name", str(tool_class))
            )
            logger.info(
                f"Herramienta registrada: {tool_instance.name}",
                extra={
                    "tool_name": tool_instance.name,
                    "tool_class": safe_tool_class_name,
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

    FastMCP no acepta funciones con **kwargs, así que creamos un wrapper
    que llama directamente al método execute de la herramienta.

    El método execute acepta **kwargs pero FastMCP no puede registrar eso,
    así que usamos una función lambda que llama a execute con los kwargs
    que FastMCP pasa como argumentos individuales.

    Args:
        mcp_server: Servidor MCP donde registrar la herramienta
        tool_instance: Instancia de la herramienta
    """
    logger = get_logger(__name__)

    # Obtener el schema de entrada para crear type hints
    input_schema = tool_instance.input_schema

    # Crear función wrapper sin **kwargs
    # FastMCP necesita una función con parámetros específicos
    # Usamos execute directamente pero necesitamos crear una función
    # que acepte los parámetros del schema como argumentos individuales

    import inspect
    from typing import get_type_hints

    # Obtener campos del schema Pydantic
    if hasattr(input_schema, "model_fields"):
        # Pydantic v2
        schema_fields = input_schema.model_fields
    elif hasattr(input_schema, "__fields__"):
        # Pydantic v1
        schema_fields = input_schema.__fields__
    else:
        schema_fields = {}

    # Crear función wrapper dinámica
    # Necesitamos una función que acepte todos los campos del schema
    # pero FastMCP necesita la firma explícita
    # Solución: usar functools para crear un wrapper que FastMCP pueda registrar

    from functools import wraps

    # Obtener los campos del schema con sus tipos
    type_hints = {}
    defaults = {}

    for field_name, field_info in schema_fields.items():
        # Obtener el tipo del campo
        if hasattr(field_info, "annotation"):
            field_type = field_info.annotation
        elif hasattr(field_info, "type_"):
            field_type = field_info.type_
        else:
            field_type = Any

        # Si es Optional, extraer el tipo interno
        if hasattr(field_type, "__args__") and len(field_type.__args__) > 0:
            # Optional[X] o Union[X, None] -> X
            non_none_args = [
                arg for arg in field_type.__args__ if arg is not type(None)
            ]
            if non_none_args:
                field_type = non_none_args[0]

        type_hints[field_name] = field_type

        # Obtener default si existe
        if hasattr(field_info, "default"):
            default = field_info.default
            if default is not None and not callable(default):
                defaults[field_name] = default

    # Crear función wrapper dinámica sin **kwargs
    # FastMCP necesita una función que acepte cada campo del schema como parámetro individual
    # Usamos types.FunctionType para crear una función con la firma correcta

    import types
    from inspect import Parameter, Signature

    # Crear parámetros para la firma de la función
    parameters = []
    for field_name, field_info in schema_fields.items():
        # Obtener tipo y default
        field_type = type_hints.get(field_name, Any)
        default_value = defaults.get(field_name, Parameter.empty)

        # Crear parámetro
        param = Parameter(
            name=field_name,
            kind=Parameter.KEYWORD_ONLY,
            default=default_value,
            annotation=field_type,
        )
        parameters.append(param)

    # Crear firma de la función
    sig = Signature(parameters, return_annotation=Dict[str, Any])

    # Crear función wrapper que acepta parámetros individuales
    # Usamos exec para crear una función dinámicamente con los parámetros del schema

    # Construir lista de nombres de parámetros
    param_names = list(schema_fields.keys())

    # Crear código de la función como string
    param_list = ", ".join([f"{name}=None" for name in param_names])
    params_dict = ", ".join([f"'{name}': {name}" for name in param_names])

    # Crear código de la función
    func_code = f'''def tool_wrapper({param_list}):
    """Wrapper para ejecutar la herramienta"""
    params = {{{params_dict}}}
    # Filtrar None values
    params = {{k: v for k, v in params.items() if v is not None}}
    try:
        return tool_instance.execute(**params)
    except TrackHSError as trackhs_error:
        raise ToolError(str(trackhs_error))
    except Exception as unexpected_error:
        logger.error(
            f"Error inesperado en herramienta {{tool_instance.name}}",
            extra={{
                "tool_name": tool_instance.name,
                "error_type": type(unexpected_error).__name__,
                "error_message": str(unexpected_error),
            }},
        )
        raise ToolError(f"Error interno: {{str(unexpected_error)}}")
'''

    # Ejecutar el código en un contexto local
    local_vars = {
        "tool_instance": tool_instance,
        "logger": logger,
        "TrackHSError": TrackHSError,
        "ToolError": ToolError,
        "Dict": Dict,
        "Any": Any,
    }

    exec(func_code, globals(), local_vars)

    tool_function = local_vars["tool_wrapper"]

    # Asignar la firma creada dinámicamente
    tool_function.__signature__ = sig
    tool_function.__annotations__ = {"return": Dict[str, Any], **type_hints}

    # Asignar nombre y docstring
    tool_function.__name__ = f"{tool_instance.name}_wrapper"
    tool_function.__doc__ = tool_instance.description

    # Registrar en FastMCP
    mcp_server.tool(name=tool_instance.name, description=tool_instance.description)(
        tool_function
    )
