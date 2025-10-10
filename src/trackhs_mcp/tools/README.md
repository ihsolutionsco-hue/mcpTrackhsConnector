# Herramientas MCP TrackHS

Este directorio contiene todas las herramientas MCP individuales para la API de Track HS. Cada herramienta está en su propio archivo para mejor organización y mantenibilidad.

## Estructura de Archivos

### Herramientas Individuales

1. **`get_reviews.py`** - Obtener reseñas de propiedades
2. **`get_reservation.py`** - Obtener una reserva específica
3. **`search_reservations.py`** - Buscar reservas con filtros
4. **`get_units.py`** - Obtener unidades con filtros
5. **`get_unit.py`** - Obtener una unidad específica
6. **`get_folios_collection.py`** - Obtener colección de folios
7. **`get_contacts.py`** - Obtener contactos
8. **`get_ledger_accounts.py`** - Obtener cuentas contables
9. **`get_ledger_account.py`** - Obtener una cuenta contable específica
10. **`get_reservation_notes.py`** - Obtener notas de reserva
11. **`get_nodes.py`** - Obtener nodos
12. **`get_node.py`** - Obtener un nodo específico
13. **`get_maintenance_work_orders.py`** - Obtener órdenes de trabajo de mantenimiento

### Archivo Principal

- **`all_tools.py`** - Registrador principal que importa y registra todas las herramientas

## Patrón de Implementación

Cada herramienta sigue el mismo patrón:

```python
def register_[nombre_herramienta](mcp, api_client: TrackHSApiClient):
    """Registra la herramienta [nombre_herramienta]"""
    
    @mcp.tool()
    async def [nombre_herramienta](...):
        """
        Descripción de la herramienta
        
        Args:
            param1: Descripción del parámetro
            param2: Descripción del parámetro
        """
        # Implementación de la herramienta
        pass
```

## Ventajas de esta Estructura

1. **Modularidad**: Cada herramienta es independiente
2. **Mantenibilidad**: Fácil de mantener y actualizar
3. **Testabilidad**: Cada herramienta puede ser probada individualmente
4. **Escalabilidad**: Fácil agregar nuevas herramientas
5. **Organización**: Código más limpio y organizado

## Uso

Las herramientas se registran automáticamente cuando se importa `register_all_tools` en el servidor principal. No es necesario modificar el servidor para agregar nuevas herramientas, solo crear el archivo correspondiente y agregarlo al import en `all_tools.py`.
