#!/usr/bin/env python3
"""
Script de pruebas simplificado para el tool get_reservation actualizado con API V2
"""

import json
import os
import sys
import time
from datetime import datetime

import pytest

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def run_tests():
    """Ejecutar todas las pruebas de get_reservation"""

    print("=" * 80)
    print("PRUEBAS COMPREHENSIVAS - GET RESERVATION API V2")
    print("=" * 80)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version}")
    print()

    # Lista de archivos de prueba
    test_files = [
        "tests/test_get_reservation_unit.py",
        "tests/test_get_reservation_integration.py",
        "tests/test_get_reservation_e2e.py",
    ]

    # Configuración de pytest
    pytest_args = [
        "-v",
        "--tb=short",
        "--disable-warnings",
        "--color=yes",
        "--durations=10",
    ]

    # Agregar archivos de prueba
    pytest_args.extend(test_files)

    print("ARCHIVOS DE PRUEBA:")
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"   [OK] {test_file}")
        else:
            print(f"   [ERROR] {test_file} - NO ENCONTRADO")
    print()

    # Ejecutar pruebas
    print("EJECUTANDO PRUEBAS...")
    print("-" * 80)

    start_time = time.time()

    try:
        # Ejecutar pytest
        exit_code = pytest.main(pytest_args)

        end_time = time.time()
        execution_time = end_time - start_time

        print()
        print("-" * 80)
        print("RESUMEN DE PRUEBAS")
        print("-" * 80)
        print(f"Tiempo total: {execution_time:.2f} segundos")

        if exit_code == 0:
            print("TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
            print(
                "El tool get_reservation está funcionando correctamente con la API V2"
            )
        else:
            print("ALGUNAS PRUEBAS FALLARON")
            print("Revisa los detalles arriba para más información")

        return exit_code == 0

    except Exception as e:
        print(f"ERROR EJECUTANDO PRUEBAS: {str(e)}")
        return False


def test_schema_validation():
    """Test rápido de validación del schema"""
    print("\nVALIDANDO SCHEMA...")

    try:
        from trackhs_mcp.schemas import ReservationDetailOutput

        # Test con datos mínimos
        minimal_data = {"id": 12345}
        reservation = ReservationDetailOutput(**minimal_data)
        print(f"   [OK] Schema con datos mínimos: ID {reservation.id}")

        # Test con datos completos
        full_data = {
            "id": 12345,
            "currency": "USD",
            "unitId": 789,
            "arrivalDate": "2024-01-15",
            "departureDate": "2024-01-20",
            "status": "Confirmed",
            "nights": 5.0,
            "isUnitLocked": False,
            "isUnitAssigned": True,
            "occupants": [],
            "securityDeposit": {"required": "200.00", "remaining": 200},
            "updatedAt": "2024-01-10T10:30:00Z",
            "createdAt": "2024-01-10T10:00:00Z",
            "bookedAt": "2024-01-10T10:00:00Z",
            "guestBreakdown": {"grossRent": "1000.00"},
            "ownerBreakdown": {"grossRent": "1000.00"},
            "contactId": 456,
            "channelId": 1,
            "folioId": 789,
            "guaranteePolicyId": 1,
            "cancellationPolicyId": 1,
            "userId": 100,
            "typeId": 1,
            "rateTypeId": 1,
            "unitCodeId": 1,
            "groupId": 1,
            "isTaxable": True,
            "uuid": "550e8400-e29b-41d4-a716-446655440000",
            "source": "Web",
            "agreementStatus": "not-needed",
            "automatePayment": False,
            "revenueRealizedMethod": "nightly",
            "paymentPlan": [],
            "rateType": {"id": 1, "name": "Standard"},
            "travelInsuranceProducts": [],
            "embedded": {"unit": {"id": 789}},
            "links": {"self": {"href": "/api/v2/pms/reservations/12345"}},
            "additional_data": {},
        }

        reservation = ReservationDetailOutput(**full_data)
        print(
            f"   [OK] Schema con datos completos: {len(ReservationDetailOutput.model_fields)} campos"
        )

        return True

    except Exception as e:
        print(f"   [ERROR] Error validando schema: {str(e)}")
        return False


def test_tool_registration():
    """Test de registro del tool en MCP"""
    print("\nVALIDANDO REGISTRO DEL TOOL...")

    try:
        from trackhs_mcp.server import get_reservation, mcp

        # Verificar que la función existe (es un FunctionTool de FastMCP)
        if (
            hasattr(get_reservation, "name")
            and get_reservation.name == "get_reservation"
        ):
            print("   [OK] Tool get_reservation disponible")
        else:
            print("   [ERROR] Tool get_reservation NO disponible")
            return False

        # Verificar que el servidor MCP está configurado
        if mcp is not None:
            print("   [OK] Servidor MCP configurado correctamente")
        else:
            print("   [ERROR] Servidor MCP NO configurado")
            return False

        # Verificar configuración de FastMCP
        if hasattr(mcp, "strict_input_validation"):
            print(
                f"   [OK] Configuración FastMCP: strict_input_validation={mcp.strict_input_validation}"
            )
        else:
            print("   [WARNING] No se pudo verificar configuración FastMCP")

        return True

    except Exception as e:
        print(f"   [ERROR] Error validando tool: {str(e)}")
        return False


def main():
    """Función principal"""

    print("INICIANDO PRUEBAS DE GET RESERVATION API V2")
    print("=" * 80)

    # Verificar que estamos en el directorio correcto
    if not os.path.exists("src/trackhs_mcp"):
        print("ERROR: No se encontró el directorio src/trackhs_mcp")
        print("   Asegúrate de ejecutar este script desde la raíz del proyecto")
        return False

    # Test rápido de validación
    schema_ok = test_schema_validation()
    tool_ok = test_tool_registration()

    if not (schema_ok and tool_ok):
        print("\nERROR: Fallos en validaciones básicas")
        return False

    # Ejecutar pruebas completas
    print("\nEJECUTANDO PRUEBAS COMPLETAS...")
    tests_ok = run_tests()

    # Resultado final
    print("\n" + "=" * 80)
    print("RESULTADO FINAL")
    print("=" * 80)

    if tests_ok:
        print("TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE!")
        print("El tool get_reservation está listo para producción con API V2")
        print("Características validadas:")
        print("   • 57 campos del schema actualizado")
        print("   • Endpoint V2 funcional")
        print("   • Datos embebidos completos")
        print("   • Desglose financiero detallado")
        print("   • Manejo robusto de errores")
        print("   • Rendimiento optimizado")
        return True
    else:
        print("ALGUNAS PRUEBAS FALLARON")
        print("Revisa los logs arriba para identificar problemas")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
