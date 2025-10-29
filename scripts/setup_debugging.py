#!/usr/bin/env python3
"""
Script de configuración para debugging de TrackHS MCP Connector
"""

import os
import sys
from pathlib import Path


def setup_environment():
    """Configura el entorno para debugging"""
    print("Configurando entorno para debugging...")

    # Crear directorio de logs si no existe
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    print(f"   [OK] Directorio de logs: {logs_dir.absolute()}")

    # Crear directorio de docs si no existe
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    print(f"   [OK] Directorio de documentacion: {docs_dir.absolute()}")

    # Verificar variables de entorno
    required_vars = ["TRACKHS_API_URL", "TRACKHS_USERNAME", "TRACKHS_PASSWORD"]
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"\n[WARNING] Variables de entorno faltantes: {', '.join(missing_vars)}")
        print("   Configura estas variables antes de ejecutar el servidor:")
        for var in missing_vars:
            print(f"   set {var}=<valor>")
    else:
        print("   [OK] Todas las variables de entorno estan configuradas")

    # Verificar estructura de archivos
    required_files = [
        "src/tools/diagnose_api.py",
        "src/utils/api_client.py",
        "src/tools/search_units.py",
        "docs/DEBUGGING.md",
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print(f"\n[ERROR] Archivos faltantes: {', '.join(missing_files)}")
        return False
    else:
        print("   [OK] Todos los archivos de debugging estan presentes")

    return True


def create_env_template():
    """Crea un template de archivo .env para configuración"""
    env_template = """# Configuración de TrackHS MCP Connector
# Copia este archivo como .env y configura los valores

# URL base de la API de TrackHS
TRACKHS_API_URL=https://ihmvacations.trackhs.com

# Credenciales de API
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_password

# Configuración opcional
TRACKHS_TIMEOUT=30

# Configuración de logging
LOG_LEVEL=INFO
LOG_FORMAT=json
"""

    env_file = Path(".env.template")
    with open(env_file, "w", encoding="utf-8") as f:
        f.write(env_template)

    print(f"   [OK] Template de .env creado: {env_file.absolute()}")


def show_debugging_commands():
    """Muestra comandos útiles para debugging"""
    print("\nComandos Utiles para Debugging:")
    print("=" * 50)

    print("\n1. Ejecutar diagnóstico completo:")
    print("   python scripts/test_debugging.py")

    print("\n2. Iniciar servidor con logging detallado:")
    print("   LOG_LEVEL=DEBUG python src/server.py")

    print("\n3. Probar búsqueda de unidades específica:")
    print("   # Usar la herramienta search_units con diferentes parámetros")

    print("\n4. Ver logs en tiempo real:")
    print("   tail -f logs/trackhs_mcp.log")

    print("\n5. Analizar estructura de respuesta:")
    print("   # Los logs ahora incluyen análisis detallado de la respuesta")


def main():
    """Función principal"""
    print("TrackHS MCP Connector - Setup de Debugging")
    print("=" * 60)

    # Configurar entorno
    if not setup_environment():
        print("\n❌ Error en configuración. Revisa los archivos faltantes.")
        sys.exit(1)

    # Crear template de .env
    create_env_template()

    # Mostrar comandos útiles
    show_debugging_commands()

    print("\n" + "=" * 60)
    print("[SUCCESS] Setup de debugging completado!")
    print("\nProximos pasos:")
    print("1. Configura las variables de entorno")
    print("2. Ejecuta: python scripts/test_debugging.py")
    print("3. Revisa la documentacion en docs/DEBUGGING.md")


if __name__ == "__main__":
    main()
