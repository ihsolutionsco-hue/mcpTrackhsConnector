/**
 * Herramienta MCP para obtener órdenes de trabajo de mantenimiento de Track HS
 */

import { BaseTrackHSTool } from '../core/base-tool.js';
import { 
  MaintenanceWorkOrdersResponse, 
  GetMaintenanceWorkOrdersParams 
} from '../types/maintenance-work-orders.js';

export class GetMaintenanceWorkOrdersTool extends BaseTrackHSTool {
  name = 'get_maintenance_work_orders';
  description = 'Retrieve paginated collection of maintenance work orders from Track HS';
  
  inputSchema = {
    type: 'object' as const,
    properties: {
      updatedSince: {
        type: 'string',
        format: 'date',
        description: 'Filter by Date Time in ISO 8601 format. Use this to find recent updates to refresh your cache'
      },
      page: {
        type: 'number',
        description: 'Page Number',
        minimum: 1
      },
      size: {
        type: 'number',
        description: 'Page size, defaults to 25. No max currently but we may consider setting it at 100 or so.',
        minimum: 1,
        maximum: 100
      },
      sortColumn: {
        type: 'string',
        enum: ['id', 'scheduledAt', 'status', 'priority', 'dateReceived', 'unitId', 'vendorId', 'userId', 'summary'],
        default: 'id',
        description: 'Only id and name supported.'
      },
      sortDirection: {
        type: 'string',
        enum: ['asc', 'desc'],
        default: 'asc',
        description: 'asc or desc'
      },
      search: {
        type: 'string',
        description: 'Search with id = number or summary, unit.name, vendor.name or user.name = string.'
      },
      isScheduled: {
        type: 'number',
        enum: [1, 0],
        description: 'Filter by scheduled'
      },
      unitId: {
        type: 'string',
        description: 'Filter by unitId csv'
      },
      userId: {
        type: 'array',
        items: { type: 'number' },
        description: 'Filter by userId'
      },
      nodeId: {
        type: 'number',
        description: 'Filter by nodeId'
      },
      roleId: {
        type: 'number',
        description: 'Filter by roleId'
      },
      ownerId: {
        type: 'number',
        description: 'Filter by ownerId'
      },
      priority: {
        type: 'array',
        items: { type: 'number' },
        description: 'Filter by cleanTypeId integers'
      },
      reservationId: {
        type: 'number',
        description: 'Filter by reservationId'
      },
      vendorId: {
        type: 'number',
        description: 'Filter by vendorId'
      },
      status: {
        type: 'array',
        items: {
          type: 'string',
          enum: ['open', 'not-started', 'in-progress', 'completed', 'processed', 
                 'vendor-not-start', 'vendor-assigned', 'vendor-declined', 
                 'vendor-completed', 'user-completed', 'cancelled']
        },
        description: 'Filter by status integers'
      },
      dateScheduled: {
        type: 'string',
        format: 'date',
        description: 'Filter by date scheduled as ISO 8601 format'
      },
      startDate: {
        type: 'string',
        format: 'date',
        description: 'Filter by start date as ISO 8601 format'
      },
      endDate: {
        type: 'string',
        format: 'date',
        description: 'Filter by end date as ISO 8601 format'
      },
      problems: {
        type: 'array',
        items: { type: 'number' },
        description: 'Filter by problems ids'
      }
    },
    required: []
  };

  async execute(params: GetMaintenanceWorkOrdersParams = {}): Promise<MaintenanceWorkOrdersResponse> {
    // Validar parámetros
    this.validateParams(params);

    // Construir query parameters
    const queryParams = new URLSearchParams();
    
    // Aplicar valores por defecto
    const page = params.page || 1;
    const size = params.size || 25;
    const sortColumn = params.sortColumn || 'id';
    const sortDirection = params.sortDirection || 'asc';

    // Agregar parámetros básicos
    queryParams.append('page', page.toString());
    queryParams.append('size', size.toString());
    queryParams.append('sortColumn', sortColumn);
    queryParams.append('sortDirection', sortDirection);

    // Agregar parámetros opcionales
    if (params.updatedSince) {
      queryParams.append('updatedSince', params.updatedSince);
    }
    if (params.search) {
      queryParams.append('search', params.search);
    }
    if (params.isScheduled !== undefined) {
      queryParams.append('isScheduled', params.isScheduled.toString());
    }
    if (params.unitId) {
      queryParams.append('unitId', params.unitId);
    }
    if (params.userId && params.userId.length > 0) {
      params.userId.forEach(id => queryParams.append('userId', id.toString()));
    }
    if (params.nodeId) {
      queryParams.append('nodeId', params.nodeId.toString());
    }
    if (params.roleId) {
      queryParams.append('roleId', params.roleId.toString());
    }
    if (params.ownerId) {
      queryParams.append('ownerId', params.ownerId.toString());
    }
    if (params.priority && params.priority.length > 0) {
      params.priority.forEach(p => queryParams.append('priority', p.toString()));
    }
    if (params.reservationId) {
      queryParams.append('reservationId', params.reservationId.toString());
    }
    if (params.vendorId) {
      queryParams.append('vendorId', params.vendorId.toString());
    }
    if (params.status && params.status.length > 0) {
      params.status.forEach(s => queryParams.append('status', s));
    }
    if (params.dateScheduled) {
      queryParams.append('dateScheduled', params.dateScheduled);
    }
    if (params.startDate) {
      queryParams.append('startDate', params.startDate);
    }
    if (params.endDate) {
      queryParams.append('endDate', params.endDate);
    }
    if (params.problems && params.problems.length > 0) {
      params.problems.forEach(p => queryParams.append('problems', p.toString()));
    }

    const endpoint = `/pms/maintenance/work-orders?${queryParams.toString()}`;
    
    try {
      const result = await this.apiClient.get<MaintenanceWorkOrdersResponse>(endpoint);
      return result;
    } catch (error) {
      throw new Error(`Error al obtener órdenes de trabajo de mantenimiento: ${error instanceof Error ? error.message : 'Error desconocido'}`);
    }
  }
}
