/**
 * Herramienta MCP para obtener un nodo específico de Track HS
 */

import { BaseTrackHSTool } from '../core/base-tool.js';
import { GetNodeParams, GetNodeResponse } from '../types/nodes.js';

export class GetNodeTool extends BaseTrackHSTool {
  name = 'get_node';
  description = 'Obtener un nodo específico (propiedad/ubicación) por su ID. Incluye información completa de ubicación, políticas, zonas, configuraciones y datos relacionados.';
  
  inputSchema = {
    type: 'object' as const,
    properties: {
      nodeId: { 
        type: 'number', 
        minimum: 1,
        description: 'ID único del nodo a recuperar (mínimo: 1)'
      }
    },
    required: ['nodeId']
  };

  async execute(params: GetNodeParams): Promise<GetNodeResponse> {
    // Validar parámetros básicos
    this.validateParams(params);

    // Validar que nodeId sea un número positivo
    if (!params.nodeId || params.nodeId < 1) {
      throw new Error('nodeId debe ser un número positivo mayor a 0');
    }

    const endpoint = `/pms/nodes/${params.nodeId}`;
    
    // Debug: Log the endpoint being called
    console.error(`[DEBUG] Calling endpoint: ${endpoint}`);
    console.error(`[DEBUG] Node ID: ${params.nodeId}`);
    
    try {
      const result = await this.apiClient.get<GetNodeResponse>(endpoint);
      return result;
    } catch (error) {
      console.error(`[DEBUG] Error details:`, error);
      throw new Error(`Error al obtener nodo: ${error instanceof Error ? error.message : 'Error desconocido'}`);
    }
  }
}
