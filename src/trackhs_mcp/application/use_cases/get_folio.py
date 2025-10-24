"""
Use Case para obtener un folio específico por ID desde TrackHS API
Implementa la lógica de negocio para el endpoint GET /pms/folios/{folioId}
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...application.ports.api_client_port import ApiClientPort

from ...domain.entities.folios import Folio, GetFolioParams
from ...domain.exceptions.api_exceptions import ValidationError
from ...infrastructure.utils.error_handling import error_handler


class GetFolioUseCase:
    """Use Case para obtener un folio específico por ID"""

    def __init__(self, api_client: "ApiClientPort"):
        self.api_client = api_client

    @error_handler("get_folio")
    async def execute(self, params: GetFolioParams) -> Folio:
        """
        Ejecuta la obtención de un folio específico por ID.

        Args:
            params: Parámetros que incluyen el folio_id

        Returns:
            Objeto Folio completo con datos embebidos

        Raises:
            ValidationError: Si el ID de folio es inválido
            ApiError: Si la API retorna error
            AuthenticationError: Si hay problemas de autenticación
        """
        # Validar parámetros de entrada
        if not params.folio_id:
            raise ValidationError(
                "folio_id es requerido",
                "folio_id",
            )

        # Convertir a entero si es string
        try:
            if isinstance(params.folio_id, str):
                folio_id_int = int(params.folio_id.strip())
            else:
                folio_id_int = int(params.folio_id)

            if folio_id_int <= 0:
                raise ValueError("ID debe ser positivo")
        except (ValueError, TypeError):
            raise ValidationError(
                "folio_id debe ser un número entero positivo válido",
                "folio_id",
            )

        try:
            # Construir endpoint
            endpoint = f"/api/pms/folios/{folio_id_int}"

            # Realizar petición GET a la API
            response_data = await self.api_client.get(endpoint)

            # Validar que la respuesta contiene datos
            if not response_data:
                raise ValidationError(
                    f"No se encontraron datos para el folio ID {folio_id_int}",
                    "folio_id",
                )

            # Manejar caso donde la respuesta llegue como string JSON
            if isinstance(response_data, str):
                import json

                try:
                    response_data = json.loads(response_data)
                except json.JSONDecodeError as e:
                    raise ValidationError(
                        f"Error al parsear respuesta JSON: {str(e)}",
                        "api",
                    )

            # Crear objeto Folio desde la respuesta
            folio = Folio.model_validate(response_data)

            return folio

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
                        "Prohibido: Permisos insuficientes para esta operación. "
                        "Por favor verifica que tu cuenta tenga acceso a "
                        "los endpoints de PMS/Folios.",
                        "permissions",
                    )
                elif e.status_code == 404:
                    raise ValidationError(
                        f"Folio no encontrado: No existe un folio con ID {folio_id_int}. "
                        "Por favor verifica que el ID sea correcto.",
                        "folio_id",
                    )
                elif e.status_code == 500:
                    raise ValidationError(
                        "Error interno del servidor: La API está temporalmente no disponible. "
                        "Por favor intenta nuevamente más tarde o contacta soporte.",
                        "api",
                    )

            # Re-lanzar otros errores
            raise ValidationError(f"Error en la petición a la API: {str(e)}", "api")
