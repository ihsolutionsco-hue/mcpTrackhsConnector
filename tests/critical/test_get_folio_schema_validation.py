"""
Tests unitarios para validar la corrección del esquema MCP de get_folio
Verifica que el parámetro folio_id sea de tipo integer según la documentación oficial
"""

import json
from unittest.mock import AsyncMock, Mock

import pytest
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError


class TestGetFolioSchemaValidation:
    """Tests para validar el esquema MCP corregido de get_folio"""

    def test_get_folio_schema_type_correction(self):
        """Test: El esquema MCP ahora usa integer en lugar de string"""
        # Arrange
        from src.trackhs_mcp.infrastructure.mcp.get_folio import register_get_folio

        mcp = FastMCP("Test")
        mock_api_client = Mock()

        # Act
        register_get_folio(mcp, mock_api_client)

        # Assert - Verificar que la herramienta se registró
        assert "get_folio" in [tool.name for tool in mcp._tools.values()]

        # Obtener la herramienta registrada
        get_folio_tool = None
        for tool in mcp._tools.values():
            if tool.name == "get_folio":
                get_folio_tool = tool
                break

        assert get_folio_tool is not None

        # Verificar el esquema de entrada
        input_schema = get_folio_tool.input_schema
        assert input_schema["type"] == "object"
        assert "properties" in input_schema
        assert "folio_id" in input_schema["properties"]

        # ✅ VERIFICACIÓN CRÍTICA: El parámetro debe ser integer, no string
        folio_id_schema = input_schema["properties"]["folio_id"]
        assert (
            folio_id_schema["type"] == "integer"
        ), f"Expected integer, got {folio_id_schema['type']}"
        assert (
            folio_id_schema["minimum"] == 1
        ), f"Expected minimum 1, got {folio_id_schema.get('minimum')}"

        # Verificar que NO tiene validaciones de string
        assert (
            "pattern" not in folio_id_schema
        ), "Should not have pattern validation for integer"
        assert (
            "minLength" not in folio_id_schema
        ), "Should not have minLength for integer"
        assert (
            "maxLength" not in folio_id_schema
        ), "Should not have maxLength for integer"

    def test_get_folio_parameter_validation_integer(self):
        """Test: El parámetro acepta integer directamente"""
        # Arrange
        from src.trackhs_mcp.infrastructure.mcp.get_folio import register_get_folio

        mcp = FastMCP("Test")
        mock_api_client = Mock()

        # Mock del caso de uso
        mock_use_case = Mock()
        mock_use_case.execute = AsyncMock()
        mock_use_case.execute.return_value = Mock()
        mock_use_case.execute.return_value.model_dump.return_value = {"id": 12345}

        # Mock del API client
        mock_api_client.get = AsyncMock()
        mock_api_client.get.return_value = {"id": 12345}

        # Act
        register_get_folio(mcp, mock_api_client)

        # Obtener la función registrada
        get_folio_func = None
        for tool in mcp._tools.values():
            if tool.name == "get_folio":
                get_folio_func = tool.function
                break

        assert get_folio_func is not None

        # Test con integer válido
        import asyncio

        result = asyncio.run(get_folio_func(folio_id=12345))
        assert result is not None

    def test_get_folio_parameter_validation_string_rejection(self):
        """Test: El parámetro rechaza strings (debe ser integer)"""
        # Arrange
        from src.trackhs_mcp.infrastructure.mcp.get_folio import register_get_folio

        mcp = FastMCP("Test")
        mock_api_client = Mock()

        # Act
        register_get_folio(mcp, mock_api_client)

        # Obtener la función registrada
        get_folio_func = None
        for tool in mcp._tools.values():
            if tool.name == "get_folio":
                get_folio_func = tool.function
                break

        assert get_folio_func is not None

        # Test que string es rechazado por Pydantic
        import asyncio

        with pytest.raises((TypeError, ValueError, ToolError)):
            asyncio.run(get_folio_func(folio_id="12345"))  # String debe ser rechazado

    def test_get_folio_parameter_validation_negative_integer(self):
        """Test: El parámetro rechaza enteros negativos"""
        # Arrange
        from src.trackhs_mcp.infrastructure.mcp.get_folio import register_get_folio

        mcp = FastMCP("Test")
        mock_api_client = Mock()

        # Act
        register_get_folio(mcp, mock_api_client)

        # Obtener la función registrada
        get_folio_func = None
        for tool in mcp._tools.values():
            if tool.name == "get_folio":
                get_folio_func = tool.function
                break

        assert get_folio_func is not None

        # Test que enteros negativos son rechazados
        import asyncio

        with pytest.raises((ValueError, ToolError)):
            asyncio.run(get_folio_func(folio_id=-1))  # Negativo debe ser rechazado

    def test_get_folio_parameter_validation_zero(self):
        """Test: El parámetro rechaza cero"""
        # Arrange
        from src.trackhs_mcp.infrastructure.mcp.get_folio import register_get_folio

        mcp = FastMCP("Test")
        mock_api_client = Mock()

        # Act
        register_get_folio(mcp, mock_api_client)

        # Obtener la función registrada
        get_folio_func = None
        for tool in mcp._tools.values():
            if tool.name == "get_folio":
                get_folio_func = tool.function
                break

        assert get_folio_func is not None

        # Test que cero es rechazado
        import asyncio

        with pytest.raises((ValueError, ToolError)):
            asyncio.run(get_folio_func(folio_id=0))  # Cero debe ser rechazado

    def test_get_folio_schema_matches_api_documentation(self):
        """Test: El esquema MCP coincide con la documentación oficial de la API"""
        # Arrange
        from src.trackhs_mcp.infrastructure.mcp.get_folio import register_get_folio

        mcp = FastMCP("Test")
        mock_api_client = Mock()

        # Act
        register_get_folio(mcp, mock_api_client)

        # Obtener la herramienta registrada
        get_folio_tool = None
        for tool in mcp._tools.values():
            if tool.name == "get_folio":
                get_folio_tool = tool
                break

        assert get_folio_tool is not None

        # Verificar que el esquema coincide con la documentación oficial
        input_schema = get_folio_tool.input_schema
        folio_id_schema = input_schema["properties"]["folio_id"]

        # Según la documentación oficial (get folio.md líneas 33-41):
        # "schema": {"type": "integer", "minimum": 1}
        assert folio_id_schema["type"] == "integer"
        assert folio_id_schema["minimum"] == 1

        # Verificar que está en required
        assert "folio_id" in input_schema.get("required", [])

    def test_get_folio_description_updated(self):
        """Test: La descripción del parámetro fue actualizada correctamente"""
        # Arrange
        from src.trackhs_mcp.infrastructure.mcp.get_folio import register_get_folio

        mcp = FastMCP("Test")
        mock_api_client = Mock()

        # Act
        register_get_folio(mcp, mock_api_client)

        # Obtener la herramienta registrada
        get_folio_tool = None
        for tool in mcp._tools.values():
            if tool.name == "get_folio":
                get_folio_tool = tool
                break

        assert get_folio_tool is not None

        # Verificar la descripción actualizada
        input_schema = get_folio_tool.input_schema
        folio_id_schema = input_schema["properties"]["folio_id"]
        description = folio_id_schema.get("description", "")

        # ✅ VERIFICACIÓN: La descripción debe indicar que es integer, no string
        assert "positive integer" in description
        assert "as string" not in description  # No debe mencionar string
        assert "Example: 12345" in description  # Debe mostrar ejemplos sin comillas

    def test_get_folio_removed_manual_conversion(self):
        """Test: Se eliminó la conversión manual de string a int"""
        # Arrange
        from src.trackhs_mcp.infrastructure.mcp.get_folio import register_get_folio

        mcp = FastMCP("Test")
        mock_api_client = Mock()

        # Act
        register_get_folio(mcp, mock_api_client)

        # Obtener la función registrada
        get_folio_func = None
        for tool in mcp._tools.values():
            if tool.name == "get_folio":
                get_folio_func = tool.function
                break

        assert get_folio_func is not None

        # Verificar que la función no tiene conversión manual
        import inspect

        source = inspect.getsource(get_folio_func)

        # ✅ VERIFICACIÓN: No debe tener conversión manual
        assert "int(folio_id" not in source, "Should not have manual int() conversion"
        assert "folio_id.strip()" not in source, "Should not have strip() for integer"
        assert "folio_id_int" not in source, "Should not have folio_id_int variable"

    def test_get_folio_uses_direct_parameter(self):
        """Test: Usa el parámetro directamente sin conversión"""
        # Arrange
        from src.trackhs_mcp.infrastructure.mcp.get_folio import register_get_folio

        mcp = FastMCP("Test")
        mock_api_client = Mock()

        # Act
        register_get_folio(mcp, mock_api_client)

        # Obtener la función registrada
        get_folio_func = None
        for tool in mcp._tools.values():
            if tool.name == "get_folio":
                get_folio_func = tool.function
                break

        assert get_folio_func is not None

        # Verificar que usa el parámetro directamente
        import inspect

        source = inspect.getsource(get_folio_func)

        # ✅ VERIFICACIÓN: Debe usar folio_id directamente
        assert (
            "GetFolioParams(folio_id=folio_id)" in source
        ), "Should use folio_id directly"
        assert (
            "GetFolioParams(folio_id=folio_id_int)" not in source
        ), "Should not use folio_id_int"

    def test_get_folio_schema_json_structure(self):
        """Test: El esquema JSON generado es correcto para MCP"""
        # Arrange
        from src.trackhs_mcp.infrastructure.mcp.get_folio import register_get_folio

        mcp = FastMCP("Test")
        mock_api_client = Mock()

        # Act
        register_get_folio(mcp, mock_api_client)

        # Obtener la herramienta registrada
        get_folio_tool = None
        for tool in mcp._tools.values():
            if tool.name == "get_folio":
                get_folio_tool = tool
                break

        assert get_folio_tool is not None

        # Verificar estructura del esquema JSON
        input_schema = get_folio_tool.input_schema

        # Estructura básica
        assert input_schema["type"] == "object"
        assert "properties" in input_schema
        assert "required" in input_schema

        # Esquema del parámetro folio_id
        folio_id_schema = input_schema["properties"]["folio_id"]

        # ✅ VERIFICACIÓN CRÍTICA: Debe ser integer con validaciones correctas
        expected_schema = {
            "type": "integer",
            "minimum": 1,
            "description": "Unique folio ID (positive integer). Example: 12345 or 37152796",
        }

        for key, expected_value in expected_schema.items():
            assert key in folio_id_schema, f"Missing {key} in schema"
            assert (
                folio_id_schema[key] == expected_value
            ), f"Schema mismatch for {key}: expected {expected_value}, got {folio_id_schema[key]}"

    def test_get_folio_compatibility_with_domain_models(self):
        """Test: Compatibilidad con los modelos de dominio existentes"""
        # Arrange
        from src.trackhs_mcp.domain.entities.folios import GetFolioParams

        # Act & Assert
        # ✅ VERIFICACIÓN: Los modelos de dominio ya usan int correctamente
        params = GetFolioParams(folio_id=12345)
        assert params.folio_id == 12345
        assert isinstance(params.folio_id, int)

        # Verificar que rechaza strings
        with pytest.raises(Exception):  # Pydantic validation error
            GetFolioParams(folio_id="12345")

    def test_get_folio_schema_consistency_with_fastmcp(self):
        """Test: El esquema es consistente con FastMCP"""
        # Arrange
        from src.trackhs_mcp.infrastructure.mcp.get_folio import register_get_folio

        mcp = FastMCP("Test")
        mock_api_client = Mock()

        # Act
        register_get_folio(mcp, mock_api_client)

        # Obtener la herramienta registrada
        get_folio_tool = None
        for tool in mcp._tools.values():
            if tool.name == "get_folio":
                get_folio_tool = tool
                break

        assert get_folio_tool is not None

        # Verificar que FastMCP generó el esquema correctamente
        input_schema = get_folio_tool.input_schema

        # ✅ VERIFICACIÓN: FastMCP debe generar el esquema JSON correcto
        assert isinstance(input_schema, dict)
        assert "type" in input_schema
        assert "properties" in input_schema

        # El esquema debe ser válido JSON Schema
        import json

        json.dumps(input_schema)  # Debe ser serializable a JSON
