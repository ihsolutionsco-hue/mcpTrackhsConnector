#!/usr/bin/env python3
"""
Test simple para verificar que los tipos en search_units están corregidos
"""

import sys
from pathlib import Path

# Agregar el directorio src al PYTHONPATH
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))


def test_search_units_types():
    """Verificar que los tipos en search_units están corregidos"""

    print("🔧 Verificando tipos en search_units...")

    try:
        # Importar el módulo
        from trackhs_mcp.infrastructure.mcp.search_units import register_search_units

        print("✅ Módulo search_units importado correctamente")

        # Verificar que la función register_search_units existe
        if callable(register_search_units):
            print("✅ Función register_search_units encontrada")
        else:
            print("❌ Función register_search_units no encontrada")
            return False

        # Verificar que no hay Union[int, str] en el código
        with open(
            "src/trackhs_mcp/infrastructure/mcp/search_units.py", "r", encoding="utf-8"
        ) as f:
            content = f.read()

        if "Union[int, str]" in content:
            print("❌ Aún hay Union[int, str] en el código")
            return False
        else:
            print("✅ No hay Union[int, str] en el código")

        # Verificar que hay tipos concretos
        if "page: int = 1" in content:
            print("✅ page es int")
        else:
            print("❌ page no es int")
            return False

        if "size: int = 25" in content:
            print("✅ size es int")
        else:
            print("❌ size no es int")
            return False

        if "bedrooms: Optional[int]" in content:
            print("✅ bedrooms es Optional[int]")
        else:
            print("❌ bedrooms no es Optional[int]")
            return False

        # Verificar que no hay _convert_param
        if "_convert_param" in content:
            print("❌ Aún hay _convert_param en el código")
            return False
        else:
            print("✅ No hay _convert_param en el código")

        print("🎉 Todos los tipos están corregidos!")
        return True

    except Exception as e:
        print(f"❌ Error durante verificación: {e}")
        return False


if __name__ == "__main__":
    result = test_search_units_types()
    if result:
        print("\n✅ SUCCESS: Los tipos están corregidos!")
        sys.exit(0)
    else:
        print("\n❌ FAILED: Los tipos no están corregidos")
        sys.exit(1)
