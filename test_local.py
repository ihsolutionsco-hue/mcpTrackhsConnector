#!/usr/bin/env python3
"""
Script de testing local para Track HS MCP Connector
Verifica la conexión API, registro de componentes y funcionalidad básica
"""

import asyncio
import os
import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from trackhs_mcp.core.api_client import TrackHSApiClient
from trackhs_mcp.core.error_handling import get_error_stats
from trackhs_mcp.core.types import TrackHSConfig
from trackhs_mcp.prompts import register_all_prompts
from trackhs_mcp.resources import register_all_resources
from trackhs_mcp.tools import register_all_tools


class LocalTester:
    """Clase para testing local del MCP Connector"""

    def __init__(self):
        self.config = None
        self.api_client = None
        self.mcp = None
        self.results = {
            "config": False,
            "api_client": False,
            "tools": False,
            "resources": False,
            "prompts": False,
            "api_connection": False,
            "error_handling": False,
        }

    def setup_config(self):
        """Configurar variables de entorno y configuración"""
        print("Configurando variables de entorno...")

        # Cargar variables de entorno
        from dotenv import load_dotenv

        load_dotenv()

        # Configuración de testing
        self.config = TrackHSConfig(
            base_url=os.getenv(
                "TRACKHS_API_URL", "https://ihmvacations.trackhs.com/api"
            ),
            username=os.getenv("TRACKHS_USERNAME", "test_user"),
            password=os.getenv("TRACKHS_PASSWORD", "test_password"),
            timeout=int(os.getenv("TRACKHS_TIMEOUT", "30")),
        )

        print(f"Configuración creada: {self.config.base_url}")
        self.results["config"] = True

    def setup_api_client(self):
        """Configurar API client"""
        print("Configurando API client...")

        try:
            self.api_client = TrackHSApiClient(self.config)
            print("API client creado exitosamente")
            self.results["api_client"] = True
        except Exception as e:
            print(f"Error creando API client: {e}")
            self.results["api_client"] = False

    def setup_mcp_components(self):
        """Configurar componentes MCP"""
        print("Configurando componentes MCP...")

        # Crear mock del servidor MCP
        class MockMCP:
            def __init__(self):
                self.tools = []
                self.resources = []
                self.prompts = []

            def tool(self):
                def decorator(func):
                    self.tools.append(func)
                    return func

                return decorator

            def resource(self, name):
                def decorator(func):
                    self.resources.append((name, func))
                    return func

                return decorator

            def prompt(self, name):
                def decorator(func):
                    self.prompts.append((name, func))
                    return func

                return decorator

        self.mcp = MockMCP()

        # Registrar componentes
        try:
            register_all_tools(self.mcp, self.api_client)
            print(f"Herramientas registradas: {len(self.mcp.tools)}")
            self.results["tools"] = True
        except Exception as e:
            print(f"Error registrando herramientas: {e}")
            self.results["tools"] = False

        try:
            register_all_resources(self.mcp, self.api_client)
            print(f"Recursos registrados: {len(self.mcp.resources)}")
            self.results["resources"] = True
        except Exception as e:
            print(f"Error registrando recursos: {e}")
            self.results["resources"] = False

        try:
            register_all_prompts(self.mcp, self.api_client)
            print(f"Prompts registrados: {len(self.mcp.prompts)}")
            self.results["prompts"] = True
        except Exception as e:
            print(f"Error registrando prompts: {e}")
            self.results["prompts"] = False

    async def test_api_connection(self):
        """Test conexión a la API"""
        print("Probando conexión a la API...")

        try:
            # Test básico de conexión (sin autenticación real)
            print("Nota: Este test no hace una llamada real a la API")
            print("   Para testing completo, configura credenciales reales")

            # Simular test de configuración
            if self.api_client and self.api_client.auth:
                print("API client configurado correctamente")
                self.results["api_connection"] = True
            else:
                print("API client no configurado")
                self.results["api_connection"] = False

        except Exception as e:
            print(f"Error en conexión API: {e}")
            self.results["api_connection"] = False

    def test_error_handling(self):
        """Test manejo de errores"""
        print("Probando manejo de errores...")

        try:
            # Obtener estadísticas de errores
            stats = get_error_stats()
            print(f"Sistema de manejo de errores funcionando")
            print(f"   Errores totales: {stats['total_errors']}")
            self.results["error_handling"] = True
        except Exception as e:
            print(f"Error en manejo de errores: {e}")
            self.results["error_handling"] = False

    def test_components_functionality(self):
        """Test funcionalidad de componentes"""
        print("Probando funcionalidad de componentes...")

        # Test herramientas
        if self.mcp.tools:
            print(f"{len(self.mcp.tools)} herramienta(s) disponible(s)")
            for i, tool in enumerate(self.mcp.tools):
                print(f"   - Herramienta {i + 1}: {tool.__name__}")
        else:
            print("No hay herramientas registradas")

        # Test recursos
        if self.mcp.resources:
            print(f"{len(self.mcp.resources)} recurso(s) disponible(s)")
            for name, func in self.mcp.resources:
                print(f"   - Recurso: {name}")
        else:
            print("No hay recursos registrados")

        # Test prompts
        if self.mcp.prompts:
            print(f"{len(self.mcp.prompts)} prompt(s) disponible(s)")
            for name, func in self.mcp.prompts:
                print(f"   - Prompt: {name}")
        else:
            print("No hay prompts registrados")

    async def run_comprehensive_test(self):
        """Ejecutar test comprehensivo"""
        print("Iniciando test comprehensivo del Track HS MCP Connector")
        print("=" * 60)

        # Configuración
        self.setup_config()
        self.setup_api_client()
        self.setup_mcp_components()

        # Tests
        await self.test_api_connection()
        self.test_error_handling()
        self.test_components_functionality()

        # Resumen
        self.print_summary()

    def print_summary(self):
        """Imprimir resumen de resultados"""
        print("\n" + "=" * 60)
        print("RESUMEN DE RESULTADOS")
        print("=" * 60)

        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results.values() if result)

        for test_name, result in self.results.items():
            status = "PASS" if result else "FAIL"
            print(f"{test_name.upper():<20} {status}")

        print("-" * 60)
        print(f"TOTAL: {passed_tests}/{total_tests} tests pasaron")

        if passed_tests == total_tests:
            print("Todos los tests pasaron! El MCP Connector está listo.")
        else:
            print("Algunos tests fallaron. Revisa la configuración.")

        print("\nPRÓXIMOS PASOS:")
        print("1. Configura credenciales reales en .env")
        print("2. Ejecuta tests unitarios: pytest tests/")
        print("3. Ejecuta tests de integración: pytest tests/integration/")
        print("4. Ejecuta tests E2E: pytest tests/e2e/")
        print("5. Despliega el servidor: python src/trackhs_mcp/server.py")


async def main():
    """Función principal"""
    print("Track HS MCP Connector - Test Local")
    print("=" * 50)

    tester = LocalTester()
    await tester.run_comprehensive_test()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTest interrumpido por el usuario")
    except Exception as e:
        print(f"\nError inesperado: {e}")
        sys.exit(1)
