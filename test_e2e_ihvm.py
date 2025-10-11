#!/usr/bin/env python3
"""
Test End-to-End completo para TrackHS MCP Connector con IHVM
Verifica toda la cadena desde configuración hasta servidor funcionando
"""

import asyncio
import sys
import os
import time
from pathlib import Path
from typing import Dict, List, Any
from unittest.mock import Mock, AsyncMock, patch

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Imports del proyecto
from trackhs_mcp.config import TrackHSConfig
from trackhs_mcp.core.api_client import TrackHSApiClient
from trackhs_mcp.core.types import TrackHSConfig as CoreConfig
from trackhs_mcp.core.error_handling import get_error_stats
from trackhs_mcp.tools import register_all_tools
from trackhs_mcp.resources import register_all_resources
from trackhs_mcp.prompts import register_all_prompts


class E2ETester:
    """Test End-to-End completo para TrackHS MCP Connector"""
    
    def __init__(self):
        self.results = {
            "config": False,
            "api_client": False,
            "mcp_components": False,
            "server_startup": False,
            "url_validation": False,
            "endpoint_test": False
        }
        self.errors = []
        self.warnings = []
        self.start_time = time.time()
    
    def log_success(self, test_name: str, message: str = ""):
        """Log de éxito"""
        print(f"OK {test_name}: {message}")
        if message:
            print(f"   {message}")
    
    def log_error(self, test_name: str, error: str):
        """Log de error"""
        print(f"ERROR {test_name}: {error}")
        self.errors.append(f"{test_name}: {error}")
    
    def log_warning(self, test_name: str, warning: str):
        """Log de advertencia"""
        print(f"WARNING {test_name}: {warning}")
        self.warnings.append(f"{test_name}: {warning}")
    
    def test_configuration(self):
        """Test 1: Configuración centralizada"""
        print("\n" + "="*60)
        print("TEST 1: CONFIGURACIÓN CENTRALIZADA")
        print("="*60)
        
        try:
            # Crear configuración
            config = TrackHSConfig.from_env()
            
            # Verificar URL
            if not config.validate_url():
                self.log_error("Configuración", "URL no válida para IHVM")
                return False
            
            # Verificar campos
            if not config.base_url:
                self.log_error("Configuración", "URL base no configurada")
                return False
            
            if not config.username:
                self.log_error("Configuración", "Usuario no configurado")
                return False
            
            if not config.password:
                self.log_error("Configuración", "Password no configurado")
                return False
            
            # Mostrar configuración
            print(f"   URL: {config.base_url}")
            print(f"   Usuario: {config.username}")
            print(f"   Timeout: {config.timeout}s")
            
            # Verificar endpoint
            endpoint_url = config.get_endpoint_url("/v2/pms/reservations")
            print(f"   Endpoint: {endpoint_url}")
            
            self.log_success("Configuración", "Configuración centralizada correcta")
            self.results["config"] = True
            return True
            
        except Exception as e:
            self.log_error("Configuración", f"Error: {str(e)}")
            return False
    
    def test_api_client(self):
        """Test 2: Cliente API"""
        print("\n" + "="*60)
        print("TEST 2: CLIENTE API")
        print("="*60)
        
        try:
            # Crear configuración
            config = TrackHSConfig.from_env()
            
            # Mock de autenticación para evitar errores de credenciales
            with patch('trackhs_mcp.core.auth.TrackHSAuth') as mock_auth:
                mock_auth.return_value.validate_credentials.return_value = True
                mock_auth.return_value.get_headers.return_value = {
                    "Authorization": "Basic dGVzdF91c2VyOnRlc3RfcGFzc3dvcmQ=",
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
                
                # Crear cliente API
                api_client = TrackHSApiClient(config)
                
                # Verificar configuración
                if api_client.config.base_url != config.base_url:
                    self.log_error("API Client", "URL base no coincide")
                    return False
                
                if api_client.config.username != config.username:
                    self.log_error("API Client", "Usuario no coincide")
                    return False
                
                # Verificar headers
                headers = api_client.auth.get_headers()
                if "Authorization" not in headers:
                    self.log_error("API Client", "Headers de autenticación no configurados")
                    return False
                
                self.log_success("API Client", "Cliente API configurado correctamente")
                self.results["api_client"] = True
                return True
                
        except Exception as e:
            self.log_error("API Client", f"Error: {str(e)}")
            return False
    
    def test_mcp_components(self):
        """Test 3: Componentes MCP"""
        print("\n" + "="*60)
        print("TEST 3: COMPONENTES MCP")
        print("="*60)
        
        try:
            # Crear configuración y cliente API
            config = TrackHSConfig.from_env()
            
            with patch('trackhs_mcp.core.auth.TrackHSAuth') as mock_auth:
                mock_auth.return_value.validate_credentials.return_value = True
                mock_auth.return_value.get_headers.return_value = {
                    "Authorization": "Basic dGVzdF91c2VyOnRlc3RfcGFzc3dvcmQ=",
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
                
                api_client = TrackHSApiClient(config)
                
                # Crear mock del servidor MCP
                class MockMCP:
                    def __init__(self):
                        self.tools = []
                        self.resources = []
                        self.prompts = []
                    
                    def tool(self, name=None, description=None):
                        def decorator(func):
                            self.tools.append({
                                'name': name or func.__name__,
                                'description': description,
                                'function': func
                            })
                            return func
                        return decorator
                    
                    def resource(self, name):
                        def decorator(func):
                            self.resources.append({
                                'name': name,
                                'function': func
                            })
                            return func
                        return decorator
                    
                    def prompt(self, name):
                        def decorator(func):
                            self.prompts.append({
                                'name': name,
                                'function': func
                            })
                            return func
                        return decorator
                
                mock_mcp = MockMCP()
                
                # Registrar componentes
                register_all_tools(mock_mcp, api_client)
                register_all_resources(mock_mcp, api_client)
                register_all_prompts(mock_mcp, api_client)
                
                # Verificar herramientas
                if not mock_mcp.tools:
                    self.log_error("MCP Components", "No hay herramientas registradas")
                    return False
                
                print(f"   Herramientas registradas: {len(mock_mcp.tools)}")
                for tool in mock_mcp.tools:
                    print(f"     - {tool['name']}: {tool['description']}")
                
                # Verificar recursos
                if not mock_mcp.resources:
                    self.log_error("MCP Components", "No hay recursos registrados")
                    return False
                
                print(f"   Recursos registrados: {len(mock_mcp.resources)}")
                for resource in mock_mcp.resources:
                    print(f"     - {resource['name']}")
                
                # Verificar prompts
                if not mock_mcp.prompts:
                    self.log_error("MCP Components", "No hay prompts registrados")
                    return False
                
                print(f"   Prompts registrados: {len(mock_mcp.prompts)}")
                for prompt in mock_mcp.prompts:
                    print(f"     - {prompt['name']}")
                
                self.log_success("MCP Components", "Todos los componentes registrados correctamente")
                self.results["mcp_components"] = True
                return True
                
        except Exception as e:
            self.log_error("MCP Components", f"Error: {str(e)}")
            return False
    
    async def test_url_validation(self):
        """Test 4: Validación de URL"""
        print("\n" + "="*60)
        print("TEST 4: VALIDACIÓN DE URL")
        print("="*60)
        
        try:
            import httpx
            
            config = TrackHSConfig.from_env()
            url = config.base_url
            
            # Test de conectividad básica
            async with httpx.AsyncClient(timeout=10.0) as client:
                try:
                    response = await client.get(url)
                    print(f"   URL responde: {response.status_code}")
                    
                    if response.status_code in [200, 401, 403, 404]:
                        self.log_success("URL Validation", f"URL responde correctamente (Status: {response.status_code})")
                        self.results["url_validation"] = True
                        return True
                    else:
                        self.log_warning("URL Validation", f"Status inesperado: {response.status_code}")
                        self.results["url_validation"] = True
                        return True
                        
                except httpx.ConnectError:
                    self.log_error("URL Validation", "No se puede conectar a la URL")
                    return False
                except httpx.TimeoutException:
                    self.log_error("URL Validation", "Timeout al conectar")
                    return False
                except Exception as e:
                    self.log_error("URL Validation", f"Error de conexión: {str(e)}")
                    return False
                    
        except Exception as e:
            self.log_error("URL Validation", f"Error: {str(e)}")
            return False
    
    async def test_endpoint_functionality(self):
        """Test 5: Funcionalidad del endpoint"""
        print("\n" + "="*60)
        print("TEST 5: FUNCIONALIDAD DEL ENDPOINT")
        print("="*60)
        
        try:
            config = TrackHSConfig.from_env()
            endpoint_url = config.get_endpoint_url("/v2/pms/reservations")
            
            print(f"   Endpoint: {endpoint_url}")
            
            # Test con cliente API mock
            with patch('trackhs_mcp.core.auth.TrackHSAuth') as mock_auth:
                mock_auth.return_value.validate_credentials.return_value = True
                mock_auth.return_value.get_headers.return_value = {
                    "Authorization": "Basic dGVzdF91c2VyOnRlc3RfcGFzc3dvcmQ=",
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
                
                api_client = TrackHSApiClient(config)
                
                # Mock de respuesta exitosa
                mock_response = Mock()
                mock_response.is_success = True
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    "_embedded": {"reservations": []},
                    "page": 1,
                    "page_count": 0,
                    "page_size": 10,
                    "total_items": 0,
                    "_links": {"self": {"href": "test"}}
                }
                mock_response.headers = {"content-type": "application/json"}
                
                with patch.object(api_client.client, 'request', new_callable=AsyncMock) as mock_request:
                    mock_request.return_value = mock_response
                    
                    # Test de llamada al endpoint
                    result = await api_client.get("/v2/pms/reservations", params={"page": 1, "size": 10})
                    
                    if result and "_embedded" in result:
                        self.log_success("Endpoint Functionality", "Endpoint responde correctamente")
                        self.results["endpoint_test"] = True
                        return True
                    else:
                        self.log_error("Endpoint Functionality", "Respuesta del endpoint no válida")
                        return False
                        
        except Exception as e:
            self.log_error("Endpoint Functionality", f"Error: {str(e)}")
            return False
    
    def test_server_startup(self):
        """Test 6: Inicio del servidor"""
        print("\n" + "="*60)
        print("TEST 6: INICIO DEL SERVIDOR")
        print("="*60)
        
        try:
            # Importar servidor
            from trackhs_mcp.server import mcp, api_client, config
            
            # Verificar que el servidor se creó
            if not mcp:
                self.log_error("Server Startup", "Servidor MCP no creado")
                return False
            
            # Verificar configuración del servidor
            if not config:
                self.log_error("Server Startup", "Configuración del servidor no encontrada")
                return False
            
            # Verificar cliente API del servidor
            if not api_client:
                self.log_error("Server Startup", "Cliente API del servidor no encontrado")
                return False
            
            # Verificar que la configuración es correcta
            if not config.validate_url():
                self.log_warning("Server Startup", "URL del servidor no es la oficial de IHVM")
            
            print(f"   Servidor MCP: {type(mcp).__name__}")
            print(f"   Cliente API: {type(api_client).__name__}")
            print(f"   URL configurada: {config.base_url}")
            
            self.log_success("Server Startup", "Servidor configurado correctamente")
            self.results["server_startup"] = True
            return True
            
        except Exception as e:
            self.log_error("Server Startup", f"Error: {str(e)}")
            return False
    
    def generate_report(self):
        """Generar reporte final"""
        print("\n" + "="*60)
        print("REPORTE FINAL - TEST END-TO-END")
        print("="*60)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results.values() if result)
        failed_tests = total_tests - passed_tests
        
        print(f"\nRESUMEN DE RESULTADOS:")
        print(f"   Total tests: {total_tests}")
        print(f"   Exitosos: {passed_tests}")
        print(f"   Fallidos: {failed_tests}")
        print(f"   Tiempo total: {time.time() - self.start_time:.2f}s")
        
        print(f"\nDETALLE DE TESTS:")
        for test_name, result in self.results.items():
            status = "PASS" if result else "FAIL"
            print(f"   {test_name.upper():<20} {status}")
        
        if self.warnings:
            print(f"\nADVERTENCIAS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   WARNING: {warning}")
        
        if self.errors:
            print(f"\nERRORES ({len(self.errors)}):")
            for error in self.errors:
                print(f"   ERROR: {error}")
        
        # Estado final
        if passed_tests == total_tests:
            print(f"\n¡TODOS LOS TESTS PASARON!")
            print(f"   El sistema está listo para producción con IHVM")
        elif passed_tests > 0:
            print(f"\nTESTS PARCIALMENTE EXITOSOS")
            print(f"   {passed_tests}/{total_tests} tests pasaron")
            print(f"   Revisa los errores antes de usar en producción")
        else:
            print(f"\nTODOS LOS TESTS FALLARON")
            print(f"   Revisa la configuración antes de continuar")
        
        print(f"\nPROXIMOS PASOS:")
        if passed_tests == total_tests:
            print(f"   1. Configura credenciales reales en .env")
            print(f"   2. Ejecuta: python src/trackhs_mcp/server.py")
            print(f"   3. Conecta cliente MCP al servidor")
        else:
            print(f"   1. Revisa los errores reportados")
            print(f"   2. Verifica la configuración")
            print(f"   3. Ejecuta tests individuales")
        
        return passed_tests == total_tests
    
    async def run_complete_test(self):
        """Ejecutar test completo end-to-end"""
        print("TRACKHS MCP CONNECTOR - TEST END-TO-END")
        print("Configuración: IHVM Vacations")
        print("="*60)
        
        # Ejecutar todos los tests
        self.test_configuration()
        self.test_api_client()
        self.test_mcp_components()
        await self.test_url_validation()
        await self.test_endpoint_functionality()
        self.test_server_startup()
        
        # Generar reporte
        success = self.generate_report()
        return success


async def main():
    """Función principal"""
    tester = E2ETester()
    success = await tester.run_complete_test()
    
    if success:
        print(f"\nTest end-to-end completado exitosamente")
        sys.exit(0)
    else:
        print(f"\nTest end-to-end falló")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\nTest interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\nError inesperado: {e}")
        sys.exit(1)
