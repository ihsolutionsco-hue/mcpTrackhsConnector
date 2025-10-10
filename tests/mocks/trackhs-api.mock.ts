/**
 * Mocks para la API de TrackHS
 * Proporciona respuestas simuladas para testing
 */

export const mockTrackHSApiResponses = {
  // Respuestas de contactos
  contacts: {
    success: {
      data: [
        {
          id: '1',
          name: 'Juan Pérez',
          email: 'juan@example.com',
          phone: '+1234567890',
          created_at: '2024-01-15T10:30:00Z',
          updated_at: '2024-01-15T10:30:00Z'
        },
        {
          id: '2',
          name: 'María García',
          email: 'maria@example.com',
          phone: '+1234567891',
          created_at: '2024-01-14T15:45:00Z',
          updated_at: '2024-01-14T15:45:00Z'
        }
      ],
      meta: {
        page: 1,
        per_page: 10,
        total: 2
      }
    },
    empty: {
      data: [],
      meta: {
        page: 1,
        per_page: 10,
        total: 0
      }
    }
  },

  // Respuestas de reseñas
  reviews: {
    success: {
      data: [
        {
          id: 1,
          guest_name: 'Juan Pérez',
          rating: 5,
          comment: 'Excelente servicio',
          created_at: '2024-01-15T10:30:00Z'
        },
        {
          id: 2,
          guest_name: 'María García',
          rating: 4,
          comment: 'Muy bueno',
          created_at: '2024-01-14T15:45:00Z'
        }
      ],
      meta: {
        page: 1,
        per_page: 10,
        total: 2
      }
    }
  },

  // Respuestas de reservaciones
  reservations: {
    success: {
      data: [
        {
          id: 123,
          guest_name: 'Ana López',
          check_in: '2024-02-01',
          check_out: '2024-02-05',
          status: 'confirmed',
          total_amount: 500,
          unit_id: 456
        }
      ],
      meta: {
        page: 1,
        per_page: 10,
        total: 1
      }
    },
    single: {
      data: {
        id: 123,
        guest_name: 'Ana López',
        check_in: '2024-02-01',
        check_out: '2024-02-05',
        status: 'confirmed',
        total_amount: 500,
        unit_id: 456
      }
    }
  },

  // Respuestas de unidades
  units: {
    success: {
      _embedded: {
        units: [
          {
            id: 456,
            name: 'Suite Deluxe',
            type: 'suite',
            capacity: 4,
            status: 'available',
            amenities: ['WiFi', 'TV', 'Minibar'],
            description: 'Suite espaciosa con vista al mar',
            price_per_night: 150
          },
          {
            id: 457,
            name: 'Habitación Estándar',
            type: 'room',
            capacity: 2,
            status: 'available',
            amenities: ['WiFi', 'TV'],
            description: 'Habitación cómoda y funcional',
            price_per_night: 80
          }
        ]
      },
      page: {
        size: 10,
        totalElements: 2,
        totalPages: 1,
        number: 0
      }
    },
    single: {
      data: {
        id: 456,
        name: 'Suite Deluxe',
        type: 'suite',
        capacity: 4,
        status: 'available',
        amenities: ['WiFi', 'TV', 'Minibar'],
        description: 'Suite espaciosa con vista al mar',
        price_per_night: 150
      }
    }
  },

  // Respuestas de nodos
  nodes: {
    success: {
      data: [
        {
          id: 'node-1',
          name: 'Hotel Central',
          type: 'hotel',
          address: 'Calle Principal 123',
          status: 'active'
        }
      ],
      meta: {
        page: 1,
        per_page: 10,
        total: 1
      }
    }
  },

  // Respuestas de cuentas contables
  ledgerAccounts: {
    success: {
      data: [
        {
          id: 'acc-1',
          name: 'Cuenta de Ingresos',
          type: 'income',
          balance: 10000,
          status: 'active'
        }
      ],
      meta: {
        page: 1,
        per_page: 10,
        total: 1
      }
    }
  },

  // Respuestas de folios
  folios: {
    success: {
      data: [
        {
          id: 'folio-1',
          number: 'F001',
          date: '2024-01-15',
          amount: 500,
          status: 'posted'
        }
      ],
      meta: {
        page: 1,
        per_page: 10,
        total: 1
      }
    }
  },

  // Respuestas de órdenes de mantenimiento
  workOrders: {
    success: {
      data: [
        {
          id: 'wo-1',
          title: 'Mantenimiento A/C',
          description: 'Revisión de aire acondicionado',
          status: 'pending',
          priority: 'medium',
          assigned_to: 'Técnico Juan',
          due_date: '2024-01-20'
        }
      ],
      meta: {
        page: 1,
        per_page: 10,
        total: 1
      }
    }
  }
};

// Errores simulados
export const mockTrackHSApiErrors = {
  notFound: {
    error: 'Not Found',
    message: 'Resource not found',
    status: 404
  },
  unauthorized: {
    error: 'Unauthorized',
    message: 'Invalid credentials',
    status: 401
  },
  serverError: {
    error: 'Internal Server Error',
    message: 'Server error',
    status: 500
  },
  notImplemented: {
    error: 'Not Implemented',
    message: 'API endpoint not implemented',
    status: 501
  }
};

// Helper para crear respuestas de error
export const createErrorResponse = (status: number, message: string) => {
  return {
    error: true,
    status,
    message,
    timestamp: new Date().toISOString()
  };
};

// Helper para crear respuestas exitosas
export const createSuccessResponse = (data: any, meta?: any) => {
  return {
    success: true,
    data,
    meta: meta || {
      page: 1,
      per_page: 10,
      total: Array.isArray(data) ? data.length : 1
    },
    timestamp: new Date().toISOString()
  };
};
