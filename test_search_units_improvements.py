#!/usr/bin/env python3
"""
Script de prueba para validar las mejoras implementadas en search_units.
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_search_units_improvements():
    """
    Probar las mejoras implementadas en search_units.
    """
    print("🧪 Iniciando pruebas de mejoras en search_units...")

    # Importar el servicio mejorado
    try:
        from src.trackhs_mcp.api_client import TrackHSAPIClient
        from src.trackhs_mcp.models import UnitData, UnitSearchParams
        from src.trackhs_mcp.repositories.unit_repository import UnitRepository
        from src.trackhs_mcp.services.unit_service import UnitService

        print("✅ Módulos importados correctamente")
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        return False

    # Configurar cliente API (simulado para pruebas)
    try:
        api_client = TrackHSAPIClient(
            base_url="https://ihmvacations.trackhs.com",
            username="test_user",
            password="test_pass",
        )
        unit_repo = UnitRepository(api_client)
        unit_service = UnitService(unit_repo)
        print("✅ Servicios inicializados correctamente")
    except Exception as e:
        print(f"❌ Error inicializando servicios: {e}")
        return False

    # Pruebas de validación Pydantic
    print("\n🔍 Probando validación Pydantic...")

    test_cases = [
        {
            "name": "Parámetros válidos básicos",
            "params": {"page": 1, "size": 10, "search": "luxury"},
        },
        {
            "name": "Parámetros con filtros numéricos",
            "params": {"page": 1, "size": 5, "bedrooms": 3, "bathrooms": 2},
        },
        {
            "name": "Parámetros con filtros booleanos",
            "params": {"page": 1, "size": 10, "is_active": 1, "is_bookable": 1},
        },
        {
            "name": "Conversión de tipos automática",
            "params": {"page": "1", "size": "10", "bedrooms": "3", "is_active": "true"},
        },
        {
            "name": "Parámetros con valores None",
            "params": {
                "page": 1,
                "size": 10,
                "search": None,
                "bedrooms": None,
                "bathrooms": None,
            },
        },
    ]

    validation_results = []

    for test_case in test_cases:
        try:
            print(f"  🧪 Probando: {test_case['name']}")
            search_params = UnitSearchParams(**test_case["params"])
            print(f"    ✅ Validación exitosa: {search_params.dict()}")
            validation_results.append(
                {
                    "test": test_case["name"],
                    "status": "success",
                    "validated_params": search_params.dict(),
                }
            )
        except Exception as e:
            print(f"    ❌ Error de validación: {e}")
            validation_results.append(
                {"test": test_case["name"], "status": "error", "error": str(e)}
            )

    # Pruebas de normalización de datos
    print("\n🔧 Probando normalización de datos...")

    test_units = [
        {
            "id": 1,
            "name": "Test Unit 1",
            "code": "TU001",
            "area": "3348.0",  # String que debe convertirse a float
            "bedrooms": "3",  # String que debe convertirse a int
            "bathrooms": 2,
            "is_active": "true",  # String que debe convertirse a bool
            "is_bookable": 1,
        },
        {
            "id": 2,
            "name": "Test Unit 2",
            "code": "TU002",
            "area": 2500.5,  # Float válido
            "bedrooms": 4,
            "bathrooms": "2",  # String que debe convertirse a int
            "is_active": False,  # Bool válido
            "is_bookable": "false",  # String que debe convertirse a bool
        },
        {
            "id": 3,
            "name": "Test Unit 3",
            "code": "TU003",
            "area": None,  # None válido
            "bedrooms": None,
            "bathrooms": None,
            "is_active": None,
            "is_bookable": None,
        },
    ]

    normalization_results = []

    for i, unit_data in enumerate(test_units):
        try:
            print(f"  🧪 Probando normalización de unidad {i+1}")
            unit = UnitData(**unit_data)
            print(f"    ✅ Normalización exitosa:")
            print(f"      - area: {unit.area} (tipo: {type(unit.area)})")
            print(f"      - bedrooms: {unit.bedrooms} (tipo: {type(unit.bedrooms)})")
            print(f"      - bathrooms: {unit.bathrooms} (tipo: {type(unit.bathrooms)})")
            print(f"      - is_active: {unit.is_active} (tipo: {type(unit.is_active)})")
            print(
                f"      - is_bookable: {unit.is_bookable} (tipo: {type(unit.is_bookable)})"
            )

            normalization_results.append(
                {
                    "unit": f"Unit {i+1}",
                    "status": "success",
                    "normalized_data": unit.dict(),
                }
            )
        except Exception as e:
            print(f"    ❌ Error de normalización: {e}")
            normalization_results.append(
                {"unit": f"Unit {i+1}", "status": "error", "error": str(e)}
            )

    # Generar reporte de resultados
    report = {
        "timestamp": datetime.now().isoformat(),
        "test_type": "search_units_improvements",
        "validation_tests": validation_results,
        "normalization_tests": normalization_results,
        "summary": {
            "total_validation_tests": len(validation_results),
            "successful_validation_tests": len(
                [r for r in validation_results if r["status"] == "success"]
            ),
            "total_normalization_tests": len(normalization_results),
            "successful_normalization_tests": len(
                [r for r in normalization_results if r["status"] == "success"]
            ),
        },
    }

    # Guardar reporte
    report_file = f"search_units_improvements_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n📊 Resumen de pruebas:")
    print(
        f"  ✅ Validación Pydantic: {report['summary']['successful_validation_tests']}/{report['summary']['total_validation_tests']} exitosas"
    )
    print(
        f"  ✅ Normalización de datos: {report['summary']['successful_normalization_tests']}/{report['summary']['total_normalization_tests']} exitosas"
    )
    print(f"  📄 Reporte guardado en: {report_file}")

    # Verificar si todas las pruebas pasaron
    all_validation_passed = (
        report["summary"]["successful_validation_tests"]
        == report["summary"]["total_validation_tests"]
    )
    all_normalization_passed = (
        report["summary"]["successful_normalization_tests"]
        == report["summary"]["total_normalization_tests"]
    )

    if all_validation_passed and all_normalization_passed:
        print("🎉 ¡Todas las pruebas pasaron exitosamente!")
        return True
    else:
        print("⚠️ Algunas pruebas fallaron. Revisar el reporte para más detalles.")
        return False


if __name__ == "__main__":
    success = test_search_units_improvements()
    sys.exit(0 if success else 1)
