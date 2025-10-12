"""
Recursos MCP mejorados para TrackHS con capacidades dinámicas
Incluye recursos en tiempo real, KPI dashboard y configuración
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from ...application.ports.api_client_port import ApiClientPort
from ..utils.logging import get_logger

logger = get_logger(__name__)


def register_enhanced_resources(mcp, api_client: ApiClientPort):
    """Registra recursos mejorados para TrackHS"""

    # Recurso de ocupación en tiempo real
    @mcp.resource("trackhs://realtime/occupancy")
    async def realtime_occupancy() -> Dict[str, Any]:
        """
        Ocupación en tiempo real de todas las propiedades.

        **Datos Incluidos:**
        - Ocupación actual por nodo
        - Check-ins/check-outs del día
        - Ocupación por tipo de unidad
        - Tendencias de ocupación
        - Alertas de ocupación
        """
        try:
            # Simular datos de ocupación en tiempo real
            # En un sistema real, esto vendría de la API de TrackHS

            current_time = datetime.now()

            occupancy_data = {
                "timestamp": current_time.isoformat(),
                "overall_occupancy": {
                    "total_units": 150,
                    "occupied_units": 120,
                    "occupancy_rate": 0.80,
                    "available_units": 30,
                },
                "by_node": {
                    "node_1": {
                        "name": "Hotel Principal",
                        "total_units": 80,
                        "occupied_units": 65,
                        "occupancy_rate": 0.81,
                        "check_ins_today": 12,
                        "check_outs_today": 8,
                    },
                    "node_2": {
                        "name": "Resort Playa",
                        "total_units": 70,
                        "occupied_units": 55,
                        "occupancy_rate": 0.79,
                        "check_ins_today": 15,
                        "check_outs_today": 10,
                    },
                },
                "by_unit_type": {
                    "studio": {"total": 50, "occupied": 40, "rate": 0.80},
                    "1br": {"total": 60, "occupied": 45, "rate": 0.75},
                    "2br": {"total": 40, "occupied": 35, "rate": 0.88},
                },
                "trends": {
                    "last_7_days": [0.75, 0.78, 0.82, 0.80, 0.85, 0.88, 0.80],
                    "forecast_next_7_days": [0.82, 0.85, 0.88, 0.90, 0.92, 0.89, 0.87],
                },
                "alerts": [
                    {
                        "type": "high_occupancy",
                        "node": "Hotel Principal",
                        "message": "Ocupación > 90% - Considerar overbooking",
                        "severity": "warning",
                    }
                ],
            }

            return occupancy_data

        except Exception as e:
            logger.error(f"Error generating realtime occupancy: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    # Recurso de dashboard KPI
    @mcp.resource("trackhs://dashboard/kpi")
    async def kpi_dashboard() -> Dict[str, Any]:
        """
        Dashboard de KPIs principales del negocio.

        **KPIs Incluidos:**
        - Ocupación y ADR
        - Ingresos y RevPAR
        - Métricas de reservas
        - Análisis de canales
        - Tendencias temporales
        """
        try:
            # Simular datos de KPI dashboard
            # En un sistema real, esto vendría de análisis de datos históricos

            current_date = datetime.now()
            last_month = current_date - timedelta(days=30)

            kpi_data = {
                "period": {
                    "current": current_date.strftime("%Y-%m-%d"),
                    "last_month": last_month.strftime("%Y-%m-%d"),
                    "generated_at": current_date.isoformat(),
                },
                "occupancy_metrics": {
                    "current_month": {
                        "occupancy_rate": 0.82,
                        "adr": 150.50,
                        "revpar": 123.41,
                        "total_revenue": 125000.00,
                    },
                    "last_month": {
                        "occupancy_rate": 0.78,
                        "adr": 145.00,
                        "revpar": 113.10,
                        "total_revenue": 118000.00,
                    },
                    "change": {
                        "occupancy_rate": 0.04,
                        "adr": 5.50,
                        "revpar": 10.31,
                        "total_revenue": 7000.00,
                    },
                },
                "reservation_metrics": {
                    "total_reservations": 245,
                    "new_reservations": 18,
                    "cancellations": 3,
                    "modifications": 7,
                    "conversion_rate": 0.15,
                    "average_booking_window": 45,  # días
                },
                "channel_performance": {
                    "direct": {"reservations": 120, "revenue": 60000, "adr": 150.00},
                    "booking.com": {
                        "reservations": 80,
                        "revenue": 40000,
                        "adr": 145.00,
                    },
                    "airbnb": {"reservations": 45, "revenue": 25000, "adr": 155.00},
                },
                "financial_summary": {
                    "total_revenue": 125000.00,
                    "gross_rent": 100000.00,
                    "fees": 15000.00,
                    "taxes": 10000.00,
                    "net_revenue": 110000.00,
                },
                "trends": {
                    "occupancy_trend": "increasing",
                    "revenue_trend": "increasing",
                    "adr_trend": "stable",
                    "booking_trend": "increasing",
                },
            }

            return kpi_data

        except Exception as e:
            logger.error(f"Error generating KPI dashboard: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    # Recurso de previsión de demanda
    @mcp.resource("trackhs://forecast/demand")
    async def demand_forecast() -> Dict[str, Any]:
        """
        Previsión de demanda para los próximos 90 días.

        **Datos de Previsión:**
        - Ocupación prevista por día
        - ADR previsto
        - Ingresos previstos
        - Análisis de estacionalidad
        - Recomendaciones de pricing
        """
        try:
            # Simular datos de previsión
            # En un sistema real, esto usaría modelos de ML

            current_date = datetime.now()
            forecast_data = {
                "generated_at": current_date.isoformat(),
                "forecast_period": {
                    "start": current_date.strftime("%Y-%m-%d"),
                    "end": (current_date + timedelta(days=90)).strftime("%Y-%m-%d"),
                    "days": 90,
                },
                "methodology": {
                    "model": "seasonal_arima",
                    "confidence_level": 0.85,
                    "last_training_date": (current_date - timedelta(days=7)).strftime(
                        "%Y-%m-%d"
                    ),
                },
                "daily_forecast": [],
                "weekly_summary": [],
                "monthly_summary": [],
                "recommendations": {
                    "pricing": [
                        "Aumentar precios en fines de semana de alta demanda",
                        "Ofrecer descuentos en días de baja ocupación prevista",
                    ],
                    "inventory": [
                        "Considerar overbooking para períodos de alta demanda",
                        "Bloquear unidades para mantenimiento en períodos de baja demanda",
                    ],
                    "marketing": [
                        "Lanzar campañas para períodos de baja ocupación",
                        "Promocionar paquetes especiales para períodos de alta demanda",
                    ],
                },
            }

            # Generar previsión diaria (simulada)
            for i in range(90):
                forecast_date = current_date + timedelta(days=i)

                # Simular estacionalidad (mayor ocupación en fines de semana)
                day_of_week = forecast_date.weekday()
                base_occupancy = 0.70
                weekend_boost = 0.15 if day_of_week >= 5 else 0

                # Simular tendencia temporal
                trend_factor = 1 + (i * 0.001)  # Ligero aumento a lo largo del tiempo

                predicted_occupancy = (
                    min(0.95, base_occupancy + weekend_boost) * trend_factor
                )
                predicted_adr = 150.00 + (
                    day_of_week * 5
                )  # ADR más alto en fines de semana

                daily_forecast = {
                    "date": forecast_date.strftime("%Y-%m-%d"),
                    "day_of_week": forecast_date.strftime("%A"),
                    "predicted_occupancy": round(predicted_occupancy, 3),
                    "predicted_adr": round(predicted_adr, 2),
                    "predicted_revenue": round(
                        predicted_occupancy * 100 * predicted_adr, 2
                    ),
                    "confidence_interval": {
                        "lower": round(predicted_occupancy * 0.85, 3),
                        "upper": round(predicted_occupancy * 1.15, 3),
                    },
                }

                forecast_data["daily_forecast"].append(daily_forecast)

            # Generar resumen semanal
            for week in range(13):  # 13 semanas = ~90 días
                week_start = current_date + timedelta(weeks=week)
                week_end = week_start + timedelta(days=6)

                week_forecast = {
                    "week": week + 1,
                    "start_date": week_start.strftime("%Y-%m-%d"),
                    "end_date": week_end.strftime("%Y-%m-%d"),
                    "avg_occupancy": round(0.75 + (week * 0.01), 3),
                    "avg_adr": round(150.00 + (week * 0.5), 2),
                    "total_revenue": round(75000 + (week * 1000), 2),
                }

                forecast_data["weekly_summary"].append(week_forecast)

            return forecast_data

        except Exception as e:
            logger.error(f"Error generating demand forecast: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    # Recurso de configuración de estados de reserva
    @mcp.resource("trackhs://config/reservation_statuses")
    async def reservation_statuses() -> Dict[str, Any]:
        """
        Configuración de estados de reserva disponibles.

        **Estados Incluidos:**
        - Hold: Reserva en espera
        - Confirmed: Reserva confirmada
        - Checked In: Huésped registrado
        - Checked Out: Huésped salido
        - Cancelled: Reserva cancelada
        """
        return {
            "statuses": [
                {
                    "code": "Hold",
                    "name": "En Espera",
                    "description": "Reserva temporal en espera de confirmación",
                    "color": "#FFA500",
                    "is_active": True,
                    "requires_payment": False,
                    "can_checkin": False,
                },
                {
                    "code": "Confirmed",
                    "name": "Confirmada",
                    "description": "Reserva confirmada y activa",
                    "color": "#28A745",
                    "is_active": True,
                    "requires_payment": True,
                    "can_checkin": True,
                },
                {
                    "code": "Checked In",
                    "name": "Registrado",
                    "description": "Huésped registrado en la propiedad",
                    "color": "#007BFF",
                    "is_active": True,
                    "requires_payment": True,
                    "can_checkin": False,
                },
                {
                    "code": "Checked Out",
                    "name": "Salido",
                    "description": "Huésped completó su estadía",
                    "color": "#6C757D",
                    "is_active": False,
                    "requires_payment": True,
                    "can_checkin": False,
                },
                {
                    "code": "Cancelled",
                    "name": "Cancelada",
                    "description": "Reserva cancelada",
                    "color": "#DC3545",
                    "is_active": False,
                    "requires_payment": False,
                    "can_checkin": False,
                },
            ],
            "workflow": {
                "Hold": ["Confirmed", "Cancelled"],
                "Confirmed": ["Checked In", "Cancelled"],
                "Checked In": ["Checked Out"],
                "Checked Out": [],
                "Cancelled": [],
            },
            "business_rules": {
                "auto_cancel_hold_after_hours": 24,
                "require_payment_for_confirmed": True,
                "allow_modification_until_checkin": True,
            },
        }

    # Recurso de tipos de unidad
    @mcp.resource("trackhs://config/unit_types")
    async def unit_types() -> Dict[str, Any]:
        """
        Configuración de tipos de unidad disponibles.

        **Tipos Incluidos:**
        - Studio: Estudio
        - 1BR: Un dormitorio
        - 2BR: Dos dormitorios
        - 3BR: Tres dormitorios
        - Penthouse: Ático
        """
        return {
            "unit_types": [
                {
                    "id": 1,
                    "name": "Studio",
                    "display_name": "Estudio",
                    "bedrooms": 0,
                    "bathrooms": 1,
                    "max_occupancy": 2,
                    "base_rate": 100.00,
                    "amenities": ["WiFi", "A/C", "Kitchenette"],
                    "description": "Unidad tipo estudio con cocina pequeña",
                },
                {
                    "id": 2,
                    "name": "1BR",
                    "display_name": "Un Dormitorio",
                    "bedrooms": 1,
                    "bathrooms": 1,
                    "max_occupancy": 4,
                    "base_rate": 150.00,
                    "amenities": ["WiFi", "A/C", "Full Kitchen", "Balcony"],
                    "description": "Apartamento de un dormitorio con cocina completa",
                },
                {
                    "id": 3,
                    "name": "2BR",
                    "display_name": "Dos Dormitorios",
                    "bedrooms": 2,
                    "bathrooms": 2,
                    "max_occupancy": 6,
                    "base_rate": 200.00,
                    "amenities": [
                        "WiFi",
                        "A/C",
                        "Full Kitchen",
                        "Balcony",
                        "Washer/Dryer",
                    ],
                    "description": "Apartamento de dos dormitorios con dos baños",
                },
                {
                    "id": 4,
                    "name": "3BR",
                    "display_name": "Tres Dormitorios",
                    "bedrooms": 3,
                    "bathrooms": 2,
                    "max_occupancy": 8,
                    "base_rate": 300.00,
                    "amenities": [
                        "WiFi",
                        "A/C",
                        "Full Kitchen",
                        "Balcony",
                        "Washer/Dryer",
                        "Parking",
                    ],
                    "description": "Apartamento de tres dormitorios para familias grandes",
                },
                {
                    "id": 5,
                    "name": "Penthouse",
                    "display_name": "Ático",
                    "bedrooms": 3,
                    "bathrooms": 3,
                    "max_occupancy": 8,
                    "base_rate": 500.00,
                    "amenities": [
                        "WiFi",
                        "A/C",
                        "Full Kitchen",
                        "Terrace",
                        "Washer/Dryer",
                        "Parking",
                        "Concierge",
                    ],
                    "description": "Ático de lujo con terraza privada",
                },
            ],
            "pricing_rules": {
                "base_rate_multiplier": {
                    "weekend": 1.2,
                    "holiday": 1.5,
                    "peak_season": 1.3,
                },
                "minimum_stay": {
                    "Studio": 1,
                    "1BR": 2,
                    "2BR": 3,
                    "3BR": 3,
                    "Penthouse": 7,
                },
            },
        }

    # Recurso de canales de reserva
    @mcp.resource("trackhs://config/booking_channels")
    async def booking_channels() -> Dict[str, Any]:
        """
        Configuración de canales de reserva disponibles.

        **Canales Incluidos:**
        - Direct: Reserva directa
        - Booking.com: Canal OTA
        - Airbnb: Canal de alquiler
        - Expedia: Canal OTA
        - Phone: Reserva telefónica
        """
        return {
            "channels": [
                {
                    "id": 1,
                    "name": "Direct",
                    "display_name": "Reserva Directa",
                    "type": "direct",
                    "commission_rate": 0.0,
                    "is_active": True,
                    "priority": 1,
                    "description": "Reservas directas a través del sitio web",
                },
                {
                    "id": 2,
                    "name": "Booking.com",
                    "display_name": "Booking.com",
                    "type": "ota",
                    "commission_rate": 0.15,
                    "is_active": True,
                    "priority": 2,
                    "description": "Canal OTA principal",
                },
                {
                    "id": 3,
                    "name": "Airbnb",
                    "display_name": "Airbnb",
                    "type": "rental",
                    "commission_rate": 0.14,
                    "is_active": True,
                    "priority": 3,
                    "description": "Canal de alquiler de corta duración",
                },
                {
                    "id": 4,
                    "name": "Expedia",
                    "display_name": "Expedia",
                    "type": "ota",
                    "commission_rate": 0.12,
                    "is_active": True,
                    "priority": 4,
                    "description": "Canal OTA secundario",
                },
                {
                    "id": 5,
                    "name": "Phone",
                    "display_name": "Reserva Telefónica",
                    "type": "phone",
                    "commission_rate": 0.0,
                    "is_active": True,
                    "priority": 5,
                    "description": "Reservas realizadas por teléfono",
                },
            ],
            "channel_performance": {
                "direct": {
                    "avg_booking_value": 200.00,
                    "conversion_rate": 0.12,
                    "repeat_booking_rate": 0.35,
                },
                "booking.com": {
                    "avg_booking_value": 180.00,
                    "conversion_rate": 0.08,
                    "repeat_booking_rate": 0.15,
                },
                "airbnb": {
                    "avg_booking_value": 220.00,
                    "conversion_rate": 0.10,
                    "repeat_booking_rate": 0.25,
                },
            },
            "best_practices": {
                "direct": "Optimizar sitio web para conversión",
                "ota": "Mantener precios competitivos",
                "phone": "Capacitar staff en ventas",
            },
        }
