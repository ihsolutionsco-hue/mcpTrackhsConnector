#!/usr/bin/env python3
"""
Test para verificar el problema de validación de parámetros en search_units
"""

from typing import Optional, Union

from pydantic import Field


def test_parameter_validation():
    """Test para demostrar el problema de validación de tipos"""

    print("🧪 Probando validación de parámetros...")

    # Simular la definición actual (problemática)
    def search_units_current(
        bedrooms: Optional[str] = None,
        is_active: Optional[str] = None,
        is_bookable: Optional[str] = None,
    ):
        print(f"bedrooms: {bedrooms} (type: {type(bedrooms)})")
        print(f"is_active: {is_active} (type: {type(is_active)})")
        print(f"is_bookable: {is_bookable} (type: {type(is_bookable)})")
        return "OK"

    # Simular la definición corregida
    def search_units_fixed(
        bedrooms: Optional[Union[int, str]] = None,
        is_active: Optional[Union[int, str]] = None,
        is_bookable: Optional[Union[int, str]] = None,
    ):
        print(f"bedrooms: {bedrooms} (type: {type(bedrooms)})")
        print(f"is_active: {is_active} (type: {type(is_active)})")
        print(f"is_bookable: {is_bookable} (type: {type(is_bookable)})")
        return "OK"

    print("\n1. Llamada con parámetros int (como viene del cliente MCP):")
    try:
        result = search_units_current(bedrooms=4, is_active=1, is_bookable=1)
        print(f"✅ Resultado: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n2. Llamada con parámetros str:")
    try:
        result = search_units_current(bedrooms="4", is_active="1", is_bookable="1")
        print(f"✅ Resultado: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n3. Llamada con definición corregida (int):")
    try:
        result = search_units_fixed(bedrooms=4, is_active=1, is_bookable=1)
        print(f"✅ Resultado: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n4. Llamada con definición corregida (str):")
    try:
        result = search_units_fixed(bedrooms="4", is_active="1", is_bookable="1")
        print(f"✅ Resultado: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    test_parameter_validation()
