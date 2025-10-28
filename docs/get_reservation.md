Get Reservation

# OpenAPI definition
```json
{
  "_id": "/branches/1.0/apis/pms-reservations-api.json",
  "openapi": "3.0.0",
  "info": {
    "title": "PMS Reservations API",
    "version": "1.0",
    "description": "The full PMS API is large, as such we have broken down the files into related components. Since some of the components may share model files, models are referenced instead of embedded.\n\nThis API covers all endpoints related to reservations.\n\nWhen used externally, this API requires a server context key.\n\nWhen used in user context, endpoints may be restricted based on role.",
    "contact": {
      "name": "Track Support",
      "email": "support@trackhs.com",
      "url": "https://support.trackhs.com"
    }
  },
  "servers": [
    {
      "url": "{customerDomain}/api",
      "variables": {
        "customerDomain": {
          "default": "https://api-integration-example.tracksandbox.io",
          "description": "API domain"
        }
      }
    }
  ],
  "paths": {
    "/pms/reservations/{reservationId}": {
      "parameters": [
        {
          "schema": {
            "type": "integer",
            "minimum": 1
          },
          "name": "reservationId",
          "in": "path",
          "description": "Reservation id",
          "required": true
        }
      ],
      "get": {
        "summary": "Get a Reservation",
        "tags": [
          "Reservation"
        ],
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Reservation Response",
                  "type": "object",
                  "description": "Get to see some additional fields depending on the reservation type.",
                  "properties": {
                    "id": {
                      "type": "integer",
                      "minimum": 1
                    },
                    "confirmationNumber": {
                      "type": "string",
                      "description": "Confirmation number for the reservation"
                    },
                    "status": {
                      "type": "string",
                      "enum": [
                        "confirmed",
                        "cancelled",
                        "checked-in",
                        "checked-out",
                        "no-show"
                      ]
                    },
                    "arrivalDate": {
                      "type": "string",
                      "format": "date",
                      "description": "Date in ISO-8601 format"
                    },
                    "departureDate": {
                      "type": "string",
                      "format": "date",
                      "description": "Date in ISO-8601 format"
                    },
                    "unitId": {
                      "type": "integer",
                      "description": "ID of the unit"
                    },
                    "contactId": {
                      "type": "integer",
                      "description": "ID of the guest contact"
                    },
                    "adults": {
                      "type": "integer",
                      "description": "Number of adults"
                    },
                    "children": {
                      "type": "integer",
                      "description": "Number of children"
                    },
                    "pets": {
                      "type": "integer",
                      "description": "Number of pets"
                    },
                    "totalAmount": {
                      "type": "number",
                      "description": "Total amount for the reservation"
                    },
                    "balance": {
                      "type": "number",
                      "description": "Outstanding balance"
                    },
                    "createdAt": {
                      "type": "string",
                      "format": "date-time",
                      "description": "Date time in ISO 8601 format"
                    },
                    "updatedAt": {
                      "type": "string",
                      "format": "date-time",
                      "description": "Date time in ISO 8601 format"
                    },
                    "_embedded": {
                      "type": "object",
                      "properties": {
                        "contact": {
                          "type": "object",
                          "description": "Guest contact information"
                        },
                        "unit": {
                          "type": "object",
                          "description": "Unit information"
                        },
                        "folio": {
                          "type": "object",
                          "description": "Financial folio information"
                        }
                      }
                    },
                    "_links": {
                      "type": "object",
                      "properties": {
                        "self": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          }
                        }
                      }
                    }
                  },
                  "required": [
                    "id",
                    "confirmationNumber",
                    "status",
                    "arrivalDate",
                    "departureDate"
                  ]
                }
              }
            }
          },
          "401": {
            "description": "Unauthorized"
          },
          "403": {
            "description": "Forbidden"
          },
          "404": {
            "description": "Not Found"
          },
          "500": {
            "description": "Internal Server Error"
          }
        },
        "operationId": "getReservation",
        "description": "Get a single reservation by ID.",
        "security": [
          {
            "basic": []
          },
          {
            "hmac": []
          }
        ]
      }
    }
  },
  "components": {
    "securitySchemes": {
      "hmac": {
        "type": "http",
        "scheme": "bearer",
        "description": "HMAC Authentication based on https://github.com/acquia/http-hmac-spec/tree/2.0"
      },
      "basic": {
        "type": "http",
        "scheme": "basic",
        "description": "Authentication is unique to each customer. Please request authorization keys from the customer you are integrating with."
      }
    }
  },
  "security": [
    {
      "basic": []
    },
    {
      "hmac": []
    }
  ],
  "tags": [
    {
      "name": "Reservation"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": true
  }
}
```
