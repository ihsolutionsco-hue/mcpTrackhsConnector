/**
 * Herramienta MCP para obtener detalles de una reservación de Track HS
 */

import { BaseTrackHSTool } from '../core/base-tool.js';
import { ReservationResponse } from '../types/reservations.js';

export class GetReservationTool extends BaseTrackHSTool {
  name = 'get_reservation';
  override title = 'Obtener Reservación';
  description = 'Get detailed information for a specific reservation by ID';
  
  inputSchema = {
    type: 'object' as const,
    properties: {
      reservationId: { 
        type: 'string', 
        description: 'The ID of the reservation to retrieve'
      }
    },
    required: ['reservationId']
  };

  override outputSchema = {
    type: 'object' as const,
    properties: {
      id: { type: 'string' },
      guestName: { type: 'string' },
      checkIn: { type: 'string', format: 'date' },
      checkOut: { type: 'string', format: 'date' },
      status: { type: 'string' },
      totalAmount: { type: 'number' },
      unitId: { type: 'string' },
      nodeId: { type: 'string' },
      guestId: { type: 'string' }
    }
  };

  async execute(params: { reservationId: string }): Promise<ReservationResponse> {
    // Validar parámetros
    this.validateParams(params);

    const { reservationId } = params;

    // Validar que el ID no esté vacío
    if (!reservationId || reservationId.trim() === '') {
      throw new Error('El ID de reservación no puede estar vacío');
    }

    const endpoint = `/v2/pms/reservations/${encodeURIComponent(reservationId)}`;
    
    try {
      const result = await this.apiClient.get<ReservationResponse>(endpoint);
      return result;
    } catch (error) {
      if (error instanceof Error && error.message.includes('404')) {
        throw new Error(`Reservación con ID '${reservationId}' no encontrada`);
      }
      throw new Error(`Error al obtener reservación: ${error instanceof Error ? error.message : 'Error desconocido'}`);
    }
  }
}
