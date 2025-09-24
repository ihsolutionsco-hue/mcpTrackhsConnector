/**
 * Herramienta MCP para obtener colección de folios de Track HS
 */

import { BaseTrackHSTool } from '../core/base-tool.js';
import { GetFoliosCollectionParams, GetFoliosCollectionResponse } from '../types/folios.js';

export class GetFoliosCollectionTool extends BaseTrackHSTool {
  name = 'get_folios_collection';
  description = 'Get a collection of folios (bills/receipts) with filtering, pagination, and sorting options';
  
  inputSchema = {
    type: 'object' as const,
    properties: {
      // Paginación
      page: { 
        type: 'number', 
        minimum: 1,
        description: 'Page number of result set'
      },
      size: { 
        type: 'number', 
        minimum: 1,
        maximum: 100,
        description: 'Page size - maximum 100 items per page'
      },
      
      // Ordenamiento
      sortColumn: { 
        type: 'string', 
        enum: ['id', 'name', 'status', 'type', 'startDate', 'endDate', 'contactName', 'companyName', 'reservationId', 'currentBalance', 'realizedBalance', 'masterFolioRule'],
        default: 'id',
        description: 'Column to sort the result set'
      },
      sortDirection: { 
        type: 'string', 
        enum: ['asc', 'desc'],
        default: 'asc',
        description: 'Direction to sort result set'
      },
      
      // Búsqueda
      search: { 
        type: 'string', 
        description: 'Search folios by id, name, company name, contact name, reservation id, unit id or unit name'
      },
      
      // Filtros por tipo
      type: { 
        type: 'string', 
        enum: ['guest', 'master', 'guest-sub-folio', 'master-sub-folio'],
        description: 'Limit results to certain folio types'
      },
      status: { 
        type: 'string', 
        enum: ['open', 'closed'],
        description: 'Search folios by their status'
      },
      
      // Filtros por ID
      masterFolioId: { 
        type: 'number', 
        minimum: 1,
        description: 'Search folios by master Folio Id - if type = guest'
      },
      contactId: { 
        type: 'number', 
        minimum: 1,
        description: 'Search folios by guest id'
      },
      companyId: { 
        type: 'number', 
        minimum: 1,
        description: 'Search folios by company id'
      }
    },
    required: []
  };

  async execute(params: GetFoliosCollectionParams = {}): Promise<GetFoliosCollectionResponse> {
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

    if (params.type) {
      queryParams.append('type', params.type);
    }

    if (params.status) {
      queryParams.append('status', params.status);
    }

    if (params.masterFolioId !== undefined) {
      queryParams.append('masterFolioId', params.masterFolioId.toString());
    }

    if (params.contactId !== undefined) {
      queryParams.append('contactId', params.contactId.toString());
    }

    if (params.companyId !== undefined) {
      queryParams.append('companyId', params.companyId.toString());
    }

    const endpoint = `/pms/folios?${queryParams.toString()}`;
    
    try {
      const result = await this.apiClient.get<GetFoliosCollectionResponse>(endpoint);
      return result;
    } catch (error) {
      throw new Error(`Error al obtener folios: ${error instanceof Error ? error.message : 'Error desconocido'}`);
    }
  }
}