#!/usr/bin/env python3
"""
Test de inicio del servidor TrackHS MCP
Verifica que el servidor se puede ejecutar sin errores
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_server_import():
    """Test de importación del servidor"""
    print("Test de importación del servidor...")
    
    try:
        # Importar componentes del servidor
        from trackhs_mcp.server import mcp, api_client, config
        
        print(f"   Servidor MCP: {type(mcp).__name__}")
        print(f"   Cliente API: {type(api_client).__name__}")
        print(f"   Configuración: {type(config).__name__}")
        
        # Verificar configuración
        print(f"   URL: {config.base_url}")
        print(f"   Usuario: {config.username}")
        print(f"   Timeout: {config.timeout}s")
        
        # Verificar validación de URL
        if config.validate_url():
            print("   URL válida para TrackHS")
        else:
            print("   WARNING: URL no válida para TrackHS")
        
        print("   OK: Servidor importado correctamente")
        return True
        
    except Exception as e:
        print(f"   ERROR: Error importando servidor: {e}")
        return False

def test_server_components():
    """Test de componentes del servidor"""
    print("\nTest de componentes del servidor...")
    
    try:
        from trackhs_mcp.server import mcp, api_client, config
        
        # Verificar que el servidor tiene los métodos necesarios
        if not hasattr(mcp, 'run'):
            print("   ERROR: Servidor no tiene método 'run'")
            return False
        
        # Verificar cliente API
        if not hasattr(api_client, 'request'):
            print("   ERROR: Cliente API no tiene método 'request'")
            return False
        
        # Verificar configuración
        if not hasattr(config, 'base_url'):
            print("   ERROR: Configuración no tiene 'base_url'")
            return False
        
        print("   OK: Componentes del servidor verificados")
        return True
        
    except Exception as e:
        print(f"   ERROR: Error verificando componentes: {e}")
        return False

def test_server_ready():
    """Test de preparación del servidor"""
    print("\nTest de preparación del servidor...")
    
    try:
        from trackhs_mcp.server import mcp, api_client, config
        
        # Verificar que todo está configurado
        if not config.base_url:
            print("   ERROR: URL base no configurada")
            return False
        
        if not config.username:
            print("   ERROR: Usuario no configurado")
            return False
        
        if not config.password:
            print("   ERROR: Password no configurado")
            return False
        
        # Verificar endpoint
        endpoint = config.get_endpoint_url("/v2/pms/reservations")
        print(f"   Endpoint: {endpoint}")
        
        print("   OK: Servidor listo para ejecutar")
        return True
        
    except Exception as e:
        print(f"   ERROR: Error verificando preparación: {e}")
        return False

def main():
    """Función principal"""
    print("TRACKHS MCP SERVER - TEST DE INICIO")
    print("=" * 50)
    
    tests = [
        test_server_import,
        test_server_components,
        test_server_ready
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\nRESUMEN:")
    print(f"   Tests pasados: {passed}/{total}")
    
    if passed == total:
        print("   ¡Servidor listo para ejecutar!")
        print("\nPara ejecutar el servidor:")
        print("   python src/trackhs_mcp/server.py")
        return True
    else:
        print("   ERROR: Algunos tests fallaron")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nTest interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\nError inesperado: {e}")
        sys.exit(1)
