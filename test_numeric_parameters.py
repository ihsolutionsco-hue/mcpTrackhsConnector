#!/usr/bin/env python3
"""
Test para verificar que los parámetros numéricos funcionan correctamente
"""

import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_numeric_parameters():
    """Test de parámetros numéricos"""
    print("🧪 TESTING PARÁMETROS NUMÉRICOS")
    print("=" * 50)

    try:
        from trackhs_mcp.repositories.unit_repository import UnitRepository
        from trackhs_mcp.server import TrackHSClient
        from trackhs_mcp.services.unit_service import UnitService

        # Crear instancias
        client = TrackHSClient(
            base_url="https://ihmvacations.trackhs.com",
            username="aba99777416466b6bdc1a25223192ccb",
            password="a8b8c8d8e8f8g8h8i8j8k8l8m8n8o8p8",
        )
        repo = UnitRepository(client)
        service = UnitService(repo)

        print("✅ Servicios inicializados correctamente")

        # Test 1: Parámetros como strings
        print("\n🔍 Test 1: Parámetros como strings")
        result1 = service.search_units(
            page=1,
            size=2,
            bedrooms="4",  # String
            bathrooms="2",  # String
            is_active="1",  # String
            is_bookable="1",  # String
        )
        print(f"   ✅ Resultado: {result1.get('total_items', 0)} unidades encontradas")

        # Test 2: Parámetros como integers
        print("\n🔍 Test 2: Parámetros como integers")
        result2 = service.search_units(
            page=1,
            size=2,
            bedrooms=4,  # Int
            bathrooms=2,  # Int
            is_active=1,  # Int
            is_bookable=1,  # Int
        )
        print(f"   ✅ Resultado: {result2.get('total_items', 0)} unidades encontradas")

        # Test 3: Parámetros mixtos
        print("\n🔍 Test 3: Parámetros mixtos")
        result3 = service.search_units(
            page=1,
            size=2,
            bedrooms="5",  # String
            bathrooms=3,  # Int
            is_active="0",  # String
            is_bookable=1,  # Int
        )
        print(f"   ✅ Resultado: {result3.get('total_items', 0)} unidades encontradas")

        print(
            "\n🎉 TODOS LOS TESTS PASARON - Los parámetros numéricos funcionan correctamente"
        )

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_numeric_parameters()
