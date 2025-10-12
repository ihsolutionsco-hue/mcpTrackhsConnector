"""
Tests consolidados para filtros de fecha V1 y V2
"""

from src.trackhs_mcp.infrastructure.mcp.search_reservations_v1 import (
    _is_valid_date_format as v1_is_valid_date_format,
)
from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
    _is_valid_date_format as v2_is_valid_date_format,
)


class TestDateFilters:
    """Tests consolidados para filtros de fecha V1 y V2"""

    def test_v1_date_format_validation(self):
        """Test validación de formato de fecha V1"""
        # Formatos válidos
        assert v1_is_valid_date_format("2024-01-01")
        assert v1_is_valid_date_format("2024-01-01T00:00:00Z")
        assert v1_is_valid_date_format("2024-01-01T00:00:00")

        # Formatos inválidos
        assert not v1_is_valid_date_format("01/01/2024")
        assert not v1_is_valid_date_format("invalid-date")
        assert not v1_is_valid_date_format("")

    def test_v2_date_format_validation(self):
        """Test validación de formato de fecha V2"""
        # Formatos válidos
        assert v2_is_valid_date_format("2024-01-01")
        assert v2_is_valid_date_format("2024-01-01T00:00:00Z")
        assert v2_is_valid_date_format("2024-01-01T00:00:00")

        # Formatos inválidos
        assert not v2_is_valid_date_format("01/01/2024")
        assert not v2_is_valid_date_format("invalid-date")
        assert not v2_is_valid_date_format("")
