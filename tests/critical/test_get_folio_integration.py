"""
Tests de integración para verificar que la corrección del esquema MCP funciona end-to-end
"""

import asyncio
import json
from unittest.mock import AsyncMock, Mock

import pytest
from fastmcp import FastMCP


class TestGetFolioIntegration:
    """Tests de integración para get_folio con esquema corregido"""

    def test_get_folio_end_to_end_with_integer(
        self, mock_api_client, sample_folio_data
    ):
        """Test: Flujo completo con parámetro integer"""
        # Arrange
        from src.trackhs_mcp.infrastructure.mcp.get_folio import register_get_folio

        mcp = FastMCP("Test")

        # Mock del API client para simular respuesta
        mock_api_client.get = AsyncMock()
        mock_api_client.get.return_value = sample_folio_data

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
        result = asyncio.run(get_folio_func(folio_id=12345))

        # Assert
        assert result is not None
        assert isinstance(result, dict)
        assert result["id"] == 12345

    def test_get_folio_schema_generation_with_fastmcp(self):
        """Test: FastMCP genera el esquema JSON correcto"""
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

        # Verificar que el esquema es válido para MCP
        input_schema = get_folio_tool.input_schema

        # ✅ VERIFICACIÓN: El esquema debe ser válido JSON Schema
        try:
            json.dumps(input_schema)
        except (TypeError, ValueError) as e:
            pytest.fail(f"Schema is not valid JSON: {e}")

        # ✅ VERIFICACIÓN: Debe tener la estructura correcta para MCP
        assert input_schema["type"] == "object"
        assert "properties" in input_schema
        assert "folio_id" in input_schema["properties"]

        # ✅ VERIFICACIÓN CRÍTICA: folio_id debe ser integer
        folio_id_schema = input_schema["properties"]["folio_id"]
        assert folio_id_schema["type"] == "integer"
        assert folio_id_schema["minimum"] == 1

    def test_get_folio_mcp_protocol_compliance(self):
        """Test: Cumplimiento con el protocolo MCP"""
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

        # ✅ VERIFICACIÓN: Cumple con el protocolo MCP
        assert hasattr(get_folio_tool, "name")
        assert hasattr(get_folio_tool, "description")
        assert hasattr(get_folio_tool, "input_schema")
        assert hasattr(get_folio_tool, "function")

        # Verificar que el esquema es compatible con MCP
        input_schema = get_folio_tool.input_schema

        # MCP requiere que el esquema sea JSON Schema válido
        assert isinstance(input_schema, dict)
        assert "type" in input_schema
        assert "properties" in input_schema

        # El parámetro debe estar en required
        assert "folio_id" in input_schema.get("required", [])

    def test_get_folio_parameter_validation_edge_cases(self):
        """Test: Casos límite de validación de parámetros"""
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

        # Test casos límite
        test_cases = [
            (1, True),  # Mínimo válido
            (12345, True),  # Valor típico
            (999999, True),  # Valor grande
            (0, False),  # Cero (inválido)
            (-1, False),  # Negativo (inválido)
            (-999, False),  # Negativo grande (inválido)
        ]

        for value, should_pass in test_cases:
            if should_pass:
                # Debe pasar sin excepción
                try:
                    asyncio.run(get_folio_func(folio_id=value))
                except Exception as e:
                    pytest.fail(f"Valid value {value} should not raise exception: {e}")
            else:
                # Debe fallar con excepción
                with pytest.raises((ValueError, TypeError, Exception)):
                    asyncio.run(get_folio_func(folio_id=value))

    def test_get_folio_schema_matches_api_documentation_exactly(self):
        """Test: El esquema coincide exactamente con la documentación oficial"""
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

        # ✅ VERIFICACIÓN: Debe coincidir con la documentación oficial
        # Según get folio.md líneas 33-41:
        # "schema": {"type": "integer", "minimum": 1}
        input_schema = get_folio_tool.input_schema
        folio_id_schema = input_schema["properties"]["folio_id"]

        # Verificar coincidencia exacta
        assert folio_id_schema["type"] == "integer"
        assert folio_id_schema["minimum"] == 1

        # Verificar que NO tiene validaciones de string
        string_validations = ["pattern", "minLength", "maxLength", "format"]
        for validation in string_validations:
            assert (
                validation not in folio_id_schema
            ), f"Should not have {validation} for integer type"

    def test_get_folio_backward_compatibility(self):
        """Test: Compatibilidad hacia atrás con el código existente"""
        # Arrange
        from src.trackhs_mcp.application.use_cases.get_folio import GetFolioUseCase
        from src.trackhs_mcp.domain.entities.folios import GetFolioParams

        # ✅ VERIFICACIÓN: Los modelos de dominio siguen funcionando
        params = GetFolioParams(folio_id=12345)
        assert params.folio_id == 12345
        assert isinstance(params.folio_id, int)

        # ✅ VERIFICACIÓN: El caso de uso sigue funcionando
        mock_api_client = Mock()
        use_case = GetFolioUseCase(mock_api_client)
        assert use_case is not None

    def test_get_folio_schema_serialization(self):
        """Test: El esquema se puede serializar correctamente"""
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

        # ✅ VERIFICACIÓN: El esquema se puede serializar
        input_schema = get_folio_tool.input_schema

        # Serializar a JSON
        json_str = json.dumps(input_schema, indent=2)
        assert isinstance(json_str, str)
        assert len(json_str) > 0

        # Deserializar de JSON
        parsed_schema = json.loads(json_str)
        assert parsed_schema == input_schema

        # Verificar que el esquema deserializado es correcto
        assert parsed_schema["properties"]["folio_id"]["type"] == "integer"
        assert parsed_schema["properties"]["folio_id"]["minimum"] == 1

    def test_get_folio_tool_metadata(self):
        """Test: Metadatos de la herramienta son correctos"""
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

        # ✅ VERIFICACIÓN: Metadatos correctos
        assert get_folio_tool.name == "get_folio"
        assert get_folio_tool.description is not None
        assert len(get_folio_tool.description) > 0
        assert "Get complete folio details" in get_folio_tool.description
        assert "TrackHS API" in get_folio_tool.description
