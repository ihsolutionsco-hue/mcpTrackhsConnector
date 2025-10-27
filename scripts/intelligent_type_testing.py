#!/usr/bin/env python3
"""
Testeo Inteligente de Tipos y Mejores Prácticas MCP
Analiza todas las herramientas MCP para verificar tipos, validaciones y mejores prácticas.
"""

import inspect
import json
import os
import sys
from datetime import datetime
from typing import get_args, get_origin, get_type_hints

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fastmcp import FastMCP
from pydantic import BaseModel, Field

from trackhs_mcp.schemas import *
from trackhs_mcp.server import mcp


class TypeAnalysisResult:
    """Resultado del análisis de tipos"""

    def __init__(self):
        self.tools_analyzed = 0
        self.type_issues = []
        self.best_practice_issues = []
        self.validation_issues = []
        self.schema_issues = []
        self.recommendations = []


def analyze_tool_signature(tool_name: str, tool_func) -> dict:
    """Analizar la firma de una herramienta MCP"""
    analysis = {
        "tool_name": tool_name,
        "parameters": {},
        "return_type": None,
        "type_issues": [],
        "best_practice_issues": [],
        "recommendations": [],
    }

    try:
        # Obtener anotaciones de tipos
        type_hints = get_type_hints(tool_func)
        sig = inspect.signature(tool_func)

        # Analizar parámetros
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
                "has_field_validation": False,
                "field_info": None,
            }

            # Verificar si tiene Field de Pydantic
            if hasattr(param.annotation, "__metadata__"):
                for metadata in param.annotation.__metadata__:
                    if isinstance(metadata, Field):
                        param_analysis["has_field_validation"] = True
                        param_analysis["field_info"] = {
                            "description": getattr(metadata, "description", None),
                            "ge": getattr(metadata, "ge", None),
                            "le": getattr(metadata, "le", None),
                            "min_length": getattr(metadata, "min_length", None),
                            "max_length": getattr(metadata, "max_length", None),
                            "pattern": getattr(metadata, "pattern", None),
                        }

            analysis["parameters"][param_name] = param_analysis

            # Verificar mejores prácticas
            if not param_analysis["has_field_validation"]:
                analysis["best_practice_issues"].append(
                    f"Parámetro '{param_name}' no tiene validación Field de Pydantic"
                )

            if (
                param_analysis["is_optional"]
                and param_analysis["type"] == "typing.Optional[None]"
            ):
                analysis["type_issues"].append(
                    f"Parámetro '{param_name}' tiene tipo Optional[None] - debería ser Optional[T]"
                )

        # Analizar tipo de retorno
        if "return" in type_hints:
            analysis["return_type"] = str(type_hints["return"])
        else:
            analysis["best_practice_issues"].append(
                "No hay anotación de tipo de retorno"
            )

        # Verificar documentación
        if not tool_func.__doc__ or len(tool_func.__doc__.strip()) < 50:
            analysis["best_practice_issues"].append(
                "Documentación insuficiente o ausente"
            )

        # Verificar ejemplos en documentación
        if (
            tool_func.__doc__
            and "Ejemplo" not in tool_func.__doc__
            and "ejemplo" not in tool_func.__doc__
        ):
            analysis["recommendations"].append(
                "Agregar ejemplos de uso en la documentación"
            )

    except Exception as e:
        analysis["type_issues"].append(f"Error analizando firma: {str(e)}")

    return analysis


def analyze_schema_consistency(schema_name: str, schema_def: dict) -> dict:
    """Analizar consistencia de esquemas"""
    analysis = {"schema_name": schema_name, "issues": [], "recommendations": []}

    try:
        # Verificar estructura básica
        if "type" not in schema_def:
            analysis["issues"].append("Falta campo 'type' en el esquema")

        if "properties" not in schema_def:
            analysis["issues"].append("Falta campo 'properties' en el esquema")

        # Verificar descripciones
        if "properties" in schema_def:
            for prop_name, prop_def in schema_def["properties"].items():
                if "description" not in prop_def:
                    analysis["issues"].append(
                        f"Propiedad '{prop_name}' no tiene descripción"
                    )

                # Verificar tipos consistentes
                if "type" in prop_def:
                    prop_type = prop_def["type"]
                    if isinstance(prop_type, list) and "null" in prop_type:
                        if len(prop_type) != 2:
                            analysis["recommendations"].append(
                                f"Propiedad '{prop_name}': tipos opcionales deberían ser [tipo_principal, 'null']"
                            )

        # Verificar metadatos de paginación
        if "page" in schema_def.get("properties", {}):
            required_pagination_fields = [
                "page",
                "page_count",
                "page_size",
                "total_items",
            ]
            for field in required_pagination_fields:
                if field not in schema_def["properties"]:
                    analysis["issues"].append(f"Falta campo de paginación '{field}'")

    except Exception as e:
        analysis["issues"].append(f"Error analizando esquema: {str(e)}")

    return analysis


def check_mcp_best_practices(tool_name: str, tool_func) -> list:
    """Verificar mejores prácticas específicas de MCP"""
    issues = []

    # Verificar nombre de herramienta
    if not tool_name.replace("_", "").isalnum():
        issues.append("Nombre de herramienta contiene caracteres no alfanuméricos")

    if tool_name[0].isdigit():
        issues.append("Nombre de herramienta no debe empezar con número")

    # Verificar documentación
    if not tool_func.__doc__:
        issues.append("Herramienta no tiene documentación")
    else:
        doc = tool_func.__doc__

        # Verificar que tenga descripción clara
        if len(doc.split("\n")[0].strip()) < 20:
            issues.append("Descripción de herramienta muy corta")

        # Verificar que tenga ejemplos
        if "ejemplo" not in doc.lower() and "example" not in doc.lower():
            issues.append("Falta ejemplos de uso en la documentación")

        # Verificar casos de uso
        if "casos de uso" not in doc.lower() and "use cases" not in doc.lower():
            issues.append("Falta sección de casos de uso")

    return issues


def analyze_all_tools():
    """Analizar todas las herramientas MCP"""
    print("🔍 ANALIZANDO HERRAMIENTAS MCP...")
    print("=" * 80)

    results = TypeAnalysisResult()

    # Obtener todas las herramientas registradas
    if hasattr(mcp, "tools"):
        tools = mcp.tools
    else:
        # Buscar herramientas en el módulo
        tools = {}
        for name, obj in inspect.getmembers(mcp):
            if hasattr(obj, "__name__") and hasattr(obj, "__annotations__"):
                if hasattr(obj, "output_schema") or "tool" in str(type(obj)):
                    tools[name] = obj

    print(f"📊 Encontradas {len(tools)} herramientas para analizar")
    print()

    # Analizar cada herramienta
    for tool_name, tool_func in tools.items():
        print(f"🔧 Analizando: {tool_name}")

        # Análisis de firma
        signature_analysis = analyze_tool_signature(tool_name, tool_func)
        results.tools_analyzed += 1

        # Análisis de mejores prácticas MCP
        mcp_issues = check_mcp_best_practices(tool_name, tool_func)

        # Mostrar resultados
        if signature_analysis["type_issues"]:
            print(f"  ❌ Problemas de tipos: {len(signature_analysis['type_issues'])}")
            for issue in signature_analysis["type_issues"]:
                print(f"     - {issue}")
                results.type_issues.append(f"{tool_name}: {issue}")

        if signature_analysis["best_practice_issues"]:
            print(
                f"  ⚠️  Mejores prácticas: {len(signature_analysis['best_practice_issues'])}"
            )
            for issue in signature_analysis["best_practice_issues"]:
                print(f"     - {issue}")
                results.best_practice_issues.append(f"{tool_name}: {issue}")

        if mcp_issues:
            print(f"  📋 MCP específico: {len(mcp_issues)}")
            for issue in mcp_issues:
                print(f"     - {issue}")
                results.best_practice_issues.append(f"{tool_name}: {issue}")

        if signature_analysis["recommendations"]:
            print(f"  💡 Recomendaciones: {len(signature_analysis['recommendations'])}")
            for rec in signature_analysis["recommendations"]:
                print(f"     - {rec}")
                results.recommendations.append(f"{tool_name}: {rec}")

        if not any(
            [
                signature_analysis["type_issues"],
                signature_analysis["best_practice_issues"],
                mcp_issues,
            ]
        ):
            print(f"  ✅ Sin problemas detectados")

        print()

    return results


def analyze_schemas():
    """Analizar todos los esquemas de salida"""
    print("📋 ANALIZANDO ESQUEMAS DE SALIDA...")
    print("=" * 80)

    schema_results = []

    # Obtener todos los esquemas
    schemas = {
        "RESERVATION_SEARCH_OUTPUT_SCHEMA": RESERVATION_SEARCH_OUTPUT_SCHEMA,
        "UNIT_SEARCH_OUTPUT_SCHEMA": UNIT_SEARCH_OUTPUT_SCHEMA,
        "WORK_ORDER_OUTPUT_SCHEMA": WORK_ORDER_OUTPUT_SCHEMA,
        "RESERVATION_DETAIL_OUTPUT_SCHEMA": RESERVATION_DETAIL_OUTPUT_SCHEMA,
        "FOLIO_OUTPUT_SCHEMA": FOLIO_OUTPUT_SCHEMA,
        "AMENITIES_OUTPUT_SCHEMA": AMENITIES_OUTPUT_SCHEMA,
    }

    for schema_name, schema_def in schemas.items():
        print(f"📄 Analizando: {schema_name}")

        analysis = analyze_schema_consistency(schema_name, schema_def)
        schema_results.append(analysis)

        if analysis["issues"]:
            print(f"  ❌ Problemas: {len(analysis['issues'])}")
            for issue in analysis["issues"]:
                print(f"     - {issue}")
        else:
            print(f"  ✅ Sin problemas")

        if analysis["recommendations"]:
            print(f"  💡 Recomendaciones: {len(analysis['recommendations'])}")
            for rec in analysis["recommendations"]:
                print(f"     - {rec}")

        print()

    return schema_results


def generate_improvement_recommendations(
    results: TypeAnalysisResult, schema_results: list
):
    """Generar recomendaciones de mejora"""
    print("💡 RECOMENDACIONES DE MEJORA")
    print("=" * 80)

    # Recomendaciones generales
    print("🎯 RECOMENDACIONES GENERALES:")
    print()

    if results.type_issues:
        print("1. 🔧 CORREGIR PROBLEMAS DE TIPOS:")
        for issue in results.type_issues[:5]:  # Mostrar solo los primeros 5
            print(f"   - {issue}")
        if len(results.type_issues) > 5:
            print(f"   ... y {len(results.type_issues) - 5} más")
        print()

    if results.best_practice_issues:
        print("2. 📋 MEJORAR MEJORES PRÁCTICAS:")
        for issue in results.best_practice_issues[:5]:
            print(f"   - {issue}")
        if len(results.best_practice_issues) > 5:
            print(f"   ... y {len(results.best_practice_issues) - 5} más")
        print()

    # Recomendaciones específicas de MCP
    print("3. 🚀 MEJORAS ESPECÍFICAS PARA MCP:")
    print("   - Agregar ejemplos de uso en todas las herramientas")
    print("   - Incluir casos de uso comunes en la documentación")
    print("   - Usar Field() de Pydantic para validación robusta")
    print("   - Implementar validación de rangos para parámetros numéricos")
    print("   - Agregar patrones regex para validación de fechas/emails")
    print("   - Documentar códigos de error y excepciones")
    print()

    # Recomendaciones de esquemas
    print("4. 📊 MEJORAS DE ESQUEMAS:")
    print("   - Agregar descripciones a todas las propiedades")
    print("   - Usar tipos consistentes (ej: [string, null] para opcionales)")
    print("   - Incluir metadatos de paginación en colecciones")
    print("   - Agregar enlaces HATEOAS para navegación")
    print("   - Documentar códigos de estado y errores")
    print()

    # Recomendaciones de arquitectura
    print("5. 🏗️ MEJORAS DE ARQUITECTURA:")
    print("   - Implementar versionado de API")
    print("   - Agregar rate limiting por herramienta")
    print("   - Implementar caching inteligente")
    print("   - Agregar métricas de uso por herramienta")
    print("   - Implementar logging estructurado por herramienta")
    print()


def main():
    """Función principal"""
    print("🧪 TESTEO INTELIGENTE DE TIPOS Y MEJORES PRÁCTICAS MCP")
    print("=" * 80)
    print()

    # Analizar herramientas
    tool_results = analyze_all_tools()

    # Analizar esquemas
    schema_results = analyze_schemas()

    # Generar recomendaciones
    generate_improvement_recommendations(tool_results, schema_results)

    # Resumen final
    print("📊 RESUMEN DEL ANÁLISIS")
    print("=" * 80)
    print(f"🔧 Herramientas analizadas: {tool_results.tools_analyzed}")
    print(f"❌ Problemas de tipos: {len(tool_results.type_issues)}")
    print(
        f"⚠️  Problemas de mejores prácticas: {len(tool_results.best_practice_issues)}"
    )
    print(f"📋 Esquemas analizados: {len(schema_results)}")
    print(f"💡 Recomendaciones generadas: {len(tool_results.recommendations)}")
    print()

    # Calificación general
    total_issues = len(tool_results.type_issues) + len(
        tool_results.best_practice_issues
    )
    if total_issues == 0:
        print("🎉 ¡EXCELENTE! No se encontraron problemas críticos")
    elif total_issues < 5:
        print("✅ BUENO: Pocos problemas encontrados")
    elif total_issues < 10:
        print("⚠️  REGULAR: Algunos problemas que corregir")
    else:
        print("❌ NECESITA MEJORAS: Varios problemas encontrados")

    print()
    print("🏨 TrackHS MCP - Análisis completado")


if __name__ == "__main__":
    main()
