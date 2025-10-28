#!/usr/bin/env python3
"""
Test para verificar que la corrección funciona
"""

from typing import Optional, Union

from pydantic import Field, ValidationError


def test_fixed_validation():
    """Test para verificar que la corrección funciona"""

    print("🧪 Probando validación corregida...")

    # Simular la definición corregida
    from pydantic import BaseModel

    class SearchUnitsFixed(BaseModel):
        bedrooms: Optional[Union[int, str]] = None
        is_active: Optional[Union[int, str]] = None
        is_bookable: Optional[Union[int, str]] = None

    print("\n1. Validación con parámetros int (como viene del cliente MCP):")
    try:
        model = SearchUnitsFixed(bedrooms=4, is_active=1, is_bookable=1)
        print(f"✅ Modelo creado exitosamente: {model}")
        print(f"   - bedrooms: {model.bedrooms} (type: {type(model.bedrooms)})")
        print(f"   - is_active: {model.is_active} (type: {type(model.is_active)})")
        print(
            f"   - is_bookable: {model.is_bookable} (type: {type(model.is_bookable)})"
        )
    except ValidationError as e:
        print(f"❌ Error de validación: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

    print("\n2. Validación con parámetros str:")
    try:
        model = SearchUnitsFixed(bedrooms="4", is_active="1", is_bookable="1")
        print(f"✅ Modelo creado exitosamente: {model}")
        print(f"   - bedrooms: {model.bedrooms} (type: {type(model.bedrooms)})")
        print(f"   - is_active: {model.is_active} (type: {type(model.is_active)})")
        print(
            f"   - is_bookable: {model.is_bookable} (type: {type(model.is_bookable)})"
        )
    except ValidationError as e:
        print(f"❌ Error de validación: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

    print("\n3. Validación con parámetros mixtos:")
    try:
        model = SearchUnitsFixed(bedrooms=4, is_active="1", is_bookable=0)
        print(f"✅ Modelo creado exitosamente: {model}")
        print(f"   - bedrooms: {model.bedrooms} (type: {type(model.bedrooms)})")
        print(f"   - is_active: {model.is_active} (type: {type(model.is_active)})")
        print(
            f"   - is_bookable: {model.is_bookable} (type: {type(model.is_bookable)})"
        )
    except ValidationError as e:
        print(f"❌ Error de validación: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    test_fixed_validation()
