Reservation Collection

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
    "/pms/reservations": {
      "get": {
        "summary": "Reservation Collection",
        "tags": [
          "Reservation"
        ],
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "_links": {
                      "title": "CollectionLinks",
                      "type": "object",
                      "properties": {
                        "self": {
                          "type": "object",
                          "required": [
                            "href"
                          ],
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          }
                        },
                        "first": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          },
                          "required": [
                            "href"
                          ]
                        },
                        "last": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          },
                          "required": [
                            "href"
                          ]
                        },
                        "next": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          },
                          "required": [
                            "href"
                          ]
                        },
                        "prev": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          },
                          "required": [
                            "href"
                          ]
                        }
                      },
                      "required": [
                        "self",
                        "first",
                        "last"
                      ],
                      "description": "All collections provide the following set of links. Next or prev will only be provided if there is a next or previous page.",
                      "x-examples": {}
                    },
                    "total_items": {
                      "type": "number"
                    },
                    "page_size": {
                      "type": "number"
                    },
                    "page_count": {
                      "type": "number"
                    },
                    "page": {
                      "type": "number"
                    },
                    "_embedded": {
                      "type": "object",
                      "properties": {
                        "reservations": {
                          "type": "array",
                          "items": {
                            "title": "Reservation Response",
                            "type": "object",
                            "description": "Reservation Response",
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
                    }
                  },
                  "required": [
                    "_links",
                    "total_items",
                    "page_size",
                    "page_count",
                    "page",
                    "_embedded"
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
          "500": {
            "description": "Internal Server Error"
          }
        },
        "operationId": "getReservations",
        "description": "Get a collection of reservations with pagination and filtering options.",
        "parameters": [
          {
            "schema": {
              "type": "integer",
              "minimum": 0,
              "maximum": 10000
            },
            "in": "query",
            "name": "page",
            "description": "Page number (0-based)"
          },
          {
            "schema": {
              "type": "integer",
              "minimum": 1,
              "maximum": 100
            },
            "in": "query",
            "name": "size",
            "description": "Page size (1-100)"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "search",
            "description": "Search in confirmation number, guest name, or email"
          },
          {
            "schema": {
              "type": "string",
              "format": "date"
            },
            "in": "query",
            "name": "arrival_start",
            "description": "Start date for arrival filter (YYYY-MM-DD)"
          },
          {
            "schema": {
              "type": "string",
              "format": "date"
            },
            "in": "query",
            "name": "arrival_end",
            "description": "End date for arrival filter (YYYY-MM-DD)"
          },
          {
            "schema": {
              "type": "string",
              "enum": [
                "confirmed",
                "cancelled",
                "checked-in",
                "checked-out",
                "no-show"
              ]
            },
            "in": "query",
            "name": "status",
            "description": "Filter by reservation status"
          }
        ],
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


