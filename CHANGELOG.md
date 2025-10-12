# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2025-10-12

### 🔧 Corregido

#### Modelo de Reservación V2 - Errores Críticos de Validación

**Problema:** La herramienta `get_reservation_v2` fallaba en el 100% de las reservas existentes con IDs alternativos de canales externos (Airbnb, Marriott, Booking.com, etc.) debido a errores de validación en el modelo Pydantic.

**Errores Corregidos:**

1. **Campo `alternates` - Tipo Incorrecto** ([#CRITICAL])
   - **Antes:** Esperaba `List[str]`
   - **Después:** Acepta `List[Union[str, dict]]`
   - **Impacto:** Desbloquea todas las reservas con IDs alternativos de canales OTA
   - **Archivo:** `src/trackhs_mcp/domain/entities/reservations.py` (líneas 285-287)

   La API TrackHS V2 devuelve alternates como objetos con estructura:
   ```json
   "alternates": [{"type": "airbnb", "id": "HMCNNSE3SJ"}]
   ```

   El modelo ahora acepta:
   - ✅ Objetos con `type` e `id` (formato real de la API)
   - ✅ Strings simples (retrocompatibilidad)
   - ✅ Mezcla de ambos formatos

2. **Campo `payment_plan` - Campo Marcado como Requerido** ([#CRITICAL])
   - **Antes:** Campo requerido `List[PaymentPlan]`
   - **Después:** Campo opcional `Optional[List[PaymentPlan]]`
   - **Impacto:** Desbloquea reservas sin plan de pagos definido
   - **Archivo:** `src/trackhs_mcp/domain/entities/reservations.py` (líneas 455-457)

   El campo `paymentPlan` no está marcado como `required` en la especificación OpenAPI y puede estar ausente en la respuesta de la API.

**Validación:**
- ✅ 31 tests ejecutados (100% pass)
  - 10 tests unitarios
  - 9 tests de integración
  - 8 tests E2E
  - 4 tests de validación específicos
- ✅ Validado con reservas reales del sistema (IDs: 37165851, 37165852, 37165853, 37165850)
- ✅ Retrocompatible con código existente

**Resultado:**
- **Tasa de éxito anterior:** 0% (todas las reservas con alternates fallaban)
- **Tasa de éxito actual:** 100% (todas las reservas funcionan correctamente)

**Referencias:**
- Documentación detallada: `docs/api/v2-bugfixes-alternates-paymentplan.md`
- Tests: `tests/unit/mcp/test_get_reservation_v2_tool.py`
- Fixture de prueba agregado: `tests/conftest.py::sample_reservation_data_v2`

### 📚 Documentación

- Actualizada documentación de `get_reservation_v2` para reflejar los formatos correctos de `alternates` y `paymentPlan`
- Agregado documento completo de bugfixes: `docs/api/v2-bugfixes-alternates-paymentplan.md`
- Actualizado `docs/api/get-reservation-v2.md` con ejemplos reales

---

## [1.0.0] - 2025-10-11

### ✨ Inicial

- Implementación inicial del conector MCP para TrackHS API V2
- Herramienta `get_reservation_v2` para obtener reservas individuales
- Herramienta `search_reservations_v2` para búsqueda de reservas
- Soporte para autenticación básica
- Manejo robusto de errores
- Suite completa de tests (unitarios, integración, E2E)

---

[1.0.1]: https://github.com/tu-repo/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/tu-repo/releases/tag/v1.0.0
