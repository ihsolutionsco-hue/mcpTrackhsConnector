/**
 * Herramienta MCP para obtener notas de una reservación específica de Track HS
 */

import { BaseTrackHSTool } from '../core/base-tool.js';
import { ReservationNotesResponse, ReservationNotesParams } from '../types/reservation-notes.js';

export class GetReservationNotesTool extends BaseTrackHSTool {
  name = 'get_reservation_notes';
  description = 'Get notes for a specific reservation with optional filtering and pagination';
  
  inputSchema = {
    type: 'object' as const,
    properties: {
      reservationId: { 
        type: 'string', 
        description: 'The ID of the reservation to get notes for'
      },
      // Paginación
      page: { 
        type: 'number', 
        minimum: 0,
        description: 'Page number of result set'
      },
      size: { 
        type: 'number', 
        minimum: 1,
        maximum: 100,
        description: 'Size of page (max 100)'
      },
      // Filtros
      isInternal: { 
        type: 'boolean', 
        description: 'Filter by internal notes (true) or external notes (false)'
      },
      noteType: { 
        type: 'string', 
        description: 'Filter by note type'
      },
      priority: { 
        type: 'string', 
        enum: ['low', 'medium', 'high'],
        description: 'Filter by note priority'
      },
      author: { 
        type: 'string', 
        description: 'Filter by note author'
      },
      // Ordenamiento
      sortBy: { 
        type: 'string', 
        enum: ['createdAt', 'updatedAt', 'author', 'priority'],
        default: 'createdAt',
        description: 'Field to sort notes by'
      },
      sortDirection: { 
        type: 'string', 
        enum: ['asc', 'desc'],
        default: 'desc',
        description: 'Sort direction'
      },
      // Búsqueda
      search: { 
        type: 'string', 
        description: 'Search in note content'
      },
      dateFrom: { 
        type: 'string', 
        format: 'date-time',
        description: 'Filter notes from this date (ISO 8601 format)'
      },
      dateTo: { 
        type: 'string', 
        format: 'date-time',
        description: 'Filter notes to this date (ISO 8601 format)'
      }
    },
    required: ['reservationId']
  };

  async execute(params: ReservationNotesParams & { reservationId: string }): Promise<ReservationNotesResponse> {
    // Validar parámetros
    this.validateParams(params);

    const { reservationId, ...queryParams } = params;

    // Validar que el ID no esté vacío
    if (!reservationId || reservationId.trim() === '') {
      throw new Error('El ID de reservación no puede estar vacío');
    }

    // Construir query parameters
    const urlParams = new URLSearchParams();
    
    // Agregar parámetros de paginación
    if (queryParams.page !== undefined) {
      urlParams.append('page', queryParams.page.toString());
    }
    if (queryParams.size !== undefined) {
      urlParams.append('size', queryParams.size.toString());
    }

    // Agregar filtros
    if (queryParams.isInternal !== undefined) {
      urlParams.append('isInternal', queryParams.isInternal.toString());
    }
    if (queryParams.noteType) {
      urlParams.append('noteType', queryParams.noteType);
    }
    if (queryParams.priority) {
      urlParams.append('priority', queryParams.priority);
    }
    if (queryParams.author) {
      urlParams.append('author', queryParams.author);
    }

    // Agregar ordenamiento
    if (queryParams.sortBy) {
      urlParams.append('sortBy', queryParams.sortBy);
    }
    if (queryParams.sortDirection) {
      urlParams.append('sortDirection', queryParams.sortDirection);
    }

    // Agregar búsqueda
    if (queryParams.search) {
      urlParams.append('search', queryParams.search);
    }
    if (queryParams.dateFrom) {
      urlParams.append('dateFrom', queryParams.dateFrom);
    }
    if (queryParams.dateTo) {
      urlParams.append('dateTo', queryParams.dateTo);
    }

    const queryString = urlParams.toString();
    const endpoint = `/pms/reservations/${encodeURIComponent(reservationId)}/notes${queryString ? `?${queryString}` : ''}`;
    
    try {
      const result = await this.apiClient.get<ReservationNotesResponse>(endpoint);
      return result;
    } catch (error) {
      if (error instanceof Error && error.message.includes('404')) {
        throw new Error(`Reservación con ID '${reservationId}' no encontrada o no tiene notas`);
      }
      throw new Error(`Error al obtener notas de reservación: ${error instanceof Error ? error.message : 'Error desconocido'}`);
    }
  }
}
