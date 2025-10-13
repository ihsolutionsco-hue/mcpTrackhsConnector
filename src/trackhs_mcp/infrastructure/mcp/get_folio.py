"""
Herramienta MCP para obtener un folio específico por ID en TrackHS API
Basado en el endpoint GET /pms/folios/{folioId}
"""

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from ...application.ports.api_client_port import ApiClientPort

from ...application.use_cases.get_folio import GetFolioUseCase
from ...domain.entities.folios import GetFolioParams
from ...domain.exceptions.api_exceptions import ValidationError
from ..utils.error_handling import error_handler
from ..utils.user_friendly_messages import format_required_error, format_type_error


def register_get_folio(mcp, api_client: "ApiClientPort"):
    """Registra la herramienta get_folio"""

    @mcp.tool
    @error_handler("get_folio")
    async def get_folio(folio_id: str) -> Dict[str, Any]:
        """
        Obtiene un folio específico por ID desde TrackHS API.

        Esta herramienta MCP permite obtener todos los detalles de un folio
        individual, incluyendo información financiera completa, datos embebidos
        de contacto, compañía, agente de viajes y reglas de folio maestro.

        **Características Principales:**
        - ✅ Obtiene folio completo por ID (guest o master)
        - ✅ Incluye datos financieros (balances, comisiones, ingresos)
        - ✅ Información embebida de contacto, compañía, agente de viajes
        - ✅ Reglas de folio maestro si aplica
        - ✅ Manejo robusto de errores
        - ✅ Optimizado para integración con modelos de IA

        **Casos de Uso:**
        - Verificar balance actual y realizado de folios
        - Análisis financiero de folios individuales
        - Auditoría de transacciones y comisiones
        - Información de excepciones y estados
        - Validación de datos de contacto y compañía
        - Consulta de reglas de folio maestro

        **Ejemplos de Uso:**

        # Obtener folio por ID
        get_folio(folio_id="12345")

        # Verificar balance de folio
        get_folio(folio_id="67890")

        # Análisis financiero
        get_folio(folio_id="11111")

        **Parámetros:**
        - folio_id: ID único del folio (string que representa un entero positivo requerido)

        **Respuesta:**
        Objeto completo de folio con:
        - Datos básicos: ID, estado, tipo, fechas, balances
        - Información financiera: comisiones, ingresos, fechas de check-in/out
        - Datos embebidos: contact, travelAgent, company, masterFolioRule
        - Metadatos: fechas de creación/actualización, usuarios
        - Enlaces y objetos embebidos adicionales

        **Manejo de Errores:**
        - 401: Credenciales inválidas o expiradas
        - 403: Permisos insuficientes para acceder al folio
        - 404: Folio no encontrado con el ID especificado
        - 500: Error interno del servidor de TrackHS

        **Notas Importantes:**
        - El ID debe ser un string que represente un entero positivo válido
        - La respuesta incluye todos los datos embebidos disponibles
        - Los datos financieros están en formato numérico para cálculos
        - Las fechas están en formato ISO 8601
        - Los campos opcionales pueden estar ausentes según el tipo de folio

        **Common Errors:**
        - folio_id: Required parameter (folio_id="37152796")
        - ID format: Must be positive integer as string ("12345")
        - Authentication: Check TRACKHS_USERNAME and TRACKHS_PASSWORD
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
