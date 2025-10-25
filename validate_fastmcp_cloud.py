#!/usr/bin/env python3
"""
Script de validación específico para FastMCP Cloud
Maneja las importaciones correctamente para el entorno de despliegue
"""

import os
import sys
from pathlib import Path

# Configurar variables de entorno para test
os.environ["TRACKHS_USERNAME"] = "test_user"
os.environ["TRACKHS_PASSWORD"] = "test_password"
os.environ["TRACKHS_BASE_URL"] = "https://api-test.trackhs.com/api"

# Agregar src al path para importaciones
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))


def validate_imports():
    """Validar que todas las importaciones funcionen"""
    try:
        print("🔍 Validando importaciones...")

        # Test importación del servidor
        from trackhs_mcp.server import mcp

        print("✅ Servidor importado correctamente")

        # Test importación de esquemas
        from trackhs_mcp.schemas import WorkOrderPriority

        print("✅ Esquemas importados correctamente")

        return True

    except Exception as e:
        print(f"❌ Error en importaciones: {str(e)}")
        return False


async def validate_server():
    """Validar que el servidor funcione correctamente"""
    try:
        print("🚀 Validando servidor...")

        from trackhs_mcp.server import mcp

        # Verificar herramientas
        tools = await mcp.get_tools()
        print(f"✅ Servidor tiene {len(tools)} herramientas")

        # Verificar recursos
        resources = await mcp.get_resources()
        print(f"✅ Servidor tiene {len(resources)} recursos")

        return True

    except Exception as e:
        print(f"❌ Error en servidor: {str(e)}")
        return False


def main():
    """Función principal de validación"""
    print("🧪 Validando servidor para FastMCP Cloud...")

    # Validar importaciones
    if not validate_imports():
        print("❌ Validación de importaciones falló")
        return False

    # Validar servidor
    import asyncio

    if not asyncio.run(validate_server()):
        print("❌ Validación del servidor falló")
        return False

    print("🎉 Validación exitosa! El servidor está listo para FastMCP Cloud.")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
