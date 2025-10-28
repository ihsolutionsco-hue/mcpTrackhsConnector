"""
Modelos Pydantic para unidades de TrackHS.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class UnitSearchParams(BaseModel):
    """
    Parámetros de búsqueda de unidades con validación robusta.
    """

    page: int = Field(ge=1, le=400, description="Número de página (1-based)")
    size: int = Field(ge=1, le=25, description="Tamaño de página (1-25)")
    search: Optional[str] = Field(
        max_length=200, description="Búsqueda de texto (nombre, descripción, código)"
    )
    bedrooms: Optional[int] = Field(
        ge=0, le=20, description="Número exacto de dormitorios"
    )
    bathrooms: Optional[int] = Field(ge=0, le=20, description="Número exacto de baños")
    is_active: Optional[int] = Field(
        ge=0, le=1, description="Unidades activas (1) o inactivas (0)"
    )
    is_bookable: Optional[int] = Field(
        ge=0, le=1, description="Unidades reservables (1) o no (0)"
    )

    @field_validator("search", mode="before")
    @classmethod
    def clean_search(cls, v):
        """Limpiar término de búsqueda."""
        if v is None:
            return None
        if isinstance(v, str):
            return v.strip() if v.strip() else None
        return str(v).strip() if v else None

    @field_validator("bedrooms", "bathrooms", mode="before")
    @classmethod
    def convert_to_int(cls, v):
        """Convertir a entero si es posible."""
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return int(v)
            except ValueError:
                raise ValueError(f"Valor no válido para dormitorios/baños: {v}")
        return int(v) if v is not None else None

    @field_validator("is_active", "is_bookable", mode="before")
    @classmethod
    def convert_boolean_to_int(cls, v):
        """Convertir booleanos a enteros."""
        if v is None:
            return None
        if isinstance(v, bool):
            return 1 if v else 0
        if isinstance(v, str):
            return 1 if v.lower() in ["true", "1", "yes"] else 0
        if isinstance(v, int):
            return 1 if v else 0
        raise ValueError(f"Valor no válido para filtro booleano: {v}")

    @model_validator(mode="after")
    def validate_combined_params(self):
        """Validaciones adicionales de parámetros combinados."""
        # Si se especifica búsqueda de texto, no es necesario otros filtros
        if self.search and not any(
            [
                self.bedrooms,
                self.bathrooms,
                self.is_active,
                self.is_bookable,
            ]
        ):
            # Solo búsqueda de texto - OK
            pass

        # Validar que al menos un filtro esté presente
        if not any(
            [
                self.search,
                self.bedrooms,
                self.bathrooms,
                self.is_active,
                self.is_bookable,
            ]
        ):
            # Sin filtros - búsqueda general permitida
            pass

        return self

    def to_api_params(self) -> Dict[str, Any]:
        """Convertir a parámetros de API, excluyendo None."""
        params = {}
        for key, value in self.model_dump().items():
            if value is not None:
                params[key] = value
        return params


class UnitData(BaseModel):
    """
    Datos de una unidad individual con validación robusta.
    """

    id: int
    name: str
    code: str
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    max_occupancy: Optional[int] = None
    area: Optional[float] = None
    address: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    is_bookable: Optional[bool] = None
    amenities: Optional[List[Dict[str, Any]]] = None
    # Campos adicionales que pueden estar presentes
    floors: Optional[int] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    pet_friendly: Optional[bool] = None
    smoking_allowed: Optional[bool] = None
    children_allowed: Optional[bool] = None
    events_allowed: Optional[bool] = None
    is_accessible: Optional[bool] = None

    @field_validator("area", mode="before")
    @classmethod
    def normalize_area(cls, v):
        """Normalizar campo area a float."""
        if v is None:
            return None
        try:
            if isinstance(v, (int, float)):
                return float(v)
            elif isinstance(v, str):
                # Limpiar string de caracteres no numéricos
                cleaned_str = "".join(c for c in v.strip() if c.isdigit() or c in ".-")
                if cleaned_str:
                    return float(cleaned_str)
                else:
                    return None
            else:
                return None
        except (ValueError, TypeError, AttributeError):
            return None

    @field_validator("bedrooms", "bathrooms", "max_occupancy", "floors", mode="before")
    @classmethod
    def normalize_numeric(cls, v):
        """Normalizar campos numéricos a int."""
        if v is None:
            return None
        try:
            if isinstance(v, (int, float)):
                return int(v)
            elif isinstance(v, str):
                cleaned_str = "".join(c for c in v.strip() if c.isdigit())
                if cleaned_str:
                    return int(cleaned_str)
                else:
                    return None
            else:
                return None
        except (ValueError, TypeError, AttributeError):
            return None

    @field_validator(
        "is_active",
        "is_bookable",
        "pet_friendly",
        "smoking_allowed",
        "children_allowed",
        "events_allowed",
        "is_accessible",
        mode="before",
    )
    @classmethod
    def normalize_boolean(cls, v):
        """Normalizar campos booleanos."""
        if v is None:
            return None
        if isinstance(v, bool):
            return v
        elif isinstance(v, int):
            return bool(v)
        elif isinstance(v, str):
            return v.lower() in ["true", "1", "yes", "on", "enabled"]
        else:
            return None

    @field_validator("longitude", "latitude", mode="before")
    @classmethod
    def normalize_float(cls, v):
        """Normalizar campos float."""
        if v is None:
            return None
        try:
            if isinstance(v, (int, float)):
                return float(v)
            elif isinstance(v, str):
                cleaned_str = "".join(c for c in v.strip() if c.isdigit() or c in ".-")
                if cleaned_str:
                    return float(cleaned_str)
                else:
                    return None
            else:
                return None
        except (ValueError, TypeError, AttributeError):
            return None

    model_config = ConfigDict(extra="allow", validate_assignment=True)


class UnitSearchResponse(BaseModel):
    """
    Respuesta de búsqueda de unidades con validación robusta.
    """

    page: int
    page_count: int
    page_size: int
    total_items: int
    _embedded: Dict[str, List[UnitData]]
    _links: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(extra="allow", validate_assignment=True)
