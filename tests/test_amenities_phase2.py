"""
Tests unitarios para la función search_amenities mejorada - Fase 2.
Implementa testing completo para el servicio y logging estructurado.
"""

import json
from unittest.mock import Mock, patch

import httpx
import pytest
from fastmcp.exceptions import ToolError
from pydantic import ValidationError

from src.trackhs_mcp.amenities_logging import AmenitiesLogger, LogLevel
from src.trackhs_mcp.amenities_service import AmenitiesService


class TestAmenitiesService:
    """Tests para el servicio de amenidades."""

    def test_init_with_api_client(self):
        """Test inicialización con cliente API."""
        mock_client = Mock()
        service = AmenitiesService(mock_client)

        assert service.api_client == mock_client
        assert service.error_handler is not None

    def test_init_without_api_client(self):
        """Test inicialización sin cliente API."""
        service = AmenitiesService(None)

        assert service.api_client is None
        assert service.error_handler is not None

    def test_search_amenities_success(self):
        """Test búsqueda exitosa de amenidades."""
        mock_client = Mock()
        mock_client.get.return_value = {
            "total_items": 5,
            "page": 1,
            "page_size": 10,
            "_embedded": {
                "amenities": [{"id": 1, "name": "WiFi"}, {"id": 2, "name": "Pool"}]
            },
        }

        service = AmenitiesService(mock_client)
        result = service.search_amenities(page=1, size=10, search="wifi")

        assert result["total_items"] == 5
        assert len(result["_embedded"]["amenities"]) == 2

        # Verificar que se llamó con parámetros correctos
        mock_client.get.assert_called_once_with(
            "api/pms/units/amenities", {"page": 1, "size": 10, "search": "wifi"}
        )

    def test_search_amenities_no_api_client(self):
        """Test búsqueda sin cliente API."""
        service = AmenitiesService(None)

        with pytest.raises(ToolError) as exc_info:
            service.search_amenities(page=1, size=10)

        assert "no disponible" in str(exc_info.value).lower()

    def test_search_amenities_validation_error(self):
        """Test error de validación de parámetros."""
        mock_client = Mock()
        service = AmenitiesService(mock_client)

        with pytest.raises(ToolError) as exc_info:
            service.search_amenities(page=-1)  # Valor inválido

        assert "inválidos" in str(exc_info.value).lower()

    def test_search_amenities_http_error(self):
        """Test error HTTP."""
        mock_client = Mock()
        mock_client.get.side_effect = httpx.HTTPStatusError(
            "Unauthorized", request=Mock(), response=Mock(status_code=401)
        )

        service = AmenitiesService(mock_client)

        with pytest.raises(ToolError) as exc_info:
            service.search_amenities(page=1, size=10)

        assert "autenticación" in str(exc_info.value).lower()

    def test_get_amenities_summary(self):
        """Test obtención de resumen de amenidades."""
        mock_client = Mock()
        service = AmenitiesService(mock_client)

        result = {
            "total_items": 10,
            "page": 1,
            "page_size": 5,
            "_embedded": {
                "amenities": [
                    {"id": 1, "name": "WiFi"},
                    {"id": 2, "name": "Pool"},
                    {"id": 3, "name": "Gym"},
                    {"id": 4, "name": "Spa"},
                    {"id": 5, "name": "Restaurant"},
                ]
            },
        }

        summary = service.get_amenities_summary(result)

        assert summary["total_items"] == 10
        assert summary["page"] == 1
        assert summary["page_size"] == 5
        assert summary["amenities_count"] == 5
        assert summary["has_amenities"] is True
        assert len(summary["amenities"]) == 5  # Primeros 5 para preview

    def test_get_amenities_summary_empty(self):
        """Test resumen con resultado vacío."""
        mock_client = Mock()
        service = AmenitiesService(mock_client)

        result = {
            "total_items": 0,
            "page": 1,
            "page_size": 10,
            "_embedded": {"amenities": []},
        }

        summary = service.get_amenities_summary(result)

        assert summary["total_items"] == 0
        assert summary["amenities_count"] == 0
        assert summary["has_amenities"] is False
        assert len(summary["amenities"]) == 0

    def test_get_amenities_summary_invalid(self):
        """Test resumen con resultado inválido."""
        mock_client = Mock()
        service = AmenitiesService(mock_client)

        summary = service.get_amenities_summary("invalid")

        assert "error" in summary
        assert summary["error"] == "Resultado inválido"

    def test_validate_search_parameters_success(self):
        """Test validación exitosa de parámetros."""
        mock_client = Mock()
        service = AmenitiesService(mock_client)

        params = service.validate_search_parameters(
            page=1, size=10, search="wifi", isPublic=1
        )

        assert params.page == 1
        assert params.size == 10
        assert params.search == "wifi"
        assert params.isPublic == 1

    def test_validate_search_parameters_error(self):
        """Test error de validación de parámetros."""
        mock_client = Mock()
        service = AmenitiesService(mock_client)

        with pytest.raises(ToolError):
            service.validate_search_parameters(page=-1)

    def test_get_available_sort_columns(self):
        """Test obtención de columnas de ordenamiento disponibles."""
        mock_client = Mock()
        service = AmenitiesService(mock_client)

        columns = service.get_available_sort_columns()

        expected = [
            "id",
            "order",
            "isPublic",
            "publicSearchable",
            "isFilterable",
            "createdAt",
        ]
        assert columns == expected

    def test_get_available_sort_directions(self):
        """Test obtención de direcciones de ordenamiento disponibles."""
        mock_client = Mock()
        service = AmenitiesService(mock_client)

        directions = service.get_available_sort_directions()

        expected = ["asc", "desc"]
        assert directions == expected

    def test_get_ota_platforms(self):
        """Test obtención de plataformas OTA soportadas."""
        mock_client = Mock()
        service = AmenitiesService(mock_client)

        platforms = service.get_ota_platforms()

        expected = ["homeawayType", "airbnbType", "tripadvisorType", "marriottType"]
        assert platforms == expected


class TestAmenitiesLogger:
    """Tests para el logger estructurado de amenidades."""

    def test_init(self):
        """Test inicialización del logger."""
        logger = AmenitiesLogger("test_context")

        assert logger.context == "test_context"
        assert logger.logger is not None

    def test_create_log_entry(self):
        """Test creación de entrada de log."""
        logger = AmenitiesLogger("test_context")

        entry = logger._create_log_entry(
            LogLevel.INFO,
            "Test message",
            "test_operation",
            param1="value1",
            param2="value2",
        )

        assert entry["level"] == "INFO"
        assert entry["context"] == "test_context"
        assert entry["operation"] == "test_operation"
        assert entry["message"] == "Test message"
        assert entry["param1"] == "value1"
        assert entry["param2"] == "value2"
        assert "timestamp" in entry

    @patch("src.trackhs_mcp.amenities_logging.logger")
    def test_log_search_start(self, mock_logger):
        """Test log de inicio de búsqueda."""
        logger = AmenitiesLogger("test_context")

        logger.log_search_start(
            page=1, size=10, search_params={"search": "wifi", "isPublic": 1}
        )

        # Verificar que se llamó el logger
        mock_logger.info.assert_called_once()

        # Verificar contenido del log
        call_args = mock_logger.info.call_args[0][0]
        log_data = json.loads(call_args)

        assert log_data["level"] == "INFO"
        assert log_data["context"] == "test_context"
        assert log_data["operation"] == "search_start"
        assert log_data["page"] == 1
        assert log_data["size"] == 10
        assert log_data["search_params"]["search"] == "wifi"

    @patch("src.trackhs_mcp.amenities_logging.logger")
    def test_log_search_success(self, mock_logger):
        """Test log de búsqueda exitosa."""
        logger = AmenitiesLogger("test_context")

        logger.log_search_success(
            total_items=5, page=1, size=10, response_time_ms=150.5
        )

        # Verificar que se llamó el logger
        mock_logger.info.assert_called_once()

        # Verificar contenido del log
        call_args = mock_logger.info.call_args[0][0]
        log_data = json.loads(call_args)

        assert log_data["level"] == "INFO"
        assert log_data["operation"] == "search_success"
        assert log_data["total_items"] == 5
        assert log_data["response_time_ms"] == 150.5

    @patch("src.trackhs_mcp.amenities_logging.logger")
    def test_log_validation_error(self, mock_logger):
        """Test log de error de validación."""
        logger = AmenitiesLogger("test_context")

        logger.log_validation_error(
            error_message="Invalid parameter",
            parameters={"page": -1},
            validation_errors=[{"field": "page", "error": "Must be positive"}],
        )

        # Verificar que se llamó el logger
        mock_logger.warning.assert_called_once()

        # Verificar contenido del log
        call_args = mock_logger.warning.call_args[0][0]
        log_data = json.loads(call_args)

        assert log_data["level"] == "WARNING"
        assert log_data["operation"] == "validation_error"
        assert "Invalid parameter" in log_data["message"]

    @patch("src.trackhs_mcp.amenities_logging.logger")
    def test_log_http_error(self, mock_logger):
        """Test log de error HTTP."""
        logger = AmenitiesLogger("test_context")

        # Test error 401 (warning)
        logger.log_http_error(
            status_code=401,
            error_message="Unauthorized",
            parameters={"page": 1},
            response_text="Invalid credentials",
        )

        mock_logger.warning.assert_called_once()

        # Test error 500 (error)
        logger.log_http_error(
            status_code=500,
            error_message="Internal Server Error",
            parameters={"page": 1},
        )

        mock_logger.error.assert_called_once()

    @patch("src.trackhs_mcp.amenities_logging.logger")
    def test_log_connection_error(self, mock_logger):
        """Test log de error de conexión."""
        logger = AmenitiesLogger("test_context")

        logger.log_connection_error(
            error_message="Connection failed", parameters={"page": 1}
        )

        # Verificar que se llamó el logger
        mock_logger.error.assert_called_once()

        # Verificar contenido del log
        call_args = mock_logger.error.call_args[0][0]
        log_data = json.loads(call_args)

        assert log_data["level"] == "ERROR"
        assert log_data["operation"] == "connection_error"
        assert "Connection failed" in log_data["message"]

    @patch("src.trackhs_mcp.amenities_logging.logger")
    def test_log_performance_metrics(self, mock_logger):
        """Test log de métricas de rendimiento."""
        logger = AmenitiesLogger("test_context")

        logger.log_performance_metrics(
            operation="search_amenities",
            duration_ms=250.5,
            total_items=100,
            page_size=10,
            cache_hit=True,
            api_calls=1,
        )

        # Verificar que se llamó el logger
        mock_logger.info.assert_called_once()

        # Verificar contenido del log
        call_args = mock_logger.info.call_args[0][0]
        log_data = json.loads(call_args)

        assert log_data["level"] == "INFO"
        assert log_data["operation"] == "performance_metrics"
        assert log_data["duration_ms"] == 250.5
        assert log_data["total_items"] == 100
        assert log_data["cache_hit"] is True
        assert log_data["api_calls"] == 1


class TestAmenitiesIntegrationPhase2:
    """Tests de integración para Fase 2."""

    def test_search_amenities_with_logging(self):
        """Test búsqueda de amenidades con logging estructurado usando servicio."""
        from src.trackhs_mcp.amenities_logging import AmenitiesLogger
        from src.trackhs_mcp.amenities_service import AmenitiesService

        # Mock del cliente API
        mock_client = Mock()
        mock_client.get.return_value = {
            "total_items": 5,
            "page": 1,
            "page_size": 10,
            "_embedded": {
                "amenities": [{"id": 1, "name": "WiFi"}, {"id": 2, "name": "Pool"}]
            },
        }

        # Crear servicio y logger
        service = AmenitiesService(mock_client)
        logger = AmenitiesLogger("test_context")

        # Mock del logger para verificar llamadas
        with (
            patch.object(logger, "log_search_start") as mock_start,
            patch.object(logger, "log_search_success") as mock_success,
        ):

            # Simular la lógica de la función principal
            logger.log_search_start(page=1, size=10, search_params={"search": "wifi"})

            result = service.search_amenities(page=1, size=10, search="wifi")

            logger.log_search_success(
                total_items=result.get("total_items", 0), page=1, size=10
            )

        assert result["total_items"] == 5

        # Verificar que se llamaron los métodos de logging
        mock_start.assert_called_once()
        mock_success.assert_called_once()

    def test_amenities_service_with_all_parameters(self):
        """Test servicio con todos los parámetros."""
        mock_client = Mock()
        mock_client.get.return_value = {
            "total_items": 1,
            "page": 1,
            "page_size": 5,
            "_embedded": {"amenities": []},
        }

        service = AmenitiesService(mock_client)

        result = service.search_amenities(
            page=1,
            size=5,
            sortColumn="id",
            sortDirection="asc",
            search="wifi",
            groupId=1,
            isPublic=1,
            publicSearchable=1,
            isFilterable=1,
            homeawayType="pool%",
            airbnbType="ac",
            tripadvisorType="wifi%",
            marriottType="pool%",
        )

        # Verificar que se llamó con todos los parámetros
        call_args = mock_client.get.call_args
        assert call_args[0][0] == "api/pms/units/amenities"

        params = call_args[0][1]
        assert params["page"] == 1
        assert params["size"] == 5
        assert params["sortColumn"] == "id"
        assert params["sortDirection"] == "asc"
        assert params["search"] == "wifi"
        assert params["groupId"] == 1
        assert params["isPublic"] == 1
        assert params["publicSearchable"] == 1
        assert params["isFilterable"] == 1
        assert params["homeawayType"] == "pool%"
        assert params["airbnbType"] == "ac"
        assert params["tripadvisorType"] == "wifi%"
        assert params["marriottType"] == "pool%"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
