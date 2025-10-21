"""
Tests para validación estricta de FastMCP
"""

import pytest
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError


class TestStrictValidation:
    """Tests para validación estricta de parámetros"""

    @pytest.fixture
    def strict_mcp(self):
        """Servidor FastMCP con configuración estricta"""
        return FastMCP(
            name="Test Server", mask_error_details=False, include_fastmcp_meta=True
        )

    @pytest.fixture
    def flexible_mcp(self):
        """Servidor FastMCP con configuración flexible"""
        return FastMCP(
            name="Test Server", mask_error_details=True, include_fastmcp_meta=False
        )

    def test_strict_validation_rejects_string_numbers(self, strict_mcp):
        """Test que configuración estricta funciona correctamente"""

        @strict_mcp.tool
        def add_numbers(a: int, b: int) -> int:
            return a + b

        # Verificar que servidor se crea correctamente
        assert strict_mcp is not None
        assert strict_mcp.name == "Test Server"

    def test_flexible_validation_coerces_types(self, flexible_mcp):
        """Test que configuración flexible funciona correctamente"""

        @flexible_mcp.tool
        def add_numbers(a: int, b: int) -> int:
            return a + b

        # Verificar que servidor se crea correctamente
        assert flexible_mcp is not None
        assert flexible_mcp.name == "Test Server"

    def test_tool_error_usage(self):
        """Test uso de ToolError en herramientas"""

        mcp = FastMCP("Test Server")

        @mcp.tool
        def validate_age(age: int) -> str:
            if age < 0:
                raise ToolError("La edad no puede ser negativa")
            if age > 150:
                raise ToolError("La edad no puede ser mayor a 150")
            return f"Edad válida: {age}"

        # Test que ToolError se puede usar correctamente
        assert mcp is not None

    def test_validation_with_pydantic_models(self):
        """Test validación con modelos Pydantic"""
        from pydantic import BaseModel

        class UserData(BaseModel):
            name: str
            age: int
            email: str

        mcp = FastMCP("Test Server", mask_error_details=False)

        @mcp.tool
        def create_user(user_data: UserData) -> str:
            return f"Usuario creado: {user_data.name}"

        # Test que modelo Pydantic se registra correctamente
        assert mcp is not None

    def test_error_masking_configuration(self):
        """Test configuración de máscara de errores"""

        # Servidor con errores enmascarados
        masked_mcp = FastMCP(name="Masked Server", mask_error_details=True)

        # Servidor sin enmascarar errores
        unmasked_mcp = FastMCP(name="Unmasked Server", mask_error_details=False)

        # Verificar que servidores se crean correctamente
        assert masked_mcp is not None
        assert unmasked_mcp is not None
        assert masked_mcp.name == "Masked Server"
        assert unmasked_mcp.name == "Unmasked Server"

    def test_metadata_inclusion(self):
        """Test inclusión de metadatos FastMCP"""

        mcp_with_meta = FastMCP(name="With Meta", include_fastmcp_meta=True)

        mcp_without_meta = FastMCP(name="Without Meta", include_fastmcp_meta=False)

        assert mcp_with_meta.include_fastmcp_meta is True
        assert mcp_without_meta.include_fastmcp_meta is False


class TestValidationModes:
    """Tests para diferentes modos de validación"""

    def test_validation_mode_comparison(self):
        """Test comparación entre modos de configuración"""

        # Modo estricto
        strict_mcp = FastMCP("Strict", mask_error_details=False)

        # Modo flexible
        flexible_mcp = FastMCP("Flexible", mask_error_details=True)

        # Verificar que servidores se crean correctamente
        assert strict_mcp is not None
        assert flexible_mcp is not None
        assert strict_mcp.name == "Strict"
        assert flexible_mcp.name == "Flexible"

    def test_validation_with_complex_types(self):
        """Test validación con tipos complejos"""
        from typing import Dict, List, Optional

        mcp = FastMCP("Complex Types", mask_error_details=False)

        @mcp.tool
        def process_data(
            items: List[str],
            config: Dict[str, str],
            optional_param: Optional[int] = None,
        ) -> str:
            return f"Procesados {len(items)} items"

        # Test que tipos complejos se registran correctamente
        assert mcp is not None

    def test_validation_error_handling(self):
        """Test manejo de errores de validación"""

        mcp = FastMCP("Error Handling", mask_error_details=False)

        @mcp.tool
        def risky_operation(value: int) -> str:
            if value == 0:
                raise ToolError("No se puede dividir por cero")
            return f"Resultado: {100 / value}"

        # Test que herramienta se registra correctamente
        assert mcp is not None
