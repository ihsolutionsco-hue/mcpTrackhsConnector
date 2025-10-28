"""
Servicio de Unidades para TrackHS.
Contiene la lógica de negocio para unidades de alojamiento.
"""

import logging
from typing import Any, Dict, Optional

from ..exceptions import TrackHSError, ValidationError
from ..models import UnitData, UnitSearchParams, UnitSearchResponse
from ..repositories import UnitRepository

logger = logging.getLogger(__name__)


class UnitService:
    """
    Servicio para gestión de unidades de alojamiento.

    Separa la lógica de negocio de las herramientas MCP,
    permitiendo testing y reutilización.
    """

    def __init__(self, unit_repo: UnitRepository):
        self.unit_repo = unit_repo

    def search_units(
        self,
        page: int = 0,
        size: int = 10,
        search: Optional[str] = None,
        bedrooms: Optional[str] = None,
        bathrooms: Optional[str] = None,
        is_active: Optional[str] = None,
        is_bookable: Optional[str] = None,
        # Parámetros adicionales para API completa
        **additional_params: Any,
    ) -> Dict[str, Any]:
        """
        Buscar unidades de alojamiento.

        Args:
            page: Número de página (1-based)
            size: Tamaño de página (1-25)
            search: Búsqueda de texto
            bedrooms: Número de dormitorios
            bathrooms: Número de baños
            is_active: Filtrar por activas (1) o inactivas (0)
            is_bookable: Filtrar por disponibles (1) o no (0)

        Returns:
            Resultado de la búsqueda

        Raises:
            ValidationError: Si los parámetros no son válidos
            TrackHSError: Si hay error en la API
        """

        # Función helper para convertir strings a int
        def safe_int(value, param_name):
            """Convertir string a int de forma segura"""
            if value is None or value == "":
                return None
            try:
                return int(value)
            except (ValueError, TypeError):
                raise ValidationError(f"{param_name} debe ser un número válido")

        # Convertir parámetros string a int
        bedrooms_int = safe_int(bedrooms, "bedrooms")
        bathrooms_int = safe_int(bathrooms, "bathrooms")

        # Validaciones de negocio
        if page < 1:
            raise ValidationError("El número de página debe ser mayor a 0")

        if size < 1 or size > 25:
            raise ValidationError("El tamaño de página debe estar entre 1 y 25")

        if bedrooms_int is not None and bedrooms_int < 0:
            raise ValidationError("El número de dormitorios no puede ser negativo")

        if bathrooms_int is not None and bathrooms_int < 0:
            raise ValidationError("El número de baños no puede ser negativo")

        # Validar is_active con conversión automática
        if is_active is not None:
            if isinstance(is_active, str):
                is_active = 1 if is_active.lower() in ["true", "1", "yes"] else 0
            elif isinstance(is_active, bool):
                is_active = 1 if is_active else 0
            elif is_active not in [0, 1]:
                raise ValidationError(
                    "is_active debe ser 0, 1, True, False, 'true', 'false', '1', '0'"
                )

        # Validar is_bookable con conversión automática
        if is_bookable is not None:
            if isinstance(is_bookable, str):
                is_bookable = 1 if is_bookable.lower() in ["true", "1", "yes"] else 0
            elif isinstance(is_bookable, bool):
                is_bookable = 1 if is_bookable else 0
            elif is_bookable not in [0, 1]:
                raise ValidationError(
                    "is_bookable debe ser 0, 1, True, False, 'true', 'false', '1', '0'"
                )

        # Log detallado de parámetros de entrada
        logger.info(f"🔍 Iniciando búsqueda de unidades:")
        logger.info(f"   📄 Página: {page}, Tamaño: {size}")
        logger.info(f"   🔍 Búsqueda: {search if search else 'N/A'}")
        logger.info(
            f"   🛏️ Dormitorios: {bedrooms_int if bedrooms_int is not None else 'N/A'}"
        )
        logger.info(
            f"   🚿 Baños: {bathrooms_int if bathrooms_int is not None else 'N/A'}"
        )
        logger.info(f"   ✅ Activas: {is_active if is_active is not None else 'N/A'}")
        logger.info(
            f"   📅 Reservables: {is_bookable if is_bookable is not None else 'N/A'}"
        )

        try:
            # Construir parámetros base
            params = {"page": page, "size": size}
            if search:
                params["search"] = search
            if bedrooms_int is not None:
                params["bedrooms"] = bedrooms_int
            if bathrooms_int is not None:
                params["bathrooms"] = bathrooms_int
            if is_active is not None:
                params["is_active"] = is_active
            if is_bookable is not None:
                params["is_bookable"] = is_bookable

            # Agregar parámetros adicionales
            params.update(additional_params)

            logger.debug(f"📤 Parámetros enviados a API: {params}")

            result = self.unit_repo.search(params)

            # Log de respuesta cruda
            total_items = result.get("total_items", 0)
            page_count = result.get("page_count", 0)
            units_count = len(result.get("_embedded", {}).get("units", []))
            logger.info(
                f"📥 Respuesta API recibida: {total_items} total, {page_count} páginas, {units_count} unidades en esta página"
            )

            # ✅ CORRECCIÓN: Limpiar datos de respuesta para evitar errores de esquema
            if "_embedded" in result and "units" in result["_embedded"]:
                original_units = result["_embedded"]["units"]
                cleaned_units = []
                cleaning_errors = 0

                logger.debug(f"🧹 Limpiando {len(original_units)} unidades...")

                for i, unit in enumerate(original_units):
                    try:
                        # Log del área original antes de limpiar
                        original_area = unit.get("area")
                        logger.debug(
                            f"Unidad {i}: área original = {original_area} (tipo: {type(original_area)})"
                        )

                        cleaned_unit = self._clean_unit_data(unit)

                        # Log del área después de limpiar
                        cleaned_area = cleaned_unit.get("area")
                        logger.debug(
                            f"Unidad {i}: área limpia = {cleaned_area} (tipo: {type(cleaned_area)})"
                        )

                        cleaned_units.append(cleaned_unit)
                    except Exception as e:
                        cleaning_errors += 1
                        logger.warning(f"⚠️ Error limpiando unidad {i}: {e}")
                        # Mantener unidad original si no se puede limpiar
                        cleaned_units.append(unit)

                result["_embedded"]["units"] = cleaned_units

                if cleaning_errors > 0:
                    logger.warning(
                        f"⚠️ {cleaning_errors} unidades tuvieron errores de limpieza"
                    )
                else:
                    logger.debug("✅ Todas las unidades se limpiaron correctamente")

            logger.info(
                f"✅ Búsqueda de unidades completada exitosamente: {total_items} unidades encontradas"
            )
            return result

        except Exception as e:
            logger.error(f"❌ Error buscando unidades: {str(e)}")
            logger.error(f"   Parámetros que causaron el error: {params}")
            raise TrackHSError(f"Error buscando unidades: {str(e)}")

    def search_units_with_validation(
        self,
        page: int = 1,
        size: int = 10,
        search: Optional[str] = None,
        bedrooms: Optional[int] = None,
        bathrooms: Optional[int] = None,
        is_active: Optional[int] = None,
        is_bookable: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Buscar unidades con validación robusta usando Pydantic.

        Esta es la versión mejorada que usa modelos Pydantic para validación.
        """
        try:
            # Validar parámetros con Pydantic
            search_params = UnitSearchParams(
                page=page,
                size=size,
                search=search,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                is_active=is_active,
                is_bookable=is_bookable,
            )

            logger.info(
                f"✅ Parámetros validados con Pydantic: {search_params.model_dump()}"
            )

            # Usar parámetros validados
            params = search_params.to_api_params()

            # Realizar búsqueda
            result = self.unit_repo.search(params)

            # Validar respuesta con Pydantic
            try:
                validated_response = UnitSearchResponse(**result)
                logger.info(
                    f"✅ Respuesta validada con Pydantic: {validated_response.total_items} unidades"
                )
                return validated_response.model_dump()
            except Exception as validation_error:
                logger.warning(
                    f"⚠️ Error validando respuesta con Pydantic: {validation_error}"
                )
                # Devolver respuesta original si falla la validación
                return result

        except Exception as e:
            logger.error(f"❌ Error en búsqueda con validación Pydantic: {str(e)}")
            raise TrackHSError(f"Error buscando unidades: {str(e)}")

    def get_unit_by_id(self, unit_id: int) -> Dict[str, Any]:
        """
        Obtener una unidad por ID.

        Args:
            unit_id: ID de la unidad

        Returns:
            Datos de la unidad

        Raises:
            ValidationError: Si el ID no es válido
            TrackHSError: Si hay error en la API
        """
        if unit_id <= 0:
            raise ValidationError("El ID de unidad debe ser mayor a 0")

        logger.info(f"Obteniendo unidad {unit_id}")

        try:
            result = self.unit_repo.get_by_id(unit_id)
            logger.info(f"Unidad {unit_id} obtenida exitosamente")
            return result

        except Exception as e:
            logger.error(f"Error obteniendo unidad {unit_id}: {str(e)}")
            raise TrackHSError(f"Error obteniendo unidad {unit_id}: {str(e)}")

    def search_amenities(
        self, page: int = 1, size: int = 10, search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Buscar amenidades disponibles.

        Args:
            page: Número de página
            size: Tamaño de página
            search: Búsqueda de texto

        Returns:
            Resultado de la búsqueda de amenidades
        """
        # Validaciones de negocio
        if page < 1:
            raise ValidationError("El número de página debe ser mayor a 0")

        if size < 1 or size > 100:
            raise ValidationError("El tamaño de página debe estar entre 1 y 100")

        logger.info(f"Buscando amenidades: página {page}, tamaño {size}")

        try:
            params = {"page": page, "size": size}
            if search:
                params["search"] = search

            result = self.unit_repo.search_amenities(params)

            logger.info(
                f"Búsqueda de amenidades completada. Encontradas: {result.get('total_items', 0)}"
            )
            return result

        except Exception as e:
            logger.error(f"Error buscando amenidades: {str(e)}")
            raise TrackHSError(f"Error buscando amenidades: {str(e)}")

    def _clean_unit_data(self, unit_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Limpia datos de unidad para evitar errores de esquema.

        MEJOR PRÁCTICA: Transformación automática de tipos problemáticos.
        """
        cleaned = unit_data.copy()

        # Limpiar campo area específicamente - MEJORADO
        if "area" in cleaned:
            cleaned["area"] = self._normalize_area(cleaned["area"])

        # Limpiar campos numéricos - MEJORADO
        numeric_fields = ["bedrooms", "bathrooms", "max_occupancy", "floors"]
        for field in numeric_fields:
            if field in cleaned:
                cleaned[field] = self._normalize_numeric(cleaned[field])

        # Limpiar campos booleanos - MEJORADO
        boolean_fields = [
            "is_active",
            "is_bookable",
            "pet_friendly",
            "smoking_allowed",
            "children_allowed",
            "events_allowed",
            "is_accessible",
        ]
        for field in boolean_fields:
            if field in cleaned:
                cleaned[field] = self._normalize_boolean(cleaned[field])

        # Limpiar campos de tipo float - MEJORADO
        float_fields = ["longitude", "latitude"]
        for field in float_fields:
            if field in cleaned:
                cleaned[field] = self._normalize_float(cleaned[field])

        return cleaned

    def _normalize_area(self, area_value: Any) -> Optional[float]:
        """
        Normaliza el campo area a float.

        Maneja casos como:
        - "3348.0" -> 3348.0
        - "3348" -> 3348.0
        - 3348 -> 3348.0
        - None -> None
        - "invalid" -> None
        - "" -> None
        - "null" -> None
        - "N/A" -> None
        - "undefined" -> None
        """
        if area_value is None or area_value == "":
            return None

        # Manejar strings que representan valores nulos
        if isinstance(area_value, str):
            area_value = area_value.strip().lower()
            if area_value in ["null", "none", "n/a", "undefined", "nan", ""]:
                return None

        try:
            if isinstance(area_value, (int, float)):
                # Verificar si es NaN o infinito
                if isinstance(area_value, float) and (
                    area_value != area_value
                    or area_value == float("inf")
                    or area_value == float("-inf")
                ):
                    logger.debug(f"Area value is NaN or infinite: {area_value}")
                    return None
                return float(area_value)
            elif isinstance(area_value, str):
                # Limpiar string de caracteres no numéricos, manteniendo punto decimal
                cleaned_str = "".join(
                    c for c in area_value.strip() if c.isdigit() or c in ".-"
                )
                if cleaned_str:
                    # Verificar que no sea solo puntos o guiones
                    if cleaned_str.replace(".", "").replace("-", ""):
                        result = float(cleaned_str)
                        # Verificar si el resultado es válido
                        if (
                            result != result
                            or result == float("inf")
                            or result == float("-inf")
                        ):
                            logger.debug(
                                f"Area value '{area_value}' resulted in invalid float: {result}"
                            )
                            return None
                        return result
                    else:
                        logger.debug(
                            f"Area value '{area_value}' contains only non-numeric characters"
                        )
                        return None
                else:
                    logger.debug(
                        f"Area value '{area_value}' could not be converted to float"
                    )
                    return None
            else:
                logger.debug(
                    f"Area value type {type(area_value)} not supported: {area_value}"
                )
                return None
        except (ValueError, TypeError, AttributeError) as e:
            logger.warning(f"Could not normalize area value '{area_value}': {e}")
            return None

    def _normalize_numeric(self, value: Any) -> Optional[int]:
        """Normaliza valores numéricos a int."""
        if value is None:
            return None

        try:
            if isinstance(value, (int, float)):
                return int(value)
            elif isinstance(value, str):
                # Limpiar string de caracteres no numéricos
                cleaned_str = "".join(c for c in value.strip() if c.isdigit())
                if cleaned_str:
                    return int(cleaned_str)
                else:
                    return None
            else:
                return None
        except (ValueError, TypeError, AttributeError):
            logger.warning(f"Could not normalize numeric value: {value}")
            return None

    def _normalize_boolean(self, value: Any) -> Optional[bool]:
        """Normaliza valores booleanos."""
        if value is None:
            return None

        if isinstance(value, bool):
            return value
        elif isinstance(value, int):
            return bool(value)
        elif isinstance(value, str):
            return value.lower() in ["true", "1", "yes", "on", "enabled"]
        else:
            return None

    def _normalize_float(self, value: Any) -> Optional[float]:
        """Normaliza valores a float."""
        if value is None:
            return None

        try:
            if isinstance(value, (int, float)):
                return float(value)
            elif isinstance(value, str):
                # Limpiar string de caracteres no numéricos
                cleaned_str = "".join(
                    c for c in value.strip() if c.isdigit() or c in ".-"
                )
                if cleaned_str:
                    return float(cleaned_str)
                else:
                    return None
            else:
                return None
        except (ValueError, TypeError, AttributeError):
            logger.warning(f"Could not normalize float value: {value}")
            return None
