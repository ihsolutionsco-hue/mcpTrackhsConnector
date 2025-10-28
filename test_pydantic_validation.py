#!/usr/bin/env python3
"""
Test para verificar el problema de validación de Pydantic en search_units
"""

from typing import Optional, Union

from pydantic import Field, ValidationError
from pydantic.functional_validators import BeforeValidator


def test_pydantic_validation():
    """Test para demostrar el problema de validación de Pydantic"""

    print("🧪 Probando validación de Pydantic...")

    # Simular la definición actual (problemática)
    from pydantic import BaseModel

    class SearchUnitsCurrent(BaseModel):
        bedrooms: Optional[str] = None
        is_active: Optional[str] = None
        is_bookable: Optional[str] = None

    class SearchUnitsFixed(BaseModel):
        bedrooms: Optional[Union[int, str]] = None
        is_active: Optional[Union[int, str]] = None
        is_bookable: Optional[Union[int, str]] = None

    print("\n1. Validación con definición actual (str) y parámetros int:")
    try:
        model = SearchUnitsCurrent(bedrooms=4, is_active=1, is_bookable=1)
        print(f"✅ Modelo creado: {model}")
    except ValidationError as e:
        print(f"❌ Error de validación: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

    print("\n2. Validación con definición actual (str) y parámetros str:")
    try:
        model = SearchUnitsCurrent(bedrooms="4", is_active="1", is_bookable="1")
        print(f"✅ Modelo creado: {model}")
    except ValidationError as e:
        print(f"❌ Error de validación: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

    print(
        "\n3. Validación con definición corregida (Union[int, str]) y parámetros int:"
    )
    try:
        model = SearchUnitsFixed(bedrooms=4, is_active=1, is_bookable=1)
        print(f"✅ Modelo creado: {model}")
    except ValidationError as e:
        print(f"❌ Error de validación: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

    print(
        "\n4. Validación con definición corregida (Union[int, str]) y parámetros str:"
    )
    try:
        model = SearchUnitsFixed(bedrooms="4", is_active="1", is_bookable="1")
        print(f"✅ Modelo creado: {model}")
    except ValidationError as e:
        print(f"❌ Error de validación: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    test_pydantic_validation()
