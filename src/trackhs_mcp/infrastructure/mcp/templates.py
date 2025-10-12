"""
Templates MCP para formateo de respuestas de TrackHS API V2
Proporciona templates para estructurar y formatear datos de reservas
"""

from typing import Any, Dict, List, Optional

from ...application.ports.api_client_port import ApiClientPort


def register_all_templates(mcp, api_client: ApiClientPort):
    """Registra todos los templates MCP para formateo de respuestas"""

    # Template para resumen de reserva
    @mcp.template
    def reservation_summary_template(reservation_data: Dict[str, Any]) -> str:
        """
        Template para formatear un resumen ejecutivo de reserva.

        Args:
            reservation_data: Datos completos de la reserva desde get_reservation_v2

        Returns:
            String formateado con resumen ejecutivo
        """
        # Extraer datos básicos
        reservation_id = reservation_data.get("id", "N/A")
        status = reservation_data.get("status", "N/A")
        arrival_date = reservation_data.get("arrivalDate", "N/A")
        departure_date = reservation_data.get("departureDate", "N/A")
        nights = reservation_data.get("nights", 0)
        currency = reservation_data.get("currency", "USD")

        # Extraer información de contacto
        embedded = reservation_data.get("_embedded", {})
        contact = embedded.get("contact", {})
        contact_name = contact.get("name", "N/A")
        contact_email = contact.get("primaryEmail", "N/A")

        # Extraer información de unidad
        unit = embedded.get("unit", {})
        unit_name = unit.get("name", "N/A")
        unit_address = unit.get("streetAddress", "N/A")

        # Extraer información financiera
        guest_breakdown = reservation_data.get("guestBreakdown", {})
        total = guest_breakdown.get("total", "0.00")
        balance = guest_breakdown.get("balance", "0.00")

        return f"""
🏨 RESUMEN DE RESERVA #{reservation_id}
═══════════════════════════════════════════════════════════════

📋 INFORMACIÓN BÁSICA
• Estado: {status}
• Fechas: {arrival_date} → {departure_date} ({nights} noches)
• Moneda: {currency}

👤 HUÉSPED
• Nombre: {contact_name}
• Email: {contact_email}

🏠 UNIDAD
• Nombre: {unit_name}
• Dirección: {unit_address}

💰 FINANZAS
• Total: {currency} {total}
• Balance: {currency} {balance}
"""

    # Template para análisis financiero
    @mcp.template
    def reservation_financial_analysis_template(
        reservation_data: Dict[str, Any]
    ) -> str:
        """
        Template para formatear análisis financiero detallado de reserva.

        Args:
            reservation_data: Datos completos de la reserva

        Returns:
            String formateado con análisis financiero
        """
        # Extraer breakdowns financieros
        guest_breakdown = reservation_data.get("guestBreakdown", {})
        owner_breakdown = reservation_data.get("ownerBreakdown", {})

        # Datos del huésped
        gross_rent = guest_breakdown.get("grossRent", "0.00")
        net_rent = guest_breakdown.get("netRent", "0.00")
        discount = guest_breakdown.get("discount", "0.00")
        total_taxes = guest_breakdown.get("totalTaxes", "0.00")
        total_fees = guest_breakdown.get("totalGuestFees", "0.00")
        grand_total = guest_breakdown.get("grandTotal", "0.00")
        balance = guest_breakdown.get("balance", "0.00")

        # Datos del propietario
        owner_gross = owner_breakdown.get("grossRent", "0.00")
        owner_net = owner_breakdown.get("netRevenue", "0.00")
        manager_commission = owner_breakdown.get("managerCommission", "0.00")

        return f"""
💰 ANÁLISIS FINANCIERO DETALLADO
═══════════════════════════════════════════════════════════════

📊 DESGLOSE DEL HUÉSPED
• Renta Bruta: {gross_rent}
• Renta Neta: {net_rent}
• Descuento: {discount}
• Impuestos: {total_taxes}
• Tarifas: {total_fees}
• Total Final: {grand_total}
• Balance Pendiente: {balance}

🏢 DESGLOSE DEL PROPIETARIO
• Renta Bruta: {owner_gross}
• Renta Neta: {owner_net}
• Comisión Manager: {manager_commission}

📈 MÉTRICAS CLAVE
• Margen de Descuento: {discount}
• Carga Fiscal: {total_taxes}
• Comisión Total: {manager_commission}
"""

    # Template para información completa
    @mcp.template
    def reservation_full_details_template(reservation_data: Dict[str, Any]) -> str:
        """
        Template para formatear información completa de reserva.

        Args:
            reservation_data: Datos completos de la reserva

        Returns:
            String formateado con información completa
        """
        # Extraer datos básicos
        reservation_id = reservation_data.get("id", "N/A")
        status = reservation_data.get("status", "N/A")
        arrival_date = reservation_data.get("arrivalDate", "N/A")
        departure_date = reservation_data.get("departureDate", "N/A")
        nights = reservation_data.get("nights", 0)
        currency = reservation_data.get("currency", "USD")

        # Extraer datos embebidos
        embedded = reservation_data.get("_embedded", {})
        contact = embedded.get("contact", {})
        unit = embedded.get("unit", {})
        guarantee_policy = embedded.get("guaranteePolicy", {})
        cancellation_policy = embedded.get("cancellationPolicy", {})

        # Extraer información financiera
        guest_breakdown = reservation_data.get("guestBreakdown", {})
        owner_breakdown = reservation_data.get("ownerBreakdown", {})

        # Template para políticas
        def policies_template(data):
            guarantee = data.get("guaranteePolicy", {})
            cancellation = data.get("cancellationPolicy", {})
            return f"""
📋 POLÍTICAS Y ACUERDOS
• Garantía: {guarantee.get('name', 'N/A')} ({guarantee.get('type', 'N/A')})
• Cancelación: {cancellation.get('name', 'N/A')} ({cancellation.get('chargeAs', 'N/A')})
"""

        # Template para información de unidad
        def unit_information_template(data):
            unit = data.get("unit", {})
            return f"""
🏠 INFORMACIÓN DE UNIDAD
• Nombre: {unit.get('name', 'N/A')}
• Dirección: {unit.get('streetAddress', 'N/A')}
• Capacidad: {unit.get('maxOccupancy', 'N/A')} huéspedes
• Habitaciones: {unit.get('bedrooms', 'N/A')}
• Baños: {unit.get('fullBathrooms', 'N/A')}
"""

        # Construir resumen
        summary = f"""
🏨 INFORMACIÓN COMPLETA DE RESERVA #{reservation_id}
═══════════════════════════════════════════════════════════════

📋 DATOS BÁSICOS
• Estado: {status}
• Fechas: {arrival_date} → {departure_date} ({nights} noches)
• Moneda: {currency}

👤 INFORMACIÓN DE CONTACTO
• Nombre: {contact.get('name', 'N/A')}
• Email: {contact.get('primaryEmail', 'N/A')}
• Teléfono: {contact.get('cellPhone', 'N/A')}
"""

        # Construir análisis financiero
        financial = f"""
💰 ANÁLISIS FINANCIERO
• Total Huésped: {guest_breakdown.get('grandTotal', '0.00')}
• Balance: {guest_breakdown.get('balance', '0.00')}
• Renta Propietario: {owner_breakdown.get('netRevenue', '0.00')}
"""

        # Construir información de huésped
        guest = f"""
👥 INFORMACIÓN DE HUÉSPED
• Nombre: {contact.get('name', 'N/A')}
• Email: {contact.get('primaryEmail', 'N/A')}
• Teléfono: {contact.get('cellPhone', 'N/A')}
"""

        # Construir políticas
        policies = policies_template(embedded)

        # Construir información de unidad
        unit = unit_information_template(embedded)

        return f"""
{summary}

{financial}

{guest}

{policies}

{unit}
"""
