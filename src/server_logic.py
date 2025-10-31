"""
Lógica del servidor MCP para TrackHS
Separación de responsabilidades siguiendo mejores prácticas
"""

import os
from typing import Any, Dict, List, Optional, Union

from dotenv import load_dotenv
from fastmcp import FastMCP

# Cargar variables de entorno desde .env
load_dotenv()
from fastmcp.exceptions import ToolError
from fastmcp.server.middleware.logging import LoggingMiddleware
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

        # Agregar logging middleware para requests/responses
        mcp_server.add_middleware(
            LoggingMiddleware(
                include_payloads=True,
                max_payload_length=1000,  # Limitar tamaño de payloads en logs
            )
        )

        # Agregar timing middleware para monitoreo de rendimiento
        mcp_server.add_middleware(TimingMiddleware())

        logger.info(
            "Servidor MCP configurado",
            extra={
                "middlewares": ["LoggingMiddleware", "TimingMiddleware"],
                "strict_input_validation": False,
            },
        )
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
    Registra una herramienta individual en el servidor MCP.

    Extrae parámetros del schema Pydantic y crea función simple.
    FastMCP infiere automáticamente desde type hints individuales.

    Args:
        mcp_server: Servidor MCP donde registrar la herramienta
        tool_instance: Instancia de la herramienta
    """
    from inspect import Parameter, Signature

    InputSchema = tool_instance.input_schema

    # Obtener campos según versión de Pydantic
    if hasattr(InputSchema, "model_fields"):
        fields = InputSchema.model_fields  # Pydantic v2
    elif hasattr(InputSchema, "__fields__"):
        fields = InputSchema.__fields__  # Pydantic v1
    else:
        fields = {}

    # Crear parámetros para la función
    # SOLUCIÓN 1: Usar Union explícito según el tipo esperado
    # Esto permite que FastMCP genere schema MCP que acepte strings Y tipos nativos
    # El schema Pydantic acepta strings, pero el schema MCP debe ser explícito
    parameters = []
    for field_name, field_info in fields.items():
        # Obtener anotación del campo Pydantic
        field_annotation = (
            field_info.annotation if hasattr(field_info, "annotation") else None
        )

        # Determinar tipo para schema MCP basándose en el campo
        # Estrategia: si es Optional[str] en Pydantic pero representa otro tipo lógico,
        # usar Union para permitir ambos tipos en el schema MCP

        field_type = None  # Inicializar como None

        # PRIMERO: Manejar enums y tipos específicos
        # Para enums (como sort_column, sort_direction, unit_status), aceptar string o el enum
        if field_annotation:
            annotation_str = str(field_annotation)
            # Detectar si es un enum
            if "Enum" in annotation_str or (
                hasattr(field_annotation, "__origin__")
                and field_annotation.__origin__ is not None
                and "Enum" in str(field_annotation.__origin__)
            ):
                # Para enums, aceptar string (valores del enum) o el tipo enum original
                field_type = Union[str, field_annotation, None]

        # SEGUNDO: Si no es enum, determinar tipo por nombre de campo
        if field_type is None:
            # Campos booleanos (pueden venir como string "true"/"1" o bool)
            if field_name in [
                "is_active",
                "is_bookable",
                "pets_friendly",
                "allow_unit_rates",
                "computed",
                "inherited",
                "limited",
                "include_descriptions",
            ]:
                field_type = Union[str, bool, None]  # Acepta string, bool o null

            # Campos de lista/array (pueden venir como string "[1,2,3]" o List[int])
            # Estos son campos que representan múltiples IDs (arrays)
            elif field_name in [
                "amenity_id",
                "node_id",
                "unit_type_id",
                "owner_id",
                "company_id",
                "channel_id",
                "lodging_type_id",
                "bed_type_id",
                "amenity_all",
                "unit_ids",
            ]:
                field_type = Union[str, List[int], None]  # Acepta string, lista o null

            # Campos numéricos (pueden venir como string "2" o int)
            elif field_name in [
                "bedrooms",
                "min_bedrooms",
                "max_bedrooms",
                "bathrooms",
                "min_bathrooms",
                "max_bathrooms",
                "occupancy",
                "min_occupancy",
                "max_occupancy",
                "page",
                "size",
                "calendar_id",  # ID único, no array
                "role_id",  # ID único, no array
            ]:
                field_type = Union[str, int, None]  # Acepta string, int o null

            # Campos string normales (fechas, texto, etc.)
            else:
                field_type = Optional[str]  # Solo acepta string o null

        # Obtener default - Pydantic v2 usa is_required()
        if hasattr(field_info, "is_required"):
            is_required = field_info.is_required()
        elif hasattr(field_info, "required"):
            is_required = field_info.required
        else:
            # Fallback: verificar si es Optional
            is_required = not (
                hasattr(field_type, "__args__") and type(None) in field_type.__args__
            )

        if is_required:
            default = Parameter.empty
        else:
            # Campo es opcional - obtener default si existe
            if hasattr(field_info, "default"):
                default_val = field_info.default
                # PydanticUndefined significa sin default, usar None
                if callable(default_val) or (
                    hasattr(default_val, "__class__")
                    and "Undefined" in str(default_val.__class__)
                ):
                    default = None
                else:
                    default = default_val  # Puede ser None u otro valor
            else:
                default = None  # Campo opcional sin default explícito

        parameters.append(
            Parameter(
                field_name,
                Parameter.KEYWORD_ONLY,
                default=default,
                annotation=field_type,
            )
        )

    # Crear función wrapper simple
    # FastMCP con strict_input_validation=False hará coerción automática
    # Pydantic con field_validator(mode='before') convertirá strings a tipos correctos
    sig = Signature(parameters, return_annotation=Dict[str, Any])

    def tool_wrapper(**kwargs) -> Dict[str, Any]:
        """Llama a la herramienta con parámetros validados"""
        logger = get_logger(__name__)

        try:
            # Log de entrada
            logger.debug(
                f"Ejecutando herramienta: {tool_instance.name}",
                extra={
                    "tool_name": tool_instance.name,
                    "params_received": {
                        k: str(v)[:100] for k, v in kwargs.items() if v is not None
                    },
                    "param_count": len([v for v in kwargs.values() if v is not None]),
                },
            )

            # Pasar parámetros directamente a Pydantic
            # FastMCP ya hizo coerción inicial, Pydantic validará y convertirá
            validated = InputSchema(**kwargs)

            # Ejecutar lógica de la herramienta
            result = tool_instance._execute_logic(validated)

            # Log de éxito
            logger.info(
                f"Herramienta ejecutada exitosamente: {tool_instance.name}",
                extra={
                    "tool_name": tool_instance.name,
                    "result_type": type(result).__name__,
                    "has_result": bool(result),
                },
            )

            return result

        except TrackHSError as e:
            logger.error(
                f"Error TrackHS en herramienta: {tool_instance.name}",
                extra={
                    "tool_name": tool_instance.name,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                },
            )
            raise ToolError(str(e))
        except Exception as e:
            logger.error(
                f"Error interno en herramienta: {tool_instance.name}",
                extra={
                    "tool_name": tool_instance.name,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "params_received": {
                        k: str(v)[:100] for k, v in kwargs.items() if v is not None
                    },
                },
                exc_info=True,  # Incluir traceback completo
            )
            raise ToolError(f"Error interno: {str(e)}")

    tool_wrapper.__signature__ = sig
    # SOLUCIÓN 1: Usar tipos Union en anotaciones para que FastMCP genere schema MCP correcto
    # Las anotaciones deben coincidir con los tipos usados en los parámetros
    tool_wrapper.__annotations__ = {
        param.name: param.annotation for param in parameters
    }
    tool_wrapper.__annotations__["return"] = Dict[str, Any]

    mcp_server.tool(name=tool_instance.name, description=tool_instance.description)(
        tool_wrapper
    )
