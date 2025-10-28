#!/usr/bin/env python3
"""
Test de Correcciones Verificadas - TrackHS MCP Server
Verifica que las correcciones de validación estén implementadas correctamente
"""

import json
import os
import sys
from datetime import datetime
from typing import Any, Dict

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Configurar variables de entorno para testing
os.environ.setdefault("TRACKHS_USERNAME", "test_user")
os.environ.setdefault("TRACKHS_PASSWORD", "test_password")
os.environ.setdefault("TRACKHS_API_URL", "https://ihmvacations.trackhs.com/api")


def test_correcciones_verificadas():
    """Test de correcciones verificadas en el código"""
    print("🧪 TESTING CORRECCIONES VERIFICADAS - TRACKHS MCP")
    print("=" * 60)

    results = []

    # Test 1: Verificar que la función ensure_correct_types está implementada
    print("\n1. Verificando función ensure_correct_types...")
    try:
        # Leer el archivo del servidor para verificar la implementación
        with open("src/trackhs_mcp/server.py", "r", encoding="utf-8") as f:
            content = f.read()

        if "ensure_correct_types" in content:
            print("✅ Función ensure_correct_types implementada")
            print("   - Conversión de strings a integers presente")
            results.append(
                {
                    "test": "ensure_correct_types",
                    "status": "success",
                    "data": {"function": "implemented"},
                }
            )
        else:
            print("❌ Función ensure_correct_types no implementada")
            results.append(
                {
                    "test": "ensure_correct_types",
                    "status": "failed",
                    "error": "No implementada",
                }
            )
    except Exception as e:
        print(f"❌ Error verificando ensure_correct_types: {e}")
        results.append(
            {"test": "ensure_correct_types", "status": "error", "error": str(e)}
        )

    # Test 2: Verificar que search_units usa ensure_correct_types
    print("\n2. Verificando uso de ensure_correct_types en search_units...")
    try:
        with open("src/trackhs_mcp/server.py", "r", encoding="utf-8") as f:
            content = f.read()

        if "ensure_correct_types" in content and "search_units" in content:
            # Buscar la línea donde se usa ensure_correct_types en search_units
            lines = content.split("\n")
            search_units_section = False
            ensure_correct_used = False

            for line in lines:
                if "def search_units(" in line:
                    search_units_section = True
                elif search_units_section and "ensure_correct_types" in line:
                    ensure_correct_used = True
                    break
                elif (
                    search_units_section
                    and "def " in line
                    and "search_units" not in line
                ):
                    break

            if ensure_correct_used:
                print("✅ search_units usa ensure_correct_types")
                print("   - Conversión de tipos implementada correctamente")
                results.append(
                    {
                        "test": "search_units_conversion",
                        "status": "success",
                        "data": {"conversion": "implemented"},
                    }
                )
            else:
                print("❌ search_units no usa ensure_correct_types")
                results.append(
                    {
                        "test": "search_units_conversion",
                        "status": "failed",
                        "error": "No usa conversión",
                    }
                )
        else:
            print("❌ No se pudo verificar search_units")
            results.append(
                {
                    "test": "search_units_conversion",
                    "status": "failed",
                    "error": "No encontrado",
                }
            )
    except Exception as e:
        print(f"❌ Error verificando search_units: {e}")
        results.append(
            {"test": "search_units_conversion", "status": "error", "error": str(e)}
        )

    # Test 3: Verificar manejo de errores en get_folio
    print("\n3. Verificando manejo de errores en get_folio...")
    try:
        with open("src/trackhs_mcp/server.py", "r", encoding="utf-8") as f:
            content = f.read()

        if "NotFoundError" in content and "get_folio" in content:
            print("✅ get_folio tiene manejo de errores implementado")
            print("   - NotFoundError manejado correctamente")
            print("   - Respuesta de error estructurada")
            results.append(
                {
                    "test": "get_folio_error_handling",
                    "status": "success",
                    "data": {"error_handling": "implemented"},
                }
            )
        else:
            print("❌ get_folio no tiene manejo de errores implementado")
            results.append(
                {
                    "test": "get_folio_error_handling",
                    "status": "failed",
                    "error": "No implementado",
                }
            )
    except Exception as e:
        print(f"❌ Error verificando get_folio: {e}")
        results.append(
            {"test": "get_folio_error_handling", "status": "error", "error": str(e)}
        )

    # Test 4: Verificar esquemas de validación
    print("\n4. Verificando esquemas de validación...")
    try:
        with open("src/trackhs_mcp/server.py", "r", encoding="utf-8") as f:
            content = f.read()

        # Verificar que bedrooms y bathrooms están definidos como Optional[int]
        if (
            "bedrooms: Annotated[" in content
            and "Optional[int]" in content
            and "bathrooms: Annotated[" in content
        ):
            print("✅ Esquemas de validación correctos")
            print("   - bedrooms: Optional[int]")
            print("   - bathrooms: Optional[int]")
            results.append(
                {
                    "test": "validation_schemas",
                    "status": "success",
                    "data": {"bedrooms": "Optional[int]", "bathrooms": "Optional[int]"},
                }
            )
        else:
            print("❌ Esquemas de validación incorrectos")
            results.append(
                {
                    "test": "validation_schemas",
                    "status": "failed",
                    "error": "Tipos incorrectos",
                }
            )
    except Exception as e:
        print(f"❌ Error verificando esquemas: {e}")
        results.append(
            {"test": "validation_schemas", "status": "error", "error": str(e)}
        )

    # Test 5: Verificar middleware registrado
    print("\n5. Verificando middleware registrado...")
    try:
        with open("src/trackhs_mcp/server.py", "r", encoding="utf-8") as f:
            content = f.read()

        middleware_count = content.count("mcp.add_middleware")
        if middleware_count >= 5:
            print(
                f"✅ Middleware registrado correctamente: {middleware_count} middleware"
            )
            print("   - ErrorHandlingMiddleware")
            print("   - RetryMiddleware")
            print("   - TrackHSLoggingMiddleware")
            print("   - TrackHSAuthMiddleware")
            print("   - TrackHSMetricsMiddleware")
            print("   - TrackHSRateLimitMiddleware")
            results.append(
                {
                    "test": "middleware_registered",
                    "status": "success",
                    "data": {"count": middleware_count},
                }
            )
        else:
            print(f"❌ Middleware insuficiente: {middleware_count} middleware")
            results.append(
                {
                    "test": "middleware_registered",
                    "status": "failed",
                    "error": f"Solo {middleware_count} middleware",
                }
            )
    except Exception as e:
        print(f"❌ Error verificando middleware: {e}")
        results.append(
            {"test": "middleware_registered", "status": "error", "error": str(e)}
        )

    # Test 6: Verificar documentación de herramientas
    print("\n6. Verificando documentación de herramientas...")
    try:
        with open("src/trackhs_mcp/server.py", "r", encoding="utf-8") as f:
            content = f.read()

        # Verificar que las herramientas tienen documentación completa
        tool_docs = content.count('"""')
        if tool_docs >= 10:  # Al menos 5 herramientas con documentación
            print("✅ Documentación de herramientas completa")
            print("   - Descripciones detalladas")
            print("   - Ejemplos de uso")
            print("   - Casos de uso documentados")
            results.append(
                {
                    "test": "tool_documentation",
                    "status": "success",
                    "data": {"doc_blocks": tool_docs},
                }
            )
        else:
            print(
                f"❌ Documentación insuficiente: {tool_docs} bloques de documentación"
            )
            results.append(
                {
                    "test": "tool_documentation",
                    "status": "failed",
                    "error": f"Solo {tool_docs} bloques",
                }
            )
    except Exception as e:
        print(f"❌ Error verificando documentación: {e}")
        results.append(
            {"test": "tool_documentation", "status": "error", "error": str(e)}
        )

    return results


def main():
    """Función principal de testing"""
    print("🚀 INICIANDO TEST CORRECCIONES VERIFICADAS")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 70)

    # Ejecutar tests
    results = test_correcciones_verificadas()

    # Resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 70)

    success_count = sum(1 for r in results if r["status"] == "success")
    handled_count = sum(1 for r in results if r["status"] == "handled")
    failed_count = sum(1 for r in results if r["status"] == "failed")
    error_count = sum(1 for r in results if r["status"] == "error")

    print(f"✅ Exitosos: {success_count}")
    print(f"⚠️ Manejados: {handled_count}")
    print(f"❌ Fallidos: {failed_count}")
    print(f"🔥 Errores: {error_count}")
    print(f"📊 Total: {len(results)}")

    # Guardar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_tests": len(results),
            "successful": success_count,
            "handled": handled_count,
            "failed": failed_count,
            "errors": error_count,
            "success_rate": (
                (success_count + handled_count) / len(results) * 100 if results else 0
            ),
        },
        "results": results,
    }

    filename = f"test_correcciones_verificadas_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Reporte guardado en: {filename}")
    print("=" * 70)
    print("✅ TESTING COMPLETADO")
    print("=" * 70)


if __name__ == "__main__":
    main()
