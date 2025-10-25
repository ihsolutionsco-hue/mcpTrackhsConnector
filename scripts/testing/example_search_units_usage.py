#!/usr/bin/env python3
"""
Ejemplo de uso de la herramienta search_units
Demuestra diferentes casos de uso y escenarios
"""

import asyncio
import os
import sys
from pathlib import Path

# Agregar src al path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport
from trackhs_mcp.server import mcp


async def example_basic_search():
    """Ejemplo de búsqueda básica"""
    print("🔍 Ejemplo 1: Búsqueda básica de unidades")

    transport = FastMCPTransport(mcp)
    async with Client(transport=transport) as client:
        result = await client.call_tool(name="search_units", arguments={})

        print(f"✅ Encontradas {result.data['total_items']} unidades")
        print(f"📄 Página {result.data['page']} de {result.data['page_count']}")

        if result.data["total_items"] > 0:
            unit = result.data["_embedded"]["units"][0]
            print(f"🏠 Primera unidad: {unit['name']}")
            print(f"   📍 {unit['address']}")
            print(f"   🛏️  {unit['bedrooms']} dormitorios, {unit['bathrooms']} baños")


async def example_filtered_search():
    """Ejemplo de búsqueda con filtros"""
    print("\n🔍 Ejemplo 2: Búsqueda con filtros")

    transport = FastMCPTransport(mcp)
    async with Client(transport=transport) as client:
        result = await client.call_tool(
            name="search_units",
            arguments={"bedrooms": 2, "bathrooms": 1, "is_active": 1, "is_bookable": 1},
        )

        print(
            f"✅ Encontradas {result.data['total_items']} unidades de 2 dormitorios, 1 baño"
        )

        if result.data["total_items"] > 0:
            units = result.data["_embedded"]["units"]
            for i, unit in enumerate(units[:3], 1):  # Mostrar primeras 3
                print(f"   {i}. {unit['name']} - {unit['address']}")


async def example_location_search():
    """Ejemplo de búsqueda por ubicación"""
    print("\n🔍 Ejemplo 3: Búsqueda por ubicación")

    transport = FastMCPTransport(mcp)
    async with Client(transport=transport) as client:
        result = await client.call_tool(
            name="search_units",
            arguments={"search": "beach", "is_active": 1, "is_bookable": 1},
        )

        print(f"✅ Encontradas {result.data['total_items']} unidades cerca de la playa")

        if result.data["total_items"] > 0:
            units = result.data["_embedded"]["units"]
            for unit in units:
                print(f"   🏖️  {unit['name']} - {unit['address']}")
                print(f"      Amenidades: {', '.join(unit['amenities'][:3])}")


async def example_pagination():
    """Ejemplo de paginación"""
    print("\n🔍 Ejemplo 4: Navegación por páginas")

    transport = FastMCPTransport(mcp)
    async with Client(transport=transport) as client:
        # Primera página
        result1 = await client.call_tool(
            name="search_units", arguments={"page": 1, "size": 5}
        )

        print(f"📄 Página 1: {result1.data['total_items']} unidades totales")
        print(f"   Mostrando {len(result1.data['_embedded']['units'])} unidades")

        # Si hay más páginas, mostrar segunda página
        if result1.data["page_count"] > 1:
            result2 = await client.call_tool(
                name="search_units", arguments={"page": 2, "size": 5}
            )

            print(
                f"📄 Página 2: Mostrando {len(result2.data['_embedded']['units'])} unidades"
            )


async def example_inventory_analysis():
    """Ejemplo de análisis de inventario"""
    print("\n🔍 Ejemplo 5: Análisis de inventario")

    transport = FastMCPTransport(mcp)
    async with Client(transport=transport) as client:
        # Obtener inventario completo
        all_units = []
        page = 1
        total_pages = 1

        while page <= total_pages:
            result = await client.call_tool(
                name="search_units", arguments={"page": page, "size": 25}
            )

            all_units.extend(result.data["_embedded"]["units"])
            total_pages = result.data["page_count"]
            page += 1

        print(f"📊 Inventario completo: {len(all_units)} unidades")

        # Análisis por características
        bedroom_distribution = {}
        for unit in all_units:
            bedrooms = unit["bedrooms"]
            bedroom_distribution[bedrooms] = bedroom_distribution.get(bedrooms, 0) + 1

        print("📊 Distribución por dormitorios:")
        for bedrooms, count in sorted(bedroom_distribution.items()):
            print(f"   {bedrooms} dormitorios: {count} unidades")

        # Análisis por estado
        active_count = sum(1 for unit in all_units if unit["is_active"])
        bookable_count = sum(1 for unit in all_units if unit["is_bookable"])

        print(f"📊 Estado de unidades:")
        print(f"   Activas: {active_count}")
        print(f"   Disponibles: {bookable_count}")


async def example_business_scenarios():
    """Ejemplo de escenarios de negocio"""
    print("\n🔍 Ejemplo 6: Escenarios de negocio")

    transport = FastMCPTransport(mcp)
    async with Client(transport=transport) as client:
        # Escenario 1: Búsqueda para familia
        family_result = await client.call_tool(
            name="search_units",
            arguments={"bedrooms": 3, "bathrooms": 2, "is_active": 1, "is_bookable": 1},
        )

        print(f"👨‍👩‍👧‍👦 Para familia: {family_result.data['total_items']} unidades")

        # Escenario 2: Búsqueda para pareja
        couple_result = await client.call_tool(
            name="search_units",
            arguments={"bedrooms": 1, "bathrooms": 1, "is_active": 1, "is_bookable": 1},
        )

        print(f"👫 Para pareja: {couple_result.data['total_items']} unidades")

        # Escenario 3: Búsqueda de lujo
        luxury_result = await client.call_tool(
            name="search_units",
            arguments={"search": "penthouse", "is_active": 1, "is_bookable": 1},
        )

        print(f"💎 De lujo: {luxury_result.data['total_items']} unidades")


async def example_error_handling():
    """Ejemplo de manejo de errores"""
    print("\n🔍 Ejemplo 7: Manejo de errores")

    transport = FastMCPTransport(mcp)
    async with Client(transport=transport) as client:
        # Test con parámetros inválidos
        try:
            await client.call_tool(
                name="search_units", arguments={"page": 0}  # Inválido
            )
        except Exception as e:
            print(f"❌ Error esperado con página inválida: {type(e).__name__}")

        # Test con parámetros válidos después del error
        try:
            result = await client.call_tool(
                name="search_units", arguments={"page": 1, "size": 5}
            )
            print(f"✅ Sistema recuperado: {result.data['total_items']} unidades")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")


async def main():
    """Función principal"""
    print("🚀 Ejemplos de uso de search_units")
    print("=" * 50)

    # Verificar credenciales
    if not os.getenv("TRACKHS_USERNAME") or not os.getenv("TRACKHS_PASSWORD"):
        print("⚠️  Credenciales de API no configuradas")
        print("   Los tests usarán mocks en lugar de la API real")
        print("   Para usar la API real, configura:")
        print("   export TRACKHS_USERNAME='tu_usuario'")
        print("   export TRACKHS_PASSWORD='tu_password'")
        print()

    try:
        # Ejecutar ejemplos
        await example_basic_search()
        await example_filtered_search()
        await example_location_search()
        await example_pagination()
        await example_inventory_analysis()
        await example_business_scenarios()
        await example_error_handling()

        print("\n✅ Todos los ejemplos completados exitosamente")

    except Exception as e:
        print(f"\n❌ Error ejecutando ejemplos: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
