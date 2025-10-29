"""
Validador de respuestas para detectar inconsistencias entre filtros y resultados
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union


@dataclass
class ValidationResult:
    """Resultado de una validación individual"""

    field_name: str
    expected_value: Any
    actual_values: List[Any]
    is_valid: bool
    invalid_count: int
    total_count: int
    message: str
    details: Dict[str, Any]


@dataclass
class ValidationReport:
    """Reporte completo de validaciones"""

    total_validations: int
    passed_validations: int
    failed_validations: int
    results: List[ValidationResult]
    summary: str
    has_issues: bool


class ResponseValidator:
    """Validador de respuestas de API para detectar inconsistencias"""

    def __init__(self):
        self.logger = None  # Se asignará desde el contexto que lo use

    def set_logger(self, logger):
        """Asigna un logger para reportar warnings"""
        self.logger = logger

    def validate_boolean_filter(
        self,
        units: List[Dict[str, Any]],
        field_name: str,
        expected_value: bool,
        filter_applied: bool = True,
    ) -> ValidationResult:
        """
        Valida que todas las unidades cumplan con un filtro booleano

        Args:
            units: Lista de unidades de la respuesta
            field_name: Nombre del campo a validar (ej: 'is_active')
            expected_value: Valor esperado (True/False)
            filter_applied: Si el filtro fue aplicado en la búsqueda

        Returns:
            ValidationResult con el resultado de la validación
        """
        if not filter_applied:
            return ValidationResult(
                field_name=field_name,
                expected_value=expected_value,
                actual_values=[],
                is_valid=True,
                invalid_count=0,
                total_count=len(units),
                message=f"Filtro {field_name}={expected_value} no fue aplicado",
                details={"filter_applied": False},
            )

        if not units:
            return ValidationResult(
                field_name=field_name,
                expected_value=expected_value,
                actual_values=[],
                is_valid=True,
                invalid_count=0,
                total_count=0,
                message=f"No hay unidades para validar {field_name}",
                details={"empty_response": True},
            )

        actual_values = []
        invalid_units = []

        for i, unit in enumerate(units):
            actual_value = unit.get(field_name)
            actual_values.append(actual_value)

            if actual_value != expected_value:
                invalid_units.append(
                    {
                        "unit_id": unit.get("id", f"unknown_{i}"),
                        "unit_name": unit.get("name", "unknown"),
                        "expected": expected_value,
                        "actual": actual_value,
                    }
                )

        is_valid = len(invalid_units) == 0
        invalid_count = len(invalid_units)

        message = (
            f"✅ Filtro {field_name}={expected_value} correcto"
            if is_valid
            else f"❌ Filtro {field_name}={expected_value} falló: {invalid_count}/{len(units)} unidades no cumplen"
        )

        # Log warning si hay inconsistencias
        if not is_valid and self.logger:
            self.logger.warning(
                f"BUG DETECTADO: Filtro {field_name} no funciona correctamente",
                extra={
                    "field_name": field_name,
                    "expected_value": expected_value,
                    "invalid_count": invalid_count,
                    "total_count": len(units),
                    "invalid_units": invalid_units[
                        :5
                    ],  # Solo primeros 5 para no saturar logs
                    "bug_type": "boolean_filter_failure",
                },
            )

        return ValidationResult(
            field_name=field_name,
            expected_value=expected_value,
            actual_values=actual_values,
            is_valid=is_valid,
            invalid_count=invalid_count,
            total_count=len(units),
            message=message,
            details={"invalid_units": invalid_units, "filter_applied": filter_applied},
        )

    def validate_range_filter(
        self,
        units: List[Dict[str, Any]],
        field_name: str,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
        filter_applied: bool = True,
    ) -> ValidationResult:
        """
        Valida que todas las unidades estén dentro de un rango numérico

        Args:
            units: Lista de unidades de la respuesta
            field_name: Nombre del campo a validar (ej: 'bedrooms')
            min_value: Valor mínimo permitido (inclusive)
            max_value: Valor máximo permitido (inclusive)
            filter_applied: Si el filtro fue aplicado en la búsqueda

        Returns:
            ValidationResult con el resultado de la validación
        """
        if not filter_applied:
            return ValidationResult(
                field_name=field_name,
                expected_value=f"{min_value}-{max_value}",
                actual_values=[],
                is_valid=True,
                invalid_count=0,
                total_count=len(units),
                message=f"Filtro de rango {field_name} no fue aplicado",
                details={"filter_applied": False},
            )

        if not units:
            return ValidationResult(
                field_name=field_name,
                expected_value=f"{min_value}-{max_value}",
                actual_values=[],
                is_valid=True,
                invalid_count=0,
                total_count=0,
                message=f"No hay unidades para validar rango {field_name}",
                details={"empty_response": True},
            )

        actual_values = []
        invalid_units = []

        for i, unit in enumerate(units):
            actual_value = unit.get(field_name)
            actual_values.append(actual_value)

            is_in_range = True
            if actual_value is not None:
                if min_value is not None and actual_value < min_value:
                    is_in_range = False
                if max_value is not None and actual_value > max_value:
                    is_in_range = False
            else:
                is_in_range = False  # Valores None no están en rango

            if not is_in_range:
                invalid_units.append(
                    {
                        "unit_id": unit.get("id", f"unknown_{i}"),
                        "unit_name": unit.get("name", "unknown"),
                        "field_value": actual_value,
                        "min_allowed": min_value,
                        "max_allowed": max_value,
                    }
                )

        is_valid = len(invalid_units) == 0
        invalid_count = len(invalid_units)

        range_desc = f"{min_value or '∞'}-{max_value or '∞'}"
        message = (
            f"✅ Rango {field_name} {range_desc} correcto"
            if is_valid
            else f"❌ Rango {field_name} {range_desc} falló: {invalid_count}/{len(units)} unidades fuera de rango"
        )

        # Log warning si hay inconsistencias
        if not is_valid and self.logger:
            self.logger.warning(
                f"BUG DETECTADO: Filtro de rango {field_name} no funciona correctamente",
                extra={
                    "field_name": field_name,
                    "min_value": min_value,
                    "max_value": max_value,
                    "invalid_count": invalid_count,
                    "total_count": len(units),
                    "invalid_units": invalid_units[:5],  # Solo primeros 5
                    "bug_type": "range_filter_failure",
                },
            )

        return ValidationResult(
            field_name=field_name,
            expected_value=f"{min_value}-{max_value}",
            actual_values=actual_values,
            is_valid=is_valid,
            invalid_count=invalid_count,
            total_count=len(units),
            message=message,
            details={
                "invalid_units": invalid_units,
                "filter_applied": filter_applied,
                "min_value": min_value,
                "max_value": max_value,
            },
        )

    def validate_array_parameter(
        self, parameter_name: str, parameter_value: Any, expected_type: type = list
    ) -> ValidationResult:
        """
        Valida que un parámetro de array tenga el formato correcto

        Args:
            parameter_name: Nombre del parámetro
            parameter_value: Valor del parámetro
            expected_type: Tipo esperado (list, str, etc.)

        Returns:
            ValidationResult con el resultado de la validación
        """
        is_valid = isinstance(parameter_value, expected_type)

        message = (
            f"✅ Parámetro {parameter_name} tiene formato correcto"
            if is_valid
            else f"❌ Parámetro {parameter_name} formato incorrecto: esperado {expected_type.__name__}, recibido {type(parameter_value).__name__}"
        )

        # Log warning si hay problemas de formato
        if not is_valid and self.logger:
            self.logger.warning(
                f"BUG DETECTADO: Formato de parámetro {parameter_name} incorrecto",
                extra={
                    "parameter_name": parameter_name,
                    "expected_type": expected_type.__name__,
                    "actual_type": type(parameter_value).__name__,
                    "actual_value": str(parameter_value)[
                        :100
                    ],  # Truncar si es muy largo
                    "bug_type": "parameter_format_error",
                },
            )

        return ValidationResult(
            field_name=parameter_name,
            expected_value=expected_type.__name__,
            actual_values=[type(parameter_value).__name__],
            is_valid=is_valid,
            invalid_count=0 if is_valid else 1,
            total_count=1,
            message=message,
            details={
                "expected_type": expected_type.__name__,
                "actual_type": type(parameter_value).__name__,
                "actual_value": parameter_value,
            },
        )

    def generate_validation_report(
        self,
        validation_results: List[ValidationResult],
        search_params: Optional[Dict[str, Any]] = None,
    ) -> ValidationReport:
        """
        Genera un reporte completo de validaciones

        Args:
            validation_results: Lista de resultados de validación
            search_params: Parámetros de búsqueda originales (opcional)

        Returns:
            ValidationReport con resumen completo
        """
        total_validations = len(validation_results)
        passed_validations = sum(1 for r in validation_results if r.is_valid)
        failed_validations = total_validations - passed_validations
        has_issues = failed_validations > 0

        # Generar resumen
        if has_issues:
            failed_fields = [r.field_name for r in validation_results if not r.is_valid]
            summary = f"❌ {failed_validations}/{total_validations} validaciones fallaron. Campos problemáticos: {', '.join(failed_fields)}"
        else:
            summary = (
                f"✅ Todas las {total_validations} validaciones pasaron correctamente"
            )

        return ValidationReport(
            total_validations=total_validations,
            passed_validations=passed_validations,
            failed_validations=failed_validations,
            results=validation_results,
            summary=summary,
            has_issues=has_issues,
        )

    def validate_units_response(
        self, units: List[Dict[str, Any]], search_params: Dict[str, Any]
    ) -> ValidationReport:
        """
        Valida una respuesta completa de búsqueda de unidades

        Args:
            units: Lista de unidades devueltas
            search_params: Parámetros de búsqueda originales

        Returns:
            ValidationReport con todas las validaciones
        """
        validation_results = []

        # Validar filtros booleanos (camelCase según documentación oficial)
        is_active_key = "isActive" if "isActive" in search_params else "is_active"
        if search_params.get(is_active_key) is not None:
            is_active_value = bool(search_params[is_active_key])
            # Buscar en el campo procesado (snake_case) no en el original (camelCase)
            result = self.validate_boolean_filter(
                units, "is_active", is_active_value, filter_applied=True
            )
            validation_results.append(result)

        is_bookable_key = (
            "isBookable" if "isBookable" in search_params else "is_bookable"
        )
        if search_params.get(is_bookable_key) is not None:
            is_bookable_value = bool(search_params[is_bookable_key])
            result = self.validate_boolean_filter(
                units, "is_bookable", is_bookable_value, filter_applied=True
            )
            validation_results.append(result)

        pets_friendly_key = (
            "petsFriendly" if "petsFriendly" in search_params else "pets_friendly"
        )
        if search_params.get(pets_friendly_key) is not None:
            pets_friendly_value = bool(search_params[pets_friendly_key])
            result = self.validate_boolean_filter(
                units, "pets_friendly", pets_friendly_value, filter_applied=True
            )
            validation_results.append(result)

        # Validar filtros de rango (camelCase según documentación oficial)
        min_bedrooms_key = (
            "minBedrooms" if "minBedrooms" in search_params else "min_bedrooms"
        )
        max_bedrooms_key = (
            "maxBedrooms" if "maxBedrooms" in search_params else "max_bedrooms"
        )
        if (
            search_params.get(min_bedrooms_key) is not None
            or search_params.get(max_bedrooms_key) is not None
        ):
            result = self.validate_range_filter(
                units,
                "bedrooms",
                min_value=search_params.get(min_bedrooms_key),
                max_value=search_params.get(max_bedrooms_key),
                filter_applied=True,
            )
            validation_results.append(result)

        if (
            search_params.get("min_bathrooms") is not None
            or search_params.get("max_bathrooms") is not None
        ):
            result = self.validate_range_filter(
                units,
                "bathrooms",
                min_value=search_params.get("min_bathrooms"),
                max_value=search_params.get("max_bathrooms"),
                filter_applied=True,
            )
            validation_results.append(result)

        if (
            search_params.get("min_occupancy") is not None
            or search_params.get("max_occupancy") is not None
        ):
            result = self.validate_range_filter(
                units,
                "occupancy",
                min_value=search_params.get("min_occupancy"),
                max_value=search_params.get("max_occupancy"),
                filter_applied=True,
            )
            validation_results.append(result)

        # Validar formato de parámetros de array
        if search_params.get("unit_ids") is not None:
            result = self.validate_array_parameter(
                "unit_ids", search_params["unit_ids"], list
            )
            validation_results.append(result)

        return self.generate_validation_report(validation_results, search_params)
