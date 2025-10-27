#!/usr/bin/env python3
"""
Test Simple de Correcciones - TrackHS MCP Server
Verifica que las correcciones de validación funcionen correctamente
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Configurar variables de entorno para testing
os.environ.setdefault("TRACKHS_USERNAME", "test_user")
os.environ.setdefault("TRACKHS_PASSWORD", "test_password")
os.environ.setdefault("TRACKHS_API_URL", "https://ihmvacations.trackhs.com/api")


def test_type_conversion():
    """Test de conversión de tipos de datos"""
    print("🧪 TESTING CONVERSIÓN DE TIPOS DE DATOS")
    print("=" * 50)

    # Importar las funciones de conversión
    from trackhs_mcp.server import (
        create_housekeeping_work_order,
        create_maintenance_work_order,
        search_amenities,
        search_units,
    )

    # Test 1: Conversión de strings a enteros
    print("\n1. Testing conversión de strings a enteros...")
    try:
        # Esto debería funcionar ahora con la conversión de tipos
        result = search_units(bedrooms="2", bathrooms="1", size=3)
        if result and "_embedded" in result:
            print("✅ search_units con parámetros string: FUNCIONA")
        else:
            print("❌ search_units con parámetros string: FALLA")
    except Exception as e:
        print(f"❌ search_units con parámetros string: ERROR - {e}")

    # Test 2: Conversión de strings a booleanos
    print("\n2. Testing conversión de strings a booleanos...")
    try:
        result = search_units(is_active="1", is_bookable="true", size=3)
        if result and "_embedded" in result:
            print("✅ search_units con booleanos string: FUNCIONA")
        else:
            print("❌ search_units con booleanos string: FALLA")
    except Exception as e:
        print(f"❌ search_units con booleanos string: ERROR - {e}")

    # Test 3: Esquema de amenidades flexible
    print("\n3. Testing esquema de amenidades flexible...")
    try:
        result = search_amenities(size=3)
        if result and "_embedded" in result:
            print("✅ search_amenities: FUNCIONA")
        else:
            print("❌ search_amenities: FALLA")
    except Exception as e:
        print(f"❌ search_amenities: ERROR - {e}")

    # Test 4: Conversión de costos y tiempos
    print("\n4. Testing conversión de costos y tiempos...")
    try:
        result = create_maintenance_work_order(
            unit_id=75,
            summary="Test de conversión",
            description="Verificar conversión de tipos",
            priority=3,
            estimated_cost="150.50",  # String
            estimated_time="120",  # String
        )
        if result and "id" in result:
            print("✅ create_maintenance_work_order con strings: FUNCIONA")
        else:
            print("❌ create_maintenance_work_order con strings: FALLA")
    except Exception as e:
        print(f"❌ create_maintenance_work_order con strings: ERROR - {e}")

    # Test 5: Conversión en housekeeping
    print("\n5. Testing conversión en housekeeping...")
    try:
        result = create_housekeeping_work_order(
            unit_id=75,
            scheduled_at="2024-01-15",
            is_inspection=False,
            clean_type_id="1",  # String
            cost="80.00",  # String
        )
        if result and "id" in result:
            print("✅ create_housekeeping_work_order con strings: FUNCIONA")
        else:
            print("❌ create_housekeeping_work_order con strings: FALLA")
    except Exception as e:
        print(f"❌ create_housekeeping_work_order con strings: ERROR - {e}")


def test_parameter_validation():
    """Test de validación de parámetros"""
    print("\n🔍 TESTING VALIDACIÓN DE PARÁMETROS")
    print("=" * 50)

    from trackhs_mcp.server import search_units

    # Test con diferentes tipos de parámetros
    test_cases = [
        {
            "name": "Parámetros normales (int/bool)",
            "params": {
                "bedrooms": 2,
                "bathrooms": 1,
                "is_active": True,
                "is_bookable": True,
                "size": 3,
            },
        },
        {
            "name": "Parámetros string",
            "params": {
                "bedrooms": "2",
                "bathrooms": "1",
                "is_active": "1",
                "is_bookable": "true",
                "size": 3,
            },
        },
        {
            "name": "Parámetros mixtos",
            "params": {
                "bedrooms": 2,
                "bathrooms": "1",
                "is_active": "true",
                "is_bookable": True,
                "size": 3,
            },
        },
        {
            "name": "Parámetros None",
            "params": {
                "bedrooms": None,
                "bathrooms": None,
                "is_active": None,
                "is_bookable": None,
                "size": 3,
            },
        },
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}...")
        try:
            result = search_units(**test_case["params"])
            if result and "_embedded" in result:
                print(f"✅ {test_case['name']}: FUNCIONA")
            else:
                print(f"❌ {test_case['name']}: FALLA - Sin datos")
        except Exception as e:
            print(f"❌ {test_case['name']}: ERROR - {e}")


def test_schema_flexibility():
    """Test de flexibilidad de esquemas"""
    print("\n📋 TESTING FLEXIBILIDAD DE ESQUEMAS")
    print("=" * 50)

    from trackhs_mcp.server import search_amenities

    try:
        result = search_amenities(size=5)
        if result and "_embedded" in result and "amenities" in result["_embedded"]:
            amenities = result["_embedded"]["amenities"]
            print(f"✅ Amenidades obtenidas: {len(amenities)}")

            # Verificar que los campos problemáticos se manejen correctamente
            for amenity in amenities[:3]:  # Solo las primeras 3
                name = amenity.get("name", "N/A")
                group = amenity.get("group", "N/A")
                print(f"  - {name} ({group})")

            print("✅ Esquema de amenidades flexible: FUNCIONA")
        else:
            print("❌ Esquema de amenidades flexible: FALLA")
    except Exception as e:
        print(f"❌ Esquema de amenidades flexible: ERROR - {e}")


def main():
    """Función principal de testing"""
    print("🚀 INICIANDO TEST SIMPLE DE CORRECCIONES")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)

    # Ejecutar tests
    test_type_conversion()
    test_parameter_validation()
    test_schema_flexibility()

    print("\n" + "=" * 60)
    print("✅ TESTING COMPLETADO")
    print("=" * 60)

    # Guardar resumen
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary = {
        "timestamp": datetime.now().isoformat(),
        "tests_run": ["type_conversion", "parameter_validation", "schema_flexibility"],
        "status": "completed",
    }

    with open(f"test_simple_results_{timestamp}.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"📄 Resumen guardado en: test_simple_results_{timestamp}.json")


if __name__ == "__main__":
    main()
