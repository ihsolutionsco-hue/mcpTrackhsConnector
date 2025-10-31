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
    parameters = []
    for field_name, field_info in fields.items():
        # Obtener tipo y default
        if hasattr(field_info, "annotation"):
            field_type = field_info.annotation
        elif hasattr(field_info, "type_"):
            field_type = field_info.type_
        else:
            field_type = Any

        # Si es Optional, extraer tipo interno
        if hasattr(field_type, "__args__") and len(field_type.__args__) > 0:
            non_none = [arg for arg in field_type.__args__ if arg is not type(None)]
            if non_none:
                field_type = non_none[0]

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

    # Funciones helper para coerción de tipos (simple y directo)
    def _coerce_bool(value: Any) -> Optional[bool]:
        """Convierte string/int a bool según MCP"""
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return bool(int(value))
        if isinstance(value, str):
            v = value.strip().lower()
            if v in {"true", "1", "yes", "y", "si", "sí"}:
                return True
            if v in {"false", "0", "no", "n"}:
                return False
        return None

    def _coerce_int(value: Any) -> Optional[int]:
        """Convierte string/float a int según MCP"""
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
        if isinstance(value, str) and value.strip():
            try:
                return int(value.strip())
            except ValueError:
                return None
        return None

    def _coerce_list(value: Any, item_type: type) -> Optional[list]:
        """Convierte string a lista según MCP"""
        import json

        if isinstance(value, list):
            return value
        if isinstance(value, str):
            v = value.strip()
            # JSON array: "[1,2,3]"
            if v.startswith("[") and v.endswith("]"):
                try:
                    parsed = json.loads(v)
                    if isinstance(parsed, list):
                        return parsed
                except json.JSONDecodeError:
                    pass
            # Separado por comas: "1,2,3"
            if "," in v:
                items = [item.strip() for item in v.split(",")]
                if item_type is int:
                    coerced = []
                    for item in items:
                        coerced_item = _coerce_int(item)
                        if coerced_item is not None:
                            coerced.append(coerced_item)
                    return coerced if coerced else None
        return None

    def _get_expected_type(field_name: str) -> type:
        """Obtiene el tipo esperado de un campo del schema"""
        from typing import get_args, get_origin

        if field_name not in fields:
            return Any

        field_info = fields[field_name]
        field_type = (
            field_info.annotation
            if hasattr(field_info, "annotation")
            else getattr(field_info, "type_", Any)
        )

        # Extraer tipo base si es Optional[Type] o Union[Type, None]
        origin = get_origin(field_type)
        if origin is not None:
            # Si es List[int], retornar list como marcador
            if origin is list:
                return list
            args = get_args(field_type)
            non_none_args = [arg for arg in args if arg is not type(None)]
            if non_none_args:
                field_type = non_none_args[0]

        return field_type

    # Crear función wrapper simple
    sig = Signature(parameters, return_annotation=Dict[str, Any])

    def tool_wrapper(**kwargs) -> Dict[str, Any]:
        """Llama a la herramienta con parámetros validados"""
        try:
            import re
            from typing import get_args, get_origin

            coerced_kwargs = {}
            for k, v in kwargs.items():
                if v is None:
                    continue

                # Obtener tipo esperado del schema
                expected_type = _get_expected_type(k)

                # Coerción de fechas (ya existente)
                if k in ("arrival", "departure") and isinstance(v, str):
                    v_stripped = v.strip()
                    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", v_stripped):
                        coerced_kwargs[k] = v_stripped
                    elif re.fullmatch(r"\d{4}", v_stripped):
                        continue
                    else:
                        coerced_kwargs[k] = v
                # Coerción de tipos según MCP/FastMCP
                elif isinstance(v, str):
                    # Verificar si es lista primero (usando el tipo original del schema)
                    field_info = fields.get(k)
                    is_list_field = False
                    item_type = int

                    if field_info:
                        field_type_orig = (
                            field_info.annotation
                            if hasattr(field_info, "annotation")
                            else getattr(field_info, "type_", Any)
                        )
                        origin = get_origin(field_type_orig)
                        # Manejar Optional[List[int]] que es Union[List[int], None]
                        if origin is list:
                            is_list_field = True
                            args = get_args(field_type_orig)
                            item_type = args[0] if args else int
                        elif origin is not None:
                            # Puede ser Union[List[int], None]
                            args = get_args(field_type_orig)
                            for arg in args:
                                arg_origin = get_origin(arg)
                                if arg_origin is list:
                                    is_list_field = True
                                    item_args = get_args(arg)
                                    item_type = item_args[0] if item_args else int
                                    break

                    if is_list_field:
                        # Es List[int], convertir string a lista
                        coerced = _coerce_list(v, item_type)
                        if coerced is not None:
                            coerced_kwargs[k] = coerced
                        # Si no se pudo convertir, omitir (será None)
                        continue
                    elif expected_type is bool:
                        coerced = _coerce_bool(v)
                        if coerced is not None:
                            coerced_kwargs[k] = coerced
                        continue
                    elif expected_type is int:
                        coerced = _coerce_int(v)
                        if coerced is not None:
                            coerced_kwargs[k] = coerced
                        continue

                    # Si no es lista/bool/int o no se pudo convertir, pasar como string
                    coerced_kwargs[k] = v
                else:
                    # Valor ya es del tipo correcto
                    coerced_kwargs[k] = v

            validated = InputSchema(**coerced_kwargs)
            return tool_instance._execute_logic(validated)
        except TrackHSError as e:
            raise ToolError(str(e))
        except Exception as e:
            logger = get_logger(__name__)
            logger.error(f"Error en {tool_instance.name}", extra={"error": str(e)})
            raise ToolError(f"Error interno: {str(e)}")

    tool_wrapper.__signature__ = sig
    tool_wrapper.__annotations__ = {
        param.name: param.annotation for param in parameters
    }
    tool_wrapper.__annotations__["return"] = Dict[str, Any]

    mcp_server.tool(name=tool_instance.name, description=tool_instance.description)(
        tool_wrapper
    )
