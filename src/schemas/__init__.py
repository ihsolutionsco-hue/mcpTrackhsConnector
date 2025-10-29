"""
Schemas para TrackHS MCP Server
Pydantic BaseModel para validación de inputs y outputs
"""

from .amenity import AmenityDetailResponse, AmenitySearchParams, AmenitySearchResponse
from .base import BaseSchema, ErrorResponse, SuccessResponse
from .folio import FolioResponse
from .reservation import (
    ReservationDetailResponse,
    ReservationSearchParams,
    ReservationSearchResponse,
)
from .unit import UnitDetailResponse, UnitSearchParams, UnitSearchResponse
from .work_order import (
    HousekeepingWorkOrderParams,
    MaintenanceWorkOrderParams,
    WorkOrderResponse,
)

__all__ = [
    # Base schemas
    "BaseSchema",
    "ErrorResponse",
    "SuccessResponse",
    # Reservation schemas
    "ReservationSearchParams",
    "ReservationDetailResponse",
    "ReservationSearchResponse",
    # Unit schemas
    "UnitSearchParams",
    "UnitDetailResponse",
    "UnitSearchResponse",
    # Amenity schemas
    "AmenitySearchParams",
    "AmenityDetailResponse",
    "AmenitySearchResponse",
    # Work order schemas
    "MaintenanceWorkOrderParams",
    "HousekeepingWorkOrderParams",
    "WorkOrderResponse",
    # Folio schemas
    "FolioResponse",
]
