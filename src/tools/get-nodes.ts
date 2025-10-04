/**
 * Herramienta MCP para obtener colección de nodos (propiedades/ubicaciones) de Track HS
 */

import { BaseTrackHSTool } from '../core/base-tool.js';
import { GetNodesParams, GetNodesResponse } from '../types/nodes.js';

export class GetNodesTool extends BaseTrackHSTool {
  name = 'get_nodes';
  description = 'Obtener colección de nodos (propiedades/ubicaciones) con filtros avanzados, paginación y ordenamiento. Incluye información completa de ubicaciones, políticas, zonas y configuraciones.';
  
  inputSchema = {
    type: 'object' as const,
    properties: {
      // Paginación
      page: { 
        type: 'number', 
        minimum: 0,
        description: 'Número de página (default: 0)'
      },
      size: { 
        type: 'number', 
        minimum: 1,
        maximum: 100,
        description: 'Tamaño de página (default: 25, máximo: 100)'
      },
      
      // Ordenamiento
      sortColumn: { 
        type: 'string', 
        enum: ['id', 'name'],
        default: 'id',
        description: 'Columna de ordenamiento (solo id y name soportados)'
      },
      sortDirection: { 
        type: 'string', 
        enum: ['asc', 'desc'],
        default: 'asc',
        description: 'Dirección de ordenamiento (asc o desc)'
      },
      
      // Búsqueda
      search: { 
        type: 'string', 
        description: 'Búsqueda por nombre o en descripciones corta y larga'
      },
      term: { 
        type: 'string', 
        description: 'Búsqueda por caption/nombre del nodo'
      },
      
      // Filtros por ID
      parentId: { 
        type: 'number', 
        description: 'Buscar nodos por ID padre, muestra todos los hijos'
      },
      typeId: { 
        type: 'number', 
        description: 'Buscar nodos por ID de tipo de nodo'
      },
      
      // Filtros adicionales
      computed: { 
        type: 'number', 
        enum: [0, 1],
        description: 'Retornar valores computados adicionales basados en atributos heredados (0 o 1)'
      },
      inherited: { 
        type: 'number', 
        enum: [0, 1],
        description: 'Retornar atributos heredados adicionales (0 o 1)'
      },
      includeDescriptions: { 
        type: 'number', 
        enum: [0, 1],
        description: 'Retornar descripciones de unidades, puede ser heredado del nodo si se establece como inherited (0 o 1)'
      }
    },
    required: []
  };

  async execute(params: GetNodesParams = {}): Promise<GetNodesResponse> {
    // Validar parámetros básicos
    this.validateParams(params);

    // Construir query parameters
    const queryParams = new URLSearchParams();
    
    // Solo agregar parámetros que están definidos y no son undefined
    if (params.page !== undefined) {
      queryParams.append('page', params.page.toString());
    }
    
    if (params.size !== undefined) {
      queryParams.append('size', params.size.toString());
    }
    
    if (params.sortColumn) {
      queryParams.append('sortColumn', params.sortColumn);
    }
    
    if (params.sortDirection) {
      queryParams.append('sortDirection', params.sortDirection);
    }

    // Agregar parámetros de búsqueda solo si están definidos
    if (params.search) {
      queryParams.append('search', params.search);
    }

    if (params.term) {
      queryParams.append('term', params.term);
    }

    // Agregar filtros por ID solo si están definidos
    if (params.parentId !== undefined) {
      queryParams.append('parentId', params.parentId.toString());
    }

    if (params.typeId !== undefined) {
      queryParams.append('typeId', params.typeId.toString());
    }

    // Agregar filtros adicionales solo si están definidos
    if (params.computed !== undefined) {
      queryParams.append('computed', params.computed.toString());
    }

    if (params.inherited !== undefined) {
      queryParams.append('inherited', params.inherited.toString());
    }

    if (params.includeDescriptions !== undefined) {
      queryParams.append('includeDescriptions', params.includeDescriptions.toString());
    }

    const endpoint = `/pms/nodes?${queryParams.toString()}`;
    
    // Debug: Log the endpoint being called
    console.error(`[DEBUG] Calling endpoint: ${endpoint}`);
    console.error(`[DEBUG] Query params:`, Object.fromEntries(queryParams.entries()));
    
    try {
      const result = await this.apiClient.get<GetNodesResponse>(endpoint);
      return result;
    } catch (error) {
      console.error(`[DEBUG] Error details:`, error);
      throw new Error(`Error al obtener nodos: ${error instanceof Error ? error.message : 'Error desconocido'}`);
    }
  }
}
