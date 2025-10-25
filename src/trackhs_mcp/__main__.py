"""
FastMCP Cloud entrypoint for TrackHS MCP Connector
This file is required by FastMCP Cloud deployment
"""

import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastmcp import FastMCP

# Agregar el directorio src al PYTHONPATH para que FastMCP pueda encontrar el módulo
current_dir = Path(__file__).parent
src_dir = current_dir.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Configurar logging estándar para FastMCP Cloud
import logging

# Configurar logging específico para FastMCP Cloud
import sys

# Usar middleware nativo de FastMCP
from fastmcp.server.middleware.logging import (
    LoggingMiddleware,
    StructuredLoggingMiddleware,
)
from fastmcp.server.middleware.timing import TimingMiddleware

from trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
from trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from trackhs_mcp.infrastructure.middleware import TrackHSErrorHandlingMiddleware
from trackhs_mcp.infrastructure.middleware.fastmcp_cloud_logging import (
    FastMCPCloudLoggingMiddleware,
)
from trackhs_mcp.infrastructure.prompts import register_all_prompts
from trackhs_mcp.infrastructure.tools.registry import register_all_tools
from trackhs_mcp.infrastructure.tools.resources import register_all_resources

# Configurar logging que funcione con FastMCP Cloud
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),  # Asegurar que vaya a stdout
        logging.StreamHandler(sys.stderr),  # También a stderr para captura
    ],
    force=True,  # Forzar reconfiguración
)

# Configurar logger principal
logger = logging.getLogger("trackhs_mcp")
logger.setLevel(logging.DEBUG)

# Configurar loggers específicos de FastMCP
fastmcp_logger = logging.getLogger("fastmcp")
fastmcp_logger.setLevel(logging.DEBUG)

# Asegurar que los logs se propaguen
logger.propagate = True
fastmcp_logger.propagate = True


def main():
    """Función principal para el servidor MCP"""
    try:
        # Load environment variables
        load_dotenv()

        logger.info("Iniciando TrackHS MCP Server...")

        # Validar variables de entorno críticas
        required_vars = ["TRACKHS_USERNAME", "TRACKHS_PASSWORD"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]

        if missing_vars:
            logger.error(f"Variables de entorno faltantes: {', '.join(missing_vars)}")
            logger.error("Configura las variables de entorno en FastMCP Cloud")
            sys.exit(1)

        # Create dependencies
        logger.info("Creando configuración...")
        config = TrackHSConfig.from_env()

        logger.info("Inicializando cliente API...")
        api_client = TrackHSApiClient(config)

        # Create MCP server instance with FastMCP best practices
        logger.info("Creando servidor MCP...")

        # Usar variables de entorno estándar de FastMCP
        mask_error_details = (
            os.getenv("FASTMCP_MASK_ERROR_DETAILS", "false").lower() == "true"
        )
        include_fastmcp_meta = (
            os.getenv("FASTMCP_INCLUDE_FASTMCP_META", "true").lower() == "true"
        )
        strict_input_validation = (
            os.getenv("FASTMCP_STRICT_INPUT_VALIDATION", "true").lower() == "true"
        )

        mcp = FastMCP(
            name="TrackHS MCP Server",
            mask_error_details=mask_error_details,
            include_fastmcp_meta=include_fastmcp_meta,
        )

        # Register all components
        logger.info("Registrando componentes...")
        register_all_tools(mcp, api_client)
        register_all_resources(mcp, api_client)
        register_all_prompts(mcp, api_client)

        # Configure logging level from environment
        log_level = os.getenv("FASTMCP_LOG_LEVEL", "INFO").upper()
        logger.info(f"Configurando logging con nivel: {log_level}")

        # Add middleware (order matters: logging first, then error handling)
        logger.info("Configurando middleware...")

        # Middleware específico para FastMCP Cloud logging
        mcp.add_middleware(FastMCPCloudLoggingMiddleware())

        # Timing middleware para medir rendimiento
        mcp.add_middleware(TimingMiddleware())

        # Logging middleware básico (sin payloads para evitar problemas)
        mcp.add_middleware(LoggingMiddleware())

        # Error handling middleware personalizado
        error_middleware = TrackHSErrorHandlingMiddleware(
            include_traceback=os.getenv("FASTMCP_INCLUDE_TRACEBACK", "false").lower()
            == "true",
            transform_errors=True,
        )
        mcp.add_middleware(error_middleware)

        logger.info(f"Servidor MCP configurado correctamente (log_level={log_level})")

        # Log adicional para debugging en FastMCP Cloud
        logger.info("=== CONFIGURACIÓN DEL SERVIDOR ===")
        logger.info(f"FastMCP Version: {__import__('fastmcp').__version__}")
        logger.info(f"Log Level: {log_level}")
        logger.info(f"Mask Error Details: {mask_error_details}")
        logger.info(f"Include FastMCP Meta: {include_fastmcp_meta}")
        logger.info("=== MIDDLEWARE CONFIGURADO ===")
        logger.info("- TimingMiddleware: ✅")
        logger.info("- LoggingMiddleware: ✅")
        logger.info("- TrackHSErrorHandlingMiddleware: ✅")
        logger.info("=== SERVIDOR LISTO ===")

        # Logging específico para FastMCP Cloud - usar print para asegurar visibilidad
        print("🚀 FASTMCP CLOUD LOGGING ACTIVATED")
        print(f"📊 Server: {mcp.name}")
        print(f"🔧 Log Level: {log_level}")
        print(f"⚙️ Middleware: 3 configured")
        print("✅ Server ready for requests")

        # También usar sys.stdout directamente
        sys.stdout.write("FastMCP Cloud: Server initialization complete\n")
        sys.stdout.flush()

        return mcp

    except Exception as e:
        logger.error(f"Error al inicializar el servidor: {e}")
        sys.exit(1)


# Crear instancia del servidor
mcp = main()

# Start the server
if __name__ == "__main__":
    try:
        logger.info("🚀 INICIANDO SERVIDOR MCP...")
        logger.info("=== INFORMACIÓN DEL SERVIDOR ===")
        logger.info(f"Servidor: {mcp.name}")
        logger.info(f"Transport: HTTP")
        logger.info(f"Puerto: 8080")
        logger.info("=== INICIANDO SERVIDOR ===")

        # Logging directo para FastMCP Cloud
        print("🚀 STARTING MCP SERVER")
        print(f"📡 Server: {mcp.name}")
        print(f"🌐 Transport: HTTP")
        print(f"🔌 Port: 8080")
        print("⚡ Server starting...")
        sys.stdout.flush()

        # FastMCP Cloud maneja automáticamente el transporte HTTP
        # Especificamos transport="http" para compatibilidad con ElevenLabs y FastMCP Cloud
        # La configuración de host, puerto y CORS está en fastmcp.yaml
        mcp.run(transport="http")
    except KeyboardInterrupt:
        logger.info("🛑 Servidor detenido por el usuario")
        print("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Error en el servidor: {e}")
        print(f"❌ Server error: {e}")
        import traceback

        logger.error(f"Traceback: {traceback.format_exc()}")
        print(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)
