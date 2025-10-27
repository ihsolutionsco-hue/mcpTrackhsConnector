#!/usr/bin/env python3
"""
Testeo Avanzado de Tipos y Mejores Prácticas MCP
Analiza directamente las herramientas MCP registradas y sus tipos.
"""

import inspect
import os
import sys
from datetime import datetime
from typing import get_args, get_origin, get_type_hints

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from trackhs_mcp.schemas import *
from trackhs_mcp.server import mcp


def analyze_mcp_tools():
    """Analizar herramientas MCP directamente"""
    print("🔍 ANALIZANDO HERRAMIENTAS MCP REGISTRADAS...")
    print("=" * 80)

    # Obtener herramientas del servidor MCP
    tools = {}

    # Buscar en el módulo server.py
    import trackhs_mcp.server as server_module

    for name, obj in inspect.getmembers(server_module):
        if hasattr(obj, "__name__") and callable(obj):
            # Verificar si es una herramienta MCP (tiene decorador @mcp.tool)
            if hasattr(obj, "__wrapped__") or "tool" in str(type(obj)):
                tools[name] = obj

    print(f"📊 Encontradas {len(tools)} funciones candidatas")

    # Filtrar solo las herramientas MCP reales
    mcp_tools = {}
    for name, func in tools.items():
        if hasattr(func, "__doc__") and func.__doc__ and len(func.__doc__) > 100:
            # Verificar si tiene anotaciones de tipos
            sig = inspect.signature(func)
            if len(sig.parameters) > 0:
                mcp_tools[name] = func

    print(f"🔧 Herramientas MCP identificadas: {len(mcp_tools)}")
    print()

    return mcp_tools


def analyze_tool_parameters(tool_name: str, tool_func) -> dict:
    """Analizar parámetros de una herramienta MCP"""
    analysis = {
        "tool_name": tool_name,
        "parameters": {},
        "type_issues": [],
        "best_practice_issues": [],
        "recommendations": [],
    }

    try:
        sig = inspect.signature(tool_func)
        type_hints = get_type_hints(tool_func)

        print(f"🔧 Analizando: {tool_name}")
        print(f"   📝 Documentación: {'✅' if tool_func.__doc__ else '❌'}")

        # Analizar cada parámetro
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue

            param_analysis = {
                "name": param_name,
                "type": str(param.annotation),
                "default": (
                    param.default if param.default != inspect.Parameter.empty else None
                ),
                "is_optional": param.default != inspect.Parameter.empty,
                "has_validation": False,
                "validation_details": {},
            }

            # Verificar si tiene validación Pydantic
            if hasattr(param.annotation, "__metadata__"):
                for metadata in param.annotation.__metadata__:
                    if hasattr(metadata, "description"):
                        param_analysis["has_validation"] = True
                        param_analysis["validation_details"] = {
                            "description": getattr(metadata, "description", None),
                            "ge": getattr(metadata, "ge", None),
                            "le": getattr(metadata, "le", None),
                            "min_length": getattr(metadata, "min_length", None),
                            "max_length": getattr(metadata, "max_length", None),
                            "pattern": getattr(metadata, "pattern", None),
                        }

            analysis["parameters"][param_name] = param_analysis

            # Verificar problemas
            if not param_analysis["has_validation"]:
                analysis["best_practice_issues"].append(
                    f"Parámetro '{param_name}' sin validación Pydantic"
                )

            if param_analysis["type"] == "typing.Optional[None]":
                analysis["type_issues"].append(
                    f"Parámetro '{param_name}' tiene tipo Optional[None]"
                )

            print(
                f"   📋 {param_name}: {param_analysis['type']} {'✅' if param_analysis['has_validation'] else '⚠️'}"
            )

        # Verificar documentación
        if tool_func.__doc__:
            doc = tool_func.__doc__

            # Verificar ejemplos
            if "ejemplo" not in doc.lower() and "example" not in doc.lower():
                analysis["recommendations"].append("Agregar ejemplos de uso")

            # Verificar casos de uso
            if "casos de uso" not in doc.lower():
                analysis["recommendations"].append("Agregar casos de uso")

            # Verificar descripción clara
            first_line = doc.split("\n")[0].strip()
            if len(first_line) < 30:
                analysis["best_practice_issues"].append("Descripción muy corta")

        print(
            f"   📊 Problemas: {len(analysis['type_issues']) + len(analysis['best_practice_issues'])}"
        )
        print()

    except Exception as e:
        analysis["type_issues"].append(f"Error analizando: {str(e)}")
        print(f"   ❌ Error: {str(e)}")
        print()

    return analysis


def analyze_schemas_detailed():
    """Análisis detallado de esquemas"""
    print("📋 ANÁLISIS DETALLADO DE ESQUEMAS...")
    print("=" * 80)

    schemas = {
        "RESERVATION_SEARCH_OUTPUT_SCHEMA": RESERVATION_SEARCH_OUTPUT_SCHEMA,
        "UNIT_SEARCH_OUTPUT_SCHEMA": UNIT_SEARCH_OUTPUT_SCHEMA,
        "WORK_ORDER_OUTPUT_SCHEMA": WORK_ORDER_OUTPUT_SCHEMA,
        "RESERVATION_DETAIL_OUTPUT_SCHEMA": RESERVATION_DETAIL_OUTPUT_SCHEMA,
        "FOLIO_OUTPUT_SCHEMA": FOLIO_OUTPUT_SCHEMA,
        "AMENITIES_OUTPUT_SCHEMA": AMENITIES_OUTPUT_SCHEMA,
    }

    total_issues = 0

    for schema_name, schema_def in schemas.items():
        print(f"📄 {schema_name}")

        issues = []

        # Verificar estructura básica
        if "type" not in schema_def:
            issues.append("Falta campo 'type'")
        if "properties" not in schema_def:
            issues.append("Falta campo 'properties'")

        # Verificar propiedades
        if "properties" in schema_def:
            for prop_name, prop_def in schema_def["properties"].items():
                if "description" not in prop_def:
                    issues.append(f"Propiedad '{prop_name}' sin descripción")

                # Verificar tipos opcionales
                if "type" in prop_def and isinstance(prop_def["type"], list):
                    if "null" in prop_def["type"] and len(prop_def["type"]) != 2:
                        issues.append(
                            f"Propiedad '{prop_name}': tipo opcional mal formado"
                        )

        # Verificar metadatos de paginación
        if "page" in schema_def.get("properties", {}):
            pagination_fields = ["page", "page_count", "page_size", "total_items"]
            for field in pagination_fields:
                if field not in schema_def["properties"]:
                    issues.append(f"Falta campo de paginación '{field}'")

        if issues:
            print(f"   ❌ Problemas: {len(issues)}")
            for issue in issues[:3]:  # Mostrar solo los primeros 3
                print(f"      - {issue}")
            if len(issues) > 3:
                print(f"      ... y {len(issues) - 3} más")
            total_issues += len(issues)
        else:
            print(f"   ✅ Sin problemas")

        print()

    return total_issues


def generate_improvement_plan():
    """Generar plan de mejoras específico"""
    print("🎯 PLAN DE MEJORAS ESPECÍFICO")
    print("=" * 80)

    print("1. 🔧 CORRECCIONES INMEDIATAS:")
    print("   - Agregar descripciones a propiedades de esquemas")
    print("   - Corregir tipos opcionales mal formados")
    print("   - Implementar validación Pydantic en todos los parámetros")
    print()

    print("2. 📋 MEJORAS DE DOCUMENTACIÓN:")
    print("   - Agregar ejemplos de uso a todas las herramientas")
    print("   - Incluir casos de uso comunes")
    print("   - Documentar códigos de error y excepciones")
    print("   - Agregar descripciones detalladas de parámetros")
    print()

    print("3. 🚀 OPTIMIZACIONES MCP:")
    print("   - Implementar validación de rangos numéricos")
    print("   - Agregar patrones regex para fechas/emails")
    print("   - Mejorar mensajes de error descriptivos")
    print("   - Implementar versionado de herramientas")
    print()

    print("4. 📊 MEJORAS DE ESQUEMAS:")
    print("   - Estandarizar estructura de respuestas")
    print("   - Agregar metadatos de paginación consistentes")
    print("   - Implementar enlaces HATEOAS")
    print("   - Documentar códigos de estado")
    print()

    print("5. 🏗️ ARQUITECTURA AVANZADA:")
    print("   - Implementar rate limiting por herramienta")
    print("   - Agregar métricas de uso detalladas")
    print("   - Implementar caching inteligente")
    print("   - Agregar logging estructurado por herramienta")
    print()


def main():
    """Función principal"""
    print("🧪 TESTEO AVANZADO DE TIPOS Y MEJORES PRÁCTICAS MCP")
    print("=" * 80)
    print()

    # Analizar herramientas MCP
    mcp_tools = analyze_mcp_tools()

    if mcp_tools:
        print("🔍 ANÁLISIS DETALLADO DE HERRAMIENTAS...")
        print("=" * 80)

        total_type_issues = 0
        total_best_practice_issues = 0
        total_recommendations = 0

        for tool_name, tool_func in mcp_tools.items():
            analysis = analyze_tool_parameters(tool_name, tool_func)
            total_type_issues += len(analysis["type_issues"])
            total_best_practice_issues += len(analysis["best_practice_issues"])
            total_recommendations += len(analysis["recommendations"])

        print(f"📊 RESUMEN DE HERRAMIENTAS:")
        print(f"   🔧 Herramientas analizadas: {len(mcp_tools)}")
        print(f"   ❌ Problemas de tipos: {total_type_issues}")
        print(f"   ⚠️  Problemas de mejores prácticas: {total_best_practice_issues}")
        print(f"   💡 Recomendaciones: {total_recommendations}")
        print()
    else:
        print("⚠️  No se pudieron detectar herramientas MCP automáticamente")
        print(
            "   Esto puede deberse a la forma en que FastMCP registra las herramientas"
        )
        print()

    # Analizar esquemas
    schema_issues = analyze_schemas_detailed()

    # Generar plan de mejoras
    generate_improvement_plan()

    # Resumen final
    print("📊 RESUMEN FINAL")
    print("=" * 80)

    if mcp_tools:
        total_issues = total_type_issues + total_best_practice_issues + schema_issues
    else:
        total_issues = schema_issues

    if total_issues == 0:
        print("🎉 ¡EXCELENTE! No se encontraron problemas críticos")
    elif total_issues < 5:
        print("✅ BUENO: Pocos problemas encontrados")
    elif total_issues < 10:
        print("⚠️  REGULAR: Algunos problemas que corregir")
    else:
        print("❌ NECESITA MEJORAS: Varios problemas encontrados")

    print(f"📈 Total de problemas encontrados: {total_issues}")
    print()
    print("🏨 TrackHS MCP - Análisis avanzado completado")


if __name__ == "__main__":
    main()
