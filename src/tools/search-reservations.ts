/**
 * Herramienta MCP para búsqueda avanzada de reservaciones de Track HS
 */

import { BaseTrackHSTool } from '../core/base-tool.js';
import { SearchReservationsParams, SearchReservationsResponse } from '../types/reservations.js';

export class SearchReservationsTool extends BaseTrackHSTool {
  name = 'search_reservations';
  description = 'Search reservations with advanced filtering options including pagination, sorting, date ranges, and multiple ID filters';
  
  inputSchema = {
    type: 'object' as const,
    properties: {
      // Paginación
      page: { 
        type: 'number', 
        minimum: 0,
        description: 'Page number of result set - Limited to 10k total results (page * size)'
      },
      size: { 
        type: 'number', 
        minimum: 1,
        maximum: 100,
        description: 'Size of page - Limited to 10k total results (page * size)'
      },
      scroll: {
        oneOf: [
          { type: 'number', description: 'Default to 1 for first page' },
          { type: 'string', description: 'Use scroll index string for subsequent pages' }
        ],
        description: 'Elasticsearch scrolling, start with 1 and then string to continue scrolling'
      },
      
      // Ordenamiento
      sortColumn: { 
        type: 'string', 
        enum: ['name', 'status', 'altConf', 'agreementStatus', 'type', 'guest', 'guests', 'unit', 'units', 'checkin', 'checkout', 'nights'],
        default: 'name',
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
        description: 'Substring search matching on name or descriptions'
      },
      tags: { 
        type: 'string', 
        description: 'Search matching on tag Id'
      },
      updatedSince: { 
        type: 'string', 
        format: 'date-time',
        description: 'Date as ISO 8601 format'
      },
      
      // Filtros por ID (soportan single value o array)
      nodeId: {
        oneOf: [
          { type: 'number', title: 'Single Node' },
          { type: 'array', items: { type: 'number' }, title: 'Multiple Nodes' }
        ],
        description: 'Return all reservations that are of the specific node ID(s). Can be single value or array.'
      },
      unitId: {
        oneOf: [
          { type: 'number', title: 'Single Unit' },
          { type: 'array', items: { type: 'number' }, title: 'Multiple Units' }
        ],
        description: 'Return all reservations that are of the specific unit ID(s). Can be single value or array.'
      },
      reservationTypeId: {
        oneOf: [
          { type: 'number', title: 'Single Reservation Type ID' },
          { type: 'array', items: { type: 'number' }, title: 'Multiple Reservation Type IDs' }
        ],
        description: 'Return all reservations that are of the specific reservation type ID(s). Can be single value or array.'
      },
      contactId: {
        oneOf: [
          { type: 'number', title: 'Single Contact ID' },
          { type: 'array', items: { type: 'number' }, title: 'Multiple Contact IDs' }
        ],
        description: 'Return all reservations that are of the specific contact ID(s). Can be single value or array.'
      },
      travelAgentId: {
        oneOf: [
          { type: 'number', title: 'Single Travel Agent ID' },
          { type: 'array', items: { type: 'number' }, title: 'Multiple Travel Agent IDs' }
        ],
        description: 'Return all reservations that are of the specific travel agent ID(s). Can be single value or array.'
      },
      campaignId: {
        oneOf: [
          { type: 'number', title: 'Single Campaign ID' },
          { type: 'array', items: { type: 'number' }, title: 'Multiple Campaign IDs' }
        ],
        description: 'Return all reservations that are of the specific campaign ID(s). Can be single value or array.'
      },
      userId: {
        oneOf: [
          { type: 'number', title: 'Single User ID' },
          { type: 'array', items: { type: 'number' }, title: 'Multiple User IDs' }
        ],
        description: 'Return all reservations that are of the specific user ID(s). Can be single value or array.'
      },
      unitTypeId: {
        oneOf: [
          { type: 'number', title: 'Single Unit Type ID' },
          { type: 'array', items: { type: 'number' }, title: 'Multiple Unit Type IDs' }
        ],
        description: 'Return all reservations that are of the specific unit type ID(s). Can be single value or array.'
      },
      rateTypeId: {
        oneOf: [
          { type: 'number', title: 'Single Rate Type ID' },
          { type: 'array', items: { type: 'number' }, title: 'Multiple Rate Type IDs' }
        ],
        description: 'Return all reservations that are of the specific rate type ID(s). Can be single value or array.'
      },
      
      // Filtros por fechas
      bookedStart: { 
        type: 'string', 
        format: 'date-time',
        description: 'Date as ISO 8601 format'
      },
      bookedEnd: { 
        type: 'string', 
        format: 'date-time',
        description: 'Date as ISO 8601 format'
      },
      arrivalStart: { 
        type: 'string', 
        format: 'date-time',
        description: 'Date as ISO 8601 format'
      },
      arrivalEnd: { 
        type: 'string', 
        format: 'date-time',
        description: 'Date as ISO 8601 format'
      },
      departureStart: { 
        type: 'string', 
        format: 'date-time',
        description: 'Date as ISO 8601 format'
      },
      departureEnd: { 
        type: 'string', 
        format: 'date-time',
        description: 'Date as ISO 8601 format'
      },
      
      // Filtros especiales
      inHouseToday: { 
        type: 'number', 
        enum: [0, 1],
        description: 'Filter by in house today'
      },
      status: {
        oneOf: [
          { type: 'string', title: 'Single Status' },
          { type: 'array', items: { type: 'string' }, title: 'Multiple Statuses' }
        ],
        description: 'Return all reservations that are of the specific status(es). Can be single value or array. {Hold, Confirmed, Checked Out, Checked In, and Cancelled}'
      }
    },
    required: []
  };

  async execute(params: SearchReservationsParams = {}): Promise<SearchReservationsResponse> {
    // Validar parámetros básicos
    this.validateParams(params);

    // Construir query parameters de forma más conservadora
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

    if (params.tags) {
      queryParams.append('tags', params.tags);
    }

    if (params.updatedSince) {
      queryParams.append('updatedSince', params.updatedSince);
    }

    // Agregar filtros por ID solo si están definidos
    this.addIdFilter(queryParams, 'nodeId', params.nodeId);
    this.addIdFilter(queryParams, 'unitId', params.unitId);
    this.addIdFilter(queryParams, 'reservationTypeId', params.reservationTypeId);
    this.addIdFilter(queryParams, 'contactId', params.contactId);
    this.addIdFilter(queryParams, 'travelAgentId', params.travelAgentId);
    this.addIdFilter(queryParams, 'campaignId', params.campaignId);
    this.addIdFilter(queryParams, 'userId', params.userId);
    this.addIdFilter(queryParams, 'unitTypeId', params.unitTypeId);
    this.addIdFilter(queryParams, 'rateTypeId', params.rateTypeId);

    // Agregar filtros por fechas solo si están definidos
    if (params.bookedStart) {
      queryParams.append('bookedStart', params.bookedStart);
    }
    if (params.bookedEnd) {
      queryParams.append('bookedEnd', params.bookedEnd);
    }
    if (params.arrivalStart) {
      queryParams.append('arrivalStart', params.arrivalStart);
    }
    if (params.arrivalEnd) {
      queryParams.append('arrivalEnd', params.arrivalEnd);
    }
    if (params.departureStart) {
      queryParams.append('departureStart', params.departureStart);
    }
    if (params.departureEnd) {
      queryParams.append('departureEnd', params.departureEnd);
    }

    // Agregar filtros especiales solo si están definidos
    if (params.inHouseToday !== undefined) {
      queryParams.append('inHouseToday', params.inHouseToday.toString());
    }

    // Agregar filtro de estado solo si está definido
    if (params.status !== undefined) {
      this.addStatusFilter(queryParams, params.status);
    }

    const endpoint = `/v2/pms/reservations?${queryParams.toString()}`;
    
    // Debug: Log the endpoint being called
    console.error(`[DEBUG] Calling endpoint: ${endpoint}`);
    console.error(`[DEBUG] Query params:`, Object.fromEntries(queryParams.entries()));
    
    try {
      const result = await this.apiClient.get<SearchReservationsResponse>(endpoint);
      return result;
    } catch (error) {
      console.error(`[DEBUG] Error details:`, error);
      throw new Error(`Error al buscar reservaciones: ${error instanceof Error ? error.message : 'Error desconocido'}`);
    }
  }

  /**
   * Agrega filtros de ID a los query parameters, manejando tanto valores únicos como arrays
   */
  private addIdFilter(queryParams: URLSearchParams, paramName: string, value: number | number[] | undefined): void {
    if (value !== undefined) {
      if (Array.isArray(value)) {
        value.forEach(id => queryParams.append(paramName, id.toString()));
      } else {
        queryParams.append(paramName, value.toString());
      }
    }
  }

  /**
   * Agrega filtros de estado a los query parameters, manejando tanto valores únicos como arrays
   */
  private addStatusFilter(queryParams: URLSearchParams, status: string | string[] | undefined): void {
    if (status !== undefined) {
      if (Array.isArray(status)) {
        status.forEach(s => queryParams.append('status', s));
      } else {
        queryParams.append('status', status);
      }
    }
  }
}
