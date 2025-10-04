/**
 * Herramienta MCP para obtener una unidad específica de Track HS
 */

import { BaseTrackHSTool } from '../core/base-tool.js';
import { GetUnitParams, Unit } from '../types/units.js';

export class GetUnitTool extends BaseTrackHSTool {
  name = 'get_unit';
  description = 'Obtener información detallada de una unidad específica por ID incluyendo datos completos, amenidades, habitaciones, políticas y configuración';
  
  inputSchema = {
    type: 'object' as const,
    properties: {
      unitId: {
        type: 'number',
        description: 'ID de la unidad a obtener'
      },
      computed: {
        type: 'number',
        enum: [0, 1],
        description: 'Return additional computed values attributes based on inherited attributes. 1 == true, 0 == false'
      },
      inherited: {
        type: 'number',
        enum: [0, 1],
        description: 'Return additional inherited attributes. 1 == true, 0 == false'
      },
      includeDescriptions: {
        type: 'number',
        enum: [0, 1],
        description: 'Return descriptions of units, may be inherited from node if set to inherited. 1 == true, 0 == false'
      }
    },
    required: ['unitId']
  };

  async execute(params: GetUnitParams): Promise<Unit> {
    // Validar parámetros
    if (!params.unitId) {
      throw new Error('unitId es requerido');
    }

    // Construir query parameters
    const queryParams = new URLSearchParams();
    
    if (params.computed !== undefined) {
      queryParams.append('computed', params.computed.toString());
    }
    if (params.inherited !== undefined) {
      queryParams.append('inherited', params.inherited.toString());
    }
    if (params.includeDescriptions !== undefined) {
      queryParams.append('includeDescriptions', params.includeDescriptions.toString());
    }

    const endpoint = `/pms/units/${params.unitId}?${queryParams.toString()}`;
    
    // Debug: Log the endpoint being called
    console.error(`[DEBUG] Calling endpoint: ${endpoint}`);
    console.error(`[DEBUG] Query params:`, Object.fromEntries(queryParams.entries()));
    
    try {
      const result = await this.apiClient.get<Unit>(endpoint);
      return result;
    } catch (error) {
      console.error(`[DEBUG] Error details:`, error);
      throw new Error(`Error al obtener unidad ${params.unitId}: ${error instanceof Error ? error.message : 'Error desconocido'}`);
    }
  }
}
