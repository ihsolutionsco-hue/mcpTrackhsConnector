"""
Clase base para herramientas MCP
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type

from pydantic import BaseModel

from utils.exceptions import TrackHSError
from utils.logger import get_logger


class BaseTool(ABC):
    """Clase base para todas las herramientas MCP"""

    def __init__(self, api_client: Any):
        self.api_client = api_client
        self.logger = get_logger(self.__class__.__name__)

    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre de la herramienta"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Descripción de la herramienta"""
        pass

    @property
    @abstractmethod
    def input_schema(self) -> Type[BaseModel]:
        """Schema de entrada (Pydantic model)"""
        pass

    @property
    @abstractmethod
    def output_schema(self) -> Type[BaseModel]:
        """Schema de salida (Pydantic model)"""
        pass

    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Ejecuta la herramienta con validación de entrada

        Args:
            **kwargs: Parámetros de entrada

        Returns:
            Resultado de la herramienta

        Raises:
            TrackHSError: Si hay error en la ejecución
        """
        self.logger.info(
            f"Iniciando ejecución de herramienta: {self.name}",
            extra={"tool_name": self.name, "action": "start", "input_params": kwargs},
        )

        try:
            # Validar entrada
            validated_input = self._validate_input(kwargs)

            # Ejecutar lógica de la herramienta
            result = self._execute_logic(validated_input)

            # Validar salida
            validated_output = self._validate_output(result)

            self.logger.info(
                f"Herramienta ejecutada exitosamente: {self.name}",
                extra={
                    "tool_name": self.name,
                    "action": "success",
                    "output_keys": (
                        list(validated_output.keys())
                        if isinstance(validated_output, dict)
                        else []
                    ),
                },
            )

            return validated_output

        except Exception as e:
            self.logger.error(
                f"Error en herramienta: {self.name}",
                extra={
                    "tool_name": self.name,
                    "action": "error",
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                },
            )
            raise

    def _validate_input(self, input_data: Dict[str, Any]) -> BaseModel:
        """
        Valida los datos de entrada usando el schema

        Args:
            input_data: Datos de entrada

        Returns:
            Datos validados como Pydantic model

        Raises:
            TrackHSValidationError: Si la validación falla
        """
        try:
            return self.input_schema(**input_data)
        except Exception as e:
            self.logger.warning(
                f"Error de validación de entrada en {self.name}",
                extra={
                    "tool_name": self.name,
                    "validation_error": str(e),
                    "input_data": input_data,
                },
            )
            raise

    def _validate_output(self, output_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida los datos de salida usando el schema

        Args:
            output_data: Datos de salida

        Returns:
            Datos validados

        Raises:
            TrackHSValidationError: Si la validación falla
        """
        try:
            # Crear instancia del schema de salida
            validated = self.output_schema(**output_data)
            return validated.model_dump()
        except Exception as e:
            self.logger.warning(
                f"Error de validación de salida en {self.name}",
                extra={
                    "tool_name": self.name,
                    "validation_error": str(e),
                    "output_data": output_data,
                },
            )
            # En caso de error de validación de salida, intentar crear una respuesta mínima válida
            try:
                # Crear una respuesta mínima con los campos requeridos
                minimal_response = {
                    "units": output_data.get("units", []),
                    "total_items": output_data.get("total_items", 0),
                    "total_pages": output_data.get("total_pages", 0),
                    "current_page": output_data.get("current_page", 1),
                    "page_size": output_data.get("page_size", 10),
                    "has_next": output_data.get("has_next", False),
                    "has_prev": output_data.get("has_prev", False),
                }
                # Agregar campos adicionales si existen
                for key, value in output_data.items():
                    if key not in minimal_response:
                        minimal_response[key] = value

                validated = self.output_schema(**minimal_response)
                return validated.model_dump()
            except Exception as e2:
                self.logger.error(
                    f"Error crítico en validación de salida en {self.name}",
                    extra={
                        "tool_name": self.name,
                        "validation_error": str(e2),
                        "original_error": str(e),
                        "output_data": output_data,
                    },
                )
                # Como último recurso, devolver los datos originales
                return output_data

    @abstractmethod
    def _execute_logic(self, validated_input: BaseModel) -> Dict[str, Any]:
        """
        Lógica específica de la herramienta

        Args:
            validated_input: Datos de entrada validados

        Returns:
            Resultado de la herramienta
        """
        pass
