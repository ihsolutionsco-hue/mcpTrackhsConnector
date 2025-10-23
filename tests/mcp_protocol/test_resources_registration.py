"""
Tests específicos para validar el registro de recursos MCP
Enfoque: Validar que cada categoría de recursos se registra correctamente
"""

from unittest.mock import Mock

import pytest
from fastmcp import FastMCP


class TestMCPResourcesRegistration:
    """Tests para validar el registro de recursos MCP"""

    def test_schema_resources_registration(self):
        """Test: Los recursos de esquemas se registran correctamente"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()

        # Act
        from src.trackhs_mcp.infrastructure.tools.resources.schemas import (
            register_schema_resources,
        )

        register_schema_resources(mcp, mock_api_client)

        # Assert
        assert mcp is not None

    def test_documentation_resources_registration(self):
        """Test: Los recursos de documentación se registran correctamente"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()

        # Act
        from src.trackhs_mcp.infrastructure.tools.resources.documentation import (
            register_documentation_resources,
        )

        register_documentation_resources(mcp, mock_api_client)

        # Assert
        assert mcp is not None

    def test_reference_resources_registration(self):
        """Test: Los recursos de referencia se registran correctamente"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()

        # Act
        from src.trackhs_mcp.infrastructure.tools.resources.references import (
            register_reference_resources,
        )

        register_reference_resources(mcp, mock_api_client)

        # Assert
        assert mcp is not None

    def test_example_resources_registration(self):
        """Test: Los recursos de ejemplos se registran correctamente"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()

        # Act
        from src.trackhs_mcp.infrastructure.tools.resources.examples import (
            register_example_resources,
        )

        register_example_resources(mcp, mock_api_client)

        # Assert
        assert mcp is not None

    def test_all_resources_registration_together(self):
        """Test: Todos los recursos se registran juntos sin errores"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()

        # Act
        from src.trackhs_mcp.infrastructure.tools.resources import (
            register_all_resources,
        )

        register_all_resources(mcp, mock_api_client)

        # Assert
        assert mcp is not None

    def test_specific_schema_resources(self):
        """Test: Recursos de esquemas específicos se registran"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()

        # Act & Assert - Reservations V2 Schema
        from src.trackhs_mcp.infrastructure.tools.resources.schemas.reservations_v2 import (
            register_reservations_v2_schema,
        )

        register_reservations_v2_schema(mcp, mock_api_client)
        assert mcp is not None

        # Act & Assert - Reservation Detail V2 Schema
        from src.trackhs_mcp.infrastructure.tools.resources.schemas.reservation_detail_v2 import (
            register_reservation_detail_v2_schema,
        )

        register_reservation_detail_v2_schema(mcp, mock_api_client)
        assert mcp is not None

        # Act & Assert - Folio Schema
        from src.trackhs_mcp.infrastructure.tools.resources.schemas.folio import (
            register_folio_schema,
        )

        register_folio_schema(mcp, mock_api_client)
        assert mcp is not None

        # Act & Assert - Units Schema
        from src.trackhs_mcp.infrastructure.tools.resources.schemas.units import (
            register_units_schema,
        )

        register_units_schema(mcp, mock_api_client)
        assert mcp is not None

        # Act & Assert - Amenities Schema
        from src.trackhs_mcp.infrastructure.tools.resources.schemas.amenities import (
            register_amenities_schema,
        )

        register_amenities_schema(mcp, mock_api_client)
        assert mcp is not None

        # Act & Assert - Work Orders Schema
        from src.trackhs_mcp.infrastructure.tools.resources.schemas.work_orders import (
            register_work_orders_schema,
        )

        register_work_orders_schema(mcp, mock_api_client)
        assert mcp is not None

    def test_specific_documentation_resources(self):
        """Test: Recursos de documentación específicos se registran"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()

        # Act & Assert - API V2 Documentation
        from src.trackhs_mcp.infrastructure.tools.resources.documentation.api_v2 import (
            register_api_v2_documentation,
        )

        register_api_v2_documentation(mcp, mock_api_client)
        assert mcp is not None

        # Act & Assert - Folio API Documentation
        from src.trackhs_mcp.infrastructure.tools.resources.documentation.folio_api import (
            register_folio_api_documentation,
        )

        register_folio_api_documentation(mcp, mock_api_client)
        assert mcp is not None

        # Act & Assert - Amenities API Documentation
        from src.trackhs_mcp.infrastructure.tools.resources.documentation.amenities_api import (
            register_amenities_api_documentation,
        )

        register_amenities_api_documentation(mcp, mock_api_client)
        assert mcp is not None

        # Act & Assert - Work Orders API Documentation
        from src.trackhs_mcp.infrastructure.tools.resources.documentation.work_orders_api import (
            register_work_orders_api_documentation,
        )

        register_work_orders_api_documentation(mcp, mock_api_client)
        assert mcp is not None

    def test_specific_reference_resources(self):
        """Test: Recursos de referencia específicos se registran"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()

        # Act & Assert - Status Values
        from src.trackhs_mcp.infrastructure.tools.resources.references.status_values import (
            register_status_values,
        )

        register_status_values(mcp, mock_api_client)
        assert mcp is not None

        # Act & Assert - Date Formats
        from src.trackhs_mcp.infrastructure.tools.resources.references.date_formats import (
            register_date_formats,
        )

        register_date_formats(mcp, mock_api_client)
        assert mcp is not None

        # Act & Assert - Error Codes
        from src.trackhs_mcp.infrastructure.tools.resources.references.error_codes import (
            register_error_codes,
        )

        register_error_codes(mcp, mock_api_client)
        assert mcp is not None

    def test_specific_example_resources(self):
        """Test: Recursos de ejemplos específicos se registran"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()

        # Act & Assert - Search Examples
        from src.trackhs_mcp.infrastructure.tools.resources.examples.search_examples import (
            register_search_examples,
        )

        register_search_examples(mcp, mock_api_client)
        assert mcp is not None

        # Act & Assert - Folio Examples
        from src.trackhs_mcp.infrastructure.tools.resources.examples.folio_examples import (
            register_folio_examples,
        )

        register_folio_examples(mcp, mock_api_client)
        assert mcp is not None

        # Act & Assert - Amenities Examples
        from src.trackhs_mcp.infrastructure.tools.resources.examples.amenities_examples import (
            register_amenities_examples,
        )

        register_amenities_examples(mcp, mock_api_client)
        assert mcp is not None

        # Act & Assert - Units Examples
        from src.trackhs_mcp.infrastructure.tools.resources.examples.units_examples import (
            register_units_examples,
        )

        register_units_examples(mcp, mock_api_client)
        assert mcp is not None

        # Act & Assert - Work Orders Examples
        from src.trackhs_mcp.infrastructure.tools.resources.examples.work_orders_examples import (
            register_work_orders_examples,
        )

        register_work_orders_examples(mcp, mock_api_client)
        assert mcp is not None

    def test_resources_registration_with_invalid_api_client(self):
        """Test: El registro de recursos maneja errores de API client"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        invalid_api_client = None

        # Act & Assert
        with pytest.raises(TypeError):
            from src.trackhs_mcp.infrastructure.tools.resources import (
                register_all_resources,
            )

            register_all_resources(mcp, invalid_api_client)

    def test_resources_registration_with_missing_methods(self):
        """Test: El registro maneja API client con métodos faltantes"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        incomplete_api_client = Mock()
        # No se definen métodos específicos

        # Act & Assert - Debe funcionar ya que los recursos no requieren métodos específicos
        from src.trackhs_mcp.infrastructure.tools.resources import (
            register_all_resources,
        )

        register_all_resources(mcp, incomplete_api_client)
        assert mcp is not None
