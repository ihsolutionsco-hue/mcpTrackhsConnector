"""
Validadores de fecha para parámetros de API TrackHS
Permite valores null y fechas en formato ISO 8601
"""

import re
from datetime import datetime
from typing import Optional, Union


class DateValidator:
    """Validador de fechas para parámetros de API TrackHS"""

    # Patrón para fechas ISO 8601 (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SSZ)
    ISO_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$")

    @classmethod
    def validate_optional_date(cls, date_value: Optional[str]) -> Optional[str]:
        """
        Valida una fecha opcional que puede ser null o formato ISO 8601

        Args:
            date_value: Valor de fecha a validar (puede ser None, 'null', o fecha ISO)

        Returns:
            Fecha validada o None si es null

        Raises:
            ValueError: Si el formato de fecha es inválido
        """
        if date_value is None:
            return None

        # Permitir string 'null' como valor nulo
        if date_value.lower() == "null":
            return None

        # Validar formato ISO 8601
        if not cls.ISO_DATE_PATTERN.match(date_value):
            raise ValueError(
                f"Formato de fecha inválido: '{date_value}'. "
                f"Use formato ISO 8601: YYYY-MM-DD o YYYY-MM-DDTHH:MM:SSZ"
            )

        # Validar que la fecha sea válida
        try:
            if "T" in date_value:
                # Fecha con tiempo
                datetime.fromisoformat(date_value.replace("Z", "+00:00"))
            else:
                # Solo fecha
                datetime.fromisoformat(date_value)
        except ValueError as e:
            raise ValueError(f"Fecha inválida: '{date_value}'. {str(e)}")

        return date_value

    @classmethod
    def validate_date_range(
        cls, start_date: Optional[str], end_date: Optional[str]
    ) -> tuple[Optional[str], Optional[str]]:
        """
        Valida un rango de fechas asegurando que start <= end

        Args:
            start_date: Fecha de inicio
            end_date: Fecha de fin

        Returns:
            Tupla con fechas validadas

        Raises:
            ValueError: Si el rango de fechas es inválido
        """
        start_validated = cls.validate_optional_date(start_date)
        end_validated = cls.validate_optional_date(end_date)

        # Si ambas fechas están presentes, validar que start <= end
        if start_validated and end_validated:
            try:
                start_dt = datetime.fromisoformat(
                    start_validated.replace("T", " ").replace("Z", "")
                )
                end_dt = datetime.fromisoformat(
                    end_validated.replace("T", " ").replace("Z", "")
                )

                if start_dt > end_dt:
                    raise ValueError(
                        f"Fecha de inicio ({start_validated}) debe ser anterior o igual "
                        f"a fecha de fin ({end_validated})"
                    )
            except ValueError as e:
                raise ValueError(f"Error validando rango de fechas: {str(e)}")

        return start_validated, end_validated

    @classmethod
    def is_valid_date_format(cls, date_value: str) -> bool:
        """
        Verifica si una fecha tiene formato válido sin lanzar excepción

        Args:
            date_value: Fecha a verificar

        Returns:
            True si el formato es válido, False en caso contrario
        """
        if not date_value or date_value.lower() == "null":
            return True

        return bool(cls.ISO_DATE_PATTERN.match(date_value))
