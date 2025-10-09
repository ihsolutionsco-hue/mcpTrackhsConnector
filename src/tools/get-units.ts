/**
 * Herramienta MCP para obtener colección de unidades de alojamiento de Track HS
 */

import { BaseTrackHSTool } from '../core/base-tool.js';
import { GetUnitsParams, GetUnitsResponse } from '../types/units.js';

export class GetUnitsTool extends BaseTrackHSTool {
  name = 'get_units';
  override title = 'Obtener Unidades';
  description = 'Obtener colección de unidades de alojamiento con filtros avanzados incluyendo paginación, ordenamiento, filtros por ID, búsqueda de texto, filtros físicos, políticas y disponibilidad';
  
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
      
      // Ordenamiento
      sortColumn: { 
        type: 'string', 
        enum: ['id', 'name', 'nodeName', 'unitTypeName'],
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
      term: { 
        type: 'string', 
        description: 'Substring search matching on term'
      },
      unitCode: { 
        type: 'string', 
        description: 'Search on unitCode, exact match or add % for wildcard'
      },
      shortName: { 
        type: 'string', 
        description: 'Search on shortName, exact match or add % for wildcard'
      },
      contentUpdatedSince: { 
        type: 'string', 
        format: 'date-time',
        description: 'Date in ISO 8601 format. Will return all units with content changes since timestamp'
      },
      updatedSince: { 
        type: 'string', 
        format: 'date',
        description: 'Date in ISO 8601 format. Will return all units updated since timestamp. @deprecated use contentUpdatedSince'
      },
      
      // Filtros por ID (soportan single value o array)
      nodeId: {
        oneOf: [
          { type: 'number', title: 'Single Node' },
          { type: 'array', items: { type: 'number' }, title: 'Multiple Nodes' }
        ],
        description: 'Return all units that are descendants of the specific node ID(s). Can be single value or array.'
      },
      unitTypeId: {
        oneOf: [
          { type: 'number', title: 'Single Unit Type' },
          { type: 'array', items: { type: 'number' }, title: 'Multiple Unit Types' }
        ],
        description: 'Return all units of the specific unit type(s). Can be single value or array.'
      },
      amenityId: {
        oneOf: [
          { type: 'number', title: 'Single Amenity' },
          { type: 'array', items: { type: 'number' }, title: 'Multiple Amenities' }
        ],
        description: 'Return all units that have these amenity ID(s). Can be single value or array.'
      },
      
      // Filtros físicos
      bedrooms: { 
        type: 'number', 
        description: 'Return all units with this exact number of bedrooms'
      },
      minBedrooms: { 
        type: 'number', 
        description: 'Return all units with this or more number of bedrooms'
      },
      maxBedrooms: { 
        type: 'number', 
        description: 'Return all units with this or less number of bedrooms'
      },
      bathrooms: { 
        type: 'number', 
        description: 'Return all units with this exact number of bathrooms'
      },
      minBathrooms: { 
        type: 'number', 
        description: 'Return all units with this or more number of bathrooms'
      },
      maxBathrooms: { 
        type: 'number', 
        description: 'Return all units with this or less number of bathrooms'
      },
      
      // Filtros de políticas
      petsFriendly: { 
        type: 'number', 
        enum: [0, 1],
        description: 'Return all units that are pet friendly (1) or not (0)'
      },
      eventsAllowed: { 
        type: 'number', 
        enum: [0, 1],
        description: 'Return all units that allow events (1) or not (0)'
      },
      smokingAllowed: { 
        type: 'number', 
        enum: [0, 1],
        description: 'Return all units that allow smoking (1) or not (0)'
      },
      childrenAllowed: { 
        type: 'number', 
        enum: [0, 1],
        description: 'Return all units that allow children (1) or not (0)'
      },
      
      // Filtros de disponibilidad
      arrival: { 
        type: 'string', 
        format: 'date',
        description: 'Date in ISO 8601 format. Will return all units available between this and departure'
      },
      departure: { 
        type: 'string', 
        format: 'date',
        description: 'Date in ISO 8601 format. Will return all units available between this and arrival'
      },
      
      // Filtros de estado
      isActive: { 
        type: 'number', 
        enum: [0, 1],
        description: 'Return active (1), inactive (0), or all (null) units'
      },
      isBookable: { 
        type: 'number', 
        enum: [0, 1],
        description: 'Return all bookable units (1) or not (0)'
      },
      unitStatus: { 
        type: 'string', 
        enum: ['clean', 'dirty', 'occupied', 'inspection', 'inprogress'],
        description: 'Filter by unit status'
      },
      
      // Filtros adicionales
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
      limited: { 
        type: 'number', 
        enum: [0, 1],
        description: 'Return very limited attributes (id, name, longitude latitude, isActive)'
      },
      includeDescriptions: { 
        type: 'number', 
        enum: [0, 1],
        description: 'Return descriptions of units, may be inherited from node if set to inherited. 1 == true, 0 == false'
      },
      allowUnitRates: { 
        type: 'number', 
        enum: [0, 1],
        description: 'Return all units who\'s type allows unit rates'
      },
      calendarId: { 
        type: 'number', 
        description: 'Return all units matching this unit\'s type with calendar group id'
      },
      roleId: { 
        type: 'number', 
        description: 'Return units by is a specific roleId is being used'
      },
      id: { 
        type: 'array', 
        items: { type: 'number' },
        description: 'Filter by Unit IDs'
      }
    },
    required: []
  };

  override outputSchema = {
    type: 'object' as const,
    properties: {
      data: {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            id: { type: 'number' },
            name: { type: 'string' },
            nodeId: { type: 'number' },
            unitTypeId: { type: 'number' },
            bedrooms: { type: 'number' },
            bathrooms: { type: 'number' },
            isActive: { type: 'boolean' },
            isBookable: { type: 'boolean' }
          }
        }
      },
      totalElements: { type: 'number' },
      totalPages: { type: 'number' },
      currentPage: { type: 'number' }
    }
  };

  async execute(params: GetUnitsParams = {}): Promise<GetUnitsResponse> {
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

    if (params.term) {
      queryParams.append('term', params.term);
    }

    if (params.unitCode) {
      queryParams.append('unitCode', params.unitCode);
    }

    if (params.shortName) {
      queryParams.append('shortName', params.shortName);
    }

    if (params.contentUpdatedSince) {
      queryParams.append('contentUpdatedSince', params.contentUpdatedSince);
    }

    if (params.updatedSince) {
      queryParams.append('updatedSince', params.updatedSince);
    }

    // Agregar filtros por ID solo si están definidos
    this.addIdFilter(queryParams, 'nodeId', params.nodeId);
    this.addIdFilter(queryParams, 'unitTypeId', params.unitTypeId);
    this.addIdFilter(queryParams, 'amenityId', params.amenityId);

    // Agregar filtros físicos solo si están definidos
    if (params.bedrooms !== undefined) {
      queryParams.append('bedrooms', params.bedrooms.toString());
    }
    if (params.minBedrooms !== undefined) {
      queryParams.append('minBedrooms', params.minBedrooms.toString());
    }
    if (params.maxBedrooms !== undefined) {
      queryParams.append('maxBedrooms', params.maxBedrooms.toString());
    }
    if (params.bathrooms !== undefined) {
      queryParams.append('bathrooms', params.bathrooms.toString());
    }
    if (params.minBathrooms !== undefined) {
      queryParams.append('minBathrooms', params.minBathrooms.toString());
    }
    if (params.maxBathrooms !== undefined) {
      queryParams.append('maxBathrooms', params.maxBathrooms.toString());
    }

    // Agregar filtros de políticas solo si están definidos
    if (params.petsFriendly !== undefined) {
      queryParams.append('petsFriendly', params.petsFriendly.toString());
    }
    if (params.eventsAllowed !== undefined) {
      queryParams.append('eventsAllowed', params.eventsAllowed.toString());
    }
    if (params.smokingAllowed !== undefined) {
      queryParams.append('smokingAllowed', params.smokingAllowed.toString());
    }
    if (params.childrenAllowed !== undefined) {
      queryParams.append('childrenAllowed', params.childrenAllowed.toString());
    }

    // Agregar filtros de disponibilidad solo si están definidos
    if (params.arrival) {
      queryParams.append('arrival', params.arrival);
    }
    if (params.departure) {
      queryParams.append('departure', params.departure);
    }

    // Agregar filtros de estado solo si están definidos
    if (params.isActive !== undefined) {
      queryParams.append('isActive', params.isActive.toString());
    }
    if (params.isBookable !== undefined) {
      queryParams.append('isBookable', params.isBookable.toString());
    }
    if (params.unitStatus) {
      queryParams.append('unitStatus', params.unitStatus);
    }

    // Agregar filtros adicionales solo si están definidos
    if (params.computed !== undefined) {
      queryParams.append('computed', params.computed.toString());
    }
    if (params.inherited !== undefined) {
      queryParams.append('inherited', params.inherited.toString());
    }
    if (params.limited !== undefined) {
      queryParams.append('limited', params.limited.toString());
    }
    if (params.includeDescriptions !== undefined) {
      queryParams.append('includeDescriptions', params.includeDescriptions.toString());
    }
    if (params.allowUnitRates !== undefined) {
      queryParams.append('allowUnitRates', params.allowUnitRates.toString());
    }
    if (params.calendarId !== undefined) {
      queryParams.append('calendarId', params.calendarId.toString());
    }
    if (params.roleId !== undefined) {
      queryParams.append('roleId', params.roleId.toString());
    }

    // Agregar filtro de IDs de unidades solo si está definido
    if (params.id !== undefined) {
      this.addIdFilter(queryParams, 'id', params.id);
    }

    const endpoint = `/pms/units?${queryParams.toString()}`;
    
    // Debug: Log the endpoint being called
    console.error(`[DEBUG] Calling endpoint: ${endpoint}`);
    console.error(`[DEBUG] Query params:`, Object.fromEntries(queryParams.entries()));
    
    try {
      const result = await this.apiClient.get<GetUnitsResponse>(endpoint);
      return result;
    } catch (error) {
      console.error(`[DEBUG] Error details:`, error);
      throw new Error(`Error al obtener unidades: ${error instanceof Error ? error.message : 'Error desconocido'}`);
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
}
