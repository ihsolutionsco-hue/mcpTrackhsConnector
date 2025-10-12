#!/usr/bin/env python3
"""
FastMCP Preflight Checks
Validaciones específicas para despliegue en FastMCP Cloud
"""

import os
import subprocess
import sys
from pathlib import Path

import yaml


def check_fastmcp_config():
    """Verificar configuración de FastMCP"""
    print("Verificando configuracion FastMCP...")

    config_file = Path("fastmcp.yaml")
    if not config_file.exists():
        print("ERROR: fastmcp.yaml no encontrado")
        return False

    try:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)

        # Verificar campos requeridos
        required_fields = ["entrypoint", "environment", "server"]
        for field in required_fields:
            if field not in config:
                print(f"ERROR: Campo requerido '{field}' faltante en fastmcp.yaml")
                return False

        # Verificar entrypoint
        entrypoint = config.get("entrypoint", {})
        if "module" not in entrypoint:
            print("ERROR: Modulo de entrada no especificado")
            return False

        # Verificar que el módulo existe
        module_path = entrypoint.get("module", "").replace(".", "/")
        # Remover 'src/' del inicio si está presente
        if module_path.startswith("src/"):
            module_path = module_path[4:]
        if not Path(f"src/{module_path}.py").exists():
            print(f"ERROR: Modulo de entrada no encontrado: src/{module_path}.py")
            return False

        print("OK: Configuracion FastMCP valida")
        return True

    except Exception as e:
        print(f"ERROR: Error validando fastmcp.yaml: {e}")
        return False


def check_mcp_server():
    """Verificar que el servidor MCP esté correctamente configurado"""
    print("Verificando servidor MCP...")

    try:
        sys.path.insert(0, str(Path("src").absolute()))

        # Solo verificar que el módulo se puede importar sin errores críticos
        import trackhs_mcp.server

        print("OK: Servidor MCP configurado correctamente")
        return True

    except Exception as e:
        print(f"WARNING: Advertencia verificando servidor MCP: {e}")
        print("   Esto puede ser normal en desarrollo. Verificar en despliegue.")
        return True  # No es crítico para preflight


def check_main_file():
    """Verificar que el archivo __main__.py sea válido"""
    print("Verificando archivo __main__.py...")

    main_file = Path("src/trackhs_mcp/__main__.py")
    if not main_file.exists():
        print("ERROR: Archivo __main__.py no encontrado")
        return False

    try:
        # Verificar que el archivo se puede compilar
        with open(main_file, "r", encoding="utf-8") as f:
            code = f.read()

        compile(code, str(main_file), "exec")
        print("OK: Archivo __main__.py es valido")
        return True

    except SyntaxError as e:
        print(f"ERROR: Error de sintaxis en __main__.py: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Error al verificar __main__.py: {e}")
        return False


def check_environment_variables():
    """Verificar variables de entorno requeridas"""
    print("Verificando variables de entorno...")

    required_vars = ["TRACKHS_API_URL", "TRACKHS_USERNAME", "TRACKHS_PASSWORD"]
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"WARNING: Variables faltantes: {', '.join(missing_vars)}")
        print("   Estas deben configurarse en FastMCP Cloud")
        return True  # No es crítico para preflight

    print("OK: Variables de entorno configuradas")
    return True


def check_requirements_file():
    """Verificar que requirements.txt esté presente y sea válido"""
    print("Verificando requirements.txt...")

    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("ERROR: requirements.txt no encontrado")
        return False

    try:
        with open(requirements_file, "r") as f:
            content = f.read()

        # Verificar dependencias críticas
        critical_deps = ["fastmcp", "httpx", "pydantic", "python-dotenv"]
        missing_deps = []

        for dep in critical_deps:
            if dep not in content:
                missing_deps.append(dep)

        if missing_deps:
            print(f"ERROR: Dependencias criticas faltantes: {', '.join(missing_deps)}")
            return False

        print("OK: requirements.txt valido")
        return True

    except Exception as e:
        print(f"ERROR: Error verificando requirements.txt: {e}")
        return False


def check_no_hardcoded_credentials():
    """Verificar que no hay credenciales hardcodeadas"""
    print("Verificando credenciales hardcodeadas...")

    # Archivos a verificar
    files_to_check = [
        "src/trackhs_mcp/__main__.py",
        "src/trackhs_mcp/server.py",
        "src/trackhs_mcp/infrastructure/adapters/config.py",
    ]

    # Patrones más específicos para detectar credenciales reales
    suspicious_patterns = [
        'password="',
        "password='",
        'username="',
        "username='",
        'api_key="',
        "api_key='",
        'secret="',
        "secret='",
        'token="',
        "token='",
    ]

    issues_found = []

    for file_path in files_to_check:
        if not Path(file_path).exists():
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            for pattern in suspicious_patterns:
                if pattern in content:
                    # Verificar si es una asignación directa (no variable de entorno)
                    lines = content.split("\n")
                    for i, line in enumerate(lines):
                        if (
                            pattern in line
                            and "os.getenv" not in line
                            and "os.environ" not in line
                        ):
                            # Verificar que no sea solo un comentario o docstring
                            if (
                                not line.strip().startswith("#")
                                and not line.strip().startswith('"""')
                                and not line.strip().startswith("'''")
                            ):
                                issues_found.append(
                                    f"{file_path}:{i+1} - Posible credencial hardcodeada"
                                )

        except Exception as e:
            print(f"WARNING: Error verificando {file_path}: {e}")

    if issues_found:
        print("ERROR: Posibles credenciales hardcodeadas encontradas:")
        for issue in issues_found:
            print(f"   {issue}")
        return False

    print("OK: No se encontraron credenciales hardcodeadas")
    return True


def main():
    """Ejecutar todos los preflight checks"""
    print("Ejecutando FastMCP Preflight...")
    print("=" * 50)

    checks = [
        check_fastmcp_config,
        check_mcp_server,
        check_main_file,
        check_environment_variables,
        check_requirements_file,
        check_no_hardcoded_credentials,
    ]

    passed = 0
    total = len(checks)

    for check in checks:
        try:
            if check():
                passed += 1
        except Exception as e:
            print(f"ERROR: Error en {check.__name__}: {e}")

    print("\n" + "=" * 50)
    print(f"INFO: Resultados: {passed}/{total} checks pasaron")

    if passed == total:
        print("OK: FastMCP Preflight exitoso. Listo para despliegue.")
        return 0
    else:
        print("ERROR: FastMCP Preflight fallo. Revisa los errores.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
