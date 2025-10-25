"""
Tests reales contra la API de TrackHS para search_units
Requiere credenciales válidas y conexión a internet
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import pytest

# Agregar src al path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport

from trackhs_mcp.exceptions import APIError, AuthenticationError, ConnectionError
from trackhs_mcp.server import mcp


class TestSearchUnitsAPIReal:
    """Tests reales contra la API de TrackHS"""

    @pytest.fixture
    async def mcp_client(self):
        """Cliente MCP para tests reales"""
        transport = FastMCPTransport(mcp)
        client = Client(transport=transport)
        await client.__aenter__()
        try:
            yield client
        finally:
            await client.__aexit__(None, None, None)

    @pytest.fixture
    def api_credentials(self):
        """Verificar credenciales de API"""
        username = os.getenv("TRACKHS_USERNAME")
        password = os.getenv("TRACKHS_PASSWORD")
        base_url = os.getenv("TRACKHS_BASE_URL", "https://api.trackhs.com/api")

        if not username or not password:
            pytest.skip("TRACKHS_USERNAME y TRACKHS_PASSWORD no están configurados")

        return {"username": username, "password": password, "base_url": base_url}

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_search_units_basic_real_api(self, mcp_client, api_credentials):
        """Test básico contra API real"""
        result = await mcp_client.call_tool(name="search_units", arguments={})

        # Verificar estructura básica de respuesta
        assert result.data is not None
        assert "page" in result.data
        assert "page_count" in result.data
        assert "page_size" in result.data
        assert "total_items" in result.data
        assert "_embedded" in result.data
        assert "_links" in result.data
        assert "units" in result.data["_embedded"]

        # Verificar que es un número válido
        assert isinstance(result.data["total_items"], int)
        assert result.data["total_items"] >= 0

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_search_units_pagination_real_api(self, mcp_client, api_credentials):
        """Test de paginación contra API real"""
        # Test primera página
        result1 = await mcp_client.call_tool(
            name="search_units", arguments={"page": 1, "size": 5}
        )

        assert result1.data["page"] == 1
        assert result1.data["page_size"] == 5

        # Si hay más páginas, test segunda página
        if result1.data["page_count"] > 1:
            result2 = await mcp_client.call_tool(
                name="search_units", arguments={"page": 2, "size": 5}
            )

            assert result2.data["page"] == 2
            assert result2.data["page_size"] == 5

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_search_units_filters_real_api(self, mcp_client, api_credentials):
        """Test de filtros contra API real"""
        # Test con diferentes filtros
        test_cases = [
            {"bedrooms": 1},
            {"bedrooms": 2},
            {"bathrooms": 1},
            {"bathrooms": 2},
            {"is_active": 1},
            {"is_bookable": 1},
            {"bedrooms": 2, "bathrooms": 1},
            {"is_active": 1, "is_bookable": 1},
        ]

        for filters in test_cases:
            result = await mcp_client.call_tool(name="search_units", arguments=filters)

            assert result.data is not None
            assert "total_items" in result.data

            # Si hay unidades, verificar que cumplen los filtros
            if result.data["total_items"] > 0:
                units = result.data["_embedded"]["units"]
                for unit in units:
                    if "bedrooms" in filters:
                        assert unit["bedrooms"] == filters["bedrooms"]
                    if "bathrooms" in filters:
                        assert unit["bathrooms"] == filters["bathrooms"]
                    if "is_active" in filters:
                        assert unit["is_active"] == bool(filters["is_active"])
                    if "is_bookable" in filters:
                        assert unit["is_bookable"] == bool(filters["is_bookable"])

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_search_units_search_text_real_api(self, mcp_client, api_credentials):
        """Test de búsqueda de texto contra API real"""
        # Test con diferentes términos de búsqueda
        search_terms = ["casa", "apartment", "villa", "suite", "beach", "downtown"]

        for term in search_terms:
            result = await mcp_client.call_tool(
                name="search_units", arguments={"search": term}
            )

            assert result.data is not None
            assert "total_items" in result.data

            # Si hay resultados, verificar que contienen el término
            if result.data["total_items"] > 0:
                units = result.data["_embedded"]["units"]
                for unit in units:
                    # El término debería estar en el nombre, descripción o código
                    unit_text = f"{unit.get('name', '')} {unit.get('code', '')} {unit.get('description', '')}".lower()
                    assert term.lower() in unit_text

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_search_units_edge_cases_real_api(self, mcp_client, api_credentials):
        """Test de casos límite contra API real"""
        # Test con tamaño máximo
        result = await mcp_client.call_tool(name="search_units", arguments={"size": 25})

        assert result.data["page_size"] == 25
        assert len(result.data["_embedded"]["units"]) <= 25

        # Test con página alta
        result = await mcp_client.call_tool(
            name="search_units", arguments={"page": 100}
        )

        # Debería devolver página vacía o error
        assert result.data is not None

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_search_units_unicode_real_api(self, mcp_client, api_credentials):
        """Test de caracteres unicode contra API real"""
        # Test con términos en español
        spanish_terms = ["casa", "apartamento", "villa", "playa", "centro"]

        for term in spanish_terms:
            result = await mcp_client.call_tool(
                name="search_units", arguments={"search": term}
            )

            assert result.data is not None

            # Si hay resultados, verificar que se manejan correctamente los unicode
            if result.data["total_items"] > 0:
                units = result.data["_embedded"]["units"]
                for unit in units:
                    # Verificar que los strings se manejan correctamente
                    assert isinstance(unit.get("name", ""), str)
                    assert isinstance(unit.get("address", ""), str)

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_search_units_performance_real_api(self, mcp_client, api_credentials):
        """Test de rendimiento contra API real"""
        import time

        # Test de tiempo de respuesta
        start_time = time.time()
        result = await mcp_client.call_tool(name="search_units", arguments={"size": 10})
        end_time = time.time()

        response_time = end_time - start_time

        # La respuesta debería ser rápida (menos de 5 segundos)
        assert (
            response_time < 5.0
        ), f"Tiempo de respuesta muy lento: {response_time:.2f}s"

        assert result.data is not None

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_search_units_concurrent_requests_real_api(
        self, mcp_client, api_credentials
    ):
        """Test de requests concurrentes contra API real"""
        # Ejecutar múltiples requests concurrentes
        tasks = [
            mcp_client.call_tool(name="search_units", arguments={"page": i, "size": 5})
            for i in range(1, 6)
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Verificar que todos los requests se completaron
        assert len(results) == 5

        for result in results:
            if isinstance(result, Exception):
                # Algunos requests pueden fallar si no hay suficientes páginas
                continue
            assert result.data is not None

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_search_units_data_consistency_real_api(
        self, mcp_client, api_credentials
    ):
        """Test de consistencia de datos contra API real"""
        # Hacer el mismo request múltiples veces
        results = []
        for i in range(3):
            result = await mcp_client.call_tool(
                name="search_units", arguments={"page": 1, "size": 10}
            )
            results.append(result.data)

        # Los resultados deberían ser consistentes
        for i in range(1, len(results)):
            assert results[i]["total_items"] == results[0]["total_items"]
            assert results[i]["page_count"] == results[0]["page_count"]

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_search_units_error_handling_real_api(
        self, mcp_client, api_credentials
    ):
        """Test de manejo de errores contra API real"""
        # Test con parámetros inválidos
        with pytest.raises(Exception):
            await mcp_client.call_tool(
                name="search_units", arguments={"page": 0}  # Inválido
            )

        with pytest.raises(Exception):
            await mcp_client.call_tool(
                name="search_units", arguments={"size": 0}  # Inválido
            )

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_search_units_unit_structure_real_api(
        self, mcp_client, api_credentials
    ):
        """Test de estructura de unidades contra API real"""
        result = await mcp_client.call_tool(name="search_units", arguments={"size": 1})

        if result.data["total_items"] > 0:
            unit = result.data["_embedded"]["units"][0]

            # Verificar campos obligatorios
            required_fields = [
                "id",
                "name",
                "code",
                "bedrooms",
                "bathrooms",
                "max_occupancy",
                "area",
                "address",
                "amenities",
                "is_active",
                "is_bookable",
            ]

            for field in required_fields:
                assert field in unit, f"Campo obligatorio '{field}' no encontrado"

            # Verificar tipos de datos
            assert isinstance(unit["id"], int)
            assert isinstance(unit["name"], str)
            assert isinstance(unit["code"], str)
            assert isinstance(unit["bedrooms"], int)
            assert isinstance(unit["bathrooms"], int)
            assert isinstance(unit["max_occupancy"], int)
            assert isinstance(unit["area"], (int, float))
            assert isinstance(unit["address"], str)
            assert isinstance(unit["amenities"], list)
            assert isinstance(unit["is_active"], bool)
            assert isinstance(unit["is_bookable"], bool)

            # Verificar rangos válidos
            assert unit["bedrooms"] >= 0
            assert unit["bathrooms"] >= 0
            assert unit["max_occupancy"] > 0
            assert unit["area"] >= 0

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_search_units_links_structure_real_api(
        self, mcp_client, api_credentials
    ):
        """Test de estructura de enlaces contra API real"""
        result = await mcp_client.call_tool(name="search_units", arguments={})

        # Verificar estructura de enlaces
        assert "_links" in result.data
        links = result.data["_links"]

        # Debería tener al menos self
        assert "self" in links
        assert "href" in links["self"]

        # Si hay múltiples páginas, debería tener first y last
        if result.data["page_count"] > 1:
            assert "first" in links
            assert "last" in links
            assert "href" in links["first"]
            assert "href" in links["last"]

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_search_units_comprehensive_real_api(
        self, mcp_client, api_credentials
    ):
        """Test comprensivo contra API real"""
        # Test con todos los parámetros posibles
        result = await mcp_client.call_tool(
            name="search_units",
            arguments={
                "page": 1,
                "size": 10,
                "search": "test",
                "bedrooms": 2,
                "bathrooms": 1,
                "is_active": 1,
                "is_bookable": 1,
            },
        )

        assert result.data is not None

        # Verificar que la respuesta tiene la estructura esperada
        assert "page" in result.data
        assert "page_count" in result.data
        assert "page_size" in result.data
        assert "total_items" in result.data
        assert "_embedded" in result.data
        assert "_links" in result.data

        # Verificar que los parámetros se aplicaron correctamente
        assert result.data["page"] == 1
        assert result.data["page_size"] == 10

        # Si hay unidades, verificar que cumplen los criterios
        if result.data["total_items"] > 0:
            units = result.data["_embedded"]["units"]
            for unit in units:
                assert unit["bedrooms"] == 2
                assert unit["bathrooms"] == 1
                assert unit["is_active"] is True
                assert unit["is_bookable"] is True

                # El término de búsqueda debería estar en algún campo
                unit_text = f"{unit.get('name', '')} {unit.get('code', '')} {unit.get('description', '')}".lower()
                assert "test" in unit_text
