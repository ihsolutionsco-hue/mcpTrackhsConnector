"""
Tests específicos para validar las correcciones de filtros de fecha
"""

import pytest
from src.trackhs_mcp.tools.search_reservations import _normalize_date_format, _is_valid_date_format


class TestDateFiltersFix:
    """Tests para validar las correcciones de filtros de fecha"""
    
    def test_normalize_date_format_solo_fecha(self):
        """Test normalización de fecha solo (YYYY-MM-DD)"""
        # Solo fecha
        result = _normalize_date_format("2025-01-01")
        assert result == "2025-01-01T00:00:00Z"
        
        result = _normalize_date_format("2024-12-31")
        assert result == "2024-12-31T00:00:00Z"
    
    def test_normalize_date_format_con_tiempo_sin_timezone(self):
        """Test normalización de fecha con tiempo sin timezone"""
        # Fecha con tiempo sin timezone
        result = _normalize_date_format("2025-01-01T00:00:00")
        assert result == "2025-01-01T00:00:00Z"
        
        result = _normalize_date_format("2025-01-01T23:59:59")
        assert result == "2025-01-01T23:59:59Z"
    
    def test_normalize_date_format_ya_normalizado(self):
        """Test que fechas ya normalizadas no cambien"""
        # Ya tiene timezone Z
        result = _normalize_date_format("2025-01-01T00:00:00Z")
        assert result == "2025-01-01T00:00:00Z"
        
        # Ya tiene timezone offset
        result = _normalize_date_format("2025-01-01T00:00:00+00:00")
        assert result == "2025-01-01T00:00:00+00:00"
    
    def test_is_valid_date_format_solo_fecha(self):
        """Test validación de formato solo fecha"""
        # Solo fecha válida
        assert _is_valid_date_format("2025-01-01") == True
        assert _is_valid_date_format("2024-12-31") == True
        
        # Solo fecha inválida
        assert _is_valid_date_format("2025/01/01") == False
        assert _is_valid_date_format("01-01-2025") == False
    
    def test_is_valid_date_format_con_tiempo(self):
        """Test validación de formato con tiempo"""
        # Con timezone Z
        assert _is_valid_date_format("2025-01-01T00:00:00Z") == True
        assert _is_valid_date_format("2025-01-01T23:59:59Z") == True
        
        # Con timezone offset
        assert _is_valid_date_format("2025-01-01T00:00:00+00:00") == True
        assert _is_valid_date_format("2025-01-01T00:00:00-05:00") == True
        
        # Sin timezone
        assert _is_valid_date_format("2025-01-01T00:00:00") == True
        assert _is_valid_date_format("2025-01-01T23:59:59") == True
    
    def test_is_valid_date_format_con_microsegundos(self):
        """Test validación de formato con microsegundos"""
        # Con microsegundos
        assert _is_valid_date_format("2025-01-01T00:00:00.123Z") == True
        assert _is_valid_date_format("2025-01-01T00:00:00.123456Z") == True
        
        # Con microsegundos y timezone offset
        assert _is_valid_date_format("2025-01-01T00:00:00.123+00:00") == True
    
    def test_is_valid_date_format_formato_espacio(self):
        """Test validación de formato con espacio"""
        # Formato con espacio
        assert _is_valid_date_format("2025-01-01 00:00:00") == True
        assert _is_valid_date_format("2025-01-01 23:59:59") == True
    
    def test_is_valid_date_format_invalidos(self):
        """Test validación de formatos inválidos"""
        # Formatos inválidos
        assert _is_valid_date_format("2025/01/01") == False
        assert _is_valid_date_format("01-01-2025") == False
        assert _is_valid_date_format("2025-1-1") == False
        assert _is_valid_date_format("invalid-date") == False
        assert _is_valid_date_format("") == False
    
    def test_normalize_date_format_edge_cases(self):
        """Test casos edge de normalización"""
        # Fecha con microsegundos
        result = _normalize_date_format("2025-01-01T00:00:00.123")
        assert result == "2025-01-01T00:00:00.123Z"
        
        # Fecha con microsegundos y timezone
        result = _normalize_date_format("2025-01-01T00:00:00.123Z")
        assert result == "2025-01-01T00:00:00.123Z"
    
    def test_normalize_date_format_error_handling(self):
        """Test manejo de errores en normalización"""
        # String inválido
        result = _normalize_date_format("invalid-date")
        assert result == "invalid-date"  # Debe devolver el original
        
        # String vacío
        result = _normalize_date_format("")
        assert result == ""
    
    def test_date_validation_comprehensive(self):
        """Test comprehensivo de validación de fechas"""
        # Casos válidos
        valid_dates = [
            "2025-01-01",
            "2025-01-01T00:00:00",
            "2025-01-01T00:00:00Z",
            "2025-01-01T00:00:00+00:00",
            "2025-01-01T00:00:00-05:00",
            "2025-01-01T00:00:00.123Z",
            "2025-01-01T00:00:00.123456Z",
            "2025-01-01 00:00:00"
        ]
        
        for date in valid_dates:
            assert _is_valid_date_format(date) == True, f"Fecha válida falló: {date}"
        
        # Casos inválidos
        invalid_dates = [
            "2025/01/01",
            "01-01-2025",
            "2025-1-1",
            "invalid-date",
            "",
            "2025-01-01T",
            "2025-01-01T00:00:00X"
        ]
        
        for date in invalid_dates:
            assert _is_valid_date_format(date) == False, f"Fecha inválida pasó: {date}"


if __name__ == "__main__":
    pytest.main([__file__])
