#!/usr/bin/env python3
"""
Debugger asíncrono para herramientas FastMCP
"""

import asyncio
import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def debug_async_tools():
    """Debugger asíncrono para herramientas"""
    print("🔍 DEBUGGER ASÍNCRONO - HERRAMIENTAS FASTMCP")
    print("=" * 50)
    
    try:
        from trackhs_mcp.server import mcp
        
        print(f"📋 Usando await mcp.get_tools():")
        tools = await mcp.get_tools()
        print(f"   Tipo: {type(tools)}")
        print(f"   Cantidad: {len(tools) if hasattr(tools, '__len__') else 'N/A'}")
        
        if isinstance(tools, dict):
            print(f"   Claves del diccionario: {list(tools.keys())}")
            for key, value in tools.items():
                print(f"   {key}: {type(value)} = {value}")
        elif hasattr(tools, '__iter__'):
            for i, tool in enumerate(tools):
                print(f"   {i}: {type(tool)} = {tool}")
                if hasattr(tool, 'name'):
                    print(f"      Nombre: {tool.name}")
                if hasattr(tool, 'description'):
                    print(f"      Descripción: {tool.description[:100]}...")
        
        # Buscar search_units específicamente
        print(f"\n🔍 Buscando search_units:")
        search_units_tool = None
        if isinstance(tools, dict):
            # Si es diccionario, buscar por clave
            if 'search_units' in tools:
                search_units_tool = tools['search_units']
                print(f"   ✅ search_units encontrada por clave")
            else:
                print(f"   ❌ search_units no encontrada en claves")
        else:
            # Si es iterable, buscar en valores
            for tool in tools:
                if hasattr(tool, 'name') and tool.name == 'search_units':
                    search_units_tool = tool
                    break
        
        if search_units_tool:
            print(f"   ✅ search_units encontrada:")
            print(f"      Tipo: {type(search_units_tool)}")
            print(f"      Nombre: {search_units_tool.name}")
            
            # Analizar esquema de entrada
            if hasattr(search_units_tool, 'inputSchema'):
                input_schema = search_units_tool.inputSchema
                print(f"      Input Schema: {type(input_schema)}")
                if isinstance(input_schema, dict):
                    props = input_schema.get('properties', {})
                    print(f"         Propiedades: {list(props.keys())}")
                    
                    # Analizar parámetros específicos
                    for param in ['bedrooms', 'bathrooms', 'is_active', 'is_bookable']:
                        if param in props:
                            param_schema = props[param]
                            print(f"         🎯 {param}: {param_schema}")
            
            # Analizar esquema de salida
            if hasattr(search_units_tool, 'outputSchema'):
                output_schema = search_units_tool.outputSchema
                print(f"      Output Schema: {type(output_schema)}")
                if isinstance(output_schema, dict):
                    props = output_schema.get('properties', {})
                    print(f"         Propiedades: {list(props.keys())}")
                    
                    # Buscar campo area en esquema de salida
                    if '_embedded' in props:
                        embedded = props['_embedded']
                        if 'properties' in embedded and 'units' in embedded['properties']:
                            units = embedded['properties']['units']
                            if 'items' in units and 'properties' in units['items']:
                                unit_props = units['items']['properties']
                                if 'area' in unit_props:
                                    area_schema = unit_props['area']
                                    print(f"         🎯 Campo area en output schema:")
                                    print(f"            {area_schema}")
        else:
            print("   ❌ search_units no encontrada")
        
        # Probar llamada directa a la herramienta
        print(f"\n🔍 Probando llamada directa:")
        if search_units_tool:
            try:
                # Intentar llamar la herramienta directamente
                if hasattr(search_units_tool, 'func'):
                    print(f"   Llamando search_units.func con size=2...")
                    result = search_units_tool.func(size=2)
                    print(f"   ✅ Llamada exitosa:")
                    print(f"      Tipo de resultado: {type(result)}")
                    if isinstance(result, dict):
                        print(f"      Claves: {list(result.keys())}")
                        if 'total_items' in result:
                            print(f"      Total items: {result['total_items']}")
                        
                        # Analizar campo area en resultado
                        if '_embedded' in result and 'units' in result['_embedded']:
                            units = result['_embedded']['units']
                            print(f"      Unidades: {len(units)}")
                            for i, unit in enumerate(units[:2]):
                                area = unit.get('area')
                                print(f"         Unidad {i+1} area: {area} (tipo: {type(area)})")
                else:
                    print(f"   ❌ search_units_tool no tiene método func")
            except Exception as e:
                print(f"   ❌ Error en llamada directa: {e}")
                import traceback
                traceback.print_exc()
        
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Ejecutar debugger asíncrono"""
    asyncio.run(debug_async_tools())

if __name__ == "__main__":
    main()
