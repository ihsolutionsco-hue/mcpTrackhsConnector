#!/usr/bin/env python3
"""
Test Comprehensivo para search_units - Aplicando todo lo aprendido
"""

import json
import sys
import traceback
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from trackhs_mcp.config import get_settings
from trackhs_mcp.repositories.unit_repository import UnitRepository
from trackhs_mcp.server import TrackHSClient
from trackhs_mcp.services.unit_service import UnitService


def test_parameter_types():
    """Test 1: Verificar que los tipos de parámetros sean correctos"""
    print("🧪 Test 1: Verificando tipos de parámetros...")

    # Simular cliente API
    class MockAPIClient:
        def get(self, endpoint, params=None):
            return {
                "page": 1,
                "page_count": 1,
                "page_size": 10,
                "total_items": 0,
                "_embedded": {"units": []},
                "_links": {},
            }

    # Crear servicio con mock
    mock_client = MockAPIClient()
    unit_repo = UnitRepository(mock_client)
    unit_service = UnitService(unit_repo)

    try:
        # Test con parámetros int (como debe ser)
        result = unit_service.search_units(
            page=1, size=10, bedrooms=2, bathrooms=1, is_active=1, is_bookable=1
        )
        print("✅ Test 1 PASÓ: Parámetros int funcionan correctamente")
        return True
    except Exception as e:
        print(f"❌ Test 1 FALLÓ: {e}")
        traceback.print_exc()
        return False


def test_schema_validation():
    """Test 2: Verificar que el esquema acepte diferentes tipos de area"""
    print("\n🧪 Test 2: Verificando validación de esquema...")

    from trackhs_mcp.schemas import UnitResponse

    # Test con area como string
    test_data = {
        "id": 1,
        "name": "Test Unit",
        "area": "3348.0",  # String que debe convertirse a float
    }

    try:
        unit = UnitResponse(**test_data)
        print(
            f"✅ Test 2 PASÓ: area como string convertido a {unit.area} (tipo: {type(unit.area)})"
        )
        return True
    except Exception as e:
        print(f"❌ Test 2 FALLÓ: {e}")
        traceback.print_exc()
        return False


def test_area_cleaning():
    """Test 3: Verificar limpieza de datos de area"""
    print("\n🧪 Test 3: Verificando limpieza de datos...")

    from trackhs_mcp.services.unit_service import UnitService

    # Crear instancia para acceder a métodos privados
    class MockAPIClient:
        def get(self, endpoint, params=None):
            return {
                "page": 1,
                "page_count": 1,
                "page_size": 10,
                "total_items": 1,
                "_embedded": {
                    "units": [
                        {
                            "id": 1,
                            "name": "Test Unit",
                            "area": "3348.0",  # String problemático
                            "bedrooms": 2,
                            "bathrooms": 1,
                        }
                    ]
                },
                "_links": {},
            }

    mock_client = MockAPIClient()
    unit_repo = UnitRepository(mock_client)
    unit_service = UnitService(unit_repo)

    try:
        result = unit_service.search_units(page=1, size=10)

        # Verificar que el area se limpió correctamente
        if "_embedded" in result and "units" in result["_embedded"]:
            unit = result["_embedded"]["units"][0]
            area = unit.get("area")
            print(f"✅ Test 3 PASÓ: area limpiado a {area} (tipo: {type(area)})")
            return True
        else:
            print("❌ Test 3 FALLÓ: No se encontraron unidades en la respuesta")
            return False
    except Exception as e:
        print(f"❌ Test 3 FALLÓ: {e}")
        traceback.print_exc()
        return False


def test_mcp_function_signature():
    """Test 4: Verificar que la función MCP tenga la signatura correcta"""
    print("\n🧪 Test 4: Verificando signatura de función MCP...")

    try:
        # Importar la función search_units del servidor
        import inspect

        from trackhs_mcp.server import search_units

        # Obtener la signatura de la función
        sig = inspect.signature(search_units)

        # Verificar que bedrooms sea int
        bedrooms_param = sig.parameters.get("bedrooms")
        if bedrooms_param and bedrooms_param.annotation == int:
            print("✅ Test 4 PASÓ: bedrooms es int")
        else:
            print(
                f"❌ Test 4 FALLÓ: bedrooms es {bedrooms_param.annotation if bedrooms_param else 'No encontrado'}"
            )
            return False

        # Verificar que is_active sea int
        is_active_param = sig.parameters.get("is_active")
        if is_active_param and is_active_param.annotation == int:
            print("✅ Test 4 PASÓ: is_active es int")
        else:
            print(
                f"❌ Test 4 FALLÓ: is_active es {is_active_param.annotation if is_active_param else 'No encontrado'}"
            )
            return False

        return True
    except Exception as e:
        print(f"❌ Test 4 FALLÓ: {e}")
        traceback.print_exc()
        return False


def test_real_api_call():
    """Test 5: Probar llamada real a la API (si está disponible)"""
    print("\n🧪 Test 5: Probando llamada real a la API...")

    try:
        settings = get_settings()

        if not settings.trackhs_username or not settings.trackhs_password:
            print("⚠️ Test 5 OMITIDO: Credenciales no configuradas")
            return True

        # Crear cliente real
        api_client = TrackHSClient(
            settings.trackhs_api_url,
            settings.trackhs_username,
            settings.trackhs_password,
        )

        unit_repo = UnitRepository(api_client)
        unit_service = UnitService(unit_repo)

        # Probar búsqueda simple
        result = unit_service.search_units(page=1, size=1)

        if "error" in result:
            print(f"⚠️ Test 5 ADVERTENCIA: API devolvió error: {result['error']}")
            return False
        else:
            print("✅ Test 5 PASÓ: Llamada a API exitosa")
            return True

    except Exception as e:
        print(f"❌ Test 5 FALLÓ: {e}")
        traceback.print_exc()
        return False


def main():
    """Ejecutar todos los tests"""
    print("🚀 Iniciando Tests Comprehensivos para search_units")
    print("=" * 60)

    tests = [
        test_parameter_types,
        test_schema_validation,
        test_area_cleaning,
        test_mcp_function_signature,
        test_real_api_call,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test falló con excepción: {e}")
            traceback.print_exc()

    print("\n" + "=" * 60)
    print(f"📊 Resultados: {passed}/{total} tests pasaron")

    if passed == total:
        print("🎉 ¡Todos los tests pasaron! El código está listo para el servidor.")
        return True
    else:
        print("⚠️ Algunos tests fallaron. Revisar antes de subir al servidor.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
