"""
Tests de integración para verificar consistencia de tipos entre herramientas
"""

import inspect

import pytest

from src.trackhs_mcp.infrastructure.mcp.get_folio import register_get_folio
from src.trackhs_mcp.infrastructure.mcp.get_reservation_v2 import (
    register_get_reservation_v2,
)
from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
    register_search_reservations_v2,
)
from src.trackhs_mcp.infrastructure.mcp.search_units import register_search_units


class TestTypeConsistency:
    """Tests para verificar consistencia de tipos entre herramientas"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del API client"""
        from unittest.mock import MagicMock

        client = MagicMock()
        return client

    @pytest.fixture
    def all_tools(self, mock_api_client):
        """Registrar todas las herramientas y obtener sus funciones"""
        from fastmcp import FastMCP

        mcp = FastMCP("Test Server")

        # Registrar todas las herramientas
        register_search_units(mcp, mock_api_client)
        register_search_reservations_v2(mcp, mock_api_client)
        register_get_reservation_v2(mcp, mock_api_client)
        register_get_folio(mcp, mock_api_client)

        return mcp._tool_manager._tools

    def test_all_tools_use_consistent_types(self, all_tools):
        """Verifica que todas las herramientas usan tipos consistentes"""

        # Herramientas que deben tener page/size como int
        pagination_tools = [
            "search_units",
            "search_reservations_v1",
            "search_reservations_v2",
        ]

        for tool_name in pagination_tools:
            if tool_name in all_tools:
                tool = all_tools[tool_name]
                sig = inspect.signature(tool.fn)

                # Verificar que page es int
                if "page" in sig.parameters:
                    page_param = sig.parameters["page"]
                    assert (
                        page_param.annotation == int
                    ), f"{tool_name}.page debe ser int"

                # Verificar que size es int
                if "size" in sig.parameters:
                    size_param = sig.parameters["size"]
                    assert (
                        size_param.annotation == int
                    ), f"{tool_name}.size debe ser int"

    def test_no_union_int_str_in_any_tool(self, all_tools):
        """Verifica que ninguna herramienta usa Union[int, str]"""

        for tool_name, tool in all_tools.items():
            sig = inspect.signature(tool.fn)

            for param_name, param in sig.parameters.items():
                annotation_str = str(param.annotation)

                # Verificar que no hay Union[int, str]
                assert (
                    "Union[int, str]" not in annotation_str
                ), f"{tool_name}.{param_name} tiene Union[int, str]"
                assert (
                    "Union[str, int]" not in annotation_str
                ), f"{tool_name}.{param_name} tiene Union[str, int]"

    def test_search_units_has_correct_integer_types(self, all_tools):
        """Verifica que search_units tiene los tipos correctos para parámetros numéricos"""

        if "search_units" not in all_tools:
            pytest.skip("search_units no está disponible")

        tool = all_tools["search_units"]
        sig = inspect.signature(tool.fn)

        # Parámetros que deben ser int
        int_params = ["page", "size", "calendar_id", "role_id"]
        for param_name in int_params:
            if param_name in sig.parameters:
                param = sig.parameters[param_name]
                assert (
                    param.annotation == int
                ), f"search_units.{param_name} debe ser int"

        # Parámetros que deben ser Optional[int]
        optional_int_params = [
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

        for param_name in optional_int_params:
            if param_name in sig.parameters:
                param = sig.parameters[param_name]
                # Verificar que es Optional[int] (Union[int, None] o similar)
                annotation_str = str(param.annotation)
                assert (
                    "int" in annotation_str
                ), f"search_units.{param_name} debe ser int o Optional[int]"
                assert (
                    "Union[int, str]" not in annotation_str
                ), f"search_units.{param_name} no debe ser Union[int, str]"

    def test_reservation_tools_have_consistent_pagination(self, all_tools):
        """Verifica que las herramientas de reservaciones tienen paginación consistente"""

        reservation_tools = ["search_reservations_v1", "search_reservations_v2"]

        for tool_name in reservation_tools:
            if tool_name in all_tools:
                tool = all_tools[tool_name]
                sig = inspect.signature(tool.fn)

                # Verificar que page y size son int
                if "page" in sig.parameters:
                    assert sig.parameters["page"].annotation == int
                if "size" in sig.parameters:
                    assert sig.parameters["size"].annotation == int

    def test_id_parameters_are_strings(self, all_tools):
        """Verifica que los parámetros de ID son strings"""

        id_tools = ["get_reservation_v2", "get_folio"]

        for tool_name in id_tools:
            if tool_name in all_tools:
                tool = all_tools[tool_name]
                sig = inspect.signature(tool.fn)

                # Verificar que los parámetros de ID son strings
                if "reservation_id" in sig.parameters:
                    assert sig.parameters["reservation_id"].annotation == str
                if "folio_id" in sig.parameters:
                    assert sig.parameters["folio_id"].annotation == str

    def test_boolean_parameters_are_integers(self, all_tools):
        """Verifica que los parámetros booleanos son integers (0/1)"""

        if "search_units" not in all_tools:
            pytest.skip("search_units no está disponible")

        tool = all_tools["search_units"]
        sig = inspect.signature(tool.fn)

        # Parámetros booleanos que deben ser Optional[int]
        boolean_params = [
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

        for param_name in boolean_params:
            if param_name in sig.parameters:
                param = sig.parameters[param_name]
                annotation_str = str(param.annotation)

                # Verificar que es int o Optional[int], no Union[int, str]
                assert (
                    "int" in annotation_str
                ), f"search_units.{param_name} debe ser int"
                assert (
                    "Union[int, str]" not in annotation_str
                ), f"search_units.{param_name} no debe ser Union[int, str]"

    def test_date_parameters_are_strings(self, all_tools):
        """Verifica que los parámetros de fecha son strings"""

        tools_with_dates = [
            "search_reservations_v1",
            "search_reservations_v2",
            "search_units",
        ]

        for tool_name in tools_with_dates:
            if tool_name in all_tools:
                tool = all_tools[tool_name]
                sig = inspect.signature(tool.fn)

                # Parámetros de fecha comunes
                date_params = [
                    "arrival_start",
                    "arrival_end",
                    "departure_start",
                    "departure_end",
                ]

                for param_name in date_params:
                    if param_name in sig.parameters:
                        param = sig.parameters[param_name]
                        # Verificar que es Optional[str]
                        annotation_str = str(param.annotation)
                        assert (
                            "str" in annotation_str
                        ), f"{tool_name}.{param_name} debe ser str"

    def test_tool_signatures_are_clean(self, all_tools):
        """Verifica que las firmas de las herramientas están limpias"""

        for tool_name, tool in all_tools.items():
            sig = inspect.signature(tool.fn)

            for param_name, param in sig.parameters.items():
                annotation_str = str(param.annotation)

                # Verificar que no hay tipos problemáticos
                assert (
                    "Union[int, str]" not in annotation_str
                ), f"{tool_name}.{param_name} tiene Union[int, str]"
                assert (
                    "Union[str, int]" not in annotation_str
                ), f"{tool_name}.{param_name} tiene Union[str, int]"

                # Verificar que los tipos son claros
                assert (
                    param.annotation != inspect.Parameter.empty
                ), f"{tool_name}.{param_name} no tiene tipo especificado"
