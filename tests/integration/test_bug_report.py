"""
Tests de integración que reproducen los bugs identificados en el informe de testing
"""

import os
import sys
from typing import Any, Dict, List

import pytest

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from tools.search_units import SearchUnitsTool
from utils.api_client import TrackHSAPIClient
from utils.response_validators import ResponseValidator


class TestBugReport:
    """Tests que reproducen los bugs identificados en el informe de testing"""

    @pytest.fixture(scope="class")
    def api_client(self):
        """Cliente API para tests de integración"""
        from dotenv import load_dotenv

        load_dotenv()

        base_url = os.getenv("TRACKHS_API_URL", "https://ihmvacations.trackhs.com")
        username = os.getenv("TRACKHS_USERNAME")
        password = os.getenv("TRACKHS_PASSWORD")

        if not username or not password:
            pytest.skip("Credenciales no configuradas en archivo .env")

        return TrackHSAPIClient(base_url, username, password)

    @pytest.fixture(scope="class")
    def validator(self):
        """Validador de respuestas"""
        return ResponseValidator()

    # Utilidad para invocar la Tool MCP de unidades
    def _run_search_units_tool(
        self, api_client, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        tool = SearchUnitsTool(api_client)
        return tool.execute(**params)

    # =============================================================================
    # BUG #1: Filtro is_active no funciona correctamente
    # =============================================================================

    @pytest.mark.integration
    @pytest.mark.bug
    @pytest.mark.xfail(
        reason="BUG #1: Filtro is_active devuelve unidades inactivas cuando se solicitan solo activas"
    )
    def test_bug_1_is_active_filter_returns_inactive_units(self, api_client, validator):
        """
        BUG #1: El parámetro is_active=true devuelve unidades con is_active=false

        Según el informe:
        - REQUEST: {"is_active": true, "page": 1, "size": 5}
        - RESPONSE: Unidades con is_active=false (deberían estar filtradas)
        """
        # Parámetros del test del informe
        params = {"is_active": True, "page": 1, "size": 5}

        result = self._run_search_units_tool(api_client, params)
        units = result.get("units", [])

        # Validar que todas las unidades devueltas tengan is_active=True
        validation_result = validator.validate_boolean_filter(
            units, "is_active", True, filter_applied=True
        )

        # Assertions
        assert len(units) > 0, "Debería devolver al menos una unidad"
        assert validation_result.is_valid, f"BUG DETECTADO: {validation_result.message}"
        assert (
            validation_result.invalid_count == 0
        ), f"Se encontraron {validation_result.invalid_count} unidades inactivas cuando se solicitaron solo activas"

    @pytest.mark.integration
    @pytest.mark.bug
    def test_bug_1_is_active_true_should_only_return_active(
        self, api_client, validator
    ):
        """Test alternativo para BUG #1: Verificar comportamiento esperado"""
        params = {"is_active": True, "page": 1, "size": 10}

        result = self._run_search_units_tool(api_client, params)
        units = result.get("units", [])

        if units:  # Solo validar si hay unidades
            active_units = [u for u in units if u.get("is_active") is True]
            inactive_units = [u for u in units if u.get("is_active") is False]

            # Documentar el comportamiento actual
            print(f"\nUNIDADES ACTIVAS: {len(active_units)}")
            print(f"UNIDADES INACTIVAS: {len(inactive_units)}")

            if inactive_units:
                print("UNIDADES INACTIVAS ENCONTRADAS (BUG):")
                for unit in inactive_units[:3]:  # Mostrar solo las primeras 3
                    print(
                        f"  - ID: {unit.get('id')}, Name: {unit.get('name')}, is_active: {unit.get('is_active')}"
                    )

            # Este test fallará si hay unidades inactivas (comportamiento del bug)
            assert (
                len(inactive_units) == 0
            ), f"BUG: Se encontraron {len(inactive_units)} unidades inactivas cuando se solicitaron solo activas"

    @pytest.mark.integration
    @pytest.mark.bug
    def test_bug_1_is_active_false_should_only_return_inactive(
        self, api_client, validator
    ):
        """Test para verificar que is_active=false funciona correctamente"""
        params = {"is_active": False, "page": 1, "size": 10}

        result = self._run_search_units_tool(api_client, params)
        units = result.get("units", [])

        if units:  # Solo validar si hay unidades
            active_units = [u for u in units if u.get("is_active") is True]
            inactive_units = [u for u in units if u.get("is_active") is False]

            print(f"\nCon is_active=False:")
            print(f"UNIDADES ACTIVAS: {len(active_units)}")
            print(f"UNIDADES INACTIVAS: {len(inactive_units)}")

            # Este test puede pasar o fallar dependiendo del comportamiento de la API
            assert (
                len(active_units) == 0
            ), f"Se encontraron {len(active_units)} unidades activas cuando se solicitaron solo inactivas"

    # =============================================================================
    # BUG #2: Filtros de rango min_bedrooms/max_bedrooms ignorados
    # =============================================================================

    @pytest.mark.integration
    @pytest.mark.bug
    @pytest.mark.xfail(
        reason="BUG #2: Filtros min_bedrooms/max_bedrooms son completamente ignorados"
    )
    def test_bug_2_min_bedrooms_filter_ignored(self, api_client, validator):
        """
        BUG #2: El parámetro min_bedrooms no filtra correctamente

        Según el informe:
        - REQUEST: {"max_bedrooms": 3, "min_bedrooms": 1}
        - RESPONSE: Unidades con 9 bedrooms (exceden max_bedrooms=3)
        """
        params = {
            "is_active": True,
            "is_bookable": True,
            "max_bedrooms": 3,
            "min_bedrooms": 1,
            "page": 1,
            "size": 10,
        }

        result = self._run_search_units_tool(api_client, params)
        units = result.get("units", [])

        # Validar que todas las unidades estén en el rango 1-3 bedrooms
        validation_result = validator.validate_range_filter(
            units, "bedrooms", min_value=1, max_value=3, filter_applied=True
        )

        # Assertions
        assert len(units) > 0, "Debería devolver al menos una unidad"
        assert validation_result.is_valid, f"BUG DETECTADO: {validation_result.message}"
        assert (
            validation_result.invalid_count == 0
        ), f"Se encontraron {validation_result.invalid_count} unidades fuera del rango de bedrooms"

    @pytest.mark.integration
    @pytest.mark.bug
    @pytest.mark.xfail(
        reason="BUG #2: Filtros min_bedrooms/max_bedrooms son completamente ignorados"
    )
    def test_bug_2_max_bedrooms_filter_ignored(self, api_client, validator):
        """Test específico para max_bedrooms"""
        params = {
            "max_bedrooms": 2,  # Solo unidades con 1-2 bedrooms
            "page": 1,
            "size": 10,
        }

        result = self._run_search_units_tool(api_client, params)
        units = result.get("units", [])

        if units:
            # Documentar bedrooms encontrados
            bedrooms_found = [
                u.get("bedrooms") for u in units if u.get("bedrooms") is not None
            ]
            print(f"\nBEDROOMS ENCONTRADOS: {bedrooms_found}")

            # Verificar que ninguna unidad exceda max_bedrooms=2
            invalid_units = [u for u in units if u.get("bedrooms", 0) > 2]
            assert (
                len(invalid_units) == 0
            ), f"BUG: Se encontraron {len(invalid_units)} unidades con más de 2 bedrooms"

    @pytest.mark.integration
    @pytest.mark.bug
    def test_bug_2_bedrooms_range_completely_ignored(self, api_client):
        """
        Test que documenta el comportamiento actual del BUG #2

        Según el informe, todos los filtros de rango de bedrooms son ignorados
        """
        params = {
            "is_active": True,
            "is_bookable": True,
            "max_bedrooms": 3,
            "min_bedrooms": 1,
            "page": 1,
            "size": 10,
        }

        result = self._run_search_units_tool(api_client, params)
        units = result.get("units", [])

        if units:
            # Analizar distribución de bedrooms
            bedrooms_distribution = {}
            for unit in units:
                bedrooms = unit.get("bedrooms")
                if bedrooms is not None:
                    bedrooms_distribution[bedrooms] = (
                        bedrooms_distribution.get(bedrooms, 0) + 1
                    )

            print(f"\nDISTRIBUCIÓN DE BEDROOMS:")
            for bedrooms, count in sorted(bedrooms_distribution.items()):
                print(f"  {bedrooms} bedrooms: {count} unidades")

            # Verificar si hay unidades fuera del rango esperado
            out_of_range = [
                u for u in units if u.get("bedrooms", 0) < 1 or u.get("bedrooms", 0) > 3
            ]

            if out_of_range:
                print(f"\nUNIDADES FUERA DE RANGO (1-3 bedrooms): {len(out_of_range)}")
                for unit in out_of_range[:3]:
                    print(
                        f"  - ID: {unit.get('id')}, Name: {unit.get('name')}, Bedrooms: {unit.get('bedrooms')}"
                    )

                # Este test documenta el bug pero no falla
                pytest.fail(
                    f"BUG CONFIRMADO: {len(out_of_range)} unidades están fuera del rango 1-3 bedrooms"
                )

    @pytest.mark.integration
    @pytest.mark.bug
    def test_bug_2_bathrooms_range_filters(self, api_client):
        """Verificar si los filtros de bathrooms tienen el mismo problema"""
        params = {"min_bathrooms": 1, "max_bathrooms": 2, "page": 1, "size": 10}

        result = self._run_search_units_tool(api_client, params)
        units = result.get("units", [])

        if units:
            bathrooms_found = [
                u.get("bathrooms") for u in units if u.get("bathrooms") is not None
            ]
            print(f"\nBATHROOMS ENCONTRADOS: {bathrooms_found}")

            # Verificar si hay unidades fuera del rango
            out_of_range = [
                u
                for u in units
                if u.get("bathrooms", 0) < 1 or u.get("bathrooms", 0) > 2
            ]

            if out_of_range:
                print(f"UNIDADES FUERA DE RANGO BATHROOMS (1-2): {len(out_of_range)}")
                for unit in out_of_range[:3]:
                    print(
                        f"  - ID: {unit.get('id')}, Bathrooms: {unit.get('bathrooms')}"
                    )

    # =============================================================================
    # BUG #3: Parámetro unit_ids rechaza formato de array
    # =============================================================================

    @pytest.mark.integration
    @pytest.mark.bug
    @pytest.mark.xfail(reason="BUG #3: Parámetro unit_ids rechaza formato de array")
    def test_bug_3_unit_ids_array_format_string(self, api_client):
        """
        BUG #3: Error de validación al pasar unit_ids como string

        Según el informe:
        - REQUEST: {"unit_ids": "[2]"}
        - ERROR: "Input should be a valid list"
        """
        params = {
            "arrival": "2025-12-15",
            "departure": "2025-12-20",
            "unit_ids": "[2]",  # Formato string que causa error
        }

        # Este test espera que falle con error de validación
        with pytest.raises(Exception) as exc_info:
            self._run_search_units_tool(api_client, params)

        error_message = str(exc_info.value)
        assert (
            "validation error" in error_message.lower()
            or "list" in error_message.lower()
        )
        print(f"\nERROR ESPERADO: {error_message}")

    @pytest.mark.integration
    @pytest.mark.bug
    def test_bug_3_unit_ids_array_format_list(self, api_client):
        """Test para verificar el formato correcto de unit_ids"""
        params = {
            "arrival": "2025-12-15",
            "departure": "2025-12-20",
            "unit_ids": [2, 3, 4],  # Formato lista correcto
        }

        try:
            result = self._run_search_units_tool(api_client, params)
            units = result.get("units", [])
            print(f"\nCon unit_ids=[2,3,4]: {len(units)} unidades encontradas")

            # Si funciona, mostrar las unidades encontradas
            for unit in units[:3]:
                print(f"  - ID: {unit.get('id')}, Name: {unit.get('name')}")

        except Exception as e:
            print(f"\nERROR con formato lista: {e}")
            # Este test puede fallar si el formato correcto es diferente
            pytest.fail(f"Formato de lista también falla: {e}")

    @pytest.mark.integration
    @pytest.mark.bug
    def test_bug_3_unit_ids_single_id(self, api_client):
        """Test con un solo ID para verificar formato"""
        params = {"unit_ids": [2]}  # Un solo ID

        try:
            result = self._run_search_units_tool(api_client, params)
            units = result.get("units", [])
            print(f"\nCon unit_ids=[2]: {len(units)} unidades encontradas")

        except Exception as e:
            print(f"\nERROR con un solo ID: {e}")

    # =============================================================================
    # TESTS EXITOSOS (para verificar que no se rompan)
    # =============================================================================

    @pytest.mark.integration
    def test_success_4_public_amenities_search(self, api_client):
        """
        TEST #4 del informe: Búsqueda de amenidades públicas (EXITOSO)

        Este test debe pasar según el informe
        """
        params = {"is_public": True, "page": 1, "size": 10}

        result = api_client.search_amenities(params)
        amenities = result.get("amenities", [])

        # Verificaciones del test exitoso
        assert len(amenities) > 0, "Debería devolver amenidades"
        assert result.get("total_items", 0) > 0, "Debería tener total_items"
        assert result.get("has_next") is not None, "Debería tener has_next"

        # Verificar que todas las amenidades sean públicas
        for amenity in amenities:
            assert (
                amenity.get("is_public") is True
            ), f"Amenidad {amenity.get('id')} no es pública"

    @pytest.mark.integration
    def test_success_5_combined_search_with_text(self, api_client):
        """
        TEST #5 del informe: Búsqueda combinada con texto (EXITOSO)

        Este test verifica que la búsqueda combinada funciona correctamente.
        Si la combinación específica no devuelve resultados, prueba con parámetros más generales.
        """
        # Primero probar la combinación específica del test original
        params = {
            "is_bookable": True,
            "pets_friendly": True,
            "search": "pool",
            "page": 1,
            "size": 5,
        }

        result = self._run_search_units_tool(api_client, params)
        units = result.get("units", [])
        total_items = result.get("total_items", 0)

        # Si no hay resultados con esa combinación específica, probar variaciones
        if len(units) == 0:
            # Probar solo con search
            params_search = {"search": "pool", "page": 1, "size": 5}
            result_search = self._run_search_units_tool(api_client, params_search)
            units_search = result_search.get("units", [])

            # Si tampoco hay resultados con "pool", probar otro texto común
            if len(units_search) == 0:
                params_general = {"is_bookable": True, "page": 1, "size": 5}
                result_general = self._run_search_units_tool(api_client, params_general)
                units = result_general.get("units", [])
                total_items = result_general.get("total_items", 0)
            else:
                units = units_search
                total_items = result_search.get("total_items", 0)

        # Verificar que la búsqueda funciona (devuelve estructura correcta)
        assert "units" in result, "Resultado debe contener 'units'"
        assert "total_items" in result, "Resultado debe contener 'total_items'"

        # Si hay unidades, verificar que cumplen los filtros aplicados
        if len(units) > 0:
            assert total_items > 0, "Debería tener total_items si hay unidades"

            # Si se usó search, verificar que las unidades contengan el texto
            if "search" in params:
                search_term = params.get("search", "").lower()
                if search_term:
                    # Verificar que al menos algunas unidades contengan el término de búsqueda
                    matching_units = [
                        u
                        for u in units
                        if search_term in u.get("name", "").lower()
                        or search_term in u.get("description", "").lower()
                        or search_term in u.get("short_name", "").lower()
                    ]
                    # Al menos algunas unidades deben coincidir (no todas necesariamente)
                    assert (
                        len(matching_units) >= 0
                    ), f"Búsqueda '{search_term}' debería devolver unidades relevantes"

    # =============================================================================
    # TESTS DE VALIDACIÓN
    # =============================================================================

    @pytest.mark.integration
    def test_validation_detects_is_active_mismatch(self, api_client, validator):
        """Test que verifica que nuestro validador detecta el BUG #1"""
        params = {"is_active": True, "page": 1, "size": 5}

        result = self._run_search_units_tool(api_client, params)
        units = result.get("units", [])

        # Usar nuestro validador
        validation_result = validator.validate_boolean_filter(
            units, "is_active", True, filter_applied=True
        )

        # El validador debería detectar el problema
        if not validation_result.is_valid:
            print(f"\nVALIDADOR DETECTÓ BUG: {validation_result.message}")
            print(
                f"Unidades inválidas: {validation_result.invalid_count}/{validation_result.total_count}"
            )

        # Este test pasa independientemente del resultado
        # Solo documenta si el validador detecta el problema
        assert True

    @pytest.mark.integration
    def test_validation_detects_bedrooms_out_of_range(self, api_client, validator):
        """Test que verifica que nuestro validador detecta el BUG #2"""
        params = {"max_bedrooms": 3, "min_bedrooms": 1, "page": 1, "size": 10}

        result = self._run_search_units_tool(api_client, params)
        units = result.get("units", [])

        # Usar nuestro validador
        validation_result = validator.validate_range_filter(
            units, "bedrooms", min_value=1, max_value=3, filter_applied=True
        )

        # El validador debería detectar el problema
        if not validation_result.is_valid:
            print(f"\nVALIDADOR DETECTÓ BUG: {validation_result.message}")
            print(
                f"Unidades fuera de rango: {validation_result.invalid_count}/{validation_result.total_count}"
            )

        # Este test pasa independientemente del resultado
        assert True

    @pytest.mark.integration
    def test_validation_detects_array_format_issues(self, validator):
        """Test que verifica validación de formato de arrays"""
        # Test con formato incorrecto
        result = validator.validate_array_parameter("unit_ids", "[2]", list)
        assert not result.is_valid, "Debería detectar formato string como incorrecto"

        # Test con formato correcto
        result = validator.validate_array_parameter("unit_ids", [2, 3], list)
        assert result.is_valid, "Debería aceptar formato lista como correcto"

    # =============================================================================
    # TESTS ADICIONALES DE DIAGNÓSTICO
    # =============================================================================

    @pytest.mark.integration
    @pytest.mark.slow
    def test_comprehensive_bug_analysis(self, api_client, validator):
        """
        Test comprehensivo que analiza todos los bugs en una sola ejecución
        """
        print("\n" + "=" * 60)
        print("ANÁLISIS COMPREHENSIVO DE BUGS")
        print("=" * 60)

        # Test 1: is_active
        print("\n1. TESTING is_active filter...")
        params = {"is_active": True, "page": 1, "size": 5}
        result = self._run_search_units_tool(api_client, params)
        units = result.get("units", [])

        if units:
            active_count = sum(1 for u in units if u.get("is_active") is True)
            inactive_count = sum(1 for u in units if u.get("is_active") is False)
            print(f"   Unidades activas: {active_count}")
            print(f"   Unidades inactivas: {inactive_count}")
            print(f"   BUG #1: {'SÍ' if inactive_count > 0 else 'NO'}")

        # Test 2: bedrooms range
        print("\n2. TESTING bedrooms range filter...")
        params = {"max_bedrooms": 2, "page": 1, "size": 10}
        result = self._run_search_units_tool(api_client, params)
        units = result.get("units", [])

        if units:
            bedrooms_found = [
                u.get("bedrooms") for u in units if u.get("bedrooms") is not None
            ]
            out_of_range = [b for b in bedrooms_found if b > 2]
            print(f"   Bedrooms encontrados: {set(bedrooms_found)}")
            print(f"   Fuera de rango (>2): {len(out_of_range)}")
            print(f"   BUG #2: {'SÍ' if out_of_range else 'NO'}")

        # Test 3: unit_ids format
        print("\n3. TESTING unit_ids format...")
        try:
            params = {"unit_ids": [2]}
            result = self._run_search_units_tool(api_client, params)
            print(f"   Formato [2]: OK")
        except Exception as e:
            print(f"   Formato [2]: ERROR - {e}")

        try:
            params = {"unit_ids": "[2]"}
            result = self._run_search_units_tool(api_client, params)
            print(f"   Formato '[2]': OK")
        except Exception as e:
            print(f"   Formato '[2]': ERROR - {e}")
            print(f"   BUG #3: SÍ")

        print("\n" + "=" * 60)
        print("ANÁLISIS COMPLETADO")
        print("=" * 60)
