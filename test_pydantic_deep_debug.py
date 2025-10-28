#!/usr/bin/env python3
"""
Test profundo para debuggear el problema de validación de Pydantic
"""

from typing import Optional, Union

from pydantic import BaseModel, Field, ValidationError


def test_pydantic_deep_debug():
    """Debug profundo del problema de validación"""

    print("🔍 Debug profundo de validación Pydantic...")

    # Simular exactamente la definición actual
    class SearchUnitsModel(BaseModel):
        bedrooms: Optional[Union[int, str]] = None
        is_active: Optional[Union[int, str]] = None
        is_bookable: Optional[Union[int, str]] = None

    print("\n1. Test con parámetros int (como viene del cliente MCP):")
    try:
        model = SearchUnitsModel(bedrooms=4, is_active=1, is_bookable=1)
        print(f"✅ Modelo creado: {model}")
        print(f"   - bedrooms: {model.bedrooms} (type: {type(model.bedrooms)})")
        print(f"   - is_active: {model.is_active} (type: {type(model.is_active)})")
        print(
            f"   - is_bookable: {model.is_bookable} (type: {type(model.is_bookable)})"
        )
    except ValidationError as e:
        print(f"❌ Error de validación: {e}")
        print(f"   - Error details: {e.errors()}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

    # Test con Annotated y Field (como debería estar según el reporte)
    from pydantic import Annotated

    class SearchUnitsModelWithField(BaseModel):
        bedrooms: Annotated[Optional[Union[int, str]], Field(ge=0, le=20)] = None
        is_active: Annotated[Optional[Union[int, str]], Field(ge=0, le=1)] = None
        is_bookable: Annotated[Optional[Union[int, str]], Field(ge=0, le=1)] = None

    print("\n2. Test con Annotated y Field (como en el reporte):")
    try:
        model = SearchUnitsModelWithField(bedrooms=4, is_active=1, is_bookable=1)
        print(f"✅ Modelo creado: {model}")
        print(f"   - bedrooms: {model.bedrooms} (type: {type(model.bedrooms)})")
        print(f"   - is_active: {model.is_active} (type: {type(model.is_active)})")
        print(
            f"   - is_bookable: {model.is_bookable} (type: {type(model.is_bookable)})"
        )
    except ValidationError as e:
        print(f"❌ Error de validación: {e}")
        print(f"   - Error details: {e.errors()}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

    # Test con validación estricta (como puede estar en MCP)
    class SearchUnitsModelStrict(BaseModel):
        bedrooms: Optional[int] = None
        is_active: Optional[int] = None
        is_bookable: Optional[int] = None

    print("\n3. Test con validación estricta (int only):")
    try:
        model = SearchUnitsModelStrict(bedrooms=4, is_active=1, is_bookable=1)
        print(f"✅ Modelo creado: {model}")
    except ValidationError as e:
        print(f"❌ Error de validación: {e}")
        print(f"   - Error details: {e.errors()}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

    print("\n4. Test con validación estricta y parámetros str:")
    try:
        model = SearchUnitsModelStrict(bedrooms="4", is_active="1", is_bookable="1")
        print(f"✅ Modelo creado: {model}")
    except ValidationError as e:
        print(f"❌ Error de validación: {e}")
        print(f"   - Error details: {e.errors()}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    test_pydantic_deep_debug()
