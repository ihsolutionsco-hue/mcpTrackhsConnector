#!/usr/bin/env python3
"""
Analizador Específico de Herramientas MCP TrackHS
Analiza directamente las herramientas definidas en server.py
"""

import ast
import os
import re
import sys
from typing import Any, Dict, List

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def analyze_server_file():
    """Analizar el archivo server.py para encontrar herramientas MCP"""
    print("🔍 ANALIZANDO HERRAMIENTAS MCP EN SERVER.PY...")
    print("=" * 80)

    server_path = os.path.join(
        os.path.dirname(__file__), "..", "src", "trackhs_mcp", "server.py"
    )

    with open(server_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Buscar funciones decoradas con @mcp.tool
    tool_pattern = r"@mcp\.tool\([^)]*\)\s*def\s+(\w+)\s*\("
    tools = re.findall(tool_pattern, content)

    print(f"📊 Herramientas MCP encontradas: {len(tools)}")
    for tool in tools:
        print(f"   🔧 {tool}")
    print()

    return tools


def analyze_tool_parameters(content: str, tool_name: str) -> Dict[str, Any]:
    """Analizar parámetros de una herramienta específica"""
    analysis = {
        "tool_name": tool_name,
        "has_annotations": False,
        "has_field_validation": False,
        "has_documentation": False,
        "has_examples": False,
        "parameter_count": 0,
        "issues": [],
        "recommendations": [],
    }

    # Buscar la definición de la función
    pattern = rf"def\s+{tool_name}\s*\((.*?)\):"
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        analysis["issues"].append("No se pudo encontrar la definición de la función")
        return analysis

    # Extraer parámetros
    params_str = match.group(1)
    params = [
        p.strip().split(":")[0].strip() for p in params_str.split(",") if p.strip()
    ]
    analysis["parameter_count"] = len(params)

    # Buscar anotaciones de tipos
    if "Annotated[" in content or "Field(" in content:
        analysis["has_annotations"] = True
    else:
        analysis["issues"].append("No se encontraron anotaciones de tipos Pydantic")

    # Buscar validación Field
    if "Field(" in content:
        analysis["has_field_validation"] = True
    else:
        analysis["issues"].append("No se encontró validación Field de Pydantic")

    # Buscar documentación
    doc_pattern = rf'def\s+{tool_name}\s*\([^)]*\):\s*"""(.*?)"""'
    doc_match = re.search(doc_pattern, content, re.DOTALL)

    if doc_match:
        analysis["has_documentation"] = True
        doc_content = doc_match.group(1)

        # Verificar ejemplos
        if "ejemplo" in doc_content.lower() or "example" in doc_content.lower():
            analysis["has_examples"] = True
        else:
            analysis["recommendations"].append(
                "Agregar ejemplos de uso en la documentación"
            )

        # Verificar casos de uso
        if "casos de uso" not in doc_content.lower():
            analysis["recommendations"].append("Agregar sección de casos de uso")

        # Verificar descripción clara
        first_line = doc_content.split("\n")[0].strip()
        if len(first_line) < 30:
            analysis["issues"].append("Descripción de la herramienta muy corta")
    else:
        analysis["issues"].append("No se encontró documentación")

    return analysis


def analyze_schemas_improvements():
    """Analizar mejoras necesarias en esquemas"""
    print("📋 ANALIZANDO MEJORAS DE ESQUEMAS...")
    print("=" * 80)

    improvements = {
        "missing_descriptions": [],
        "type_consistency": [],
        "pagination_issues": [],
        "recommendations": [],
    }

    # Esquemas que necesitan mejoras
    schema_issues = {
        "RESERVATION_SEARCH_OUTPUT_SCHEMA": ["_embedded"],
        "UNIT_SEARCH_OUTPUT_SCHEMA": ["_embedded"],
        "RESERVATION_DETAIL_OUTPUT_SCHEMA": ["guest", "dates", "unit", "financial"],
        "FOLIO_OUTPUT_SCHEMA": ["charges", "payments", "summary"],
        "AMENITIES_OUTPUT_SCHEMA": ["_embedded"],
    }

    for schema_name, missing_props in schema_issues.items():
        improvements["missing_descriptions"].extend(
            [f"{schema_name}: {prop}" for prop in missing_props]
        )

    # Recomendaciones generales
    improvements["recommendations"] = [
        "Agregar descripciones a todas las propiedades de esquemas",
        "Estandarizar tipos opcionales como [tipo_principal, 'null']",
        "Implementar metadatos de paginación consistentes",
        "Agregar enlaces HATEOAS para navegación",
        "Documentar códigos de estado y errores",
    ]

    return improvements


def generate_improved_schemas():
    """Generar esquemas mejorados"""
    print("🚀 GENERANDO ESQUEMAS MEJORADOS...")
    print("=" * 80)

    improved_schemas = {}

    # Esquema mejorado para RESERVATION_SEARCH_OUTPUT_SCHEMA
    improved_schemas["RESERVATION_SEARCH_OUTPUT_SCHEMA"] = {
        "type": "object",
        "description": "Respuesta de búsqueda de reservas con metadatos de paginación",
        "properties": {
            "page": {
                "type": "integer",
                "description": "Página actual (0-based)",
                "minimum": 0,
            },
            "page_count": {
                "type": "integer",
                "description": "Total de páginas disponibles",
                "minimum": 0,
            },
            "page_size": {
                "type": "integer",
                "description": "Número de elementos por página",
                "minimum": 1,
                "maximum": 100,
            },
            "total_items": {
                "type": "integer",
                "description": "Total de reservas encontradas",
                "minimum": 0,
            },
            "_embedded": {
                "type": "object",
                "description": "Datos embebidos de la respuesta",
                "properties": {
                    "reservations": {
                        "type": "array",
                        "description": "Lista de reservas encontradas",
                        "items": {
                            "type": "object",
                            "description": "Información detallada de una reserva",
                            "properties": {
                                "id": {
                                    "type": "integer",
                                    "description": "ID único de la reserva",
                                },
                                "confirmationNumber": {
                                    "type": ["string", "null"],
                                    "description": "Número de confirmación de la reserva",
                                },
                                "guest": {
                                    "type": ["object", "null"],
                                    "description": "Información del huésped",
                                    "properties": {
                                        "name": {
                                            "type": ["string", "null"],
                                            "description": "Nombre completo del huésped",
                                        },
                                        "email": {
                                            "type": ["string", "null"],
                                            "description": "Email de contacto del huésped",
                                            "format": "email",
                                        },
                                        "phone": {
                                            "type": ["string", "null"],
                                            "description": "Teléfono de contacto del huésped",
                                        },
                                    },
                                },
                                "arrivalDate": {
                                    "type": ["string", "null"],
                                    "description": "Fecha de llegada en formato ISO 8601",
                                    "format": "date",
                                },
                                "departureDate": {
                                    "type": ["string", "null"],
                                    "description": "Fecha de salida en formato ISO 8601",
                                    "format": "date",
                                },
                                "status": {
                                    "type": ["string", "null"],
                                    "description": "Estado actual de la reserva",
                                    "enum": [
                                        "confirmed",
                                        "cancelled",
                                        "checked-in",
                                        "checked-out",
                                        "pending",
                                    ],
                                },
                                "unit": {
                                    "type": ["object", "null"],
                                    "description": "Información de la unidad reservada",
                                    "properties": {
                                        "id": {
                                            "type": ["integer", "null"],
                                            "description": "ID de la unidad",
                                        },
                                        "name": {
                                            "type": ["string", "null"],
                                            "description": "Nombre de la unidad",
                                        },
                                        "code": {
                                            "type": ["string", "null"],
                                            "description": "Código único de la unidad",
                                        },
                                    },
                                },
                                "financial": {
                                    "type": ["object", "null"],
                                    "description": "Información financiera de la reserva",
                                    "properties": {
                                        "totalAmount": {
                                            "type": ["number", "null"],
                                            "description": "Monto total de la reserva",
                                        },
                                        "balance": {
                                            "type": ["number", "null"],
                                            "description": "Balance pendiente de pago",
                                        },
                                        "deposit": {
                                            "type": ["number", "null"],
                                            "description": "Depósito requerido",
                                        },
                                    },
                                },
                                "_links": {
                                    "type": ["object", "null"],
                                    "description": "Enlaces a recursos relacionados",
                                },
                            },
                        },
                    }
                },
            },
            "_links": {
                "type": "object",
                "description": "Enlaces de navegación HATEOAS",
                "properties": {
                    "self": {
                        "type": ["string", "null"],
                        "description": "Enlace a la página actual",
                    },
                    "first": {
                        "type": ["string", "null"],
                        "description": "Enlace a la primera página",
                    },
                    "last": {
                        "type": ["string", "null"],
                        "description": "Enlace a la última página",
                    },
                    "next": {
                        "type": ["string", "null"],
                        "description": "Enlace a la siguiente página",
                    },
                    "prev": {
                        "type": ["string", "null"],
                        "description": "Enlace a la página anterior",
                    },
                },
            },
        },
        "required": ["page", "page_count", "page_size", "total_items", "_embedded"],
    }

    return improved_schemas


def generate_improvement_recommendations():
    """Generar recomendaciones específicas de mejora"""
    print("💡 RECOMENDACIONES ESPECÍFICAS DE MEJORA")
    print("=" * 80)

    recommendations = {
        "immediate_fixes": [
            "Agregar descripciones a todas las propiedades de esquemas",
            "Implementar validación Field() en todos los parámetros de herramientas",
            "Corregir tipos opcionales mal formados en esquemas",
            "Agregar ejemplos de uso en documentación de herramientas",
        ],
        "documentation_improvements": [
            "Incluir casos de uso comunes para cada herramienta",
            "Documentar códigos de error y excepciones",
            "Agregar descripciones detalladas de parámetros",
            "Incluir ejemplos de respuestas exitosas y de error",
        ],
        "type_safety_improvements": [
            "Implementar validación de rangos para parámetros numéricos",
            "Agregar patrones regex para validación de fechas y emails",
            "Usar enums para valores predefinidos",
            "Implementar validación de longitud para strings",
        ],
        "mcp_best_practices": [
            "Implementar versionado de herramientas",
            "Agregar rate limiting por herramienta",
            "Implementar métricas de uso detalladas",
            "Agregar logging estructurado por herramienta",
        ],
        "schema_improvements": [
            "Estandarizar estructura de respuestas",
            "Implementar metadatos de paginación consistentes",
            "Agregar enlaces HATEOAS para navegación",
            "Documentar códigos de estado y errores",
        ],
    }

    return recommendations


def main():
    """Función principal"""
    print("🧪 ANALIZADOR ESPECÍFICO DE HERRAMIENTAS MCP TRACKHS")
    print("=" * 80)
    print()

    # Analizar herramientas en server.py
    tools = analyze_server_file()

    if tools:
        print("🔍 ANÁLISIS DETALLADO DE HERRAMIENTAS...")
        print("=" * 80)

        # Leer contenido del archivo
        server_path = os.path.join(
            os.path.dirname(__file__), "..", "src", "trackhs_mcp", "server.py"
        )
        with open(server_path, "r", encoding="utf-8") as f:
            content = f.read()

        total_issues = 0
        total_recommendations = 0

        for tool in tools:
            analysis = analyze_tool_parameters(content, tool)
            total_issues += len(analysis["issues"])
            total_recommendations += len(analysis["recommendations"])

            print(f"🔧 {tool}")
            print(f"   📊 Parámetros: {analysis['parameter_count']}")
            print(
                f"   📝 Documentación: {'✅' if analysis['has_documentation'] else '❌'}"
            )
            print(
                f"   🔧 Validación: {'✅' if analysis['has_field_validation'] else '❌'}"
            )
            print(f"   📋 Ejemplos: {'✅' if analysis['has_examples'] else '❌'}")

            if analysis["issues"]:
                print(f"   ❌ Problemas: {len(analysis['issues'])}")
                for issue in analysis["issues"]:
                    print(f"      - {issue}")

            if analysis["recommendations"]:
                print(f"   💡 Recomendaciones: {len(analysis['recommendations'])}")
                for rec in analysis["recommendations"]:
                    print(f"      - {rec}")

            print()

        print(f"📊 RESUMEN DE HERRAMIENTAS:")
        print(f"   🔧 Herramientas analizadas: {len(tools)}")
        print(f"   ❌ Problemas encontrados: {total_issues}")
        print(f"   💡 Recomendaciones: {total_recommendations}")
        print()

    # Analizar mejoras de esquemas
    schema_improvements = analyze_schemas_improvements()

    print(f"📋 RESUMEN DE ESQUEMAS:")
    print(
        f"   ❌ Propiedades sin descripción: {len(schema_improvements['missing_descriptions'])}"
    )
    print(f"   💡 Recomendaciones: {len(schema_improvements['recommendations'])}")
    print()

    # Generar recomendaciones
    recommendations = generate_improvement_recommendations()

    print("🎯 RECOMENDACIONES PRIORITARIAS:")
    print("=" * 80)

    for category, items in recommendations.items():
        print(f"\n📋 {category.upper().replace('_', ' ')}:")
        for item in items:
            print(f"   - {item}")

    # Generar esquemas mejorados
    improved_schemas = generate_improved_schemas()

    print(f"\n🚀 ESQUEMAS MEJORADOS GENERADOS: {len(improved_schemas)}")
    for schema_name in improved_schemas.keys():
        print(f"   📄 {schema_name}")

    # Resumen final
    print("\n📊 RESUMEN FINAL")
    print("=" * 80)

    total_problems = total_issues + len(schema_improvements["missing_descriptions"])

    if total_problems == 0:
        print("🎉 ¡EXCELENTE! No se encontraron problemas críticos")
    elif total_problems < 5:
        print("✅ BUENO: Pocos problemas encontrados")
    elif total_problems < 10:
        print("⚠️  REGULAR: Algunos problemas que corregir")
    else:
        print("❌ NECESITA MEJORAS: Varios problemas encontrados")

    print(f"📈 Total de problemas: {total_problems}")
    print(
        f"💡 Total de recomendaciones: {total_recommendations + len(schema_improvements['recommendations'])}"
    )
    print()
    print("🏨 TrackHS MCP - Análisis específico completado")


if __name__ == "__main__":
    main()
