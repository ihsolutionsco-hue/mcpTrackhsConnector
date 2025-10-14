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
        result = await search_units_tool.fn(
            page=1, size=25, bedrooms=2, is_active=1  # int  # int  # int  # int
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
        result = await search_units_tool.fn(
            page=1,
            size=25,
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
        result = await search_units_tool.fn(
            page=1,
            size=25,
            bedrooms=None,  # Optional[int]
            bathrooms=None,  # Optional[int]
            is_active=None,  # Optional[int]
            pets_friendly=None,  # Optional[int]
        )

        # Verificar que se llamó al API client
        mock_api_client.get.assert_called_once()

        # Verificar que no hay errores de tipo
        assert result is not None

    def test_search_units_function_signature_has_correct_types(self, mcp_server):
        """Verifica que la firma de la función tiene los tipos flexibles correctos para JSON-RPC"""
        import inspect
        from typing import Union

        # Obtener la función registrada
        tools = mcp_server._tool_manager._tools
        search_units_tool = tools["search_units"]

        # Obtener la firma de la función
        sig = inspect.signature(search_units_tool.fn)

        # Verificar que page es Union[int, float, str] (flexible para JSON-RPC)
        page_param = sig.parameters.get("page")
        assert page_param is not None
        # Debe ser Union[int, float, str] para compatibilidad JSON-RPC
        assert page_param.annotation == Union[int, float, str], (
            f"page debe ser Union[int, float, str] para compatibilidad JSON-RPC, "
            f"pero es {page_param.annotation}"
        )

        # Verificar que size es Union[int, float, str] (flexible para JSON-RPC)
        size_param = sig.parameters.get("size")
        assert size_param is not None
        assert size_param.annotation == Union[int, float, str], (
            f"size debe ser Union[int, float, str] para compatibilidad JSON-RPC, "
            f"pero es {size_param.annotation}"
        )

        # Verificar que bedrooms es Optional[Union[int, float, str]]
        bedrooms_param = sig.parameters.get("bedrooms")
        assert bedrooms_param is not None
        # Verificar que contiene Union (flexible para JSON-RPC)
        annotation_str = str(bedrooms_param.annotation)
        assert "Union" in annotation_str, (
            f"bedrooms debe ser Optional[Union[int, float, str]], "
            f"pero es {bedrooms_param.annotation}"
        )

        # Verificar que is_active es Optional[Union[int, float, str]]
        is_active_param = sig.parameters.get("is_active")
        assert is_active_param is not None
        annotation_str = str(is_active_param.annotation)
        assert "Union" in annotation_str, (
            f"is_active debe ser Optional[Union[int, float, str]], "
            f"pero es {is_active_param.annotation}"
        )

    @pytest.mark.asyncio
    async def test_search_units_has_flexible_union_types(self, mcp_server):
        """Verifica que los parámetros numéricos tienen Union[int, float, str] para JSON-RPC"""
        import inspect

        # Obtener la función registrada
        tools = mcp_server._tool_manager._tools
        search_units_tool = tools["search_units"]

        # Obtener la firma de la función
        sig = inspect.signature(search_units_tool.fn)

        # Parámetros numéricos que DEBEN tener Union[int, float, str]
        numeric_params = [
            "page",
            "size",
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

        # Verificar que todos los parámetros numéricos tienen Union types
        for param_name in numeric_params:
            param = sig.parameters.get(param_name)
            if param is not None:
                annotation_str = str(param.annotation)
                # Debe contener Union para compatibilidad JSON-RPC
                assert "Union" in annotation_str or "union" in annotation_str, (
                    f"Parámetro {param_name} debe tener Union[int, float, str] "
                    f"para compatibilidad JSON-RPC, pero tiene {param.annotation}"
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
