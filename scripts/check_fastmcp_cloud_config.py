#!/usr/bin/env python3
"""
Script para verificar la configuración específica de FastMCP Cloud
"""

import os
import sys
import json

def check_environment_variables():
    """Verificar variables de entorno"""
    print("🔍 Verificando variables de entorno para FastMCP Cloud")
    print("=" * 60)
    
    required_vars = ["TRACKHS_USERNAME", "TRACKHS_PASSWORD"]
    optional_vars = ["TRACKHS_API_URL"]
    
    print("Variables requeridas:")
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}: {value[:3]}***" if len(value) > 3 else f"   ✅ {var}: {value}")
        else:
            print(f"   ❌ {var}: No configurada")
    
    print("\nVariables opcionales:")
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}: {value}")
        else:
            print(f"   ⚠️  {var}: No configurada (usando default)")
    
    # Verificar configuración por defecto
    default_url = "https://ihmvacations.trackhs.com/api"
    actual_url = os.getenv("TRACKHS_API_URL", default_url)
    
    print(f"\n📊 Configuración de URL:")
    print(f"   URL configurada: {actual_url}")
    print(f"   URL por defecto: {default_url}")
    
    return all(os.getenv(var) for var in required_vars)

def check_fastmcp_json():
    """Verificar configuración de fastmcp.json"""
    print("\n🔍 Verificando configuración de fastmcp.json")
    print("=" * 60)
    
    try:
        with open("fastmcp.json", "r") as f:
            config = json.load(f)
        
        print("✅ fastmcp.json encontrado")
        
        # Verificar variables de entorno requeridas
        env_vars = config.get("environment_variables", {})
        required = env_vars.get("required", [])
        optional = env_vars.get("optional", [])
        
        print(f"Variables requeridas en fastmcp.json: {required}")
        print(f"Variables opcionales en fastmcp.json: {optional}")
        
        # Verificar que las variables estén configuradas
        missing_required = []
        for var in required:
            if not os.getenv(var):
                missing_required.append(var)
        
        if missing_required:
            print(f"❌ Variables requeridas faltantes: {missing_required}")
            return False
        else:
            print("✅ Todas las variables requeridas están configuradas")
            return True
            
    except FileNotFoundError:
        print("❌ fastmcp.json no encontrado")
        return False
    except json.JSONDecodeError:
        print("❌ fastmcp.json no es JSON válido")
        return False
    except Exception as e:
        print(f"❌ Error leyendo fastmcp.json: {str(e)}")
        return False

def check_server_config():
    """Verificar configuración del servidor"""
    print("\n🔍 Verificando configuración del servidor")
    print("=" * 60)
    
    try:
        # Verificar que el archivo del servidor existe
        server_file = "src/trackhs_mcp/server.py"
        if not os.path.exists(server_file):
            print(f"❌ Archivo del servidor no encontrado: {server_file}")
            return False
        
        print(f"✅ Archivo del servidor encontrado: {server_file}")
        
        # Verificar que el archivo __main__.py existe
        main_file = "src/trackhs_mcp/__main__.py"
        if not os.path.exists(main_file):
            print(f"❌ Archivo __main__.py no encontrado: {main_file}")
            return False
        
        print(f"✅ Archivo __main__.py encontrado: {main_file}")
        
        # Verificar que el archivo __main__.py tiene la configuración correcta
        with open(main_file, "r") as f:
            content = f.read()
        
        if "from .server import mcp" in content:
            print("✅ __main__.py configurado correctamente")
        else:
            print("❌ __main__.py no está configurado correctamente")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando configuración del servidor: {str(e)}")
        return False

def check_dependencies():
    """Verificar dependencias"""
    print("\n🔍 Verificando dependencias")
    print("=" * 60)
    
    try:
        import httpx
        print("✅ httpx disponible")
    except ImportError:
        print("❌ httpx no disponible")
        return False
    
    try:
        import fastmcp
        print("✅ fastmcp disponible")
    except ImportError:
        print("❌ fastmcp no disponible")
        return False
    
    try:
        import pydantic
        print("✅ pydantic disponible")
    except ImportError:
        print("❌ pydantic no disponible")
        return False
    
    return True

def generate_recommendations():
    """Generar recomendaciones basadas en la verificación"""
    print("\n" + "=" * 60)
    print("💡 RECOMENDACIONES PARA FASTMCP CLOUD")
    print("=" * 60)
    
    print("1. 🔧 Configuración de Variables de Entorno:")
    print("   En FastMCP Cloud, asegúrate de configurar:")
    print("   - TRACKHS_USERNAME=tu_usuario")
    print("   - TRACKHS_PASSWORD=tu_password")
    print("   - TRACKHS_API_URL=https://ihmvacations.trackhs.com/api (opcional)")
    
    print("\n2. 📁 Estructura de Archivos:")
    print("   Asegúrate de que la estructura sea:")
    print("   - src/trackhs_mcp/__main__.py")
    print("   - src/trackhs_mcp/server.py")
    print("   - fastmcp.json")
    
    print("\n3. 🚀 Despliegue en FastMCP Cloud:")
    print("   - Sube el código al repositorio")
    print("   - Configura las variables de entorno")
    print("   - Despliega el servidor")
    
    print("\n4. 🔍 Diagnóstico:")
    print("   Si el problema persiste, ejecuta:")
    print("   - python scripts/test_specific_issue.py")
    print("   - python scripts/run_full_diagnosis.py")
    
    print("\n5. 📞 Soporte:")
    print("   Si nada funciona, contacta soporte con:")
    print("   - Logs del servidor")
    print("   - Resultados de los scripts de diagnóstico")
    print("   - Configuración de variables (sin credenciales)")

def main():
    """Función principal"""
    print("🚀 Verificación de Configuración para FastMCP Cloud")
    print("=" * 80)
    
    checks = [
        ("Variables de Entorno", check_environment_variables),
        ("fastmcp.json", check_fastmcp_json),
        ("Configuración del Servidor", check_server_config),
        ("Dependencias", check_dependencies),
    ]
    
    results = {}
    
    for check_name, check_func in checks:
        print(f"\n{'='*20} {check_name} {'='*20}")
        try:
            result = check_func()
            results[check_name] = result
        except Exception as e:
            print(f"❌ Error en {check_name}: {str(e)}")
            results[check_name] = False
    
    # Resumen
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 80)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    print(f"Verificaciones exitosas: {passed}/{total}")
    
    for check_name, result in results.items():
        status = "✅" if result else "❌"
        print(f"   {status} {check_name}")
    
    if passed == total:
        print("\n🎉 ¡Todas las verificaciones pasaron!")
        print("La configuración está lista para FastMCP Cloud")
    else:
        print(f"\n⚠️  {total - passed} verificaciones fallaron")
        print("Revisa los errores arriba y corrige la configuración")
    
    generate_recommendations()

if __name__ == "__main__":
    main()
