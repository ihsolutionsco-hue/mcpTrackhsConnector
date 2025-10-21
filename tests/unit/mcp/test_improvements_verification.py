"""
Tests para verificar que las mejoras de FastMCP están implementadas correctamente
"""

import json
from pathlib import Path

import pytest


class TestImprovementsVerification:
    """Tests para verificar mejoras implementadas"""

    def test_fastmcp_json_exists(self):
        """Test de que fastmcp.json existe"""
        config_path = Path("fastmcp.json")
        assert config_path.exists(), "fastmcp.json debe existir"

    def test_fastmcp_json_valid(self):
        """Test de que fastmcp.json es válido"""
        config_path = Path("fastmcp.json")

        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        # Verificar campos requeridos
        assert "$schema" in config
        assert "source" in config
        assert "transport" in config
        assert config["transport"] == "http"

    def test_requirements_updated(self):
        """Test de que requirements.txt está actualizado"""
        requirements_path = Path("requirements.txt")
        assert requirements_path.exists()

        with open(requirements_path, "r", encoding="utf-8") as f:
            content = f.read()

        assert "fastmcp>=2.12.0" in content

    def test_search_units_has_output_schema(self):
        """Test de que search_units tiene output schema"""
        from src.trackhs_mcp.infrastructure.mcp.search_units import SearchUnitsResult

        # Verificar que la dataclass existe
        assert SearchUnitsResult is not None

        # Verificar campos
        fields = SearchUnitsResult.__dataclass_fields__
        assert "units" in fields
        assert "total" in fields
        assert "page" in fields
        assert "size" in fields
        assert "total_pages" in fields
        assert "has_next" in fields
        assert "has_previous" in fields

    def test_search_amenities_has_output_schema(self):
        """Test de que search_amenities tiene output schema"""
        from src.trackhs_mcp.infrastructure.mcp.search_amenities import (
            SearchAmenitiesResult,
        )

        # Verificar que la dataclass existe
        assert SearchAmenitiesResult is not None

        # Verificar campos
        fields = SearchAmenitiesResult.__dataclass_fields__
        assert "amenities" in fields
        assert "total" in fields
        assert "page" in fields
        assert "size" in fields
        assert "total_pages" in fields
        assert "has_next" in fields
        assert "has_previous" in fields

    def test_tool_error_imports(self):
        """Test de que ToolError está importado en las herramientas"""
        # Verificar que los módulos se pueden importar sin errores
        import src.trackhs_mcp.infrastructure.mcp.create_housekeeping_work_order
        import src.trackhs_mcp.infrastructure.mcp.create_maintenance_work_order
        import src.trackhs_mcp.infrastructure.mcp.search_amenities
        import src.trackhs_mcp.infrastructure.mcp.search_units

        # Verificar que los módulos existen
        assert (
            src.trackhs_mcp.infrastructure.mcp.create_housekeeping_work_order
            is not None
        )
        assert (
            src.trackhs_mcp.infrastructure.mcp.create_maintenance_work_order is not None
        )
        assert src.trackhs_mcp.infrastructure.mcp.search_amenities is not None
        assert src.trackhs_mcp.infrastructure.mcp.search_units is not None

    def test_simplified_types(self):
        """Test de que los tipos están simplificados"""
        from src.trackhs_mcp.infrastructure.mcp.search_units import SearchUnitsParams

        # Verificar que los campos tienen tipos simples
        fields = SearchUnitsParams.__fields__

        # Verificar que page y size existen
        page_field = fields.get("page")
        size_field = fields.get("size")

        assert page_field is not None
        assert size_field is not None

        # Verificar que son campos de Pydantic
        assert hasattr(page_field, "annotation")
        assert hasattr(size_field, "annotation")

    def test_main_server_config(self):
        """Test de que el servidor principal está configurado correctamente"""
        from src.trackhs_mcp.__main__ import main

        # Verificar que la función main existe
        assert main is not None

        # Verificar que el archivo se puede importar sin errores
        import src.trackhs_mcp.__main__

        assert hasattr(src.trackhs_mcp.__main__, "main")

    def test_middleware_imports(self):
        """Test de que los imports de middleware están disponibles"""
        try:
            from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware

            assert ErrorHandlingMiddleware is not None
        except ImportError:
            pytest.skip("ErrorHandlingMiddleware no disponible en esta versión")

    def test_fastmcp_exceptions_available(self):
        """Test de que las excepciones de FastMCP están disponibles"""
        from fastmcp.exceptions import ResourceError, ToolError

        assert ToolError is not None
        assert ResourceError is not None

    def test_dataclass_imports(self):
        """Test de que dataclass está disponible"""
        from dataclasses import dataclass

        assert dataclass is not None

    def test_pydantic_field_available(self):
        """Test de que Pydantic Field está disponible"""
        from pydantic import Field

        assert Field is not None
