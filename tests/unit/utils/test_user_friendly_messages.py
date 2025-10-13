"""
Tests de mensajes de error amigables
"""

import pytest

from src.trackhs_mcp.infrastructure.utils.user_friendly_messages import (
    format_boolean_error,
    format_date_error,
    format_id_list_error,
    format_range_error,
    format_required_error,
    format_type_error,
)


class TestUserFriendlyMessages:
    """Tests para verificar que los mensajes de error son amigables"""

    def test_format_date_error_includes_examples(self):
        """Verifica que mensajes de fecha incluyen ejemplos"""
        message = format_date_error("arrival_start")

        # Verificar que incluye ejemplos
        assert "2025-01-01" in message
        assert "2025-01-01T00:00:00Z" in message
        assert "arrival_start='2025-01-15'" in message

        # Verificar que es claro
        assert "Formato de fecha inválido" in message
        assert "Usa formato ISO 8601" in message

    def test_format_date_error_is_clear(self):
        """Verifica que mensajes de fecha son claros"""
        message = format_date_error("departure_end")

        # Verificar estructura del mensaje
        assert "departure_end" in message
        assert "Solo fecha:" in message
        assert "Fecha y hora:" in message
        assert "Ejemplo:" in message

    def test_format_type_error_is_clear(self):
        """Verifica que mensajes de tipo son claros"""
        message = format_type_error("bedrooms", "número entero", "dos")

        # Verificar que incluye información útil
        assert "bedrooms" in message
        assert "dos" in message
        assert "número entero" in message
        assert "bedrooms=1" in message

    def test_format_range_error_includes_bounds(self):
        """Verifica que mensajes de rango incluyen límites"""
        message = format_range_error("size", 1, 1000)

        # Verificar que incluye límites
        assert "size" in message
        assert "1" in message
        assert "1000" in message
        assert "size=1" in message

    def test_format_required_error_is_clear(self):
        """Verifica que mensajes de parámetros requeridos son claros"""
        message = format_required_error("reservation_id")

        # Verificar que es claro
        assert "reservation_id" in message
        assert "es requerido" in message
        assert "reservation_id=1" in message

    def test_format_boolean_error_includes_examples(self):
        """Verifica que mensajes de boolean incluyen ejemplos"""
        message = format_boolean_error("is_active", "true")

        # Verificar que incluye ejemplos
        assert "is_active" in message
        assert "true" in message
        assert "0 (No)" in message
        assert "1 (Sí)" in message
        assert "is_active=1" in message

    def test_format_id_list_error_includes_formats(self):
        """Verifica que mensajes de lista de IDs incluyen formatos"""
        message = format_id_list_error("node_id", "1 2 3")

        # Verificar que incluye formatos válidos
        assert "node_id" in message
        assert "1 2 3" in message
        assert "'1,2,3'" in message
        assert "'[1,2,3]'" in message

    def test_all_messages_are_in_spanish(self):
        """Verifica que todos los mensajes están en español"""
        messages = [
            format_date_error("test"),
            format_type_error("test", "tipo", "valor"),
            format_range_error("test", 1, 10),
            format_required_error("test"),
            format_boolean_error("test", "valor"),
            format_id_list_error("test", "valor"),
        ]

        for message in messages:
            # Verificar que no hay palabras en inglés comunes
            assert "Invalid" not in message
            assert "Error" not in message
            assert "Use" not in message
            assert "Must" not in message

    def test_messages_include_practical_examples(self):
        """Verifica que los mensajes incluyen ejemplos prácticos"""
        # Test date error
        date_msg = format_date_error("arrival_start")
        assert "arrival_start='2025-01-15'" in date_msg

        # Test type error
        type_msg = format_type_error("bedrooms", "número entero", "dos")
        assert "bedrooms=1" in type_msg

        # Test required error
        required_msg = format_required_error("reservation_id")
        assert "reservation_id=1" in required_msg

    def test_messages_are_user_friendly(self):
        """Verifica que los mensajes son amigables para usuarios no técnicos"""
        # Test que no hay jerga técnica
        date_msg = format_date_error("test")
        assert "ISO 8601" in date_msg  # Pero con explicación

        # Test que incluye contexto
        type_msg = format_type_error("bedrooms", "número entero", "dos")
        assert "Se esperaba" in type_msg
        assert "Ejemplo" in type_msg

    def test_messages_are_helpful(self):
        """Verifica que los mensajes son útiles para resolver problemas"""
        # Test date error - debe mostrar formatos válidos
        date_msg = format_date_error("arrival_start")
        assert "Solo fecha:" in date_msg
        assert "Fecha y hora:" in date_msg

        # Test boolean error - debe mostrar valores válidos
        bool_msg = format_boolean_error("is_active", "true")
        assert "0 (No)" in bool_msg
        assert "1 (Sí)" in bool_msg

        # Test ID list error - debe mostrar formatos válidos
        id_msg = format_id_list_error("node_id", "1 2 3")
        assert "1,2,3" in id_msg
        assert "[1,2,3]" in id_msg
