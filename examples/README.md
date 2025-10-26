# 📚 Ejemplos de Uso - TrackHS MCP Server

Esta carpeta contiene ejemplos prácticos de cómo usar el TrackHS MCP Server.

## 📋 Ejemplos Disponibles

### `basic_usage.py` - Uso Básico de Todas las Herramientas

Demuestra el uso básico de las 7 herramientas del servidor MCP:

1. **search_reservations** - Buscar reservas que llegan hoy
2. **get_reservation** - Obtener detalles de una reserva
3. **search_units** - Buscar unidades disponibles
4. **get_folio** - Obtener folio financiero
5. **create_maintenance_work_order** - Crear orden de mantenimiento
6. **create_housekeeping_work_order** - Crear orden de housekeeping
7. **search_amenities** - Buscar amenidades

**Ejecutar:**
```bash
python examples/basic_usage.py
```

## ⚙️ Requisitos

### 1. Credenciales Configuradas

Asegúrate de tener un archivo `.env` en la raíz del proyecto con:

```bash
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_password
TRACKHS_API_URL=https://ihmvacations.trackhs.com/api
```

### 2. Dependencias Instaladas

```bash
pip install -r requirements.txt
```

### 3. IDs Válidos

Algunos ejemplos requieren IDs específicos (reservas, unidades). Actualiza estos valores en los scripts con IDs válidos de tu sistema TrackHS.

## 🎯 Casos de Uso por Ejemplo

### basic_usage.py

- ✅ Ver llegadas del día
- ✅ Consultar detalles de reserva
- ✅ Buscar inventario disponible
- ✅ Verificar balance financiero
- ✅ Reportar mantenimiento
- ✅ Programar limpiezas
- ✅ Consultar amenidades

## 💡 Tips

### Manejo de Errores

Todos los ejemplos incluyen manejo de errores básico. Para producción, considera:

```python
try:
    result = server.search_reservations(...)
except AuthenticationError as e:
    # Credenciales inválidas
    print(f"Error de autenticación: {e}")
except NotFoundError as e:
    # Recurso no encontrado
    print(f"No encontrado: {e}")
except ValidationError as e:
    # Datos inválidos
    print(f"Error de validación: {e}")
except APIError as e:
    # Error general de API
    print(f"Error de API: {e}")
except ConnectionError as e:
    # Error de red
    print(f"Error de conexión: {e}")
```

### Logging

Para ver más detalles durante la ejecución:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Testing

Antes de ejecutar en producción, prueba con datos de test:

```python
# Usar IDs de test
TEST_RESERVATION_ID = 99999  # ID que no existe
TEST_UNIT_ID = 88888         # ID que no existe

# Verificar que los errores se manejan correctamente
try:
    result = server.get_reservation(reservation_id=TEST_RESERVATION_ID)
except NotFoundError:
    print("✅ Error manejado correctamente")
```

## 🔒 Seguridad

### Datos Sensibles

Los logs están automáticamente sanitizados. Los siguientes datos se ocultan:

- ❌ Emails
- ❌ Teléfonos
- ❌ Direcciones
- ❌ Información de pago
- ❌ Credenciales

### Ejemplo de Log Sanitizado:

```
GET request to /pms/reservations/12345 with params: ***REDACTED***
Response preview (sanitized): {'id': 12345, 'email': '***REDACTED***', ...}
```

## 📖 Documentación Adicional

- **[README.md](../README.md)** - Documentación principal
- **[START_HERE.md](../START_HERE.md)** - Guía de inicio rápido
- **[MVP_V1.0_PLAN.md](../MVP_V1.0_PLAN.md)** - Plan detallado del MVP

## 🆘 Soporte

Si encuentras problemas con los ejemplos:

1. Verifica que las credenciales sean correctas
2. Verifica que los IDs existan en tu sistema
3. Revisa los logs para más detalles
4. Consulta la documentación de la API de TrackHS

## 🤝 Contribuir

¿Tienes un caso de uso interesante? ¡Compártelo!

1. Crea un nuevo archivo de ejemplo
2. Documenta bien el caso de uso
3. Incluye manejo de errores
4. Abre un Pull Request

---

<p align="center">
  ¿Preguntas? Abre un <a href="https://github.com/tu-org/trackhs-mcp-server/issues">issue</a>
</p>

