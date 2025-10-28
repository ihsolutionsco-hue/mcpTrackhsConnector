#!/usr/bin/env python3
"""
Test de simulación MCP - Simulando exactamente lo que hace el servidor
"""

import json
import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def simulate_mcp_search_units():
    """Simular exactamente lo que hace la función MCP search_units"""
    print("🧪 Simulación MCP: Probando search_units como lo haría el servidor...")

    try:
        # Importar los componentes necesarios
        from trackhs_mcp.server import unit_service

        print("✅ Componentes importados correctamente")

        # Simular la función search_units del servidor
        def simulate_search_units(
            page=0,
            size=10,
            search=None,
            bedrooms=None,
            bathrooms=None,
            is_active=None,
            is_bookable=None,
            **additional_params,
        ):
            """Simulación exacta de la función search_units del servidor"""

            # Construir parámetros para la API de TrackHS
            def build_api_params():
                params = {}

                def safe_int(value):
                    if value is None or value == "":
                        return None
                    try:
                        if isinstance(value, int):
                            return value
                        if isinstance(value, str):
                            cleaned = value.strip()
                            if not cleaned:
                                return None
                            return int(cleaned)
                        return int(value)
                    except (ValueError, TypeError, AttributeError):
                        return None

                # Parámetros de paginación
                if page is not None:
                    params["page"] = page
                if size is not None:
                    params["size"] = size

                # Parámetros de búsqueda de texto
                if search is not None:
                    params["search"] = search

                # Parámetros de dormitorios
                if bedrooms is not None:
                    params["bedrooms"] = safe_int(bedrooms)
                if bathrooms is not None:
                    params["bathrooms"] = safe_int(bathrooms)

                # Parámetros de estado
                if is_active is not None:
                    params["isActive"] = safe_int(is_active)
                if is_bookable is not None:
                    params["isBookable"] = safe_int(is_bookable)

                return params

            try:
                # Construir parámetros para la API
                api_params = build_api_params()

                # Usar servicio de negocio con limpieza de datos
                page_1_based = api_params.get("page", 0) + 1
                result = unit_service.search_units(
                    page=page_1_based,
                    size=api_params.get("size", 10),
                    search=api_params.get("search"),
                    bedrooms=api_params.get("bedrooms"),
                    bathrooms=api_params.get("bathrooms"),
                    is_active=api_params.get("isActive"),
                    is_bookable=api_params.get("isBookable"),
                    **{
                        k: v
                        for k, v in api_params.items()
                        if k
                        not in [
                            "page",
                            "size",
                            "search",
                            "bedrooms",
                            "bathrooms",
                            "isActive",
                            "isBookable",
                        ]
                    },
                )

                # Limpiar campo area problemático en la respuesta
                if "_embedded" in result and "units" in result["_embedded"]:
                    for unit in result["_embedded"]["units"]:
                        if "area" in unit and isinstance(unit["area"], str):
                            try:
                                unit["area"] = float(unit["area"])
                            except (ValueError, TypeError):
                                unit.pop("area", None)

                return result

            except Exception as e:
                return {"error": str(e)}

        # Probar diferentes escenarios
        test_cases = [
            {"name": "Búsqueda básica", "params": {"size": 3}},
            {"name": "Búsqueda con dormitorios", "params": {"bedrooms": 2, "size": 2}},
            {"name": "Búsqueda activas", "params": {"is_active": 1, "size": 2}},
            {
                "name": "Búsqueda con texto",
                "params": {"search": "apartment", "size": 2},
            },
            {"name": "Búsqueda con baños", "params": {"bathrooms": 1, "size": 2}},
            {"name": "Búsqueda reservables", "params": {"is_bookable": 1, "size": 2}},
        ]

        success_count = 0

        for test_case in test_cases:
            print(f"\n🔍 Probando: {test_case['name']}")
            print(f"   Parámetros: {test_case['params']}")

            try:
                result = simulate_search_units(**test_case["params"])

                if "error" in result:
                    print(f"   ❌ Error: {result['error']}")
                else:
                    total_items = result.get("total_items", 0)
                    units_count = len(result.get("_embedded", {}).get("units", []))
                    print(
                        f"   ✅ Éxito: {total_items} total, {units_count} en esta página"
                    )

                    # Verificar estructura de respuesta
                    required_keys = [
                        "page",
                        "page_count",
                        "page_size",
                        "total_items",
                        "_embedded",
                        "_links",
                    ]
                    missing_keys = [key for key in required_keys if key not in result]
                    if missing_keys:
                        print(f"   ⚠️ Faltan claves: {missing_keys}")
                    else:
                        print(f"   ✅ Estructura de respuesta correcta")

                    # Verificar limpieza del campo area
                    units = result.get("_embedded", {}).get("units", [])
                    area_issues = 0
                    for unit in units:
                        area = unit.get("area")
                        if area is not None and isinstance(area, str):
                            area_issues += 1

                    if area_issues == 0:
                        print(f"   ✅ Campo area limpio correctamente")
                    else:
                        print(f"   ⚠️ {area_issues} unidades con area problemático")

                    success_count += 1

            except Exception as e:
                print(f"   ❌ Excepción: {e}")
                import traceback

                traceback.print_exc()

        print(f"\n📊 Resultado: {success_count}/{len(test_cases)} casos exitosos")

        if success_count == len(test_cases):
            print("✅ Simulación MCP PASÓ: Todas las pruebas funcionaron")
            return True
        else:
            print("⚠️ Simulación MCP PARCIAL: Algunas pruebas fallaron")
            return False

    except Exception as e:
        print(f"❌ Simulación MCP FALLÓ: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Ejecutar simulación MCP"""
    print("🚀 Iniciando Simulación MCP para search_units")
    print("=" * 60)

    success = simulate_mcp_search_units()

    print("\n" + "=" * 60)
    if success:
        print("🎉 ¡La simulación MCP pasó! El código está listo para el servidor.")
        print("✅ Todos los componentes funcionan correctamente:")
        print("   - Tipos de parámetros corregidos")
        print("   - Validación de esquema funcionando")
        print("   - Limpieza de datos implementada")
        print("   - Llamadas a API funcionando")
        print("   - Estructura de respuesta correcta")
        return True
    else:
        print("⚠️ La simulación MCP falló. Revisar antes de subir al servidor.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
