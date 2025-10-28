#!/usr/bin/env python3
"""
Debugger específico para configuración de FastMCP
"""

import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def debug_fastmcp_config():
    """Debugger específico para FastMCP"""
    print("🔍 DEBUGGER FASTMCP - CONFIGURACIÓN Y HERRAMIENTAS")
    print("=" * 60)
    
    try:
        from trackhs_mcp.server import mcp
        
        print(f"📋 Objeto MCP:")
        print(f"   Tipo: {type(mcp)}")
        print(f"   Módulo: {mcp.__class__.__module__}")
        
        # Verificar atributos disponibles
        print(f"\n🔍 Atributos disponibles:")
        attrs = [attr for attr in dir(mcp) if not attr.startswith('_')]
        for attr in attrs:
            try:
                value = getattr(mcp, attr)
                print(f"   {attr}: {type(value)} = {value}")
            except Exception as e:
                print(f"   {attr}: ERROR - {e}")
        
        # Verificar si hay herramientas registradas
        print(f"\n🔍 Verificando herramientas:")
        
        # Método 1: tools
        if hasattr(mcp, 'tools'):
            tools = mcp.tools
            print(f"   mcp.tools: {type(tools)} = {tools}")
            if hasattr(tools, '__len__'):
                print(f"   Cantidad de herramientas: {len(tools)}")
                for i, tool in enumerate(tools):
                    print(f"      {i}: {type(tool)} = {tool}")
        else:
            print("   ❌ mcp.tools no existe")
        
        # Método 2: _tools
        if hasattr(mcp, '_tools'):
            tools = mcp._tools
            print(f"   mcp._tools: {type(tools)} = {tools}")
        else:
            print("   ❌ mcp._tools no existe")
        
        # Método 3: tool_registry
        if hasattr(mcp, 'tool_registry'):
            registry = mcp.tool_registry
            print(f"   mcp.tool_registry: {type(registry)} = {registry}")
        else:
            print("   ❌ mcp.tool_registry no existe")
        
        # Método 4: Buscar en todos los atributos
        print(f"\n🔍 Buscando herramientas en todos los atributos:")
        for attr_name in dir(mcp):
            if 'tool' in attr_name.lower():
                try:
                    attr_value = getattr(mcp, attr_name)
                    print(f"   {attr_name}: {type(attr_value)} = {attr_value}")
                except Exception as e:
                    print(f"   {attr_name}: ERROR - {e}")
        
        # Verificar configuración del servidor
        print(f"\n🔍 Configuración del servidor:")
        if hasattr(mcp, 'config'):
            config = mcp.config
            print(f"   mcp.config: {type(config)} = {config}")
        else:
            print("   ❌ mcp.config no existe")
        
        # Verificar si hay métodos de registro
        print(f"\n🔍 Métodos de registro disponibles:")
        reg_methods = [attr for attr in dir(mcp) if 'register' in attr.lower() or 'tool' in attr.lower()]
        for method in reg_methods:
            try:
                method_obj = getattr(mcp, method)
                print(f"   {method}: {type(method_obj)}")
            except Exception as e:
                print(f"   {method}: ERROR - {e}")
        
        # Verificar si search_units está registrada de alguna manera
        print(f"\n🔍 Buscando search_units:")
        search_units_found = False
        
        # Buscar en tools
        if hasattr(mcp, 'tools'):
            tools = mcp.tools
            if hasattr(tools, '__iter__'):
                for tool in tools:
                    if hasattr(tool, 'name') and tool.name == 'search_units':
                        print(f"   ✅ search_units encontrada en mcp.tools: {tool}")
                        search_units_found = True
                    elif hasattr(tool, '__name__') and tool.__name__ == 'search_units':
                        print(f"   ✅ search_units encontrada en mcp.tools: {tool}")
                        search_units_found = True
        
        # Buscar en todos los atributos
        for attr_name in dir(mcp):
            try:
                attr_value = getattr(mcp, attr_name)
                if hasattr(attr_value, 'name') and attr_value.name == 'search_units':
                    print(f"   ✅ search_units encontrada en mcp.{attr_name}: {attr_value}")
                    search_units_found = True
                elif hasattr(attr_value, '__name__') and attr_value.__name__ == 'search_units':
                    print(f"   ✅ search_units encontrada en mcp.{attr_name}: {attr_value}")
                    search_units_found = True
            except:
                pass
        
        if not search_units_found:
            print("   ❌ search_units no encontrada en ningún lugar")
        
        # Verificar el decorador @mcp.tool
        print(f"\n🔍 Verificando decorador @mcp.tool:")
        from trackhs_mcp.server import search_units
        print(f"   search_units: {type(search_units)}")
        print(f"   Es FunctionTool: {type(search_units).__name__ == 'FunctionTool'}")
        
        if hasattr(search_units, 'name'):
            print(f"   Nombre: {search_units.name}")
        if hasattr(search_units, 'description'):
            print(f"   Descripción: {search_units.description[:100]}...")
        
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Ejecutar debugger FastMCP"""
    debug_fastmcp_config()

if __name__ == "__main__":
    main()
