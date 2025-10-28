#!/usr/bin/env python3
"""
Test profundo para verificar la validación de Pydantic con Annotated
"""

from typing import Optional, Union

from pydantic import BaseModel, Field, ValidationError
from typing_extensions import Annotated


def test_pydantic_validation_deep():
    """Test profundo de validación Pydantic con Annotated"""

    print("🔍 Test profundo de validación Pydantic...")

    # Simular exactamente la definición que tenemos ahora
    class SearchUnitsModel(BaseModel):
        bedrooms: Annotated[
            Optional[Union[int, str]],
            Field(ge=0, le=20, description="Número exacto de dormitorios"),
        ] = None
        is_active: Annotated[
            Optional[Union[int, str]],
            Field(
                ge=0,
                le=1,
                description="Filtrar por unidades activas (1) o inactivas (0)",
            ),
        ] = None
        is_bookable: Annotated[
            Optional[Union[int, str]],
            Field(
                ge=0,
                le=1,
                description="Filtrar por unidades disponibles para reservar (1) o no (0)",
            ),
        ] = None

    print("\n1. Test con parámetros int (como viene del cliente MCP):")
    try:
        model = SearchUnitsModel(bedrooms=4, is_active=1, is_bookable=1)
        print(f"✅ Modelo creado exitosamente: {model}")
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

    print("\n2. Test con parámetros str:")
    try:
        model = SearchUnitsModel(bedrooms="4", is_active="1", is_bookable="1")
        print(f"✅ Modelo creado exitosamente: {model}")
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

    print("\n3. Test con parámetros mixtos:")
    try:
        model = SearchUnitsModel(bedrooms=4, is_active="1", is_bookable=0)
        print(f"✅ Modelo creado exitosamente: {model}")
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

    # Test con valores fuera de rango para ver si la validación funciona
    print("\n4. Test con valores fuera de rango:")
    try:
        model = SearchUnitsModel(bedrooms=25, is_active=2, is_bookable=3)
        print(f"✅ Modelo creado (no debería): {model}")
    except ValidationError as e:
        print(f"✅ Error de validación esperado: {e}")
        print(f"   - Error details: {e.errors()}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    test_pydantic_validation_deep()
