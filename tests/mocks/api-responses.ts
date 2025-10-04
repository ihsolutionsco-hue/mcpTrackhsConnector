/**
 * Respuestas mock para la API de Track HS
 */

export const mockApiResponses = {
  // Respuestas para get-reviews
  reviews: {
    success: {
      data: [
        {
          id: 1,
          rating: 5,
          comment: "Excelente servicio",
          guest_name: "Juan Pérez",
          created_at: "2024-01-15T10:30:00Z"
        },
        {
          id: 2,
          rating: 4,
          comment: "Muy bueno",
          guest_name: "María García",
          created_at: "2024-01-14T15:45:00Z"
        }
      ],
      meta: {
        total: 2,
        page: 1,
        per_page: 10
      }
    }
  },

  // Respuestas para get-reservation
  reservation: {
    success: {
      data: {
        id: 123,
        guest_name: "Ana López",
        check_in: "2024-02-01",
        check_out: "2024-02-05",
        status: "confirmed",
        total_amount: 500.00,
        unit_id: 456
      }
    },
    notFound: {
      error: "Reservation not found",
      code: 404
    }
  },

  // Respuestas para search-reservations
  searchReservations: {
    success: {
      _embedded: {
        reservations: [
          {
            id: 123,
            guest_name: "Ana López",
            check_in: "2024-02-01",
            check_out: "2024-02-05",
            status: "confirmed",
            arrivalDate: "2024-02-01",
            departureDate: "2024-02-05",
            unitId: 456
          },
          {
            id: 124,
            guest_name: "Carlos Ruiz",
            check_in: "2024-02-10",
            check_out: "2024-02-15",
            status: "pending",
            arrivalDate: "2024-02-10",
            departureDate: "2024-02-15",
            unitId: 457
          }
        ]
      },
      page: 0,
      page_count: 1,
      page_size: 10,
      total_items: 2,
      _links: {
        self: { href: "/v2/pms/reservations?page=0&size=10" },
        first: { href: "/v2/pms/reservations?page=0&size=10" },
        last: { href: "/v2/pms/reservations?page=0&size=10" }
      }
    }
  },

  // Respuestas para get-units
  units: {
    success: {
      data: [
        {
          id: 456,
          name: "Suite Deluxe",
          type: "suite",
          capacity: 4,
          price_per_night: 150.00,
          status: "available"
        },
        {
          id: 457,
          name: "Habitación Estándar",
          type: "room",
          capacity: 2,
          price_per_night: 80.00,
          status: "available"
        }
      ],
      meta: {
        total: 2,
        page: 1,
        per_page: 10
      }
    }
  },

  // Respuestas para get-unit
  unit: {
    success: {
      data: {
        id: 456,
        name: "Suite Deluxe",
        type: "suite",
        capacity: 4,
        price_per_night: 150.00,
        status: "available",
        amenities: ["WiFi", "TV", "Minibar"],
        description: "Suite espaciosa con vista al mar"
      }
    },
    notFound: {
      error: "Unit not found",
      code: 404
    }
  },

  // Respuestas para get-folios-collection
  foliosCollection: {
    success: {
      data: [
        {
          id: 789,
          folio_number: "FOL-001",
          guest_name: "Ana López",
          total_amount: 500.00,
          status: "paid",
          created_at: "2024-01-15T10:30:00Z"
        }
      ],
      meta: {
        total: 1,
        page: 1,
        per_page: 10
      }
    }
  },

  // Respuestas para get-contacts
  contacts: {
    success: {
      data: [
        {
          id: 101,
          name: "Juan Pérez",
          email: "juan@example.com",
          phone: "+1234567890",
          type: "guest"
        },
        {
          id: 102,
          name: "María García",
          email: "maria@example.com",
          phone: "+0987654321",
          type: "vendor"
        }
      ],
      meta: {
        total: 2,
        page: 1,
        per_page: 10
      }
    }
  },

  // Respuestas para get-ledger-accounts
  ledgerAccounts: {
    success: {
      data: [
        {
          id: 201,
          account_code: "1001",
          account_name: "Caja",
          account_type: "asset",
          balance: 5000.00
        },
        {
          id: 202,
          account_code: "2001",
          account_name: "Cuentas por Pagar",
          account_type: "liability",
          balance: 2500.00
        }
      ],
      meta: {
        total: 2,
        page: 1,
        per_page: 10
      }
    }
  },

  // Respuestas para get-ledger-account
  ledgerAccount: {
    success: {
      data: {
        id: 201,
        account_code: "1001",
        account_name: "Caja",
        account_type: "asset",
        balance: 5000.00,
        description: "Cuenta de caja principal"
      }
    },
    notFound: {
      error: "Ledger account not found",
      code: 404
    }
  },

  // Respuestas para get-reservation-notes
  reservationNotes: {
    success: {
      data: [
        {
          id: 301,
          reservation_id: 123,
          note: "Cliente solicita cama extra",
          created_by: "Recepción",
          created_at: "2024-01-15T10:30:00Z"
        }
      ],
      meta: {
        total: 1,
        page: 1,
        per_page: 10
      }
    }
  },

  // Respuestas para get-nodes
  nodes: {
    success: {
      data: [
        {
          id: 401,
          name: "Recepción",
          type: "department",
          status: "active"
        },
        {
          id: 402,
          name: "Mantenimiento",
          type: "department",
          status: "active"
        }
      ],
      meta: {
        total: 2,
        page: 1,
        per_page: 10
      }
    }
  },

  // Respuestas para get-node
  node: {
    success: {
      data: {
        id: 401,
        name: "Recepción",
        type: "department",
        status: "active",
        description: "Departamento de recepción principal"
      }
    },
    notFound: {
      error: "Node not found",
      code: 404
    }
  },

  // Respuestas de error comunes
  errors: {
    unauthorized: {
      error: "Unauthorized",
      code: 401,
      message: "Invalid credentials"
    },
    forbidden: {
      error: "Forbidden",
      code: 403,
      message: "Access denied"
    },
    notFound: {
      error: "Not Found",
      code: 404,
      message: "Resource not found"
    },
    serverError: {
      error: "Internal Server Error",
      code: 500,
      message: "Something went wrong"
    },
    badRequest: {
      error: "Bad Request",
      code: 400,
      message: "Invalid request parameters"
    }
  }
};
