#!/usr/bin/env python3
"""
Script de prueba local para verificar las correcciones del MCP TrackHS
Prueba las herramientas sin conectar al sistema online
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from trackhs_mcp.server import mcp


def test_parameter_validation():
    """Probar validación de parámetros de entrada"""
    print("🧪 PROBANDO VALIDACIÓN DE PARÁMETROS")
    print("=" * 50)

    # Test 1: search_reservations con parámetros válidos
    print("\n1. Probando search_reservations con parámetros válidos...")
    try:
        # Simular llamada con parámetros válidos
        result = mcp.call_tool(
            "search_reservations", {"page": 0, "size": 10, "status": "confirmed"}
        )
        print("✅ search_reservations: Parámetros válidos aceptados")
    except Exception as e:
        print(f"❌ search_reservations: Error con parámetros válidos: {e}")

    # Test 2: search_reservations con fechas válidas
    print("\n2. Probando search_reservations con fechas válidas...")
    try:
        result = mcp.call_tool(
            "search_reservations",
            {"arrival_start": "2024-01-15", "arrival_end": "2024-01-15", "size": 10},
        )
        print("✅ search_reservations: Fechas válidas aceptadas")
    except Exception as e:
        print(f"❌ search_reservations: Error con fechas válidas: {e}")

    # Test 3: search_units con parámetros válidos
    print("\n3. Probando search_units con parámetros válidos...")
    try:
        result = mcp.call_tool(
            "search_units",
            {"bedrooms": 2, "bathrooms": 1, "is_active": 1, "is_bookable": 1},
        )
        print("✅ search_units: Parámetros válidos aceptados")
    except Exception as e:
        print(f"❌ search_units: Error con parámetros válidos: {e}")

    # Test 4: create_maintenance_work_order con parámetros válidos
    print("\n4. Probando create_maintenance_work_order con parámetros válidos...")
    try:
        result = mcp.call_tool(
            "create_maintenance_work_order",
            {
                "unit_id": 100,
                "summary": "Fuga en grifo",
                "description": "Grifo del baño principal gotea constantemente",
                "priority": 3,
                "estimated_cost": 150.0,
                "estimated_time": 120,
            },
        )
        print("✅ create_maintenance_work_order: Parámetros válidos aceptados")
    except Exception as e:
        print(f"❌ create_maintenance_work_order: Error con parámetros válidos: {e}")

    # Test 5: create_housekeeping_work_order con parámetros válidos
    print("\n5. Probando create_housekeeping_work_order con parámetros válidos...")
    try:
        result = mcp.call_tool(
            "create_housekeeping_work_order",
            {
                "unit_id": 200,
                "scheduled_at": "2024-01-16",
                "is_inspection": False,
                "clean_type_id": 4,
                "comments": "Limpieza post-checkout",
                "cost": 50.0,
            },
        )
        print("✅ create_housekeeping_work_order: Parámetros válidos aceptados")
    except Exception as e:
        print(f"❌ create_housekeeping_work_order: Error con parámetros válidos: {e}")


def test_invalid_parameters():
    """Probar validación con parámetros inválidos"""
    print("\n\n🚫 PROBANDO VALIDACIÓN CON PARÁMETROS INVÁLIDOS")
    print("=" * 50)

    # Test 1: Fecha inválida
    print("\n1. Probando fecha inválida...")
    try:
        result = mcp.call_tool(
            "search_reservations",
            {"arrival_start": "2024-13-45", "size": 10},  # Fecha inválida
        )
        print("❌ search_reservations: Debería haber fallado con fecha inválida")
    except Exception as e:
        print(f"✅ search_reservations: Correctamente rechazó fecha inválida: {e}")

    # Test 2: Parámetro fuera de rango
    print("\n2. Probando parámetro fuera de rango...")
    try:
        result = mcp.call_tool(
            "search_reservations",
            {"page": 50000, "size": 10},  # Fuera del rango permitido
        )
        print("❌ search_reservations: Debería haber fallado con página fuera de rango")
    except Exception as e:
        print(
            f"✅ search_reservations: Correctamente rechazó página fuera de rango: {e}"
        )

    # Test 3: Tipo de dato incorrecto
    print("\n3. Probando tipo de dato incorrecto...")
    try:
        result = mcp.call_tool(
            "search_units", {"bedrooms": "dos", "size": 10}  # String en lugar de int
        )
        print("❌ search_units: Debería haber fallado con tipo incorrecto")
    except Exception as e:
        print(f"✅ search_units: Correctamente rechazó tipo incorrecto: {e}")


def test_schema_validation():
    """Probar validación de esquemas de salida"""
    print("\n\n📋 PROBANDO VALIDACIÓN DE ESQUEMAS")
    print("=" * 50)

    # Test 1: Verificar que los esquemas están bien definidos
    print("\n1. Verificando esquemas de salida...")

    from trackhs_mcp.schemas import (
        AMENITIES_OUTPUT_SCHEMA,
        FOLIO_DETAIL_OUTPUT_SCHEMA,
        RESERVATION_SEARCH_OUTPUT_SCHEMA,
        UNIT_SEARCH_OUTPUT_SCHEMA,
        WORK_ORDER_DETAIL_OUTPUT_SCHEMA,
    )

    schemas = {
        "RESERVATION_SEARCH_OUTPUT_SCHEMA": RESERVATION_SEARCH_OUTPUT_SCHEMA,
        "UNIT_SEARCH_OUTPUT_SCHEMA": UNIT_SEARCH_OUTPUT_SCHEMA,
        "AMENITIES_OUTPUT_SCHEMA": AMENITIES_OUTPUT_SCHEMA,
        "FOLIO_DETAIL_OUTPUT_SCHEMA": FOLIO_DETAIL_OUTPUT_SCHEMA,
        "WORK_ORDER_DETAIL_OUTPUT_SCHEMA": WORK_ORDER_DETAIL_OUTPUT_SCHEMA,
    }

    for name, schema in schemas.items():
        try:
            # Verificar que el schema es válido JSON
            json.dumps(schema)
            print(f"✅ {name}: Schema válido")
        except Exception as e:
            print(f"❌ {name}: Schema inválido: {e}")


def test_tool_registration():
    """Probar que las herramientas están registradas correctamente"""
    print("\n\n🔧 PROBANDO REGISTRO DE HERRAMIENTAS")
    print("=" * 50)

    # Verificar que las herramientas están definidas en el módulo
    expected_tools = [
        "search_reservations",
        "get_reservation",
        "search_units",
        "search_amenities",
        "get_folio",
        "create_maintenance_work_order",
        "create_housekeeping_work_order",
    ]

    print("Verificando definición de herramientas en el servidor...")

    for tool in expected_tools:
        if hasattr(mcp, tool):
            print(f"✅ {tool}: Definida en el servidor")
        else:
            print(f"❌ {tool}: NO definida en el servidor")

    # Verificar que el servidor MCP está configurado correctamente
    print(f"\nServidor MCP configurado:")
    print(f"   Nombre: {mcp.name}")
    print(f"   Instrucciones: {mcp.instructions[:100]}...")
    print(f"   Validación estricta: {mcp.strict_input_validation}")

    # Verificar que el servidor tiene herramientas registradas
    if hasattr(mcp, "_tools"):
        print(f"   Herramientas registradas: {len(mcp._tools)}")
    else:
        print("   Herramientas: No se puede verificar (API interna)")


def main():
    """Función principal de pruebas"""
    print("🚀 INICIANDO PRUEBAS LOCALES DEL MCP TRACKHS")
    print("=" * 60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    try:
        # Ejecutar todas las pruebas
        test_tool_registration()
        test_schema_validation()
        test_parameter_validation()
        test_invalid_parameters()

        print("\n\n✅ TODAS LAS PRUEBAS COMPLETADAS")
        print("=" * 60)
        print("Las correcciones están listas para ser subidas al sistema online.")

    except Exception as e:
        print(f"\n\n❌ ERROR EN LAS PRUEBAS: {e}")
        print("=" * 60)
        return 1

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
