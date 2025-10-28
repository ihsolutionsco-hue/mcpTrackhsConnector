#!/usr/bin/env python3
"""
Debugger para acceder correctamente a las herramientas FastMCP
"""

import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def debug_tools_access():
    """Debugger para acceso a herramientas"""
    print("🔍 DEBUGGER ACCESO A HERRAMIENTAS FASTMCP")
    print("=" * 50)
    
    try:
        from trackhs_mcp.server import mcp
        
        print(f"📋 Usando mcp.get_tools():")
        tools = mcp.get_tools()
        print(f"   Tipo: {type(tools)}")
        print(f"   Cantidad: {len(tools) if hasattr(tools, '__len__') else 'N/A'}")
        
        if hasattr(tools, '__iter__'):
            for i, tool in enumerate(tools):
                print(f"   {i}: {type(tool)}")
                if hasattr(tool, 'name'):
                    print(f"      Nombre: {tool.name}")
                if hasattr(tool, 'description'):
                    print(f"      Descripción: {tool.description[:100]}...")
                if hasattr(tool, 'inputSchema'):
                    print(f"      Input Schema: {type(tool.inputSchema)}")
                if hasattr(tool, 'outputSchema'):
                    print(f"      Output Schema: {type(tool.outputSchema)}")
        
        # Buscar search_units específicamente
        print(f"\n🔍 Buscando search_units:")
        search_units_tool = None
        for tool in tools:
            if hasattr(tool, 'name') and tool.name == 'search_units':
                search_units_tool = tool
                break
        
        if search_units_tool:
            print(f"   ✅ search_units encontrada:")
            print(f"      Tipo: {type(search_units_tool)}")
            print(f"      Nombre: {search_units_tool.name}")
            print(f"      Descripción: {search_units_tool.description[:100]}...")
            
            # Analizar esquema de entrada
            if hasattr(search_units_tool, 'inputSchema'):
                input_schema = search_units_tool.inputSchema
                print(f"      Input Schema: {type(input_schema)}")
                if isinstance(input_schema, dict):
                    print(f"         Propiedades: {list(input_schema.get('properties', {}).keys())}")
                    
                    # Analizar parámetros específicos
                    props = input_schema.get('properties', {})
                    for param in ['bedrooms', 'bathrooms', 'is_active', 'is_bookable']:
                        if param in props:
                            param_schema = props[param]
                            print(f"         🎯 {param}: {param_schema}")
            
            # Analizar esquema de salida
            if hasattr(search_units_tool, 'outputSchema'):
                output_schema = search_units_tool.outputSchema
                print(f"      Output Schema: {type(output_schema)}")
                if isinstance(output_schema, dict):
                    print(f"         Propiedades: {list(output_schema.get('properties', {}).keys())}")
                    
                    # Buscar campo area en esquema de salida
                    props = output_schema.get('properties', {})
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
    """Ejecutar debugger"""
    debug_tools_access()

if __name__ == "__main__":
    main()
