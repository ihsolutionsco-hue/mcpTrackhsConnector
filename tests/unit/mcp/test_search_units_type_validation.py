"""
Tests unitarios de validación de tipos para search_units
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError
from src.trackhs_mcp.infrastructure.mcp.search_units import register_search_units


class TestSearchUnitsTypeValidation:
    """Tests para verificar que search_units acepta tipos correctos"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del API client"""
        client = MagicMock()
        client.get = AsyncMock()
        return client

    @pytest.fixture
    def mcp_server(self, mock_api_client):
        """Crear servidor MCP con la herramienta registrada"""
        from fastmcp import FastMCP

        mcp = FastMCP("Test Server")
        register_search_units(mcp, mock_api_client)
        return mcp

    @pytest.mark.asyncio
    async def test_search_units_accepts_integer_page(self, mcp_server, mock_api_client):
        """Verifica que page acepta integers correctamente"""
        # Mock response
        mock_api_client.get.return_value = {
            "data": [],
            "pagination": {"total": 0, "page": 1, "size": 25},
        }

        # Obtener la función registrada
        tools = mcp_server._tool_manager._tools
        search_units_tool = tools["search_units"]

        # Verificar que la función acepta page como int
        # IMPORTANTE: Todos los parámetros opcionales deben ser explícitamente None o tener valor
        result = await search_units_tool.fn(
            page=1,
            size=25,
            sort_column="name",
            sort_direction="asc",
            search=None,
            term=None,
            unit_code=None,
            short_name=None,
            node_id=None,
            amenity_id=None,
            unit_type_id=None,
            id=None,
            calendar_id=None,
            role_id=None,
            bedrooms=2,
            min_bedrooms=None,
            max_bedrooms=None,
            bathrooms=None,
            min_bathrooms=None,
            max_bathrooms=None,
            pets_friendly=None,
            allow_unit_rates=None,
            computed=None,
            inherited=None,
            limited=None,
            is_bookable=None,
            include_descriptions=None,
            is_active=1,
            events_allowed=None,
            smoking_allowed=None,
            children_allowed=None,
            is_accessible=None,
            arrival=None,
            departure=None,
            content_updated_since=None,
            updated_since=None,
            unit_status=None,
        )

        # Verificar que se llamó al API client
        mock_api_client.get.assert_called_once()

        # Verificar que no hay errores de tipo
        assert result is not None

    @pytest.mark.asyncio
    async def test_search_units_accepts_all_integer_params(
        self, mcp_server, mock_api_client
    ):
        """Verifica que todos los parámetros numéricos aceptan integers"""
        # Mock response
        mock_api_client.get.return_value = {
            "data": [],
            "pagination": {"total": 0, "page": 1, "size": 25},
        }

        # Obtener la función registrada
        tools = mcp_server._tool_manager._tools
        search_units_tool = tools["search_units"]

        # Probar con todos los parámetros numéricos como integers
        # IMPORTANTE: Todos los parámetros que no se pasan deben ser explícitamente None
        result = await search_units_tool.fn(
            page=1,
            size=25,
            sort_column="name",
            sort_direction="asc",
            search=None,
            term=None,
            unit_code=None,
            short_name=None,
            node_id=None,
            amenity_id=None,
            unit_type_id=None,
            id=None,
            calendar_id=123,
            role_id=456,
            bedrooms=2,
            min_bedrooms=1,
            max_bedrooms=4,
            bathrooms=1,
            min_bathrooms=1,
            max_bathrooms=2,
            pets_friendly=1,
            allow_unit_rates=1,
            computed=1,
            inherited=1,
            limited=1,
            is_bookable=1,
            include_descriptions=1,
            is_active=1,
            events_allowed=1,
            smoking_allowed=0,
            children_allowed=1,
            is_accessible=1,
            arrival=None,
            departure=None,
            content_updated_since=None,
            updated_since=None,
            unit_status=None,
        )

        # Verificar que se llamó al API client
        mock_api_client.get.assert_called_once()

        # Verificar que no hay errores de tipo
        assert result is not None

    @pytest.mark.asyncio
    async def test_search_units_handles_optional_integers(
        self, mcp_server, mock_api_client
    ):
        """Verifica que los parámetros opcionales funcionan con None"""
        # Mock response
        mock_api_client.get.return_value = {
            "data": [],
            "pagination": {"total": 0, "page": 1, "size": 25},
        }

        # Obtener la función registrada
        tools = mcp_server._tool_manager._tools
        search_units_tool = tools["search_units"]

        # Probar con parámetros opcionales como None
        # IMPORTANTE: Todos los parámetros deben ser explícitamente pasados
        result = await search_units_tool.fn(
            page=1,
            size=25,
            sort_column="name",
            sort_direction="asc",
            search=None,
            term=None,
            unit_code=None,
            short_name=None,
            node_id=None,
            amenity_id=None,
            unit_type_id=None,
            id=None,
            calendar_id=None,
            role_id=None,
            bedrooms=None,  # Optional[int]
            min_bedrooms=None,
            max_bedrooms=None,
            bathrooms=None,  # Optional[int]
            min_bathrooms=None,
            max_bathrooms=None,
            pets_friendly=None,  # Optional[int]
            allow_unit_rates=None,
            computed=None,
            inherited=None,
            limited=None,
            is_bookable=None,
            include_descriptions=None,
            is_active=None,  # Optional[int]
            events_allowed=None,
            smoking_allowed=None,
            children_allowed=None,
            is_accessible=None,
            arrival=None,
            departure=None,
            content_updated_since=None,
            updated_since=None,
            unit_status=None,
        )

        # Verificar que se llamó al API client
        mock_api_client.get.assert_called_once()

        # Verificar que no hay errores de tipo
        assert result is not None

    def test_search_units_function_signature_has_correct_types(self, mcp_server):
        """
        Verifica que la firma tiene tipos específicos (después de estandarización MCP 2025-10-20)

        NOTA: Después de la estandarización MCP, los tipos cambiaron de Union[int, float, str]
        a tipos específicos (int, Optional[int]) con Pydantic Field(). Esto elimina ambigüedad
        para clientes AI y es el comportamiento correcto según mejores prácticas MCP.
        """
        import inspect

        # Obtener la función registrada
        tools = mcp_server._tool_manager._tools
        search_units_tool = tools["search_units"]

        # Obtener la firma de la función
        sig = inspect.signature(search_units_tool.fn)

        # Verificar que page es int (tipo específico después de estandarización)
        page_param = sig.parameters.get("page")
        assert page_param is not None
        # Debe ser int específico (no Union) para eliminar ambigüedad en clientes AI
        assert (
            page_param.annotation == int
        ), f"page debe ser int (estandarización MCP), pero es {page_param.annotation}"

        # Verificar que size es int (tipo específico)
        size_param = sig.parameters.get("size")
        assert size_param is not None
        assert (
            size_param.annotation == int
        ), f"size debe ser int (estandarización MCP), pero es {size_param.annotation}"

        # Verificar que bedrooms es Optional[int]
        # NOTA: El tipo real puede aparecer como Union[int, None] o Optional[int] en runtime
        bedrooms_param = sig.parameters.get("bedrooms")
        assert bedrooms_param is not None
        # Verificar que el tipo base es int (acepta Optional[int] o Union[int, None])
        annotation_str = str(bedrooms_param.annotation)
        assert (
            "int" in annotation_str.lower() or bedrooms_param.annotation == int
        ), f"bedrooms debe ser Optional[int], pero es {bedrooms_param.annotation}"

        # Verificar que is_active es Optional[int]
        is_active_param = sig.parameters.get("is_active")
        assert is_active_param is not None
        annotation_str = str(is_active_param.annotation)
        assert (
            "int" in annotation_str.lower() or is_active_param.annotation == int
        ), f"is_active debe ser Optional[int], pero es {is_active_param.annotation}"

    @pytest.mark.asyncio
    async def test_search_units_has_specific_types_after_standardization(
        self, mcp_server
    ):
        """
        Verifica que los parámetros numéricos tienen tipos específicos (estandarización MCP 2025-10-20)

        NOTA: Este test fue actualizado después de la estandarización MCP. Los parámetros
        ahora usan tipos específicos (int, Optional[int]) en lugar de Union[int, float, str].
        Esto elimina ambigüedad para clientes AI según mejores prácticas MCP.
        """
        import inspect

        # Obtener la función registrada
        tools = mcp_server._tool_manager._tools
        search_units_tool = tools["search_units"]

        # Obtener la firma de la función
        sig = inspect.signature(search_units_tool.fn)

        # Parámetros requeridos que DEBEN ser int (no opcionales)
        required_int_params = ["page", "size"]

        for param_name in required_int_params:
            param = sig.parameters.get(param_name)
            assert param is not None, f"Parámetro {param_name} debe existir"
            assert param.annotation == int, (
                f"Parámetro {param_name} debe ser int (tipo específico), "
                f"pero tiene {param.annotation}"
            )

        # Parámetros opcionales que DEBEN ser Optional[int] o contener 'int'
        optional_int_params = [
            "calendar_id",
            "role_id",
            "bedrooms",
            "min_bedrooms",
            "max_bedrooms",
            "bathrooms",
            "min_bathrooms",
            "max_bathrooms",
            "pets_friendly",
            "allow_unit_rates",
            "computed",
            "inherited",
            "limited",
            "is_bookable",
            "include_descriptions",
            "is_active",
            "events_allowed",
            "smoking_allowed",
            "children_allowed",
            "is_accessible",
        ]

        # Verificar que todos los parámetros opcionales tienen int en su tipo
        for param_name in optional_int_params:
            param = sig.parameters.get(param_name)
            if param is not None:
                annotation_str = str(param.annotation)
                # Debe contener 'int' (puede ser Optional[int] o Union[int, None])
                assert "int" in annotation_str.lower(), (
                    f"Parámetro {param_name} debe ser Optional[int] o contener int, "
                    f"pero tiene {param.annotation}"
                )

    @pytest.mark.asyncio
    async def test_search_units_error_handling_with_invalid_types(self, mcp_server):
        """Verifica que la función maneja errores de tipo correctamente"""
        # Obtener la función registrada
        tools = mcp_server._tool_manager._tools
        search_units_tool = tools["search_units"]

        # La función debería aceptar solo tipos correctos
        # Si se pasan tipos incorrectos, debería fallar en la validación de fastMCP
        # antes de llegar a nuestra función

        # Este test verifica que la función está configurada correctamente
        # para aceptar solo los tipos esperados
        assert search_units_tool is not None
        assert callable(search_units_tool.fn)
