#!/usr/bin/env python3
"""
Script para probar con credenciales reales del archivo .env
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def load_credentials():
    """Carga credenciales desde el archivo .env"""
    print("Cargando credenciales desde .env...")

    # Cargar variables de entorno desde .env
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"  [OK] Archivo .env encontrado: {env_path}")
    else:
        print(f"  [WARNING] Archivo .env no encontrado en: {env_path}")

    # Verificar variables
    api_url = os.getenv("TRACKHS_API_URL")
    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")

    print(f"\nCredenciales cargadas:")
    print(f"  TRACKHS_API_URL: {api_url}")
    print(f"  TRACKHS_USERNAME: {username}")
    print(f"  TRACKHS_PASSWORD: {'SET' if password else 'NOT SET'}")

    if not all([api_url, username, password]):
        print(f"\n[ERROR] Faltan credenciales requeridas")
        return None, None, None

    return api_url, username, password


def test_authentication(api_url, username, password):
    """Prueba la autenticación con credenciales reales"""
    print(f"\n" + "=" * 60)
    print("Testing Autenticacion con Credenciales Reales")
    print("=" * 60)

    try:
        from tools.diagnose_api import DiagnoseAPITool
        from utils.api_client import TrackHSAPIClient

        # Crear cliente API
        print(f"\n1. Creando cliente API...")
        api_client = TrackHSAPIClient(
            base_url=api_url, username=username, password=password
        )
        print(f"   [OK] Cliente API creado")

        # Test de diagnóstico completo
        print(f"\n2. Ejecutando diagnostico completo...")
        diagnose_tool = DiagnoseAPITool(api_client)

        # Test de conectividad
        print(f"\n   a) Test de Conectividad:")
        connectivity_result = diagnose_tool._test_connectivity()
        print(f"      Status: {connectivity_result['status']}")
        print(f"      Message: {connectivity_result['message']}")

        # Test de autenticación
        print(f"\n   b) Test de Autenticacion:")
        auth_result = diagnose_tool._test_authentication()
        print(f"      Status: {auth_result['status']}")
        print(f"      Message: {auth_result['message']}")

        # Test de endpoints
        print(f"\n   c) Test de Endpoints:")
        endpoints_result = diagnose_tool._test_endpoints()
        print(f"      Endpoints probados: {endpoints_result['endpoints_tested']}")
        print(f"      Exitosos: {endpoints_result['successful']}")
        print(f"      Fallidos: {endpoints_result['failed']}")

        # Mostrar detalles de cada endpoint
        if "details" in endpoints_result:
            print(f"\n      Detalles por endpoint:")
            for endpoint, result in endpoints_result["details"].items():
                status = result.get("status", "unknown")
                error = result.get("error", "")
                print(f"        {endpoint}: {status}")
                if error:
                    if "401" in str(error):
                        print(f"          -> ERROR 401: Problema de autenticacion")
                    elif "404" in str(error):
                        print(f"          -> ERROR 404: Endpoint no encontrado")
                    elif "403" in str(error):
                        print(f"          -> ERROR 403: Sin permisos")
                    else:
                        print(f"          -> Error: {error}")

        # Test de estructura de datos
        print(f"\n   d) Test de Estructura de Datos:")
        data_structure_result = diagnose_tool._test_data_structure()
        print(f"      Test cases: {data_structure_result['test_cases']}")
        print(f"      Exitosos: {data_structure_result['successful_tests']}")
        print(f"      Fallidos: {data_structure_result['failed_tests']}")

        # Generar resumen
        print(f"\n3. Resumen del Diagnostico:")
        summary = diagnose_tool._generate_summary(
            {
                "connectivity": connectivity_result,
                "authentication": auth_result,
                "endpoints": endpoints_result,
                "data_structure": data_structure_result,
            }
        )

        print(f"   Estado general: {summary['overall_status']}")
        print(f"   Tests ejecutados: {summary['tests_executed']}")
        print(f"   Exitosos: {summary['successful_tests']}")
        print(f"   Fallidos: {summary['failed_tests']}")

        if summary["critical_issues"]:
            print(f"\n   Problemas criticos:")
            for issue in summary["critical_issues"]:
                print(f"     - {issue}")

        if summary["recommendations"]:
            print(f"\n   Recomendaciones:")
            for rec in summary["recommendations"]:
                print(f"     - {rec}")

        api_client.close()

        return auth_result["status"] == "success"

    except Exception as e:
        print(f"\n[ERROR] Error en testing: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Función principal"""
    print("Test de Credenciales Reales - TrackHS MCP Connector")
    print("=" * 70)

    # Cargar credenciales
    api_url, username, password = load_credentials()

    if not all([api_url, username, password]):
        print(f"\n[ERROR] No se pudieron cargar las credenciales")
        print(f"Verifica que el archivo .env contenga:")
        print(f"  TRACKHS_API_URL=https://tu-api-url.com")
        print(f"  TRACKHS_USERNAME=tu_usuario")
        print(f"  TRACKHS_PASSWORD=tu_password")
        sys.exit(1)

    # Probar autenticación
    success = test_authentication(api_url, username, password)

    print(f"\n" + "=" * 70)
    if success:
        print("[SUCCESS] Autenticacion exitosa! El problema original esta resuelto.")
    else:
        print("[INFO] Problemas de autenticacion detectados. Revisa las credenciales.")
    print("=" * 70)


if __name__ == "__main__":
    main()
