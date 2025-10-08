/**
 * Esquemas estandarizados de herramientas MCP para Track HS
 * Centraliza todas las definiciones de herramientas para consistencia
 */

export const MCP_TOOLS_SCHEMAS = [
  {
    name: "get_contacts",
    description: "Obtener lista de contactos de Track HS",
    inputSchema: {
      type: "object",
      properties: {
        page: { 
          type: "number", 
          default: 1, 
          description: "Número de página (paginación)" 
        },
        size: { 
          type: "number", 
          default: 10, 
          description: "Tamaño de página (máximo 100)" 
        },
        search: { 
          type: "string", 
          description: "Término de búsqueda en nombre o email" 
        },
        email: { 
          type: "string", 
          description: "Filtrar por dirección de email específica" 
        }
      }
    }
  },
  {
    name: "get_reservation",
    description: "Obtener información detallada de una reserva específica",
    inputSchema: {
      type: "object",
      properties: {
        reservationId: { 
          type: "string", 
          description: "ID único de la reserva" 
        }
      },
      required: ["reservationId"]
    }
  },
  {
    name: "search_reservations",
    description: "Buscar reservas con filtros avanzados",
    inputSchema: {
      type: "object",
      properties: {
        page: { 
          type: "number", 
          default: 1, 
          description: "Número de página" 
        },
        size: { 
          type: "number", 
          default: 10, 
          description: "Tamaño de página" 
        },
        search: { 
          type: "string", 
          description: "Término de búsqueda en nombre del huésped" 
        },
        nodeId: { 
          type: "number", 
          description: "ID del nodo/propiedad" 
        },
        unitId: { 
          type: "number", 
          description: "ID de la unidad específica" 
        },
        status: { 
          type: "string", 
          description: "Estado de la reserva (confirmed, cancelled, etc.)" 
        }
      }
    }
  },
  {
    name: "get_nodes",
    description: "Obtener lista de propiedades/nodos del sistema",
    inputSchema: {
      type: "object",
      properties: {
        page: { 
          type: "number", 
          default: 1, 
          description: "Número de página" 
        },
        size: { 
          type: "number", 
          default: 10, 
          description: "Tamaño de página" 
        },
        search: { 
          type: "string", 
          description: "Término de búsqueda en nombre de la propiedad" 
        }
      }
    }
  },
  {
    name: "get_node",
    description: "Obtener información detallada de una propiedad específica",
    inputSchema: {
      type: "object",
      properties: {
        nodeId: { 
          type: "number", 
          description: "ID único de la propiedad/nodo" 
        }
      },
      required: ["nodeId"]
    }
  },
  {
    name: "get_units",
    description: "Obtener lista de unidades disponibles",
    inputSchema: {
      type: "object",
      properties: {
        page: { 
          type: "number", 
          default: 1, 
          description: "Número de página" 
        },
        size: { 
          type: "number", 
          default: 10, 
          description: "Tamaño de página" 
        },
        search: { 
          type: "string", 
          description: "Término de búsqueda en nombre de la unidad" 
        },
        nodeId: { 
          type: "number", 
          description: "ID del nodo/propiedad para filtrar unidades" 
        }
      }
    }
  },
  {
    name: "get_unit",
    description: "Obtener información detallada de una unidad específica",
    inputSchema: {
      type: "object",
      properties: {
        unitId: { 
          type: "number", 
          description: "ID único de la unidad" 
        }
      },
      required: ["unitId"]
    }
  },
  {
    name: "get_ledger_accounts",
    description: "Obtener lista de cuentas contables",
    inputSchema: {
      type: "object",
      properties: {
        page: { 
          type: "number", 
          default: 1, 
          description: "Número de página" 
        },
        size: { 
          type: "number", 
          default: 10, 
          description: "Tamaño de página" 
        },
        search: { 
          type: "string", 
          description: "Término de búsqueda en nombre de la cuenta" 
        },
        category: { 
          type: "string", 
          description: "Categoría de la cuenta contable" 
        },
        isActive: { 
          type: "number", 
          description: "Estado activo (1=activo, 0=inactivo)" 
        }
      }
    }
  },
  {
    name: "get_ledger_account",
    description: "Obtener información detallada de una cuenta contable específica",
    inputSchema: {
      type: "object",
      properties: {
        accountId: { 
          type: "number", 
          description: "ID único de la cuenta contable" 
        }
      },
      required: ["accountId"]
    }
  },
  {
    name: "get_folios_collection",
    description: "Obtener colección de folios/facturas contables",
    inputSchema: {
      type: "object",
      properties: {
        page: { 
          type: "number", 
          default: 1, 
          description: "Número de página" 
        },
        size: { 
          type: "number", 
          default: 10, 
          description: "Tamaño de página" 
        },
        search: { 
          type: "string", 
          description: "Término de búsqueda en número de folio" 
        },
        type: { 
          type: "string", 
          description: "Tipo de folio (invoice, receipt, etc.)" 
        },
        status: { 
          type: "string", 
          description: "Estado del folio (pending, paid, cancelled)" 
        }
      }
    }
  },
  {
    name: "get_maintenance_work_orders",
    description: "Obtener órdenes de trabajo de mantenimiento",
    inputSchema: {
      type: "object",
      properties: {
        page: { 
          type: "number", 
          default: 1, 
          description: "Número de página" 
        },
        size: { 
          type: "number", 
          default: 10, 
          description: "Tamaño de página" 
        },
        search: { 
          type: "string", 
          description: "Término de búsqueda en descripción" 
        },
        status: { 
          type: "string", 
          description: "Estado de la orden (open, in_progress, completed)" 
        }
      }
    }
  },
  {
    name: "get_reviews",
    description: "Obtener reseñas de propiedades",
    inputSchema: {
      type: "object",
      properties: {
        page: { 
          type: "number", 
          default: 1, 
          description: "Número de página" 
        },
        size: { 
          type: "number", 
          default: 10, 
          description: "Tamaño de página" 
        },
        search: { 
          type: "string", 
          description: "Término de búsqueda en comentarios" 
        },
        updatedSince: { 
          type: "string", 
          description: "Fecha de actualización desde (formato ISO 8601)" 
        }
      }
    }
  },
  {
    name: "get_reservation_notes",
    description: "Obtener notas y comentarios de una reserva",
    inputSchema: {
      type: "object",
      properties: {
        reservationId: { 
          type: "string", 
          description: "ID único de la reserva" 
        },
        page: { 
          type: "number", 
          default: 1, 
          description: "Número de página" 
        },
        size: { 
          type: "number", 
          default: 10, 
          description: "Tamaño de página" 
        }
      },
      required: ["reservationId"]
    }
  }
];

// Función helper para validar esquemas
export function validateToolSchema(toolName, args) {
  const tool = MCP_TOOLS_SCHEMAS.find(t => t.name === toolName);
  if (!tool) {
    throw new Error(`Herramienta desconocida: ${toolName}`);
  }

  // Validar campos requeridos
  if (tool.inputSchema.required) {
    for (const requiredField of tool.inputSchema.required) {
      if (!(requiredField in args)) {
        throw new Error(`Campo requerido faltante: ${requiredField}`);
      }
    }
  }

  return true;
}

// Función helper para obtener esquema de herramienta
export function getToolSchema(toolName) {
  return MCP_TOOLS_SCHEMAS.find(t => t.name === toolName);
}

// Función helper para listar todas las herramientas
export function getAllTools() {
  return MCP_TOOLS_SCHEMAS;
}
