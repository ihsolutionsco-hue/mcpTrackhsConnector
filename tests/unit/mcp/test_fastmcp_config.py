"""
Tests para verificar la configuración declarativa de FastMCP
"""

import json
from pathlib import Path

import pytest


class TestFastMCPConfig:
    """Tests para configuración declarativa"""

    def test_fastmcp_json_exists(self):
        """Test de que fastmcp.json existe"""
        config_path = Path("fastmcp.json")
        assert config_path.exists(), "fastmcp.json no existe"

    def test_fastmcp_json_valid_schema(self):
        """Test de que fastmcp.json tiene schema válido"""
        config_path = Path("fastmcp.json")

        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        # Verificar que tiene schema
        assert "$schema" in config, "fastmcp.json debe incluir $schema"
        assert "gofastmcp.com" in config["$schema"], "Schema debe ser de FastMCP"

    def test_fastmcp_json_required_fields(self):
        """Test de que fastmcp.json tiene campos requeridos"""
        config_path = Path("fastmcp.json")

        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        # Verificar campos requeridos
        required_fields = ["source", "transport", "host", "port"]
        for field in required_fields:
            assert field in config, f"Campo {field} faltante en fastmcp.json"

        # Verificar source
        assert "path" in config["source"], "source debe tener path"
        assert "entrypoint" in config["source"], "source debe tener entrypoint"

        # Verificar que apunta al archivo correcto
        assert config["source"]["path"] == "src/trackhs_mcp/__main__.py"
        assert config["source"]["entrypoint"] == "mcp"

    def test_fastmcp_json_transport_config(self):
        """Test de configuración de transporte"""
        config_path = Path("fastmcp.json")

        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        # Verificar configuración de transporte
        assert config["transport"] == "http", "Transport debe ser http"
        assert config["host"] == "0.0.0.0", "Host debe ser 0.0.0.0"
        assert config["port"] == 8080, "Puerto debe ser 8080"

    def test_fastmcp_json_cors_config(self):
        """Test de configuración CORS"""
        config_path = Path("fastmcp.json")

        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        # Verificar configuración CORS
        assert "cors" in config, "Debe tener configuración CORS"
        cors = config["cors"]

        assert "origins" in cors, "CORS debe tener origins"
        assert "credentials" in cors, "CORS debe tener credentials"
        assert "methods" in cors, "CORS debe tener methods"

        # Verificar origins específicos
        expected_origins = [
            "https://elevenlabs.io",
            "https://api.elevenlabs.io",
            "https://app.elevenlabs.io",
            "https://claude.ai",
            "https://app.claude.ai",
        ]

        for origin in expected_origins:
            assert origin in cors["origins"], f"Origin {origin} faltante en CORS"

    def test_fastmcp_json_health_check_config(self):
        """Test de configuración de health check"""
        config_path = Path("fastmcp.json")

        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        # Verificar configuración de health check
        assert "health_check" in config, "Debe tener configuración de health check"
        health_check = config["health_check"]

        assert health_check["enabled"] is True, "Health check debe estar habilitado"
        assert health_check["endpoint"] == "/health", "Endpoint debe ser /health"
        assert health_check["timeout"] == 30, "Timeout debe ser 30"

    def test_fastmcp_json_logging_config(self):
        """Test de configuración de logging"""
        config_path = Path("fastmcp.json")

        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        # Verificar configuración de logging
        assert "logging" in config, "Debe tener configuración de logging"
        logging = config["logging"]

        assert logging["level"] == "INFO", "Log level debe ser INFO"
        assert logging["format"] == "json", "Log format debe ser json"

    def test_fastmcp_json_environment_config(self):
        """Test de configuración de environment"""
        config_path = Path("fastmcp.json")

        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        # Verificar configuración de environment
        assert "environment" in config, "Debe tener configuración de environment"
        environment = config["environment"]

        assert environment["type"] == "standard", "Environment type debe ser standard"
