import pytest
from pydantic import ValidationError

async def test_search_units(mcp_client):
    """Test búsqueda de unidades"""
    result = await mcp_client.call_tool("search_units", {
        "page": 1,
        "size": 2
    })
    assert result is not None

async def test_search_units_validation():
    """Test validación de parámetros de búsqueda de unidades"""
    from src.trackhs_mcp.tools.units import SearchUnitsRequest
    
    # Test validación de campos numéricos
    with pytest.raises(ValidationError) as exc_info:
        SearchUnitsRequest(bedrooms="abc")  # No numérico
    assert "Debe ser un número válido" in str(exc_info.value)
    
    # Test validación de rango
    with pytest.raises(ValidationError) as exc_info:
        SearchUnitsRequest(bedrooms="25")  # Fuera de rango
    assert "Valor fuera del rango válido" in str(exc_info.value)
    
    # Test validación de lógica de negocio
    with pytest.raises(ValidationError) as exc_info:
        SearchUnitsRequest(bedrooms="2", bathrooms="0")  # Dormitorios sin baños
    assert "Unidades con dormitorios deben tener al menos 1 baño" in str(exc_info.value)

async def test_search_units_error_handling(mcp_client):
    """Test manejo de errores en búsqueda de unidades"""
    # Test con parámetros inválidos
    with pytest.raises(Exception):  # Puede ser ValidationError o API error
        await mcp_client.call_tool("search_units", {
            "page": 0,  # Página inválida
            "size": 0   # Tamaño inválido
        })
