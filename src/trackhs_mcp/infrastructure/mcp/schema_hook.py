"""
Hook para interceptar y corregir esquemas JSON en FastMCP.

Este módulo implementa un hook que corrige la serialización incorrecta
de esquemas JSON donde los valores numéricos se convierten a strings.
"""

import logging
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP

from ..utils.schema_fixer import compare_schemas, fix_and_validate_schema

logger = logging.getLogger(__name__)


class SchemaFixerHook:
    """
    Hook que intercepta la generación de esquemas MCP y los corrige.
    """

    def __init__(self, mcp_server: FastMCP):
        """
        Inicializa el hook con el servidor FastMCP.

        Args:
            mcp_server: Instancia del servidor FastMCP
        """
        self.mcp_server = mcp_server
        self.original_list_tools = None
        self.original_get_tool = None
        self._hook_applied = False

    def apply_hook(self) -> None:
        """
        Aplica el hook al servidor FastMCP.

        Intercepta los métodos list_tools() y get_tool() para corregir
        los esquemas antes de enviarlos a los clientes.
        """
        if self._hook_applied:
            logger.warning("Hook already applied, skipping")
            return

        logger.info("Applying schema fixer hook to FastMCP server")

        # Guardar métodos originales
        self.original_list_tools = getattr(self.mcp_server, "get_tools", None)
        self.original_get_tool = getattr(self.mcp_server, "get_tool", None)

        # Aplicar monkey patch
        if self.original_list_tools:
            self.mcp_server.get_tools = self._patched_list_tools
        if self.original_get_tool:
            self.mcp_server.get_tool = self._patched_get_tool

        self._hook_applied = True
        logger.info("Schema fixer hook applied successfully")

    def remove_hook(self) -> None:
        """
        Remueve el hook y restaura los métodos originales.
        """
        if not self._hook_applied:
            logger.warning("Hook not applied, nothing to remove")
            return

        logger.info("Removing schema fixer hook")

        # Restaurar métodos originales
        if self.original_list_tools:
            self.mcp_server.get_tools = self.original_list_tools
        if self.original_get_tool:
            self.mcp_server.get_tool = self.original_get_tool

        self._hook_applied = False
        logger.info("Schema fixer hook removed successfully")

    async def _patched_list_tools(self) -> List[Dict[str, Any]]:
        """
        Versión parcheada de list_tools que corrige esquemas.

        Returns:
            Lista de herramientas con esquemas corregidos
        """
        logger.debug("Intercepting list_tools() - applying schema fixes")

        # Obtener herramientas originales
        tools = await self.original_list_tools()

        # Corregir esquemas de cada herramienta
        fixed_tools = []
        for tool in tools:
            try:
                fixed_tool = self._fix_tool_schema(tool)
                fixed_tools.append(fixed_tool)

                # Log de cambios si hay diferencias
                if fixed_tool != tool:
                    differences = compare_schemas(tool, fixed_tool)
                    logger.info(
                        f"Fixed schema for tool '{tool.get('name', 'unknown')}': {differences['total_changes']} changes"
                    )

            except Exception as e:
                logger.error(
                    f"Error fixing schema for tool {tool.get('name', 'unknown')}: {e}"
                )
                # En caso de error, usar herramienta original
                fixed_tools.append(tool)

        logger.debug(f"Schema fixing completed for {len(fixed_tools)} tools")
        return fixed_tools

    async def _patched_get_tool(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Versión parcheada de get_tool que corrige esquemas.

        Args:
            tool_name: Nombre de la herramienta

        Returns:
            Herramienta con esquema corregido o None
        """
        logger.debug(f"Intercepting get_tool('{tool_name}') - applying schema fixes")

        # Obtener herramienta original
        tool = await self.original_get_tool(tool_name)

        if tool is None:
            logger.debug(f"Tool '{tool_name}' not found")
            return None

        try:
            # Corregir esquema
            fixed_tool = self._fix_tool_schema(tool)

            # Log de cambios si hay diferencias
            if fixed_tool != tool:
                differences = compare_schemas(tool, fixed_tool)
                logger.info(
                    f"Fixed schema for tool '{tool_name}': {differences['total_changes']} changes"
                )

            return fixed_tool

        except Exception as e:
            logger.error(f"Error fixing schema for tool '{tool_name}': {e}")
            # En caso de error, usar herramienta original
            return tool

    def _fix_tool_schema(self, tool: Dict[str, Any]) -> Dict[str, Any]:
        """
        Corrige el esquema de una herramienta específica.

        Args:
            tool: Herramienta con esquema a corregir

        Returns:
            Herramienta con esquema corregido
        """
        if not isinstance(tool, dict):
            return tool

        # Crear copia para no modificar el original
        fixed_tool = tool.copy()

        # Corregir inputSchema si existe
        if "inputSchema" in fixed_tool and isinstance(fixed_tool["inputSchema"], dict):
            try:
                fixed_tool["inputSchema"] = fix_and_validate_schema(
                    fixed_tool["inputSchema"]
                )
                logger.debug(
                    f"Fixed inputSchema for tool '{tool.get('name', 'unknown')}'"
                )
            except Exception as e:
                logger.error(
                    f"Error fixing inputSchema for tool '{tool.get('name', 'unknown')}': {e}"
                )
                # Mantener esquema original en caso de error

        # Corregir outputSchema si existe
        if "outputSchema" in fixed_tool and isinstance(
            fixed_tool["outputSchema"], dict
        ):
            try:
                fixed_tool["outputSchema"] = fix_and_validate_schema(
                    fixed_tool["outputSchema"]
                )
                logger.debug(
                    f"Fixed outputSchema for tool '{tool.get('name', 'unknown')}'"
                )
            except Exception as e:
                logger.error(
                    f"Error fixing outputSchema for tool '{tool.get('name', 'unknown')}': {e}"
                )
                # Mantener esquema original en caso de error

        return fixed_tool


def apply_schema_fixer_hook(mcp_server: FastMCP) -> SchemaFixerHook:
    """
    Aplica el hook de corrección de esquemas a un servidor FastMCP.

    Args:
        mcp_server: Servidor FastMCP al que aplicar el hook

    Returns:
        Instancia del hook aplicado
    """
    hook = SchemaFixerHook(mcp_server)
    hook.apply_hook()
    return hook


def create_schema_fixed_server(name: str = "TrackHS MCP Server") -> FastMCP:
    """
    Crea un servidor FastMCP con corrección automática de esquemas.

    Args:
        name: Nombre del servidor

    Returns:
        Servidor FastMCP con hook aplicado
    """
    # Crear servidor FastMCP
    mcp_server = FastMCP(name)

    # Aplicar hook de corrección de esquemas
    hook = apply_schema_fixer_hook(mcp_server)

    # Agregar hook como atributo para acceso posterior
    mcp_server._schema_fixer_hook = hook

    logger.info(f"Created FastMCP server '{name}' with schema fixer hook")
    return mcp_server
