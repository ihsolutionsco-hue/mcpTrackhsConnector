#!/usr/bin/env python3
"""
Script para validar URLs y endpoints de TrackHS API
"""

import asyncio
import httpx
import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from trackhs_mcp.config import TrackHSConfig


class URLValidator:
    """Validador de URLs y endpoints para TrackHS API"""
    
    def __init__(self):
        self.results = {}
    
    async def validate_url(self, url: str, endpoint: str = "/v2/pms/reservations") -> dict:
        """Validar una URL base y endpoint"""
        full_url = f"{url.rstrip('/')}{endpoint}"
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(full_url)
                
                return {
                    "url": full_url,
                    "status_code": response.status_code,
                    "success": response.is_success,
                    "headers": dict(response.headers),
                    "error": None
                }
        except Exception as e:
            return {
                "url": full_url,
                "status_code": None,
                "success": False,
                "headers": {},
                "error": str(e)
            }
    
    async def validate_all_urls(self):
        """Validar todas las URLs configuradas"""
        print("Validando URLs de TrackHS API...")
        print("=" * 60)
        
        # URL oficial de IHVM Vacations
        urls_to_test = [
            TrackHSConfig.DEFAULT_URL
        ]
        
        endpoints_to_test = [
            "/v2/pms/reservations",
            "/pms/reservations",
            "/v1/pms/reservations"
        ]
        
        for url in urls_to_test:
            print(f"\nValidando URL base: {url}")
            print("-" * 40)
            
            for endpoint in endpoints_to_test:
                result = await self.validate_url(url, endpoint)
                self.results[f"{url}{endpoint}"] = result
                
                status_icon = "OK" if result["success"] else "ERROR"
                status_code = result["status_code"] or "ERROR"
                error = result["error"] or ""
                
                print(f"  {status_icon} {endpoint:<25} {status_code:<10} {error}")
        
        return self.results
    
    def print_summary(self):
        """Imprimir resumen de validación"""
        print("\n" + "=" * 60)
        print("RESUMEN DE VALIDACIÓN")
        print("=" * 60)
        
        successful_urls = []
        failed_urls = []
        
        for url, result in self.results.items():
            if result["success"]:
                successful_urls.append((url, result["status_code"]))
            else:
                failed_urls.append((url, result["error"]))
        
        print(f"\nURLs EXITOSAS ({len(successful_urls)}):")
        for url, status_code in successful_urls:
            print(f"   {url} - Status: {status_code}")
        
        print(f"\nURLs FALLIDAS ({len(failed_urls)}):")
        for url, error in failed_urls:
            print(f"   {url} - Error: {error}")
        
        print(f"\nESTADISTICAS:")
        print(f"   Total URLs probadas: {len(self.results)}")
        print(f"   Exitosas: {len(successful_urls)}")
        print(f"   Fallidas: {len(failed_urls)}")
        
        # Recomendaciones
        print(f"\nRECOMENDACIONES:")
        if successful_urls:
            print(f"   URL oficial de IHVM funcionando correctamente")
            print(f"   Endpoint /v2/pms/reservations disponible")
            print(f"   Configura credenciales reales en .env")
        else:
            print("   URL de IHVM no responde. Verifica:")
            print("   - Conectividad de red")
            print("   - Credenciales validas")
            print("   - Firewall o proxy")
        
        print(f"\nPROXIMOS PASOS:")
        print(f"   1. Configura credenciales reales en .env")
        print(f"   2. Ejecuta: python test_local.py")
        print(f"   3. Ejecuta: pytest tests/")
        print(f"   4. Ejecuta: python src/trackhs_mcp/server.py")


async def main():
    """Función principal"""
    print("TrackHS API URL Validator")
    print("=" * 60)
    
    validator = URLValidator()
    await validator.validate_all_urls()
    validator.print_summary()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nValidación interrumpida por el usuario")
    except Exception as e:
        print(f"\nError inesperado: {e}")
        sys.exit(1)
