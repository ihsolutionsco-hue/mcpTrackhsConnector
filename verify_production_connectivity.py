#!/usr/bin/env python3
"""
Script para verificar la conectividad en producción
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Cargar variables de entorno
load_dotenv()

from trackhs_mcp.config import TrackHSConfig
from trackhs_mcp.core.api_client import TrackHSApiClient


async def verify_production_connectivity():
    """Verificar conectividad en producción"""
    print("VERIFICACION: Conectividad en Produccion")
    print("=" * 60)
    
    try:
        # Crear configuración
        config = TrackHSConfig.from_env()
        print(f"Configuracion cargada:")
        print(f"  Base URL: {config.base_url}")
        print(f"  Username: {config.username}")
        print(f"  Password: {config.password[:10]}...")
        print(f"  Timeout: {config.timeout}")
        
        # Validar URL
        if not config.validate_url():
            print("ERROR: URL no valida")
            return False
        
        # Crear cliente API
        api_client = TrackHSApiClient(config)
        print("Cliente API creado exitosamente")
        
        # Test de conectividad básica
        print("\nProbando conectividad...")
        
        # Test endpoint V2
        try:
            print("Probando endpoint V2: /v2/pms/reservations")
            response = await api_client.get("/v2/pms/reservations", params={"size": 1})
            print(f"V2: Exito - {len(str(response))} caracteres")
            v2_success = True
        except Exception as e:
            print(f"V2: Error - {str(e)[:100]}...")
            v2_success = False
        
        # Test endpoint V1
        try:
            print("Probando endpoint V1: /pms/reservations")
            response = await api_client.get("/pms/reservations", params={"size": 1})
            print(f"V1: Exito - {len(str(response))} caracteres")
            v1_success = True
        except Exception as e:
            print(f"V1: Error - {str(e)[:100]}...")
            v1_success = False
        
        # Resumen
        print(f"\nResumen de Conectividad:")
        print(f"  API V2: {'OK' if v2_success else 'ERROR'}")
        print(f"  API V1: {'OK' if v1_success else 'ERROR'}")
        
        if v2_success or v1_success:
            print("Conectividad: EXITOSA")
            return True
        else:
            print("Conectividad: FALLIDA")
            return False
            
    except Exception as e:
        print(f"Error en verificacion: {e}")
        return False


async def test_direct_http():
    """Test directo de HTTP"""
    print(f"\nTest Directo HTTP:")
    print("=" * 30)
    
    import httpx
    
    test_urls = [
        "https://ihmvacations.trackhs.com",
        "https://ihmvacations.trackhs.com/api",
        "https://ihmvacations.trackhs.com/api/v2/pms/reservations"
    ]
    
    for url in test_urls:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                print(f"{url}: Status {response.status_code}")
        except Exception as e:
            print(f"{url}: Error - {str(e)[:50]}...")


async def main():
    """Función principal"""
    print("INICIANDO VERIFICACION DE PRODUCCION")
    print("=" * 60)
    
    # Verificar variables de entorno
    print("\nVariables de Entorno:")
    required_vars = ["TRACKHS_API_URL", "TRACKHS_USERNAME", "TRACKHS_PASSWORD"]
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if "PASSWORD" in var:
                print(f"  {var}: Configurada")
            else:
                print(f"  {var}: {value}")
        else:
            print(f"  {var}: NO CONFIGURADA")
    
    # Verificar conectividad
    connectivity_ok = await verify_production_connectivity()
    
    # Test HTTP directo
    await test_direct_http()
    
    # Resultado final
    print(f"\nResultado Final:")
    print("=" * 30)
    if connectivity_ok:
        print("ESTADO: LISTO PARA PRODUCCION")
    else:
        print("ESTADO: REQUIERE CONFIGURACION")
        print("\nAcciones necesarias:")
        print("1. Configurar variables de entorno")
        print("2. Verificar credenciales de TrackHS")
        print("3. Verificar conectividad de red")


if __name__ == "__main__":
    asyncio.run(main())
