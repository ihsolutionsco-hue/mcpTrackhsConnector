#!/usr/bin/env python3
"""
Debugger sistemático para problemas de esquemas y tipos en MCP
Analiza todo el flujo de datos desde la API hasta la validación
"""

import json
import sys
from pathlib import Path
from typing import get_type_hints, get_origin, get_args
import inspect

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def debug_schemas_and_types():
    """Debugger sistemático de esquemas y tipos"""
    print("🔍 DEBUGGER SISTEMÁTICO MCP - ANÁLISIS DE ESQUEMAS Y TIPOS")
    print("=" * 80)

    try:
        # 1. Analizar esquemas JSON
        print("\n1️⃣ ANÁLISIS DE ESQUEMAS JSON")
        print("-" * 40)
        from trackhs_mcp.schemas import UNIT_SEARCH_OUTPUT_SCHEMA

        print("📋 Esquema UNIT_SEARCH_OUTPUT_SCHEMA:")
        print(f"   Tipo: {type(UNIT_SEARCH_OUTPUT_SCHEMA)}")
        print(f"   Claves principales: {list(UNIT_SEARCH_OUTPUT_SCHEMA.keys())}")

        # Analizar campo area específicamente
        if "properties" in UNIT_SEARCH_OUTPUT_SCHEMA:
            properties = UNIT_SEARCH_OUTPUT_SCHEMA["properties"]
            if "_embedded" in properties:
                embedded = properties["_embedded"]
                if "properties" in embedded and "units" in embedded["properties"]:
                    units = embedded["properties"]["units"]
                    if "items" in units and "properties" in units["items"]:
                        unit_props = units["items"]["properties"]
                        if "area" in unit_props:
                            area_schema = unit_props["area"]
                            print(f"   🎯 Campo area en esquema JSON:")
                            print(f"      {json.dumps(area_schema, indent=6)}")

        # 2. Analizar modelos Pydantic
        print("\n2️⃣ ANÁLISIS DE MODELOS PYDANTIC")
        print("-" * 40)
        from trackhs_mcp.schemas import UnitResponse

        print("📋 Modelo UnitResponse:")
        print(f"   Tipo: {type(UnitResponse)}")

        # Analizar campo area en Pydantic
        if hasattr(UnitResponse, 'model_fields'):
            fields = UnitResponse.model_fields
            if 'area' in fields:
                area_field = fields['area']
                print(f"   🎯 Campo area en Pydantic:")
                print(f"      Tipo: {area_field.annotation}")
                print(f"      Descripción: {area_field.description}")
                print(f"      Default: {area_field.default}")

        # 3. Analizar función MCP search_units
        print("\n3️⃣ ANÁLISIS DE FUNCIÓN MCP SEARCH_UNITS")
        print("-" * 40)
        from trackhs_mcp.server import search_units

        print(f"📋 Función search_units:")
        print(f"   Tipo: {type(search_units)}")
        print(f"   Es callable: {callable(search_units)}")

        # Analizar signature de la función
        try:
            sig = inspect.signature(search_units)
            print(f"   Parámetros: {list(sig.parameters.keys())}")

            # Analizar tipos de parámetros específicos
            for param_name in ['bedrooms', 'bathrooms', 'is_active', 'is_bookable']:
                if param_name in sig.parameters:
                    param = sig.parameters[param_name]
                    print(f"   🎯 {param_name}: {param.annotation}")
        except Exception as e:
            print(f"   ❌ Error analizando signature: {e}")

        # 4. Analizar servicio unit_service
        print("\n4️⃣ ANÁLISIS DE SERVICIO UNIT_SERVICE")
        print("-" * 40)
        from trackhs_mcp.services.unit_service import UnitService

        unit_service = UnitService(None)  # No necesitamos repo para analizar tipos
        search_units_method = getattr(unit_service, 'search_units', None)

        if search_units_method:
            print(f"📋 Método search_units en UnitService:")
            print(f"   Tipo: {type(search_units_method)}")

            try:
                sig = inspect.signature(search_units_method)
                print(f"   Parámetros: {list(sig.parameters.keys())}")

                # Analizar tipos de parámetros específicos
                for param_name in ['bedrooms', 'bathrooms', 'is_active', 'is_bookable']:
                    if param_name in sig.parameters:
                        param = sig.parameters[param_name]
                        print(f"   🎯 {param_name}: {param.annotation}")
            except Exception as e:
                print(f"   ❌ Error analizando signature: {e}")

        # 5. Probar llamada real a la API
        print("\n5️⃣ PRUEBA REAL DE LLAMADA A API")
        print("-" * 40)

        try:
            from trackhs_mcp.server import unit_service

            print("🔍 Haciendo llamada real a search_units...")
            result = unit_service.search_units(page=1, size=2)

            print(f"✅ Llamada exitosa:")
            print(f"   Total items: {result.get('total_items', 'N/A')}")
            print(f"   Página: {result.get('page', 'N/A')}")
            print(f"   Tamaño: {result.get('page_size', 'N/A')}")

            # Analizar unidades devueltas
            if "_embedded" in result and "units" in result["_embedded"]:
                units = result["_embedded"]["units"]
                print(f"   Unidades en respuesta: {len(units)}")

                for i, unit in enumerate(units[:2]):  # Solo las primeras 2
                    print(f"   🏠 Unidad {i+1}:")
                    print(f"      ID: {unit.get('id', 'N/A')}")
                    print(f"      Nombre: {unit.get('name', 'N/A')}")

                    # Analizar campo area específicamente
                    area = unit.get('area')
                    print(f"      🎯 Area: {area} (tipo: {type(area)})")

                    if area is not None:
                        if isinstance(area, str):
                            print(f"         ⚠️ PROBLEMA: area es string '{area}'")
                            try:
                                float_val = float(area)
                                print(f"         ✅ Se puede convertir a float: {float_val}")
                            except (ValueError, TypeError) as e:
                                print(f"         ❌ NO se puede convertir a float: {e}")
                        elif isinstance(area, (int, float)):
                            print(f"         ✅ area es number: {area}")
                        else:
                            print(f"         ⚠️ area es tipo inesperado: {type(area)}")
                    else:
                        print(f"         ℹ️ area es None")

        except Exception as e:
            print(f"❌ Error en llamada real: {e}")
            import traceback
            traceback.print_exc()

        # 6. Analizar esquema de validación de FastMCP
        print("\n6️⃣ ANÁLISIS DE VALIDACIÓN FASTMCP")
        print("-" * 40)

        try:
            from trackhs_mcp.server import mcp

            print(f"📋 Objeto MCP:")
            print(f"   Tipo: {type(mcp)}")
            print(f"   Herramientas: {len(mcp.tools) if hasattr(mcp, 'tools') else 'N/A'}")

            # Buscar la herramienta search_units
            search_units_tool = None
            if hasattr(mcp, 'tools'):
                for tool in mcp.tools:
                    if hasattr(tool, 'name') and tool.name == 'search_units':
                        search_units_tool = tool
                        break

            if search_units_tool:
                print(f"   🎯 Herramienta search_units encontrada:")
                print(f"      Tipo: {type(search_units_tool)}")
                print(f"      Nombre: {getattr(search_units_tool, 'name', 'N/A')}")
                print(f"      Descripción: {getattr(search_units_tool, 'description', 'N/A')[:100]}...")

                # Analizar esquema de entrada
                if hasattr(search_units_tool, 'inputSchema'):
                    input_schema = search_units_tool.inputSchema
                    print(f"      Esquema de entrada: {type(input_schema)}")
                    if isinstance(input_schema, dict):
                        print(f"         Propiedades: {list(input_schema.get('properties', {}).keys())}")

                # Analizar esquema de salida
                if hasattr(search_units_tool, 'outputSchema'):
                    output_schema = search_units_tool.outputSchema
                    print(f"      Esquema de salida: {type(output_schema)}")
                    if isinstance(output_schema, dict):
                        print(f"         Propiedades: {list(output_schema.get('properties', {}).keys())}")

                        # Buscar campo area en esquema de salida
                        if 'properties' in output_schema:
                            props = output_schema['properties']
                            if '_embedded' in props:
                                embedded = props['_embedded']
                                if 'properties' in embedded and 'units' in embedded['properties']:
                                    units = embedded['properties']['units']
                                    if 'items' in units and 'properties' in units['items']:
                                        unit_props = units['items']['properties']
                                        if 'area' in unit_props:
                                            area_schema = unit_props['area']
                                            print(f"         🎯 Campo area en esquema de salida:")
                                            print(f"            {json.dumps(area_schema, indent=12)}")
            else:
                print("   ❌ Herramienta search_units no encontrada")

        except Exception as e:
            print(f"❌ Error analizando FastMCP: {e}")
            import traceback
            traceback.print_exc()

        print("\n" + "=" * 80)
        print("🏁 ANÁLISIS COMPLETADO")

    except Exception as e:
        print(f"❌ ERROR CRÍTICO EN DEBUGGER: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Ejecutar debugger"""
    debug_schemas_and_types()

if __name__ == "__main__":
    main()
