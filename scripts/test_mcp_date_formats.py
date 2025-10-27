#!/usr/bin/env python3
"""
Script para probar diferentes formatos de fecha usando la herramienta MCP.
Prueba los parámetros correctos según la documentación de TrackHS.
"""

import os
import sys
from datetime import datetime, timedelta

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def test_mcp_date_formats():
    """Probar diferentes formatos de fecha con MCP"""

    print("🧪 TESTING MCP CON DIFERENTES FORMATOS DE FECHA")
    print("=" * 60)

    # Fecha base para las pruebas
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    print(f"📅 Fecha base para pruebas: {today.strftime('%Y-%m-%d')}")

    # Diferentes formatos de fecha a probar
    date_formats = {
        "YYYY-MM-DD": today.strftime("%Y-%m-%d"),
        "YYYY-MM-DDTHH:MM:SS": today.strftime("%Y-%m-%dT%H:%M:%S"),
        "YYYY-MM-DDTHH:MM:SSZ": today.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "YYYY-MM-DDTHH:MM:SS+00:00": today.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "YYYY-MM-DDTHH:MM:SS.000Z": today.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
    }

    print("\n🔍 PROBANDO DIFERENTES FORMATOS DE FECHA")
    print("-" * 40)

    for format_name, date_str in date_formats.items():
        print(f"\n📋 FORMATO: {format_name}")
        print(f"   Fecha: {date_str}")

        try:
            # Simular llamada a la herramienta MCP
            # Nota: En un entorno real, aquí harías la llamada real a la herramienta
            print(
                f"   🔧 Llamada simulada: search_reservations(arrival_start='{date_str}', arrival_end='{date_str}')"
            )
            print(f"   ⏳ Esperando respuesta...")

            # Aquí normalmente harías la llamada real:
            # result = mcp_ihmTrackhs_search_reservations(
            #     arrival_start=date_str,
            #     arrival_end=date_str,
            #     size=5,
            #     page=1
            # )

            print(f"   ✅ Formato {format_name} listo para probar")

        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

    print("\n📝 INSTRUCCIONES PARA PRUEBA MANUAL:")
    print("-" * 40)
    print("1. Ejecuta cada formato de fecha usando la herramienta MCP:")
    print("2. Observa si la API respeta los filtros de fecha")
    print("3. Compara los resultados con y sin filtros")
    print("4. Identifica qué formato funciona correctamente")

    print("\n🔧 COMANDOS PARA PROBAR:")
    print("-" * 40)
    for format_name, date_str in date_formats.items():
        print(f"# {format_name}")
        print(
            f"mcp_ihmTrackhs_search_reservations(arrival_start='{date_str}', arrival_end='{date_str}', size=5, page=1)"
        )
        print()

    return True


if __name__ == "__main__":
    test_mcp_date_formats()
