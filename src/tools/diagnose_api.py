"""
Herramienta de diagnóstico para la API de TrackHS
"""

from typing import Any, Dict, List, Optional

from pydantic import ConfigDict

from schemas.base import BaseSchema
from utils.exceptions import TrackHSAPIError

from .base import BaseTool


class DiagnoseAPIInput(BaseSchema):
    """Parámetros de entrada para diagnóstico de API"""

    test_type: str = "full"

    model_config = ConfigDict(json_schema_extra={"example": {"test_type": "full"}})


class DiagnoseAPIOutput(BaseSchema):
    """Resultado del diagnóstico de API"""

    connectivity: Optional[Dict[str, Any]] = None
    authentication: Optional[Dict[str, Any]] = None
    endpoints: Optional[Dict[str, Any]] = None
    data_structure: Optional[Dict[str, Any]] = None
    summary: Dict[str, Any]


class DiagnoseAPITool(BaseTool):
    """Herramienta para diagnosticar problemas con la API de TrackHS"""

    @property
    def name(self) -> str:
        return "diagnose_api"

    @property
    def description(self) -> str:
        return """
        Diagnostica problemas con la API de TrackHS ejecutando una serie de tests.

        Esta herramienta ayuda a identificar:
        - Problemas de conectividad
        - Errores de autenticación
        - Configuración incorrecta de endpoints
        - Problemas con la estructura de datos
        - Validación de permisos

        Args:
            test_type: Tipo de diagnóstico a ejecutar
                - "connectivity": Test básico de conectividad
                - "auth": Test de autenticación
                - "endpoints": Test de endpoints disponibles
                - "data_structure": Test de estructura de datos
                - "full": Ejecutar todos los tests

        Returns:
            Reporte detallado del diagnóstico
        """

    @property
    def input_schema(self) -> type:
        return DiagnoseAPIInput

    @property
    def output_schema(self) -> type:
        return DiagnoseAPIOutput

    def _execute_logic(self, validated_input) -> Dict[str, Any]:
        """
        Ejecuta el diagnóstico de la API

        Args:
            validated_input: Parámetros de diagnóstico

        Returns:
            Resultado del diagnóstico
        """
        test_type = validated_input.test_type
        results = {}

        try:
            if test_type in ["connectivity", "full"]:
                results["connectivity"] = self._test_connectivity()

            if test_type in ["auth", "full"]:
                results["authentication"] = self._test_authentication()

            if test_type in ["endpoints", "full"]:
                results["endpoints"] = self._test_endpoints()

            if test_type in ["data_structure", "full"]:
                results["data_structure"] = self._test_data_structure()

            # Generar resumen
            results["summary"] = self._generate_summary(results)

            return results

        except Exception as e:
            self.logger.error(
                f"Error en diagnóstico de API: {str(e)}",
                extra={"error_type": type(e).__name__, "test_type": test_type},
            )
            raise TrackHSAPIError(f"Error en diagnóstico: {str(e)}")

    def _test_connectivity(self) -> Dict[str, Any]:
        """Test básico de conectividad"""
        try:
            # Test simple de conectividad
            response = self.api_client.get("health")

            return {
                "status": "success",
                "message": "Conectividad exitosa",
                "response": response,
                "timestamp": self._get_timestamp(),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error de conectividad: {str(e)}",
                "error_type": type(e).__name__,
                "timestamp": self._get_timestamp(),
            }

    def _test_authentication(self) -> Dict[str, Any]:
        """Test de autenticación"""
        try:
            # Intentar acceder a un endpoint que requiere autenticación
            response = self.api_client.get("api/pms/units", {"page": 1, "size": 1})

            return {
                "status": "success",
                "message": "Autenticación exitosa",
                "response_keys": (
                    list(response.keys()) if isinstance(response, dict) else "not_dict"
                ),
                "timestamp": self._get_timestamp(),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error de autenticación: {str(e)}",
                "error_type": type(e).__name__,
                "timestamp": self._get_timestamp(),
            }

    def _test_endpoints(self) -> Dict[str, Any]:
        """Test de endpoints disponibles"""
        endpoints_to_test = [
            "api/pms/units",
            "api/pms/reservations",
            "api/pms/amenities",
            "health",
        ]

        results = {}

        for endpoint in endpoints_to_test:
            try:
                if endpoint == "health":
                    response = self.api_client.get(endpoint)
                else:
                    response = self.api_client.get(endpoint, {"page": 1, "size": 1})

                results[endpoint] = {
                    "status": "success",
                    "response_type": type(response).__name__,
                    "has_data": bool(response) if isinstance(response, dict) else False,
                    "keys": (
                        list(response.keys())
                        if isinstance(response, dict)
                        else "not_dict"
                    ),
                }
            except Exception as e:
                results[endpoint] = {
                    "status": "error",
                    "error": str(e),
                    "error_type": type(e).__name__,
                }

        return {
            "endpoints_tested": len(endpoints_to_test),
            "successful": sum(1 for r in results.values() if r["status"] == "success"),
            "failed": sum(1 for r in results.values() if r["status"] == "error"),
            "details": results,
            "timestamp": self._get_timestamp(),
        }

    def _test_data_structure(self) -> Dict[str, Any]:
        """Test de estructura de datos"""
        try:
            # Test con diferentes parámetros para ver estructura de respuesta
            test_cases = [
                {"page": 1, "size": 1},
                {"page": 1, "size": 1, "is_active": 1},
                {"page": 1, "size": 1, "search": "test"},
                {"page": 1, "size": 1, "bedrooms": 1},
            ]

            results = []

            for i, params in enumerate(test_cases):
                try:
                    response = self.api_client.get("api/pms/units", params)
                    results.append(
                        {
                            "test_case": i + 1,
                            "params": params,
                            "status": "success",
                            "response_structure": self._analyze_response_structure(
                                response
                            ),
                            "has_units": (
                                "units" in response
                                if isinstance(response, dict)
                                else False
                            ),
                            "units_count": (
                                len(response.get("units", []))
                                if isinstance(response, dict)
                                else 0
                            ),
                            "total_items": (
                                response.get("total_items", "not_found")
                                if isinstance(response, dict)
                                else "not_found"
                            ),
                        }
                    )
                except Exception as e:
                    results.append(
                        {
                            "test_case": i + 1,
                            "params": params,
                            "status": "error",
                            "error": str(e),
                        }
                    )

            return {
                "test_cases": len(test_cases),
                "successful_tests": sum(1 for r in results if r["status"] == "success"),
                "failed_tests": sum(1 for r in results if r["status"] == "error"),
                "results": results,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error en test de estructura: {str(e)}",
                "error_type": type(e).__name__,
                "timestamp": self._get_timestamp(),
            }

    def _analyze_response_structure(self, response: Any) -> Dict[str, Any]:
        """Analiza la estructura de una respuesta"""
        if not isinstance(response, dict):
            return {"type": "not_dict", "value": str(response)[:100]}

        structure = {
            "type": "dict",
            "keys": list(response.keys()),
            "key_count": len(response.keys()),
            "has_units": "units" in response,
            "has_embedded": "_embedded" in response,
            "has_data": "data" in response,
            "has_pagination": any(
                k in response for k in ["page", "size", "total_items"]
            ),
        }

        if "units" in response:
            units = response["units"]
            structure["units_type"] = type(units).__name__
            structure["units_count"] = (
                len(units) if isinstance(units, list) else "not_list"
            )
            if isinstance(units, list) and units:
                structure["first_unit_keys"] = (
                    list(units[0].keys()) if isinstance(units[0], dict) else "not_dict"
                )

        return structure

    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Genera un resumen del diagnóstico"""
        summary = {
            "overall_status": "unknown",
            "tests_executed": len(results) - 1,  # Excluir summary
            "successful_tests": 0,
            "failed_tests": 0,
            "recommendations": [],
            "critical_issues": [],
            "timestamp": self._get_timestamp(),
        }

        for test_name, result in results.items():
            if test_name == "summary":
                continue

            if isinstance(result, dict):
                if result.get("status") == "success":
                    summary["successful_tests"] += 1
                elif result.get("status") == "error":
                    summary["failed_tests"] += 1
                    summary["critical_issues"].append(
                        f"{test_name}: {result.get('message', 'Error desconocido')}"
                    )

        # Determinar estado general
        if summary["failed_tests"] == 0:
            summary["overall_status"] = "healthy"
        elif summary["successful_tests"] > 0:
            summary["overall_status"] = "partial"
        else:
            summary["overall_status"] = "critical"

        # Generar recomendaciones
        if "connectivity" in results and results["connectivity"]["status"] == "error":
            summary["recommendations"].append(
                "Verificar URL base y conectividad de red"
            )

        if (
            "authentication" in results
            and results["authentication"]["status"] == "error"
        ):
            summary["recommendations"].append("Verificar credenciales de API")

        if "data_structure" in results:
            data_result = results["data_structure"]
            if data_result.get("successful_tests", 0) == 0:
                summary["recommendations"].append(
                    "Verificar estructura de respuesta de la API"
                )
            elif all(
                r.get("units_count", 0) == 0
                for r in data_result.get("results", [])
                if r.get("status") == "success"
            ):
                summary["recommendations"].append(
                    "Verificar si hay datos en la base de datos de TrackHS"
                )

        return summary

    def _get_timestamp(self) -> str:
        """Obtiene timestamp actual"""
        from datetime import datetime

        return datetime.now().isoformat()
