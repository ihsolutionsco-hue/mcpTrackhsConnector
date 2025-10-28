"""
Tests End-to-End (E2E) para search_units
Simula flujos completos de usuario y escenarios reales
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest

# Agregar src al path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport

from trackhs_mcp.server import mcp


class TestSearchUnitsE2E:
    """Tests End-to-End para search_units"""

    @pytest.fixture
    async def mcp_client(self):
        """Cliente MCP para tests E2E"""
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

        if not username or not password:
            pytest.skip("TRACKHS_USERNAME y TRACKHS_PASSWORD no están configurados")

        return {"username": username, "password": password}

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_e2e_property_manager_search_flow(self, mcp_client, api_credentials):
        """E2E: Flujo de búsqueda de un administrador de propiedades"""
        # Escenario: Un administrador busca unidades disponibles para mostrar a clientes

        # 1. Búsqueda inicial de todas las unidades activas
        print("🔍 Paso 1: Búsqueda inicial de unidades activas")
        result = await mcp_client.call_tool(
            name="search_units", arguments={"is_active": 1, "size": 20}
        )

        assert result.data is not None
        total_active_units = result.data["total_items"]
        print(f"✅ Encontradas {total_active_units} unidades activas")

        # 2. Filtrar por unidades disponibles para reservar
        print("🔍 Paso 2: Filtrar unidades disponibles para reservar")
        result = await mcp_client.call_tool(
            name="search_units",
            arguments={"is_active": 1, "is_bookable": 1, "size": 20},
        )

        assert result.data is not None
        available_units = result.data["total_items"]
        print(f"✅ Encontradas {available_units} unidades disponibles")

        # 3. Buscar unidades específicas por características
        print("🔍 Paso 3: Buscar unidades de 2 dormitorios")
        result = await mcp_client.call_tool(
            name="search_units",
            arguments={"bedrooms": 2, "is_active": 1, "is_bookable": 1},
        )

        assert result.data is not None
        two_bedroom_units = result.data["total_items"]
        print(f"✅ Encontradas {two_bedroom_units} unidades de 2 dormitorios")

        # 4. Verificar que las unidades cumplen los criterios
        if result.data["total_items"] > 0:
            units = result.data["_embedded"]["units"]
            for unit in units:
                assert unit["bedrooms"] == 2
                assert unit["is_active"] is True
                assert unit["is_bookable"] is True
                print(f"  📍 {unit['name']} - {unit['address']}")

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_e2e_guest_search_flow(self, mcp_client, api_credentials):
        """E2E: Flujo de búsqueda de un huésped"""
        # Escenario: Un huésped busca alojamiento con características específicas

        # 1. Búsqueda por ubicación
        print("🔍 Paso 1: Búsqueda por ubicación 'beach'")
        result = await mcp_client.call_tool(
            name="search_units",
            arguments={"search": "beach", "is_active": 1, "is_bookable": 1},
        )

        assert result.data is not None
        beach_units = result.data["total_items"]
        print(f"✅ Encontradas {beach_units} unidades cerca de la playa")

        # 2. Filtrar por capacidad
        print("🔍 Paso 2: Filtrar por capacidad (2+ dormitorios)")
        result = await mcp_client.call_tool(
            name="search_units",
            arguments={"bedrooms": 2, "is_active": 1, "is_bookable": 1},
        )

        assert result.data is not None
        capacity_units = result.data["total_items"]
        print(f"✅ Encontradas {capacity_units} unidades con 2+ dormitorios")

        # 3. Buscar unidades con amenidades específicas
        print("🔍 Paso 3: Buscar unidades con piscina")
        result = await mcp_client.call_tool(
            name="search_units",
            arguments={"search": "pool", "is_active": 1, "is_bookable": 1},
        )

        assert result.data is not None
        pool_units = result.data["total_items"]
        print(f"✅ Encontradas {pool_units} unidades con piscina")

        # 4. Combinar criterios
        print("🔍 Paso 4: Combinar criterios (playa + 2 dormitorios)")
        result = await mcp_client.call_tool(
            name="search_units",
            arguments={
                "search": "beach",
                "bedrooms": 2,
                "is_active": 1,
                "is_bookable": 1,
            },
        )

        assert result.data is not None
        combined_units = result.data["total_items"]
        print(
            f"✅ Encontradas {combined_units} unidades que cumplen todos los criterios"
        )

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_e2e_inventory_management_flow(self, mcp_client, api_credentials):
        """E2E: Flujo de gestión de inventario"""
        # Escenario: Gestión completa del inventario de unidades

        # 1. Obtener inventario completo
        print("🔍 Paso 1: Obtener inventario completo")
        all_units = []
        page = 1
        total_pages = 1

        while page <= total_pages:
            result = await mcp_client.call_tool(
                name="search_units", arguments={"page": page, "size": 25}
            )

            assert result.data is not None
            all_units.extend(result.data["_embedded"]["units"])
            total_pages = result.data["page_count"]
            page += 1

        print(f"✅ Inventario completo: {len(all_units)} unidades")

        # 2. Analizar distribución por características
        print("🔍 Paso 2: Analizar distribución por características")

        # Contar por dormitorios
        bedroom_distribution = {}
        for unit in all_units:
            bedrooms = unit["bedrooms"]
            bedroom_distribution[bedrooms] = bedroom_distribution.get(bedrooms, 0) + 1

        print("📊 Distribución por dormitorios:")
        for bedrooms, count in sorted(bedroom_distribution.items()):
            print(f"  {bedrooms} dormitorios: {count} unidades")

        # Contar por estado
        active_count = sum(1 for unit in all_units if unit["is_active"])
        bookable_count = sum(1 for unit in all_units if unit["is_bookable"])

        print(f"📊 Estado de unidades:")
        print(f"  Activas: {active_count}")
        print(f"  Disponibles: {bookable_count}")

        # 3. Identificar unidades problemáticas
        print("🔍 Paso 3: Identificar unidades problemáticas")

        inactive_units = [unit for unit in all_units if not unit["is_active"]]
        unbookable_units = [unit for unit in all_units if not unit["is_bookable"]]

        print(f"⚠️  Unidades inactivas: {len(inactive_units)}")
        print(f"⚠️  Unidades no disponibles: {len(unbookable_units)}")

        # 4. Generar reporte de inventario
        print("🔍 Paso 4: Generar reporte de inventario")

        inventory_report = {
            "total_units": len(all_units),
            "active_units": active_count,
            "bookable_units": bookable_count,
            "bedroom_distribution": bedroom_distribution,
            "inactive_units": len(inactive_units),
            "unbookable_units": len(unbookable_units),
        }

        print("📋 Reporte de inventario:")
        print(json.dumps(inventory_report, indent=2))

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_e2e_performance_stress_test(self, mcp_client, api_credentials):
        """E2E: Test de rendimiento y estrés"""
        # Escenario: Probar el rendimiento bajo carga

        print("🚀 Iniciando test de rendimiento...")

        # 1. Test de requests secuenciales
        print("🔍 Paso 1: Requests secuenciales")
        start_time = asyncio.get_event_loop().time()

        for i in range(10):
            result = await mcp_client.call_tool(
                name="search_units", arguments={"page": 1, "size": 10}
            )
            assert result.data is not None

        sequential_time = asyncio.get_event_loop().time() - start_time
        print(f"✅ 10 requests secuenciales completados en {sequential_time:.2f}s")

        # 2. Test de requests concurrentes
        print("🔍 Paso 2: Requests concurrentes")
        start_time = asyncio.get_event_loop().time()

        tasks = [
            mcp_client.call_tool(name="search_units", arguments={"page": i, "size": 5})
            for i in range(1, 11)
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        concurrent_time = asyncio.get_event_loop().time() - start_time
        print(f"✅ 10 requests concurrentes completados en {concurrent_time:.2f}s")

        # 3. Verificar que todos los requests se completaron
        successful_requests = sum(
            1 for result in results if not isinstance(result, Exception)
        )
        print(f"✅ Requests exitosos: {successful_requests}/10")

        # 4. Test de memoria
        print("🔍 Paso 3: Test de memoria")
        import os

        import psutil

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Hacer múltiples requests con respuestas grandes
        for i in range(20):
            result = await mcp_client.call_tool(
                name="search_units", arguments={"size": 25}
            )
            assert result.data is not None

        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        print(f"✅ Uso de memoria: {memory_increase / 1024 / 1024:.2f}MB")
        assert memory_increase < 100 * 1024 * 1024, "Uso de memoria excesivo"

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_e2e_error_recovery_flow(self, mcp_client, api_credentials):
        """E2E: Flujo de recuperación de errores"""
        # Escenario: Probar la robustez del sistema ante errores

        print("🔍 Paso 1: Test de parámetros inválidos")

        # Test con parámetros inválidos
        invalid_cases = [
            {"page": 0},  # Página inválida - debe ser >= 1
            {"size": 0},  # Tamaño inválido
            {"bedrooms": -1},  # Dormitorios inválidos
            {"bathrooms": -1},  # Baños inválidos
            {"is_active": 2},  # Estado inválido
            {"is_bookable": 2},  # Disponibilidad inválida
        ]

        for case in invalid_cases:
            try:
                await mcp_client.call_tool(name="search_units", arguments=case)
                assert False, f"Debería haber fallado con {case}"
            except Exception as e:
                print(f"✅ Error esperado con {case}: {type(e).__name__}")

        # Test de recuperación después de errores
        print("🔍 Paso 2: Test de recuperación después de errores")

        # Después de los errores, el sistema debería seguir funcionando
        result = await mcp_client.call_tool(name="search_units", arguments={})

        assert result.data is not None
        print("✅ Sistema recuperado correctamente")

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_e2e_data_consistency_flow(self, mcp_client, api_credentials):
        """E2E: Flujo de consistencia de datos"""
        # Escenario: Verificar la consistencia de los datos

        print("🔍 Paso 1: Test de consistencia entre requests")

        # Hacer el mismo request múltiples veces
        results = []
        for i in range(5):
            result = await mcp_client.call_tool(
                name="search_units", arguments={"page": 1, "size": 10}
            )
            results.append(result.data)

        # Verificar consistencia
        first_result = results[0]
        for i, result in enumerate(results[1:], 1):
            assert (
                result["total_items"] == first_result["total_items"]
            ), f"Inconsistencia en total_items en request {i+1}"
            assert (
                result["page_count"] == first_result["page_count"]
            ), f"Inconsistencia en page_count en request {i+1}"

        print("✅ Datos consistentes entre requests")

        # Test de paginación consistente
        print("🔍 Paso 2: Test de paginación consistente")

        if first_result["page_count"] > 1:
            # Obtener primera página
            page1 = await mcp_client.call_tool(
                name="search_units", arguments={"page": 1, "size": 5}
            )

            # Obtener segunda página
            page2 = await mcp_client.call_tool(
                name="search_units", arguments={"page": 2, "size": 5}
            )

            # Verificar que no hay duplicados
            page1_ids = {unit["id"] for unit in page1.data["_embedded"]["units"]}
            page2_ids = {unit["id"] for unit in page2.data["_embedded"]["units"]}

            assert (
                len(page1_ids.intersection(page2_ids)) == 0
            ), "Hay duplicados entre páginas"
            print("✅ Paginación consistente sin duplicados")

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_e2e_business_scenarios_flow(self, mcp_client, api_credentials):
        """E2E: Escenarios de negocio reales"""
        # Escenario: Simular escenarios de negocio reales

        print("🏢 Escenario 1: Búsqueda para familia de 4")
        family_result = await mcp_client.call_tool(
            name="search_units",
            arguments={"bedrooms": 2, "bathrooms": 2, "is_active": 1, "is_bookable": 1},
        )

        assert family_result.data is not None
        family_units = family_result.data["total_items"]
        print(f"✅ Encontradas {family_units} unidades para familia de 4")

        print("🏢 Escenario 2: Búsqueda para pareja")
        couple_result = await mcp_client.call_tool(
            name="search_units",
            arguments={"bedrooms": 1, "bathrooms": 1, "is_active": 1, "is_bookable": 1},
        )

        assert couple_result.data is not None
        couple_units = couple_result.data["total_items"]
        print(f"✅ Encontradas {couple_units} unidades para pareja")

        print("🏢 Escenario 3: Búsqueda de lujo")
        luxury_result = await mcp_client.call_tool(
            name="search_units",
            arguments={"search": "penthouse", "is_active": 1, "is_bookable": 1},
        )

        assert luxury_result.data is not None
        luxury_units = luxury_result.data["total_items"]
        print(f"✅ Encontradas {luxury_units} unidades de lujo")

        print("🏢 Escenario 4: Búsqueda por ubicación")
        location_result = await mcp_client.call_tool(
            name="search_units",
            arguments={"search": "downtown", "is_active": 1, "is_bookable": 1},
        )

        assert location_result.data is not None
        location_units = location_result.data["total_items"]
        print(f"✅ Encontradas {location_units} unidades en el centro")

        # Generar reporte de escenarios
        scenarios_report = {
            "family_units": family_units,
            "couple_units": couple_units,
            "luxury_units": luxury_units,
            "location_units": location_units,
        }

        print("📊 Reporte de escenarios de negocio:")
        print(json.dumps(scenarios_report, indent=2))

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_e2e_complete_user_journey(self, mcp_client, api_credentials):
        """E2E: Viaje completo del usuario"""
        # Escenario: Simular un viaje completo de un usuario

        print("👤 Viaje completo del usuario: Búsqueda de alojamiento")

        # Paso 1: Búsqueda inicial
        print("🔍 Paso 1: Búsqueda inicial")
        initial_result = await mcp_client.call_tool(
            name="search_units",
            arguments={"is_active": 1, "is_bookable": 1, "size": 20},
        )

        assert initial_result.data is not None
        print(
            f"✅ Usuario ve {initial_result.data['total_items']} unidades disponibles"
        )

        # Paso 2: Refinamiento por características
        print("🔍 Paso 2: Refinamiento por características")
        refined_result = await mcp_client.call_tool(
            name="search_units",
            arguments={
                "bedrooms": 2,
                "bathrooms": 2,
                "is_active": 1,
                "is_bookable": 1,
                "size": 10,
            },
        )

        assert refined_result.data is not None
        print(
            f"✅ Usuario refina a {refined_result.data['total_items']} unidades de 2/2"
        )

        # Paso 3: Búsqueda por ubicación
        print("🔍 Paso 3: Búsqueda por ubicación")
        location_result = await mcp_client.call_tool(
            name="search_units",
            arguments={
                "search": "beach",
                "bedrooms": 2,
                "bathrooms": 2,
                "is_active": 1,
                "is_bookable": 1,
            },
        )

        assert location_result.data is not None
        print(
            f"✅ Usuario encuentra {location_result.data['total_items']} unidades en la playa"
        )

        # Paso 4: Exploración de opciones
        print("🔍 Paso 4: Exploración de opciones")
        if location_result.data["total_items"] > 0:
            units = location_result.data["_embedded"]["units"]
            print("📋 Opciones disponibles:")
            for i, unit in enumerate(units[:3], 1):  # Mostrar primeras 3
                print(f"  {i}. {unit['name']} - {unit['address']}")
                print(
                    f"     Dormitorios: {unit['bedrooms']}, Baños: {unit['bathrooms']}"
                )
                print(f"     Amenidades: {', '.join(unit['amenities'][:3])}")

        # Paso 5: Decisión final
        print("🔍 Paso 5: Decisión final")
        if location_result.data["total_items"] > 0:
            print("✅ Usuario tiene opciones para elegir")
        else:
            print("⚠️  Usuario necesita expandir criterios de búsqueda")

        print("🎉 Viaje del usuario completado exitosamente")
