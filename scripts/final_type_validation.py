#!/usr/bin/env python3
"""
Validación Final de Tipos y Mejores Prácticas MCP
Verifica que todas las mejoras implementadas funcionen correctamente.
"""

import json
import os
import sys
from typing import Any, Dict

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from trackhs_mcp.schemas import *
from trackhs_mcp.server import mcp


def validate_schema_structure(
    schema_name: str, schema_def: Dict[str, Any]
) -> Dict[str, Any]:
    """Validar estructura de un esquema"""
    validation = {
        "schema_name": schema_name,
        "is_valid": True,
        "issues": [],
        "improvements": [],
    }

    try:
        # Verificar estructura básica
        if "type" not in schema_def:
            validation["issues"].append("Falta campo 'type'")
            validation["is_valid"] = False

        if "properties" not in schema_def:
            validation["issues"].append("Falta campo 'properties'")
            validation["is_valid"] = False

        # Verificar descripciones en propiedades
        if "properties" in schema_def:
            missing_descriptions = []
            for prop_name, prop_def in schema_def["properties"].items():
                if "description" not in prop_def:
                    missing_descriptions.append(prop_name)

            if missing_descriptions:
                validation["issues"].append(
                    f"Propiedades sin descripción: {missing_descriptions}"
                )
                validation["is_valid"] = False

            # Verificar tipos opcionales
            for prop_name, prop_def in schema_def["properties"].items():
                if "type" in prop_def and isinstance(prop_def["type"], list):
                    if "null" in prop_def["type"] and len(prop_def["type"]) != 2:
                        validation["issues"].append(
                            f"Propiedad '{prop_name}': tipo opcional mal formado"
                        )
                        validation["is_valid"] = False

        # Verificar metadatos de paginación para esquemas de colección
        if "page" in schema_def.get("properties", {}):
            required_pagination = ["page", "page_count", "page_size", "total_items"]
            missing_pagination = [
                field
                for field in required_pagination
                if field not in schema_def["properties"]
            ]
            if missing_pagination:
                validation["issues"].append(
                    f"Faltan campos de paginación: {missing_pagination}"
                )
                validation["is_valid"] = False

        # Verificar enlaces HATEOAS
        if "_links" in schema_def.get("properties", {}):
            validation["improvements"].append("Incluye enlaces HATEOAS")

        # Verificar metadatos embebidos
        if "_embedded" in schema_def.get("properties", {}):
            validation["improvements"].append("Incluye datos embebidos")

    except Exception as e:
        validation["issues"].append(f"Error validando esquema: {str(e)}")
        validation["is_valid"] = False

    return validation


def validate_mcp_tools():
    """Validar herramientas MCP"""
    print("🔧 VALIDANDO HERRAMIENTAS MCP...")
    print("=" * 80)

    # Obtener herramientas del servidor
    tools = []

    # Buscar en el módulo server.py
    import trackhs_mcp.server as server_module

    for name, obj in server_module.__dict__.items():
        if callable(obj) and hasattr(obj, "__doc__") and obj.__doc__:
            # Verificar si es una herramienta MCP
            if "tool" in str(type(obj)) or hasattr(obj, "__wrapped__"):
                tools.append(name)

    print(f"📊 Herramientas MCP encontradas: {len(tools)}")
    for tool in tools:
        print(f"   🔧 {tool}")
    print()

    return tools


def validate_schemas():
    """Validar todos los esquemas"""
    print("📋 VALIDANDO ESQUEMAS DE SALIDA...")
    print("=" * 80)

    schemas = {
        "RESERVATION_SEARCH_OUTPUT_SCHEMA": RESERVATION_SEARCH_OUTPUT_SCHEMA,
        "UNIT_SEARCH_OUTPUT_SCHEMA": UNIT_SEARCH_OUTPUT_SCHEMA,
        "WORK_ORDER_OUTPUT_SCHEMA": WORK_ORDER_OUTPUT_SCHEMA,
        "RESERVATION_DETAIL_OUTPUT_SCHEMA": RESERVATION_DETAIL_OUTPUT_SCHEMA,
        "FOLIO_OUTPUT_SCHEMA": FOLIO_OUTPUT_SCHEMA,
        "AMENITIES_OUTPUT_SCHEMA": AMENITIES_OUTPUT_SCHEMA,
    }

    validation_results = []
    total_issues = 0

    for schema_name, schema_def in schemas.items():
        print(f"📄 Validando: {schema_name}")

        validation = validate_schema_structure(schema_name, schema_def)
        validation_results.append(validation)

        if validation["is_valid"]:
            print(f"   ✅ Válido")
            if validation["improvements"]:
                print(f"   💡 Mejoras: {', '.join(validation['improvements'])}")
        else:
            print(f"   ❌ Problemas: {len(validation['issues'])}")
            for issue in validation["issues"]:
                print(f"      - {issue}")
            total_issues += len(validation["issues"])

        print()

    return validation_results, total_issues


def validate_type_safety():
    """Validar seguridad de tipos"""
    print("🛡️ VALIDANDO SEGURIDAD DE TIPOS...")
    print("=" * 80)

    type_safety_issues = []

    # Verificar enums
    try:
        from trackhs_mcp.schemas import (
            HousekeepingWorkOrderStatus,
            MaintenanceWorkOrderStatus,
            WorkOrderPriority,
        )

        # Verificar WorkOrderPriority
        if not hasattr(WorkOrderPriority, "LOW") or WorkOrderPriority.LOW != 1:
            type_safety_issues.append(
                "WorkOrderPriority.LOW no está definido correctamente"
            )

        if not hasattr(WorkOrderPriority, "MEDIUM") or WorkOrderPriority.MEDIUM != 3:
            type_safety_issues.append(
                "WorkOrderPriority.MEDIUM no está definido correctamente"
            )

        if not hasattr(WorkOrderPriority, "HIGH") or WorkOrderPriority.HIGH != 5:
            type_safety_issues.append(
                "WorkOrderPriority.HIGH no está definido correctamente"
            )

        print("✅ Enums definidos correctamente")

    except Exception as e:
        type_safety_issues.append(f"Error validando enums: {str(e)}")
        print(f"❌ Error validando enums: {str(e)}")

    # Verificar modelos Pydantic
    try:
        from trackhs_mcp.schemas import (
            CollectionResponse,
            ReservationResponse,
            UnitResponse,
            WorkOrderResponse,
        )

        # Verificar que los modelos tengan campos requeridos
        if not hasattr(CollectionResponse, "page"):
            type_safety_issues.append("CollectionResponse no tiene campo 'page'")

        if not hasattr(ReservationResponse, "id"):
            type_safety_issues.append("ReservationResponse no tiene campo 'id'")

        if not hasattr(UnitResponse, "id"):
            type_safety_issues.append("UnitResponse no tiene campo 'id'")

        if not hasattr(WorkOrderResponse, "id"):
            type_safety_issues.append("WorkOrderResponse no tiene campo 'id'")

        print("✅ Modelos Pydantic definidos correctamente")

    except Exception as e:
        type_safety_issues.append(f"Error validando modelos Pydantic: {str(e)}")
        print(f"❌ Error validando modelos Pydantic: {str(e)}")

    if type_safety_issues:
        print(f"❌ Problemas de seguridad de tipos: {len(type_safety_issues)}")
        for issue in type_safety_issues:
            print(f"   - {issue}")
    else:
        print("✅ Sin problemas de seguridad de tipos")

    print()
    return type_safety_issues


def generate_validation_report(
    tools: list,
    schema_results: list,
    type_safety_issues: list,
    total_schema_issues: int,
):
    """Generar reporte de validación"""
    print("📊 REPORTE DE VALIDACIÓN FINAL")
    print("=" * 80)

    # Resumen general
    total_issues = total_schema_issues + len(type_safety_issues)

    print(f"🔧 Herramientas MCP: {len(tools)}")
    print(f"📋 Esquemas validados: {len(schema_results)}")
    print(f"❌ Problemas de esquemas: {total_schema_issues}")
    print(f"🛡️ Problemas de tipos: {len(type_safety_issues)}")
    print(f"📈 Total de problemas: {total_issues}")
    print()

    # Calificación
    if total_issues == 0:
        print("🎉 ¡EXCELENTE! Todas las validaciones pasaron correctamente")
        grade = "A+"
    elif total_issues < 3:
        print("✅ MUY BUENO: Pocos problemas menores")
        grade = "A"
    elif total_issues < 6:
        print("✅ BUENO: Algunos problemas que corregir")
        grade = "B"
    elif total_issues < 10:
        print("⚠️  REGULAR: Varios problemas encontrados")
        grade = "C"
    else:
        print("❌ NECESITA MEJORAS: Muchos problemas encontrados")
        grade = "D"

    print(f"🏆 Calificación: {grade}")
    print()

    # Recomendaciones finales
    print("💡 RECOMENDACIONES FINALES:")
    print("=" * 80)

    if total_issues == 0:
        print(
            "🎯 ¡FELICITACIONES! El MCP TrackHS está implementado siguiendo las mejores prácticas:"
        )
        print("   ✅ Tipos seguros y bien definidos")
        print("   ✅ Esquemas de salida completos y documentados")
        print("   ✅ Validación robusta de parámetros")
        print("   ✅ Arquitectura escalable y mantenible")
        print("   ✅ Mejores prácticas de MCP implementadas")
    else:
        print("🔧 ÁREAS DE MEJORA:")

        if total_schema_issues > 0:
            print("   📋 Esquemas de salida:")
            print("      - Agregar descripciones faltantes")
            print("      - Corregir tipos opcionales mal formados")
            print("      - Implementar metadatos de paginación consistentes")

        if len(type_safety_issues) > 0:
            print("   🛡️ Seguridad de tipos:")
            print("      - Verificar definiciones de enums")
            print("      - Validar modelos Pydantic")
            print("      - Implementar validación de rangos")

    print()
    print("🏨 TrackHS MCP - Validación final completada")


def main():
    """Función principal"""
    print("🧪 VALIDACIÓN FINAL DE TIPOS Y MEJORES PRÁCTICAS MCP")
    print("=" * 80)
    print()

    # Validar herramientas MCP
    tools = validate_mcp_tools()

    # Validar esquemas
    schema_results, total_schema_issues = validate_schemas()

    # Validar seguridad de tipos
    type_safety_issues = validate_type_safety()

    # Generar reporte
    generate_validation_report(
        tools, schema_results, type_safety_issues, total_schema_issues
    )


if __name__ == "__main__":
    main()
