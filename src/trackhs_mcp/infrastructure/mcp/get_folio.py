"""
Herramienta MCP para obtener un folio específico por ID en TrackHS API
Versión mejorada con tipos específicos siguiendo mejores prácticas MCP
"""

from typing import TYPE_CHECKING, Any, Dict

from pydantic import Field

if TYPE_CHECKING:
    from ...application.ports.api_client_port import ApiClientPort

from ...application.use_cases.get_folio import GetFolioUseCase
from ...domain.entities.folios import GetFolioParams
from ...domain.exceptions.api_exceptions import ValidationError
from ..utils.error_handling import error_handler
from ..utils.user_friendly_messages import format_required_error, format_type_error


def register_get_folio(mcp, api_client: "ApiClientPort"):
    """Registra la herramienta get_folio mejorada"""

    @mcp.tool(name="get_folio")
    @error_handler("get_folio")
    async def get_folio(
        folio_id: str = Field(
            description=(
                "Unique folio ID (positive integer as string). "
                "Example: '12345' or '37152796'"
            ),
            pattern=r"^\d+$",
            min_length=1,
            max_length=20,
        )
    ) -> Dict[str, Any]:
        """
        Get complete folio details by ID from TrackHS API.

        Retrieves all information for a specific folio including financial data,
        embedded objects (contact, company, travel agent), master folio rules, and metadata.

        Returns:
            Complete folio object with balances, commissions, revenue, embedded contact
            and company data, and master folio rules if applicable.

        Raises:
            ValidationError: If folio_id is invalid or folio not found
            APIError: If API request fails (401, 403, 404, 500)
        """
        # Validar parámetros de entrada
        if not folio_id or not folio_id.strip():
            raise ValidationError(
                format_required_error("folio_id"),
                "folio_id",
            )

        # Validar que sea un número entero positivo válido
        try:
            folio_id_int = int(folio_id.strip())
            if folio_id_int <= 0:
                raise ValueError("ID debe ser positivo")
        except (ValueError, TypeError):
            raise ValidationError(
                format_type_error("folio_id", "número entero positivo", folio_id),
                "folio_id",
            )

        try:
            # Crear caso de uso
            use_case = GetFolioUseCase(api_client)

            # Crear parámetros con el ID convertido a entero
            params = GetFolioParams(folio_id=folio_id_int)

            # Ejecutar caso de uso
            folio = await use_case.execute(params)

            # Convertir a diccionario para respuesta MCP
            return folio.model_dump(by_alias=True, exclude_none=True)

        except Exception as e:
            # Manejar errores específicos de la API
            if hasattr(e, "status_code"):
                if e.status_code == 401:
                    raise ValidationError(
                        "No autorizado: Credenciales de autenticación inválidas. "
                        "Por favor verifica que TRACKHS_USERNAME y TRACKHS_PASSWORD "
                        "sean correctos y no hayan expirado.",
                        "auth",
                    )
                elif e.status_code == 403:
                    raise ValidationError(
                        "Prohibido: Permisos insuficientes para acceder a este folio. "
                        "Por favor verifica que tu cuenta tenga acceso a "
                        "los endpoints de PMS/Folios.",
                        "permissions",
                    )
                elif e.status_code == 404:
                    raise ValidationError(
                        f"Folio no encontrado: No existe un folio con ID {folio_id}. "
                        "Por favor verifica que el ID sea correcto y que el folio exista.",
                        "folio_id",
                    )
                elif e.status_code == 500:
                    raise ValidationError(
                        "Error interno del servidor: La API de TrackHS está temporalmente no disponible. "
                        "Por favor intenta nuevamente más tarde o contacta soporte técnico.",
                        "api",
                    )

            # Re-lanzar otros errores con contexto
            raise ValidationError(f"Error al obtener el folio: {str(e)}", "api")
