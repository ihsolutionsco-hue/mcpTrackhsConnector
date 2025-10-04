/**
 * Tipos específicos para las notas de reservaciones de Track HS
 */

export interface ReservationNote {
  id: number;
  reservationId: number;
  content: string;
  author: string;
  createdAt: string;
  updatedAt: string;
  isInternal: boolean;
  noteType?: string;
  priority?: 'low' | 'medium' | 'high';
  tags?: string[];
}

export interface ReservationNotesResponse {
  _embedded: {
    notes: ReservationNote[];
  };
  page?: number;
  page_count?: number;
  page_size?: number;
  total_items?: number;
  _links: {
    self: { href: string };
    first?: { href: string };
    last?: { href: string };
    next?: { href: string };
    prev?: { href: string };
  };
}

export interface ReservationNotesParams {
  // Paginación
  page?: number;
  size?: number;
  
  // Filtros
  isInternal?: boolean;
  noteType?: string;
  priority?: 'low' | 'medium' | 'high';
  author?: string;
  
  // Ordenamiento
  sortBy?: 'createdAt' | 'updatedAt' | 'author' | 'priority';
  sortDirection?: 'asc' | 'desc';
  
  // Búsqueda
  search?: string;
  dateFrom?: string;
  dateTo?: string;
}

export interface CreateReservationNoteRequest {
  content: string;
  isInternal?: boolean;
  noteType?: string;
  priority?: 'low' | 'medium' | 'high';
  tags?: string[];
}

export interface UpdateReservationNoteRequest {
  content?: string;
  isInternal?: boolean;
  noteType?: string;
  priority?: 'low' | 'medium' | 'high';
  tags?: string[];
}

export interface ReservationNoteResponse {
  data: ReservationNote;
  success: boolean;
  message?: string;
}
