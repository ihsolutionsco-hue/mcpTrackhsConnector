"""
Herramienta MCP para buscar reservas en Track HS API V2
Basado en la especificación completa de la API Search Reservations V2
"""

from typing import List, Literal, Optional, Union

from ...application.ports.api_client_port import ApiClientPort
from ...application.use_cases.search_reservations import SearchReservationsUseCase
from ...domain.entities.reservations import SearchReservationsParams
from ...domain.exceptions.api_exceptions import ValidationError
from ..utils.error_handling import error_handler


def register_search_reservations(mcp, api_client: ApiClientPort):
    """Registra la herramienta search_reservations"""

    @mcp.tool
    @error_handler("search_reservations")
    async def search_reservations(
        page: int = 1,
        size: int = 10,
        sort_column: Literal[
            "name",
            "status",
            "altCon",
            "agreementStatus",
            "type",
            "guest",
            "guests",
            "unit",
            "units",
            "checkin",
            "checkout",
            "nights",
        ] = "name",
        sort_direction: Literal["asc", "desc"] = "asc",
        search: Optional[str] = None,
        tags: Optional[str] = None,
        node_id: Optional[str] = None,
        unit_id: Optional[str] = None,
        reservation_type_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        travel_agent_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        user_id: Optional[str] = None,
        unit_type_id: Optional[str] = None,
        rate_type_id: Optional[str] = None,
        booked_start: Optional[str] = None,
        booked_end: Optional[str] = None,
        arrival_start: Optional[str] = None,
        arrival_end: Optional[str] = None,
        departure_start: Optional[str] = None,
        departure_end: Optional[str] = None,
        updated_since: Optional[str] = None,
        scroll: Optional[Union[int, str]] = None,
        in_house_today: Optional[Literal[0, 1]] = None,
        status: Optional[Union[str, List[str]]] = None,
        group_id: Optional[int] = None,
        checkin_office_id: Optional[int] = None,
    ):
        """
        Search reservations in Track HS API V2 with comprehensive filtering options.

        This MCP tool provides advanced reservation search capabilities with full API V2
        compatibility, including pagination, filtering, sorting, and scroll support for
        large datasets.

        **Key Features:**
        - ✅ Full API V2 compatibility with all 25+ parameters
        - ✅ Advanced pagination (standard + Elasticsearch scroll)
        - ✅ Comprehensive filtering (dates, IDs, status, etc.)
        - ✅ Flexible sorting options
        - ✅ Robust error handling
        - ✅ MCP-optimized for AI model integration

        **Examples:**

        # Basic search
        search_reservations(page=1, size=10)

        # Date range search (múltiples formatos soportados)
        search_reservations(
            arrival_start="2024-01-01",  # Solo fecha
            arrival_end="2024-01-31T23:59:59Z",  # Fecha con tiempo
            status=["Confirmed", "Checked In"]
        )

        # Date range search (formato ISO completo)
        search_reservations(
            arrival_start="2024-01-01T00:00:00Z",
            arrival_end="2024-01-31T23:59:59Z",
            status=["Confirmed", "Checked In"]
        )

        # Large dataset with scroll
        search_reservations(scroll=1, size=1000)

        # Multi-ID filtering
        search_reservations(
            node_id="1,2,3",
            unit_id="10,20,30",
            status=["Confirmed"]
        )

        # Status filtering
        search_reservations(
            status=["Hold", "Confirmed"],
            in_house_today=1
        )

        **Parameters:**
        - page: Page number (0-based, max 10k total results)
        - size: Page size (max 10k total results)
        - sort_column: Sort by field (name, status, checkin, etc.)
        - sort_direction: Sort direction (asc/desc)
        - search: Text search in names/descriptions
        - tags: Tag ID search
        - node_id: Node ID(s) - single int, comma-separated, or array
        - unit_id: Unit ID(s) - single int, comma-separated, or array
        - contact_id: Contact ID(s) - single int, comma-separated, or array
        - travel_agent_id: Travel agent ID(s)
        - campaign_id: Campaign ID(s)
        - user_id: User ID(s)
        - unit_type_id: Unit type ID(s)
        - rate_type_id: Rate type ID(s)
        - reservation_type_id: Reservation type ID(s)
        - booked_start/end: Booking date range (ISO 8601).
          Examples: "2025-01-01", "2025-01-01T00:00:00Z"
        - arrival_start/end: Arrival date range (ISO 8601).
          Examples: "2025-01-01", "2025-01-01T00:00:00Z"
        - departure_start/end: Departure date range (ISO 8601).
          Examples: "2025-01-01", "2025-01-01T00:00:00Z"
        - updated_since: Updated since date (ISO 8601).
          Examples: "2025-01-01", "2025-01-01T00:00:00Z"
        - scroll: Elasticsearch scroll (1 to start, string to continue)
        - in_house_today: Filter by in-house today (0/1)
        - status: Reservation status(es) - single string or list
        - group_id: Group ID
        - checkin_office_id: Check-in office ID

        **Returns:**
        Complete reservation data with embedded objects (unit, contact, policies, etc.)
        and pagination information.

        **Error Handling:**
        - Validates all parameters according to API V2 specification
        - Handles API errors (401, 403, 500) with descriptive messages
        - Validates ISO 8601 date formats strictly
        - Enforces 10k total results limit
        - Disables sorting when using scroll
        """
        # Validar parámetros básicos según documentación API V2
        if page < 0:
            raise ValidationError("Page must be >= 0", "page")
        if size < 1:
            raise ValidationError("Size must be >= 1", "size")
        if size > 1000:
            raise ValidationError("Size must be <= 1000", "size")

        # Validar límite total de resultados (10k máximo)
        if page * size > 10000:
            raise ValidationError(
                "Total results (page * size) must be <= 10,000", "page"
            )

        # Validar parámetro scroll según documentación API V2
        if scroll is not None:
            if isinstance(scroll, int) and scroll != 1:
                raise ValidationError("Scroll must start with 1", "scroll")
            if isinstance(scroll, str) and not scroll.strip():
                raise ValidationError("Scroll string cannot be empty", "scroll")

            # Cuando se usa scroll, el sorting se deshabilita
            if sort_column != "name" or sort_direction != "asc":
                raise ValidationError(
                    "When using scroll, \
     sorting is disabled. Use default sort_column='name' and sort_direction='asc'",
                    "scroll",
                )

        # Validar fechas si se proporcionan
        date_params = {
            "booked_start": booked_start,
            "booked_end": booked_end,
            "arrival_start": arrival_start,
            "arrival_end": arrival_end,
            "departure_start": departure_start,
            "departure_end": departure_end,
            "updated_since": updated_since,
        }

        for param_name, param_value in date_params.items():
            if param_value and not _is_valid_date_format(param_value):
                raise ValidationError(
                    f"Invalid date format for {param_name}. Use ISO 8601 format.",
                    param_name,
                )

        query_params = {
            "page": page,
            "size": size,
            "sortColumn": sort_column,
            "sortDirection": sort_direction,
        }

        # Agregar parámetros opcionales con validación correcta
        if search:
            query_params["search"] = search
        if tags:
            query_params["tags"] = tags
        if node_id is not None:
            query_params["nodeId"] = _parse_id_string(node_id)
        if unit_id:
            query_params["unitId"] = _parse_id_string(unit_id)
        if reservation_type_id:
            query_params["reservationTypeId"] = _parse_id_string(reservation_type_id)
        if contact_id:
            query_params["contactId"] = _parse_id_string(contact_id)
        if travel_agent_id:
            query_params["travelAgentId"] = _parse_id_string(travel_agent_id)
        if campaign_id:
            query_params["campaignId"] = _parse_id_string(campaign_id)
        if user_id:
            query_params["userId"] = _parse_id_string(user_id)
        if unit_type_id:
            query_params["unitTypeId"] = _parse_id_string(unit_type_id)
        if rate_type_id:
            query_params["rateTypeId"] = _parse_id_string(rate_type_id)
        if booked_start:
            query_params["bookedStart"] = _normalize_date_format(booked_start)
        if booked_end:
            query_params["bookedEnd"] = _normalize_date_format(booked_end)
        if arrival_start:
            query_params["arrivalStart"] = _normalize_date_format(arrival_start)
        if arrival_end:
            query_params["arrivalEnd"] = _normalize_date_format(arrival_end)
        if departure_start:
            query_params["departureStart"] = _normalize_date_format(departure_start)
        if departure_end:
            query_params["departureEnd"] = _normalize_date_format(departure_end)
        if updated_since:
            query_params["updatedSince"] = _normalize_date_format(updated_since)
        if scroll:
            query_params["scroll"] = scroll
        if in_house_today is not None:
            # Validar que in_house_today sea 0 o 1
            if in_house_today not in [0, 1]:
                raise ValidationError("in_house_today must be 0 or 1", "in_house_today")
            # Asegurar que in_house_today sea un entero
            query_params["inHouseToday"] = int(in_house_today)
        if status:
            formatted_status = _format_status_param(status)
            if isinstance(formatted_status, list):
                # Para múltiples estados, httpx maneja automáticamente arrays
                # convirtiéndolos a múltiples parámetros con el mismo nombre
                query_params["status"] = formatted_status
            else:
                query_params["status"] = formatted_status
        if group_id:
            query_params["groupId"] = group_id
        if checkin_office_id:
            query_params["checkinOfficeId"] = checkin_office_id

        endpoint = "/v2/pms/reservations"

        # Logging detallado para debugging de filtros de fecha
        import logging

        logger = logging.getLogger(__name__)
        logger.info(f"Search reservations query params: {query_params}")

        # Logging específico para parámetros de fecha
        date_params = {
            k: v
            for k, v in query_params.items()
            if "Start" in k or "End" in k or "Since" in k
        }
        if date_params:
            logger.info(f"Date filter parameters: {date_params}")
        else:
            logger.warning("No date filter parameters found in query")

        try:
            # Crear caso de uso
            use_case = SearchReservationsUseCase(api_client)

            # Crear parámetros de búsqueda
            search_params = SearchReservationsParams(
                page=page,
                size=size,
                sort_column=sort_column,
                sort_direction=sort_direction,
                search=search,
                tags=tags,
                node_id=_parse_id_string(node_id) if node_id else None,
                unit_id=_parse_id_string(unit_id) if unit_id else None,
                reservation_type_id=(
                    _parse_id_string(reservation_type_id)
                    if reservation_type_id
                    else None
                ),
                contact_id=_parse_id_string(contact_id) if contact_id else None,
                travel_agent_id=(
                    _parse_id_string(travel_agent_id) if travel_agent_id else None
                ),
                campaign_id=_parse_id_string(campaign_id) if campaign_id else None,
                user_id=_parse_id_string(user_id) if user_id else None,
                unit_type_id=_parse_id_string(unit_type_id) if unit_type_id else None,
                rate_type_id=_parse_id_string(rate_type_id) if rate_type_id else None,
                booked_start=booked_start,
                booked_end=booked_end,
                arrival_start=arrival_start,
                arrival_end=arrival_end,
                departure_start=departure_start,
                departure_end=departure_end,
                updated_since=updated_since,
                scroll=scroll,
                in_house_today=in_house_today,
                status=_format_status_param(status) if status else None,
                group_id=group_id,
                checkin_office_id=checkin_office_id,
            )

            # Ejecutar caso de uso
            result = await use_case.execute(search_params)
            return result
        except Exception as e:
            # Logging detallado para debugging
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"API request failed for endpoint {endpoint}: {str(e)}")
            logger.error(f"Query params: {query_params}")

            # Manejar errores específicos de la API según documentación
            if hasattr(e, "status_code"):
                if e.status_code == 401:
                    raise ValidationError(
                        "Unauthorized: Invalid authentication credentials. "
                        "Please verify your TRACKHS_USERNAME and TRACKHS_PASSWORD "
                        "are correct and not expired.",
                        "auth",
                    )
                elif e.status_code == 403:
                    raise ValidationError(
                        "Forbidden: Insufficient permissions for this operation. "
                        "Please verify your account has access to "
                        "PMS/Reservations endpoints.",
                        "permissions",
                    )
                elif e.status_code == 404:
                    raise ValidationError(
                        f"Endpoint not found: {endpoint}. "
                        "Please verify the API URL and endpoint path are correct.",
                        "endpoint",
                    )
                elif e.status_code == 500:
                    raise ValidationError(
                        "Internal Server Error: API temporarily unavailable. "
                        "Please try again later or contact support.",
                        "api",
                    )
            raise ValidationError(f"API request failed: {str(e)}", "api")


def _is_valid_date_format(date_string: str) -> bool:
    """Valida formato de fecha con múltiples formatos soportados"""
    try:
        import re
        from datetime import datetime

        # Patrones de fecha soportados
        patterns = [
            # ISO 8601 completo con timezone
            r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$",
            # ISO 8601 sin timezone
            r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?$",
            # Solo fecha ISO
            r"^\d{4}-\d{2}-\d{2}$",
            # Formato con espacio (alternativo)
            r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$",
        ]

        # Verificar si coincide con algún patrón
        for pattern in patterns:
            if re.match(pattern, date_string):
                # Intentar parsear la fecha
                try:
                    if "T" in date_string:
                        # Formato ISO con tiempo
                        if date_string.endswith("Z"):
                            datetime.fromisoformat(date_string.replace("Z", "+00:00"))
                        elif "+" in date_string or "-" in date_string[-6:]:
                            datetime.fromisoformat(date_string)
                        else:
                            datetime.fromisoformat(date_string)
                    else:
                        # Solo fecha
                        datetime.fromisoformat(date_string)
                    return True
                except ValueError:
                    continue

        return False
    except (ValueError, AttributeError):
        return False


def _normalize_date_format(date_string: str) -> str:
    """Normaliza formato de fecha para la API de TrackHS - CORREGIDO FINAL"""
    try:
        # Si es solo fecha, agregar tiempo con timezone UTC
        if len(date_string) == 10 and date_string.count("-") == 2:
            # Solo fecha: 2025-01-01 -> 2025-01-01T00:00:00Z
            return f"{date_string}T00:00:00Z"

        # Si tiene tiempo con timezone, remover timezone
        if "T" in date_string:
            if date_string.endswith("Z") or date_string.endswith("z"):
                # Ya tiene Z: 2025-01-01T00:00:00Z -> mantener
                return date_string
            elif "+" in date_string:
                # Si es +00:00, mantenerlo (ya está normalizado)
                if date_string.endswith("+00:00"):
                    return date_string
                # Remover otros offsets positivos: 2025-01-01T00:00:00+05:00 ->
                # 2025-01-01T00:00:00
                return date_string.split("+")[0]
            elif "-" in date_string and len(date_string) > 19:
                # Verificar si es realmente un offset negativo
                # Los offsets negativos tienen formato: -HH:MM al final
                # Buscar el último - que esté después de la T
                t_pos = date_string.find("T")
                if t_pos > 0:
                    # Buscar el último - después de la T
                    last_dash = date_string.rfind("-")
                    # Verificar si es un offset negativo real (formato -HH:MM)
                    if last_dash > t_pos and last_dash >= len(date_string) - 6:
                        # Verificar si después del - hay exactamente 5 caracteres
                        remaining = date_string[last_dash + 1 :]
                        if len(remaining) == 5 and ":" in remaining:
                            # Es un offset negativo real, removerlo
                            return date_string[:last_dash]
                        else:
                            # No es un offset, es parte de la fecha - agregar Z
                            return date_string + "Z"
                    else:
                        # No es un offset, es parte de la fecha - agregar Z
                        return date_string + "Z"
                else:
                    # No hay T, agregar Z
                    return date_string + "Z"
            else:
                # Tiempo sin timezone: 2025-01-01T00:00:00 -> 2025-01-01T00:00:00Z
                # También manejar microsegundos:
                # 2025-01-01T00:00:00.123 -> 2025-01-01T00:00:00.123Z
                return date_string + "Z"

        # Si tiene tiempo con espacio, convertir a formato T
        if " " in date_string and len(date_string) > 10:
            # Convertir espacio a T: 2025-01-01 00:00:00 -> 2025-01-01T00:00:00Z
            return date_string.replace(" ", "T") + "Z"

        # Si ya tiene formato correcto, devolverlo
        return date_string

    except Exception:
        # Si hay error, devolver el string original
        return date_string


def _normalize_date_format_flexible(date_string: str) -> str:
    """Normaliza fecha con múltiples formatos para máxima compatibilidad"""
    try:
        # Si es solo fecha, probar múltiples formatos
        if len(date_string) == 10 and date_string.count("-") == 2:
            # Formato 1: Con Z (UTC)
            format1 = f"{date_string}T00:00:00Z"
            # Formato 2: Con offset UTC (no usado)
            # format2 = f"{date_string}T00:00:00+00:00"
            # Formato 3: Sin timezone (no usado)
            # format3 = f"{date_string}T00:00:00"

            # Por defecto usar formato 1 (con Z)
            return format1

        # Si tiene tiempo pero no timezone, probar múltiples formatos
        if "T" in date_string and not (
            date_string.endswith("Z") or "+" in date_string or "-" in date_string[-6:]
        ):
            # Formato 1: Con Z
            format1 = f"{date_string}Z"
            # Formato 2: Con offset UTC (no usado)
            # format2 = f"{date_string}+00:00"
            # Formato 3: Sin timezone (original) (no usado)
            # format3 = date_string

            # Por defecto usar formato 1 (con Z)
            return format1

        # Si ya tiene formato correcto, devolverlo
        return date_string

    except Exception:
        # Si hay error, devolver el string original
        return date_string


def _parse_id_string(id_string: Union[str, int, List[int]]) -> Union[int, List[int]]:
    """
    Parsea un string de ID que puede ser:
    - Un entero simple: "48" o 48
    - Múltiples IDs separados por comas: "48,49,50"
    - Array en formato string: "[48,49,50]"
    - Lista de Python: [1, 2, 3]
    """
    # Si ya es un entero, devolverlo directamente
    if isinstance(id_string, int):
        return id_string

    # Si ya es una lista, devolverla directamente
    if isinstance(id_string, list):
        return id_string

    if not id_string or not str(id_string).strip():
        raise ValidationError("ID string cannot be empty", "id")

    # Limpiar espacios
    id_string = id_string.strip()

    # Si es un array en formato string, parsearlo
    if id_string.startswith("[") and id_string.endswith("]"):
        try:
            # Remover corchetes y dividir por comas
            content = id_string[1:-1].strip()
            if not content:
                raise ValidationError("Empty array not allowed", "id")
            # Dividir por comas y convertir a enteros
            ids = [int(x.strip()) for x in content.split(",")]
            return ids if len(ids) > 1 else ids[0]
        except ValueError:
            raise ValidationError(f"Invalid array format: {id_string}", "id")

    # Si contiene comas, es una lista de IDs
    if "," in id_string:
        try:
            ids = [int(x.strip()) for x in id_string.split(",") if x.strip()]
            if not ids:
                raise ValidationError("No valid IDs found", "id")
            return ids if len(ids) > 1 else ids[0]
        except ValueError:
            raise ValidationError(f"Invalid ID format: {id_string}", "id")

    # Es un ID único
    try:
        return int(id_string)
    except ValueError:
        raise ValidationError(f"Invalid ID format: {id_string}", "id")


def _format_id_param(param_value: Union[int, List[int]]) -> Union[int, List[int]]:
    """
    Formatea parámetros de ID para la API.
    Asegura que los enteros se mantengan como enteros y los arrays como arrays.
    """
    if isinstance(param_value, list):
        # Asegurar que todos los elementos sean enteros
        return [int(x) for x in param_value]
    else:
        # Asegurar que sea entero
        return int(param_value)


def _format_status_param(status_value: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    Formatea parámetros de status para la API.
    Valida que los valores sean válidos según la especificación.
    Maneja tanto strings individuales como listas de strings.
    """
    valid_statuses = {"Hold", "Confirmed", "Checked Out", "Checked In", "Cancelled"}

    if isinstance(status_value, list):
        # Validar cada status en la lista
        for status in status_value:
            if status not in valid_statuses:
                valid_statuses_str = ", ".join(valid_statuses)
                raise ValidationError(
                    f"Invalid status: {status}. Must be one of: {valid_statuses_str}",
                    "status",
                )
        return status_value
    else:
        # Si es un string, verificar si es un array JSON
        if status_value.startswith("[") and status_value.endswith("]"):
            try:
                import json

                # Parsear como JSON array
                statuses = json.loads(status_value)
                if not isinstance(statuses, list):
                    raise ValidationError(
                        f"Invalid status format: {status_value}", "status"
                    )
                # Validar cada status
                for status in statuses:
                    if status not in valid_statuses:
                        raise ValidationError(
                            f"Invalid status: {status}. Must be one of: "
                            f"{', '.join(valid_statuses)}",
                            "status",
                        )
                return statuses if len(statuses) > 1 else statuses[0]
            except (json.JSONDecodeError, ValueError):
                raise ValidationError(
                    f"Invalid status format: {status_value}", "status"
                )
        # Si es un string, verificar si contiene comas (múltiples status)
        elif "," in status_value:
            # Dividir por comas y limpiar comillas
            statuses = [
                s.strip().strip('"').strip("'")
                for s in status_value.split(",")
                if s.strip()
            ]
            for status in statuses:
                if status not in valid_statuses:
                    raise ValidationError(
                        f"Invalid status: {status}. Must be one of: "
                        f"{', '.join(valid_statuses)}",
                        "status",
                    )
            return statuses if len(statuses) > 1 else statuses[0]
        else:
            # Validar status único
            if status_value not in valid_statuses:
                raise ValidationError(
                    f"Invalid status: {status_value}. Must be one of: "
                    f"{', '.join(valid_statuses)}",
                    "status",
                )
            return status_value
