#!/usr/bin/env python3
"""
Script para probar conectividad básica con TrackHS
Verifica que se pueda conectar a la API antes de probar autenticación
"""

import json
import os
import sys
from typing import List, Tuple

import httpx


def test_basic_connectivity(base_url: str) -> bool:
    """Probar conectividad básica sin autenticación"""
    print(f"\n🔍 Probando conectividad básica:")
    print(f"   URL: {base_url}")

    try:
        with httpx.Client(timeout=10.0) as client:
            # Probar endpoints comunes sin autenticación
            endpoints_to_try = [
                "",
                "health",
                "status",
                "ping",
                "docs",
                "swagger",
                "openapi",
                "api",
                "pms",
            ]

            for endpoint in endpoints_to_try:
                test_url = f"{base_url}/{endpoint}" if endpoint else base_url
                print(f"   Probando: {test_url}")

                try:
                    response = client.get(test_url)
                    print(f"      Status: {response.status_code}")
                    print(
                        f"      Content-Type: {response.headers.get('content-type', 'N/A')}"
                    )

                    if response.status_code == 200:
                        print(f"      ✅ Endpoint accesible: {endpoint or 'root'}")
                        return True
                    elif response.status_code == 401:
                        print(f"      🔐 Requiere autenticación: {endpoint or 'root'}")
                        return True  # El endpoint existe pero requiere auth
                    elif response.status_code == 404:
                        print(f"      ❌ No encontrado: {endpoint or 'root'}")
                    else:
                        print(f"      ⚠️  Status inesperado: {response.status_code}")

                except httpx.RequestError as e:
                    print(f"      ❌ Error de conexión: {str(e)}")

            return False

    except Exception as e:
        print(f"   ❌ Error general: {str(e)}")
        return False


def test_domain_resolution(domain: str) -> bool:
    """Probar resolución de dominio"""
    print(f"\n🔍 Probando resolución de dominio:")
    print(f"   Dominio: {domain}")

    try:
        import socket

        ip = socket.gethostbyname(domain)
        print(f"   ✅ Dominio resuelve a: {ip}")
        return True
    except socket.gaierror as e:
        print(f"   ❌ Error de resolución: {str(e)}")
        return False
    except Exception as e:
        print(f"   ❌ Error inesperado: {str(e)}")
        return False


def test_https_connectivity(base_url: str) -> bool:
    """Probar conectividad HTTPS"""
    print(f"\n🔍 Probando conectividad HTTPS:")
    print(f"   URL: {base_url}")

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(base_url)
            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
            print(f"   Content-Length: {len(response.text)}")

            if response.status_code in [200, 401, 403]:
                print(f"   ✅ Conectividad HTTPS exitosa")
                return True
            else:
                print(f"   ❌ Status inesperado: {response.status_code}")
                return False

    except httpx.RequestError as e:
        print(f"   ❌ Error de conexión HTTPS: {str(e)}")
        return False
    except Exception as e:
        print(f"   ❌ Error inesperado: {str(e)}")
        return False


def main():
    """Función principal"""
    print("🔍 PRUEBA DE CONECTIVIDAD BÁSICA - TRACKHS")
    print("=" * 80)
    print("Este script prueba la conectividad básica con TrackHS")
    print("antes de probar autenticación y endpoints específicos")
    print("=" * 80)

    # URLs base a probar
    base_urls = [
        "https://ihmvacations.trackhs.com",
        "https://ihmvacations.trackhs.com/api",
        "https://api.trackhs.com",
        "https://api.trackhs.com/api",
        "https://trackhs.com",
        "https://trackhs.com/api",
    ]

    results = {}

    for base_url in base_urls:
        print(f"\n{'='*20} Probando {base_url} {'='*20}")

        # Extraer dominio para prueba de resolución
        domain = base_url.replace("https://", "").replace("http://", "").split("/")[0]

        # Probar resolución de dominio
        domain_ok = test_domain_resolution(domain)

        # Probar conectividad HTTPS
        https_ok = test_https_connectivity(base_url)

        # Probar conectividad básica
        basic_ok = test_basic_connectivity(base_url)

        results[base_url] = {
            "domain_resolution": domain_ok,
            "https_connectivity": https_ok,
            "basic_connectivity": basic_ok,
            "overall": domain_ok and https_ok and basic_ok,
        }

    # Resumen de resultados
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE CONECTIVIDAD")
    print("=" * 80)

    successful_urls = [url for url, result in results.items() if result["overall"]]
    failed_urls = [url for url, result in results.items() if not result["overall"]]

    print(f"URLs exitosas: {len(successful_urls)}")
    print(f"URLs fallidas: {len(failed_urls)}")

    if successful_urls:
        print(f"\n✅ URLs EXITOSAS:")
        for url in successful_urls:
            print(f"   - {url}")

        print(f"\n💡 RECOMENDACIÓN:")
        print(f"   Usar: {successful_urls[0]}")
        print(f"   Esta URL tiene conectividad completa")

    else:
        print(f"\n❌ NINGUNA URL EXITOSA")
        print(f"   Posibles problemas:")
        print(f"   - Problemas de red")
        print(f"   - URLs incorrectas")
        print(f"   - Servidor no disponible")

        print(f"\n🔍 DETALLE DE FALLOS:")
        for url, result in results.items():
            print(f"   {url}:")
            print(
                f"      Resolución DNS: {'✅' if result['domain_resolution'] else '❌'}"
            )
            print(
                f"      Conectividad HTTPS: {'✅' if result['https_connectivity'] else '❌'}"
            )
            print(
                f"      Conectividad básica: {'✅' if result['basic_connectivity'] else '❌'}"
            )

    # Guardar resultados
    results_file = "connectivity_test_results.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "timestamp": os.popen("date").read().strip(),
                "total_urls": len(base_urls),
                "successful_urls": len(successful_urls),
                "failed_urls": len(failed_urls),
                "results": results,
                "recommendations": {
                    "best_url": successful_urls[0] if successful_urls else None,
                    "fastmcp_cloud_config": {
                        "TRACKHS_API_URL": (
                            successful_urls[0] if successful_urls else None
                        )
                    },
                },
            },
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"\n📄 Resultados guardados en: {results_file}")

    # Próximos pasos
    print(f"\n🎯 PRÓXIMOS PASOS:")
    if successful_urls:
        print(f"✅ Conectividad básica exitosa")
        print(f"   - Proceder con tests de autenticación")
        print(f"   - Ejecutar: python scripts/run_local_tests.py")
    else:
        print(f"❌ Problemas de conectividad")
        print(f"   - Verificar conexión a internet")
        print(f"   - Verificar URLs correctas")
        print(f"   - Contactar soporte técnico")


if __name__ == "__main__":
    main()
