# Inicio Rápido - Agentes de Voz 🎙️

## 🚀 Configuración en 3 Pasos

### 1. Configurar Variables de Entorno

Copia `env.example` a `.env` y configura:

```bash
# Credenciales TrackHS (requeridas)
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_contraseña
TRACKHS_API_URL=https://ihmvacations.trackhs.com

# ⚠️ IMPORTANTE: Optimización para agentes de voz
TRACKHS_COMPACT_RESPONSES=true
TRACKHS_MAX_RESPONSE_ITEMS=3
TRACKHS_MAX_RESPONSE_TOKENS=2000
```

### 2. Verificar Configuración

El archivo `fastmcp.json` ya incluye:

```json
{
  "response_optimization": {
    "compact_responses": true,
    "voice_agent_mode": {
      "enabled": true,
      "max_reservation_results": 3,
      "max_unit_results": 2,
      "max_amenity_results": 10
    }
  }
}
```

### 3. Usar con Límites Apropiados

En tus llamadas a herramientas, usa los defaults o especifica valores bajos:

```python
# ✅ BIEN - Para agentes de voz
search_reservations(
    arrival_start="2024-10-24",
    status="Confirmed",
    size=3  # Default optimizado
)

# ❌ EVITAR - Para agentes de voz
search_reservations(
    size=50  # Demasiado grande
)
```

---

## 📊 Límites Recomendados

| Herramienta | Default | Recomendado Voz | Máximo Seguro |
|-------------|---------|-----------------|---------------|
| `search_reservations` | 3 | 3-5 | 10 |
| `search_units` | 2 | 2-3 | 5 |
| `search_amenities` | 10 | 5-10 | 20 |
| `get_reservation` | N/A | 1 (usar compactor) | 1 |

---

## 🎯 Ejemplos de Uso

### Caso 1: Check-in de Huésped

```python
# Buscar reserva del cliente
search_reservations(
    contact_id="123456",
    arrival_start="2024-10-24",
    size=1
)
# Respuesta: ~500 tokens (compactada)
```

### Caso 2: Disponibilidad de Unidades

```python
# Buscar unidades disponibles
search_units(
    arrival="2024-11-01",
    departure="2024-11-05",
    bedrooms="2",
    size=2
)
# Respuesta: ~800 tokens (compactada)
```

### Caso 3: Información de Amenidades

```python
# Buscar amenidades pet-friendly
search_amenities(
    search="pet",
    is_public="1",
    size=10
)
# Respuesta: ~300 tokens (compactada)
```

---

## ⚠️ Señales de Advertencia

Si experimentas estos problemas, **reduce los límites**:

- ❌ Error "Context window exceeded"
- ❌ Timeouts frecuentes
- ❌ Respuestas cortadas
- ❌ Latencia > 5 segundos
- ❌ Errores de ElevenLabs

---

## 🔧 Troubleshooting Rápido

### Error de Contexto

```bash
# Reduce límites
TRACKHS_MAX_RESPONSE_ITEMS=2
TRACKHS_MAX_RESPONSE_TOKENS=1500
```

### Timeout

```bash
# Activa compactación
TRACKHS_COMPACT_RESPONSES=true
```

### Respuestas Incompletas

```python
# Usa filtros más específicos
search_reservations(
    arrival_start="2024-10-24",  # Fecha específica
    arrival_end="2024-10-24",    # Rango pequeño
    status="Confirmed",          # Estado específico
    size=3
)
```

---

## 📖 Documentación Completa

- [Mejores Prácticas Detalladas](./VOICE_AGENT_BEST_PRACTICES.md)
- [Ejemplos de Uso](../examples/)
- [Documentación API](./trackhsDoc/)

---

## 🆘 Soporte

**¿Problemas?** Revisa:
1. Variables de entorno configuradas correctamente
2. Límites apropiados para tu caso de uso
3. Logs: `FASTMCP_LOG_LEVEL=DEBUG`
4. [GitHub Issues](https://github.com/ihsolutionsco-hue/mcpTrackhsConnector/issues)

---

**Configurado correctamente:** ✅ Respuestas rápidas, sin errores de contexto, conversaciones fluidas
**Mal configurado:** ❌ Timeouts, errores, respuestas largas, mala experiencia

