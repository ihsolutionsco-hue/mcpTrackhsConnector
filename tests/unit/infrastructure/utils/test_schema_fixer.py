"""
Tests unitarios para schema_fixer utility
Implementando el patrón oficial de FastMCP para testing
"""

from typing import Any, Dict
from unittest.mock import MagicMock, patch

import pytest

from trackhs_mcp.infrastructure.utils.schema_fixer import (
    _fix_list_schemas,
    _is_numeric_string,
    compare_schemas,
    fix_and_validate_schema,
    fix_json_schema_types,
    validate_json_schema,
)


class TestSchemaFixer:
    """Tests para schema_fixer utility"""

    def test_fix_json_schema_types_basic_numeric_fields(self):
        """Test corrección de campos numéricos básicos"""
        # Arrange
        schema = {
            "type": "integer",
            "minimum": "0",
            "maximum": "100",
            "minLength": "1",
            "maxLength": "50",
        }

        # Act
        result = fix_json_schema_types(schema)

        # Assert
        assert result["minimum"] == 0
        assert result["maximum"] == 100
        assert result["minLength"] == 1
        assert result["maxLength"] == 50
        assert result["type"] == "integer"

    def test_fix_json_schema_types_float_values(self):
        """Test corrección de valores flotantes"""
        # Arrange
        schema = {"type": "number", "minimum": "0.5", "maximum": "99.9"}

        # Act
        result = fix_json_schema_types(schema)

        # Assert
        assert result["minimum"] == 0.5
        assert result["maximum"] == 99.9
        assert result["type"] == "number"

    def test_fix_json_schema_types_default_numeric(self):
        """Test corrección de valores default numéricos"""
        # Arrange
        schema = {"type": "integer", "default": "42"}

        # Act
        result = fix_json_schema_types(schema)

        # Assert
        assert result["default"] == 42
        assert result["type"] == "integer"

    def test_fix_json_schema_types_default_string(self):
        """Test que valores default no numéricos se mantengan como string"""
        # Arrange
        schema = {"type": "string", "default": "hello"}

        # Act
        result = fix_json_schema_types(schema)

        # Assert
        assert result["default"] == "hello"
        assert result["type"] == "string"

    def test_fix_json_schema_types_nested_objects(self):
        """Test corrección en objetos anidados"""
        # Arrange
        schema = {
            "type": "object",
            "properties": {
                "age": {"type": "integer", "minimum": "0", "maximum": "120"},
                "name": {"type": "string", "minLength": "1", "maxLength": "100"},
            },
        }

        # Act
        result = fix_json_schema_types(schema)

        # Assert
        assert result["properties"]["age"]["minimum"] == 0
        assert result["properties"]["age"]["maximum"] == 120
        assert result["properties"]["name"]["minLength"] == 1
        assert result["properties"]["name"]["maxLength"] == 100

    def test_fix_json_schema_types_arrays(self):
        """Test corrección en arrays"""
        # Arrange
        schema = {
            "type": "array",
            "items": {"type": "integer", "minimum": "0"},
            "minItems": "1",
            "maxItems": "10",
        }

        # Act
        result = fix_json_schema_types(schema)

        # Assert
        assert result["items"]["minimum"] == 0
        assert result["minItems"] == 1
        assert result["maxItems"] == 10

    def test_fix_json_schema_types_anyof_onof(self):
        """Test corrección en anyOf y oneOf"""
        # Arrange
        schema = {
            "anyOf": [
                {"type": "integer", "minimum": "0"},
                {"type": "string", "minLength": "1"},
            ]
        }

        # Act
        result = fix_json_schema_types(schema)

        # Assert
        assert result["anyOf"][0]["minimum"] == 0
        assert result["anyOf"][1]["minLength"] == 1

    def test_fix_json_schema_types_invalid_numeric_strings(self):
        """Test manejo de strings que no son números válidos"""
        # Arrange
        schema = {"type": "integer", "minimum": "invalid", "maximum": "also_invalid"}

        # Act
        result = fix_json_schema_types(schema)

        # Assert - Debe mantener los strings inválidos
        assert result["minimum"] == "invalid"
        assert result["maximum"] == "also_invalid"

    def test_fix_json_schema_types_non_dict_input(self):
        """Test manejo de entrada que no es diccionario"""
        # Arrange
        schema = "not a dict"

        # Act
        result = fix_json_schema_types(schema)

        # Assert
        assert result == "not a dict"

    def test_is_numeric_string_valid_integers(self):
        """Test detección de strings numéricos enteros"""
        # Arrange & Act & Assert
        assert _is_numeric_string("123") == True
        assert _is_numeric_string("0") == True
        assert _is_numeric_string("-42") == True

    def test_is_numeric_string_valid_floats(self):
        """Test detección de strings numéricos flotantes"""
        # Arrange & Act & Assert
        assert _is_numeric_string("123.45") == True
        assert _is_numeric_string("0.0") == True
        assert _is_numeric_string("-42.5") == True

    def test_is_numeric_string_invalid_strings(self):
        """Test detección de strings no numéricos"""
        # Arrange & Act & Assert
        assert _is_numeric_string("hello") == False
        assert _is_numeric_string("123abc") == False
        assert _is_numeric_string("") == False
        assert _is_numeric_string("12.34.56") == False

    def test_is_numeric_string_non_string_input(self):
        """Test detección con entrada que no es string"""
        # Arrange & Act & Assert
        assert _is_numeric_string(123) == False
        assert _is_numeric_string(None) == False
        assert _is_numeric_string([]) == False

    def test_fix_list_schemas_valid_list(self):
        """Test corrección de listas de esquemas"""
        # Arrange
        schema_list = [
            {"type": "integer", "minimum": "0"},
            {"type": "string", "minLength": "1"},
        ]

        # Act
        result = _fix_list_schemas(schema_list)

        # Assert
        assert result[0]["minimum"] == 0
        assert result[1]["minLength"] == 1

    def test_fix_list_schemas_nested_lists(self):
        """Test corrección de listas anidadas"""
        # Arrange
        schema_list = [[{"type": "integer", "minimum": "0"}]]

        # Act
        result = _fix_list_schemas(schema_list)

        # Assert
        assert result[0][0]["minimum"] == 0

    def test_fix_list_schemas_non_list_input(self):
        """Test manejo de entrada que no es lista"""
        # Arrange
        schema = {"type": "integer"}

        # Act
        result = _fix_list_schemas(schema)

        # Assert
        assert result == schema

    def test_validate_json_schema_valid_schema(self):
        """Test validación de esquema válido"""
        # Arrange
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string", "minLength": 1, "maxLength": 100},
                "age": {"type": "integer", "minimum": 0, "maximum": 120},
            },
            "required": ["name"],
        }

        # Act
        result = validate_json_schema(schema)

        # Assert
        assert result == True

    def test_validate_json_schema_invalid_type(self):
        """Test validación de esquema con tipo inválido"""
        # Arrange
        schema = {"type": "invalid_type"}

        # Act
        result = validate_json_schema(schema)

        # Assert
        assert result == False

    def test_validate_json_schema_invalid_constraints(self):
        """Test validación de esquema con constraints inválidos"""
        # Arrange
        schema = {"type": "integer", "minimum": "not_a_number"}

        # Act
        result = validate_json_schema(schema)

        # Assert
        assert result == False

    def test_validate_json_schema_non_dict_input(self):
        """Test validación de entrada que no es diccionario"""
        # Arrange
        schema = "not a dict"

        # Act
        result = validate_json_schema(schema)

        # Assert
        assert result == False

    def test_validate_json_schema_nested_invalid(self):
        """Test validación de esquema con objetos anidados inválidos"""
        # Arrange
        schema = {"type": "object", "properties": {"age": {"type": "invalid_type"}}}

        # Act
        result = validate_json_schema(schema)

        # Assert
        assert result == False

    @patch("trackhs_mcp.infrastructure.utils.schema_fixer.logger")
    def test_fix_and_validate_schema_success(self, mock_logger):
        """Test corrección y validación exitosa"""
        # Arrange
        schema = {"type": "integer", "minimum": "0", "maximum": "100"}

        # Act
        result = fix_and_validate_schema(schema)

        # Assert
        assert result["minimum"] == 0
        assert result["maximum"] == 100
        assert result["type"] == "integer"
        mock_logger.info.assert_called()

    @patch("trackhs_mcp.infrastructure.utils.schema_fixer.logger")
    def test_fix_and_validate_schema_validation_failure(self, mock_logger):
        """Test fallo en validación después de corrección"""
        # Arrange
        schema = {"type": "invalid_type", "minimum": "0"}

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid JSON schema after correction"):
            fix_and_validate_schema(schema)

        mock_logger.error.assert_called()

    def test_compare_schemas_no_changes(self):
        """Test comparación de esquemas sin cambios"""
        # Arrange
        original = {"type": "integer", "minimum": 0, "maximum": 100}
        fixed = {"type": "integer", "minimum": 0, "maximum": 100}

        # Act
        result = compare_schemas(original, fixed)

        # Assert
        assert result["total_changes"] == 0
        assert result["changes"] == []

    def test_compare_schemas_with_changes(self):
        """Test comparación de esquemas con cambios"""
        # Arrange
        original = {"type": "integer", "minimum": "0", "maximum": "100"}
        fixed = {"type": "integer", "minimum": 0, "maximum": 100}

        # Act
        result = compare_schemas(original, fixed)

        # Assert
        assert result["total_changes"] == 2
        assert len(result["changes"]) == 2
        # Verificar que los cambios contienen la información esperada
        change_paths = [change.get("path", "") for change in result["changes"]]
        assert "minimum" in change_paths
        assert "maximum" in change_paths

    def test_compare_schemas_nested_changes(self):
        """Test comparación de esquemas con cambios anidados"""
        # Arrange
        original = {
            "type": "object",
            "properties": {"age": {"type": "integer", "minimum": "0"}},
        }
        fixed = {
            "type": "object",
            "properties": {"age": {"type": "integer", "minimum": 0}},
        }

        # Act
        result = compare_schemas(original, fixed)

        # Assert
        assert result["total_changes"] == 1
        assert len(result["changes"]) == 1
        # Verificar que el cambio contiene la ruta esperada
        change = result["changes"][0]
        assert change.get("path") == "properties.age.minimum"

    def test_compare_schemas_added_fields(self):
        """Test comparación de esquemas con campos agregados"""
        # Arrange
        original = {"type": "integer"}
        fixed = {"type": "integer", "minimum": 0, "maximum": 100}

        # Act
        result = compare_schemas(original, fixed)

        # Assert
        assert result["total_changes"] == 2
        assert len(result["changes"]) == 2

    def test_compare_schemas_removed_fields(self):
        """Test comparación de esquemas con campos removidos"""
        # Arrange
        original = {"type": "integer", "minimum": 0, "maximum": 100}
        fixed = {"type": "integer"}

        # Act
        result = compare_schemas(original, fixed)

        # Assert
        assert result["total_changes"] == 2
        assert len(result["changes"]) == 2

    @patch("trackhs_mcp.infrastructure.utils.schema_fixer.logger")
    def test_fix_json_schema_types_with_logging(self, mock_logger):
        """Test que el logging funciona correctamente"""
        # Arrange
        schema = {"type": "integer", "minimum": "0"}

        # Act
        result = fix_json_schema_types(schema)

        # Assert
        assert result["minimum"] == 0
        mock_logger.debug.assert_called()

    @patch("trackhs_mcp.infrastructure.utils.schema_fixer.logger")
    def test_fix_json_schema_types_invalid_conversion_logging(self, mock_logger):
        """Test logging de conversiones inválidas"""
        # Arrange
        schema = {"type": "integer", "minimum": "invalid"}

        # Act
        result = fix_json_schema_types(schema)

        # Assert
        assert result["minimum"] == "invalid"
        mock_logger.warning.assert_called()

    def test_fix_json_schema_types_complex_schema(self):
        """Test corrección de esquema complejo"""
        # Arrange
        schema = {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "minimum": "1"},
                        "name": {
                            "type": "string",
                            "minLength": "1",
                            "maxLength": "100",
                        },
                    },
                },
                "items": {
                    "type": "array",
                    "items": {"type": "integer", "minimum": "0"},
                    "minItems": "1",
                    "maxItems": "10",
                },
            },
            "required": ["user"],
        }

        # Act
        result = fix_json_schema_types(schema)

        # Assert
        assert result["properties"]["user"]["properties"]["id"]["minimum"] == 1
        assert result["properties"]["user"]["properties"]["name"]["minLength"] == 1
        assert result["properties"]["user"]["properties"]["name"]["maxLength"] == 100
        assert result["properties"]["items"]["items"]["minimum"] == 0
        assert result["properties"]["items"]["minItems"] == 1
        assert result["properties"]["items"]["maxItems"] == 10
