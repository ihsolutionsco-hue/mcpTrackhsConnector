"""
Modelos Pydantic para validación de parámetros de amenidades.
Implementa validación robusta siguiendo mejores prácticas de FastMCP.
"""

from typing import Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator


class AmenitiesSearchParams(BaseModel):
    """
    Modelo Pydantic para validación de parámetros de búsqueda de amenidades.

    Proporciona validación robusta y automática de todos los parámetros
    de la función search_amenities, siguiendo las mejores prácticas de FastMCP.
    """

    # Parámetros de paginación
    page: int = Field(
        ge=1, le=10000, default=1, description="Número de página (1-based)"
    )
    size: int = Field(ge=1, le=100, default=10, description="Tamaño de página")

    # Parámetros de ordenamiento
    sortColumn: Optional[
        Literal[
            "id", "order", "isPublic", "publicSearchable", "isFilterable", "createdAt"
        ]
    ] = Field(default=None, description="Columna para ordenar resultados")
    sortDirection: Optional[Literal["asc", "desc"]] = Field(
        default=None, description="Dirección de ordenamiento"
    )

    # Parámetros de búsqueda
    search: Optional[str] = Field(
        max_length=200, default=None, description="Búsqueda en nombre de amenidad"
    )

    # Parámetros de filtrado
    groupId: Optional[int] = Field(
        gt=0, default=None, description="Filtrar por ID de grupo"
    )
    isPublic: Optional[int] = Field(
        ge=0,
        le=1,
        default=None,
        description="Filtrar por amenidades públicas (1) o privadas (0)",
    )
    publicSearchable: Optional[int] = Field(
        ge=0,
        le=1,
        default=None,
        description="Filtrar por amenidades buscables públicamente (1) o no (0)",
    )
    isFilterable: Optional[int] = Field(
        ge=0,
        le=1,
        default=None,
        description="Filtrar por amenidades filtrables (1) o no (0)",
    )

    # Parámetros de tipos de plataformas OTA
    homeawayType: Optional[str] = Field(
        max_length=200,
        default=None,
        description="Buscar por tipo de HomeAway (soporta % para wildcard)",
    )
    airbnbType: Optional[str] = Field(
        max_length=200,
        default=None,
        description="Buscar por tipo de Airbnb (soporta % para wildcard)",
    )
    tripadvisorType: Optional[str] = Field(
        max_length=200,
        default=None,
        description="Buscar por tipo de TripAdvisor (soporta % para wildcard)",
    )
    marriottType: Optional[str] = Field(
        max_length=200,
        default=None,
        description="Buscar por tipo de Marriott (soporta % para wildcard)",
    )

    @field_validator(
        "page",
        "size",
        "groupId",
        "isPublic",
        "publicSearchable",
        "isFilterable",
        mode="before",
    )
    @classmethod
    def validate_int_fields(cls, v):
        """
        Validar campos enteros - convertir strings a enteros.

        Args:
            v: Valor a validar

        Returns:
            Valor convertido a entero
        """
        if v is None:
            return v
        if isinstance(v, str):
            try:
                return int(v)
            except ValueError:
                raise ValueError(f"Valor '{v}' no puede ser convertido a entero")
        return v

    @field_validator(
        "search", "homeawayType", "airbnbType", "tripadvisorType", "marriottType"
    )
    @classmethod
    def validate_string_fields(cls, v):
        """
        Validar campos de texto - convertir strings vacíos a None.

        Args:
            v: Valor a validar

        Returns:
            Valor validado o None si está vacío
        """
        if v is not None and v.strip() == "":
            return None
        return v

    @field_validator("search")
    @classmethod
    def validate_search_term(cls, v):
        """
        Validar término de búsqueda.

        Args:
            v: Término de búsqueda

        Returns:
            Término validado

        Raises:
            ValueError: Si el término es muy corto
        """
        if v is not None:
            # Limpiar y normalizar término de búsqueda
            cleaned = v.strip()
            if len(cleaned) < 2:
                raise ValueError("Término de búsqueda debe tener al menos 2 caracteres")
            return cleaned
        return v

    def to_api_params(self) -> dict:
        """
        Convertir parámetros validados a formato de API.

        Returns:
            Diccionario de parámetros para la API de TrackHS
        """
        api_params = {"page": self.page, "size": self.size}

        # Parámetros opcionales - solo agregar si no son None
        optional_params = {
            "sortColumn": self.sortColumn,
            "sortDirection": self.sortDirection,
            "search": self.search,
            "groupId": self.groupId,
            "isPublic": self.isPublic,
            "publicSearchable": self.publicSearchable,
            "isFilterable": self.isFilterable,
            "homeawayType": self.homeawayType,
            "airbnbType": self.airbnbType,
            "tripadvisorType": self.tripadvisorType,
            "marriottType": self.marriottType,
        }

        for key, value in optional_params.items():
            if value is not None:
                api_params[key] = value

        return api_params


class AmenitiesErrorInfo(BaseModel):
    """Información estructurada de errores para logging."""

    error_type: str = Field(description="Tipo de error")
    error_message: str = Field(description="Mensaje de error")
    status_code: Optional[int] = Field(
        default=None, description="Código de estado HTTP"
    )
    context: Optional[str] = Field(default=None, description="Contexto adicional")
    parameters: Optional[dict] = Field(
        default=None, description="Parámetros que causaron el error"
    )

    def to_log_dict(self) -> dict:
        """Convertir a diccionario para logging estructurado."""
        return {
            "error_type": self.error_type,
            "error_message": self.error_message,
            "status_code": self.status_code,
            "context": self.context,
            "parameters": self.parameters,
        }
