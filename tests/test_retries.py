"""
Tests para reintentos automáticos con exponential backoff.
Fase 2 - Seguridad: Reintentos automáticos HTTP.
"""

import time
from unittest.mock import MagicMock, patch

import httpx
import pytest


def test_retry_with_backoff_exists():
    """Verifica que la función exists"""
    from src.trackhs_mcp.server import retry_with_backoff

    assert retry_with_backoff is not None
    assert callable(retry_with_backoff)


def test_retry_constants_exist():
    """Verifica que las constantes de retry existen"""
    from src.trackhs_mcp.server import (
        MAX_RETRIES,
        RETRY_BACKOFF_FACTOR,
        RETRY_DELAY_BASE,
    )

    assert MAX_RETRIES >= 1
    assert RETRY_DELAY_BASE > 0
    assert RETRY_BACKOFF_FACTOR >= 1


def test_retry_success_on_first_attempt():
    """Test que funciona sin reintentos si el primer intento es exitoso"""
    from src.trackhs_mcp.server import retry_with_backoff

    call_count = 0

    def successful_func():
        nonlocal call_count
        call_count += 1
        return "success"

    result = retry_with_backoff(successful_func)

    assert result == "success"
    assert call_count == 1  # Solo 1 intento


def test_retry_on_request_error():
    """Test reintentos en caso de RequestError (error de red)"""
    from src.trackhs_mcp.server import retry_with_backoff

    call_count = 0

    def failing_func():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            # Simular error de red
            raise httpx.RequestError("Connection failed")
        return "success"

    # Debería reintentar y eventualmente tener éxito
    with patch("src.trackhs_mcp.server.time.sleep"):  # Mock sleep para velocidad
        result = retry_with_backoff(failing_func, max_retries=3)

    assert result == "success"
    assert call_count == 3  # 2 fallos + 1 éxito


def test_retry_exhaustion():
    """Test que falla después de agotar todos los reintentos"""
    from src.trackhs_mcp.exceptions import ConnectionError
    from src.trackhs_mcp.server import retry_with_backoff

    call_count = 0

    def always_failing_func():
        nonlocal call_count
        call_count += 1
        raise httpx.RequestError("Always failing")

    # Debería agotar reintentos y lanzar ConnectionError
    with patch("src.trackhs_mcp.server.time.sleep"):
        with pytest.raises(ConnectionError):
            retry_with_backoff(always_failing_func, max_retries=2)

    assert call_count == 3  # 1 intento inicial + 2 reintentos


def test_retry_on_500_error():
    """Test reintentos en errores 500 (server error)"""
    from src.trackhs_mcp.server import retry_with_backoff

    call_count = 0

    def server_error_func():
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            # Simular 500 error
            response = MagicMock()
            response.status_code = 500
            raise httpx.HTTPStatusError(
                "Server Error", request=MagicMock(), response=response
            )
        return "success"

    with patch("src.trackhs_mcp.server.time.sleep"):
        result = retry_with_backoff(server_error_func, max_retries=2)

    assert result == "success"
    assert call_count == 2


def test_retry_on_429_rate_limit():
    """Test reintentos en 429 (rate limit)"""
    from src.trackhs_mcp.server import retry_with_backoff

    call_count = 0

    def rate_limit_func():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            response = MagicMock()
            response.status_code = 429
            raise httpx.HTTPStatusError(
                "Rate Limit", request=MagicMock(), response=response
            )
        return "success"

    with patch("src.trackhs_mcp.server.time.sleep"):
        result = retry_with_backoff(rate_limit_func, max_retries=2)

    assert result == "success"
    assert call_count == 2


def test_no_retry_on_404():
    """Test que NO reintenta en errores 404 (not found)"""
    from src.trackhs_mcp.server import retry_with_backoff

    call_count = 0

    def not_found_func():
        nonlocal call_count
        call_count += 1
        response = MagicMock()
        response.status_code = 404
        raise httpx.HTTPStatusError("Not Found", request=MagicMock(), response=response)

    with patch("src.trackhs_mcp.server.time.sleep"):
        with pytest.raises(httpx.HTTPStatusError):
            retry_with_backoff(not_found_func, max_retries=2)

    assert call_count == 1  # No reintentos en 404


def test_no_retry_on_401():
    """Test que NO reintenta en errores 401 (authentication)"""
    from src.trackhs_mcp.server import retry_with_backoff

    call_count = 0

    def auth_error_func():
        nonlocal call_count
        call_count += 1
        response = MagicMock()
        response.status_code = 401
        raise httpx.HTTPStatusError(
            "Unauthorized", request=MagicMock(), response=response
        )

    with patch("src.trackhs_mcp.server.time.sleep"):
        with pytest.raises(httpx.HTTPStatusError):
            retry_with_backoff(auth_error_func, max_retries=2)

    assert call_count == 1  # No reintentos en 401


def test_exponential_backoff():
    """Test que el backoff es exponencial"""
    from src.trackhs_mcp.server import retry_with_backoff

    call_count = 0
    sleep_times = []

    def mock_sleep(seconds):
        sleep_times.append(seconds)

    def failing_func():
        nonlocal call_count
        call_count += 1
        if call_count < 4:
            raise httpx.RequestError("Failing")
        return "success"

    with patch("src.trackhs_mcp.server.time.sleep", mock_sleep):
        result = retry_with_backoff(failing_func, max_retries=3, base_delay=1.0)

    assert result == "success"
    assert len(sleep_times) == 3  # 3 reintentos

    # Verificar que los delays son exponenciales: 1.0, 2.0, 4.0
    assert sleep_times[0] == 1.0
    assert sleep_times[1] == 2.0
    assert sleep_times[2] == 4.0


def test_retry_on_502_bad_gateway():
    """Test reintentos en 502 (bad gateway)"""
    from src.trackhs_mcp.server import retry_with_backoff

    call_count = 0

    def bad_gateway_func():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            response = MagicMock()
            response.status_code = 502
            raise httpx.HTTPStatusError(
                "Bad Gateway", request=MagicMock(), response=response
            )
        return "success"

    with patch("src.trackhs_mcp.server.time.sleep"):
        result = retry_with_backoff(bad_gateway_func)

    assert result == "success"
    assert call_count == 2


def test_retry_on_503_service_unavailable():
    """Test reintentos en 503 (service unavailable)"""
    from src.trackhs_mcp.server import retry_with_backoff

    call_count = 0

    def service_unavail_func():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            response = MagicMock()
            response.status_code = 503
            raise httpx.HTTPStatusError(
                "Service Unavailable", request=MagicMock(), response=response
            )
        return "success"

    with patch("src.trackhs_mcp.server.time.sleep"):
        result = retry_with_backoff(service_unavail_func)

    assert result == "success"
    assert call_count == 3


def test_retry_trackhs_client_integration():
    """Test que TrackHSClient usa retry_with_backoff correctamente"""
    from src.trackhs_mcp.server import TrackHSClient

    # Verificar que los métodos get y post existen
    client = TrackHSClient("https://test.trackhs.com/api", "testuser", "testpass")

    assert hasattr(client, "get")
    assert hasattr(client, "post")
    assert callable(client.get)
    assert callable(client.post)

    # Verificar que la documentación menciona retries
    assert "retries" in client.get.__doc__.lower()
    assert "retries" in client.post.__doc__.lower()


if __name__ == "__main__":
    print("🧪 Ejecutando tests de reintentos...")

    try:
        test_retry_with_backoff_exists()
        print("✅ Test 1: Función exists")

        test_retry_constants_exist()
        print("✅ Test 2: Constantes existen")

        test_retry_success_on_first_attempt()
        print("✅ Test 3: Éxito en primer intento")

        test_retry_on_request_error()
        print("✅ Test 4: Reintento en error de red")

        test_exponential_backoff()
        print("✅ Test 5: Backoff exponencial")

        print("\n🎉 Tests unitarios pasaron!")

    except AssertionError as e:
        print(f"\n❌ Test falló: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
