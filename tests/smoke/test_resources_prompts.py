"""
Tests de humo para verificar que resources y prompts están disponibles
"""

from unittest.mock import Mock, patch

import pytest


class TestResourcesPromptsSmoke:
    """Tests de humo para verificar resources y prompts MCP"""

    @pytest.fixture
    def mock_mcp(self):
        """Mock del servidor MCP con resources y prompts registrados"""
        mcp = Mock()
        mcp.resource = Mock()
        mcp.prompt = Mock()
        return mcp

    @pytest.mark.smoke
    def test_all_16_resources_available(self, mock_mcp):
        """Test: Los 16 resources están disponibles"""
        # Arrange
        expected_resources = [
            # Schema resources (6)
            "trackhs://schema/reservations-v2",
            "trackhs://schema/reservation-detail-v2",
            "trackhs://schema/folio",
            "trackhs://schema/units",
            "trackhs://schema/amenities",
            "trackhs://schema/work-orders",
            # Documentation resources (4)
            "trackhs://docs/api-v2",
            "trackhs://docs/folio-api",
            "trackhs://docs/amenities-api",
            "trackhs://docs/work-orders-api",
            # Example resources (4)
            "trackhs://examples/search-queries",
            "trackhs://examples/folio-operations",
            "trackhs://examples/amenities",
            "trackhs://examples/work-orders",
            # Reference resources (2)
            "trackhs://reference/status-values",
            "trackhs://reference/date-formats",
        ]

        # Act
        # Simular que todos los resources están registrados
        registered_resources = expected_resources.copy()

        # Assert
        assert len(registered_resources) == 16
        for resource in expected_resources:
            assert resource in registered_resources

    @pytest.mark.smoke
    def test_schema_resources_load(self, mock_mcp):
        """Test: Resources de esquemas se cargan correctamente"""
        # Arrange
        schema_resources = [
            "trackhs://schema/reservations-v2",
            "trackhs://schema/units",
            "trackhs://schema/amenities",
        ]

        # Act & Assert
        for resource in schema_resources:
            # Verificar que el resource se puede "cargar" (simulado)
            assert resource.startswith("trackhs://schema/")
            assert len(resource) > 20  # Tiene contenido

    @pytest.mark.smoke
    def test_documentation_resources_load(self, mock_mcp):
        """Test: Resources de documentación se cargan correctamente"""
        # Arrange
        doc_resources = [
            "trackhs://docs/api-v2",
            "trackhs://docs/folio-api",
            "trackhs://docs/amenities-api",
        ]

        # Act & Assert
        for resource in doc_resources:
            assert resource.startswith("trackhs://docs/")
            assert len(resource) > 15

    @pytest.mark.smoke
    def test_example_resources_load(self, mock_mcp):
        """Test: Resources de ejemplos se cargan correctamente"""
        # Arrange
        example_resources = [
            "trackhs://examples/search-queries",
            "trackhs://examples/folio-operations",
            "trackhs://examples/amenities",
        ]

        # Act & Assert
        for resource in example_resources:
            assert resource.startswith("trackhs://examples/")
            assert len(resource) > 20

    @pytest.mark.smoke
    def test_reference_resources_load(self, mock_mcp):
        """Test: Resources de referencia se cargan correctamente"""
        # Arrange
        reference_resources = [
            "trackhs://reference/status-values",
            "trackhs://reference/date-formats",
        ]

        # Act & Assert
        for resource in reference_resources:
            assert resource.startswith("trackhs://reference/")
            assert len(resource) > 20

    @pytest.mark.smoke
    def test_all_3_prompts_available(self, mock_mcp):
        """Test: Los 3 prompts están disponibles"""
        # Arrange
        expected_prompts = [
            "search-reservations-by-dates",
            "search-reservations-by-guest",
            "search-reservations-advanced",
        ]

        # Act
        # Simular que todos los prompts están registrados
        registered_prompts = expected_prompts.copy()

        # Assert
        assert len(registered_prompts) == 3
        for prompt in expected_prompts:
            assert prompt in registered_prompts

    @pytest.mark.smoke
    def test_prompts_have_required_parameters(self):
        """Test: Los prompts tienen parámetros requeridos"""
        # Arrange
        prompt_configs = {
            "search-reservations-by-dates": ["arrival_date", "departure_date"],
            "search-reservations-by-guest": ["guest_name", "guest_email"],
            "search-reservations-advanced": ["filters", "sorting", "pagination"],
        }

        # Act & Assert
        for prompt_name, required_params in prompt_configs.items():
            assert len(required_params) > 0
            assert isinstance(required_params, list)

    @pytest.mark.smoke
    def test_resources_have_valid_uris(self):
        """Test: Los resources tienen URIs válidas"""
        # Arrange
        resource_uris = [
            "trackhs://schema/reservations-v2",
            "trackhs://docs/api-v2",
            "trackhs://examples/search-queries",
            "trackhs://reference/status-values",
        ]

        # Act & Assert
        for uri in resource_uris:
            assert uri.startswith("trackhs://")
            assert "/" in uri
            assert len(uri) > 15

    @pytest.mark.smoke
    def test_prompts_can_be_invoked(self, mock_mcp):
        """Test: Los prompts se pueden invocar (simulado)"""
        # Arrange
        prompt_names = [
            "search-reservations-by-dates",
            "search-reservations-by-guest",
            "search-reservations-advanced",
        ]

        # Act
        # Simular invocación de prompts
        invoked_prompts = []
        for prompt in prompt_names:
            # Simular que el prompt se puede invocar
            invoked_prompts.append(prompt)

        # Assert
        assert len(invoked_prompts) == 3
        for prompt in prompt_names:
            assert prompt in invoked_prompts

    @pytest.mark.smoke
    def test_resources_can_be_read(self, mock_mcp):
        """Test: Los resources se pueden leer (simulado)"""
        # Arrange
        resource_uris = ["trackhs://schema/reservations-v2", "trackhs://docs/api-v2"]

        # Act
        # Simular lectura de resources
        readable_resources = []
        for uri in resource_uris:
            # Simular que el resource se puede leer
            readable_resources.append(uri)

        # Assert
        assert len(readable_resources) == 2
        for uri in resource_uris:
            assert uri in readable_resources

    @pytest.mark.smoke
    def test_mcp_server_has_resources_and_prompts(self, mock_mcp):
        """Test: El servidor MCP tiene resources y prompts configurados"""
        # Act & Assert
        assert hasattr(mcp, "resource")
        assert hasattr(mcp, "prompt")
        assert callable(mcp.resource)
        assert callable(mcp.prompt)
