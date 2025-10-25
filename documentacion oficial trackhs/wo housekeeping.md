Create Housekeeping Work Order

# OpenAPI definition
```json
{
  "_id": "/branches/1.0/apis/pms-housekeeping-api.json",
  "openapi": "3.0.0",
  "info": {
    "title": "PMS Housekeeping API",
    "version": "1.0",
    "contact": {
      "name": "Track Support",
      "email": "support@trackhs.com",
      "url": "https://support.trackhs.com"
    },
    "description": "The full PMS API is large, as such we have broken down the files into related components. Since some of the components may share model files, models are referenced instead of embedded.\n\nThis API covers all endpoints related to housekeeping.\n\nWhen used externally, this API requires a server context key.\n\nWhen used in user context, endpoints may be restricted based on role.\n"
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
  "tags": [
    {
      "name": "Work Order"
    }
  ],
  "paths": {
    "/pms/housekeeping/work-orders": {
      "post": {
        "summary": "Create Housekeeping Work Order",
        "operationId": "createHousekeepingWorkOrder",
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Housekeeping Work Order Response",
                  "type": "object",
                  "description": "Response contains fields for all tasks.",
                  "properties": {
                    "id": {
                      "type": "integer",
                      "description": "ID"
                    },
                    "isInspection": {
                      "type": "boolean",
                      "description": "Is this an inspection - required if not clean type."
                    },
                    "cleanTypeId": {
                      "type": "integer",
                      "description": "Type of Cleaning - required if not inspection type."
                    },
                    "scheduledAt": {
                      "type": "string",
                      "format": "date",
                      "description": "Date due in ISO-8601 format"
                    },
                    "timeEstimate": {
                      "type": "number",
                      "description": "Estimated time to complete (in minutes)"
                    },
                    "actualTime": {
                      "type": "number",
                      "description": "Actual time took to complete (in minutes). Requires time tracking BETA feature."
                    },
                    "status": {
                      "type": "string",
                      "enum": [
                        "pending",
                        "not-started",
                        "in-progress",
                        "completed",
                        "processed",
                        "cancelled",
                        "exception"
                      ]
                    },
                    "unitId": {
                      "type": "integer",
                      "description": "ID for Unit - required if not unit block"
                    },
                    "unitBlockId": {
                      "type": "integer",
                      "description": "ID for Unit Blocking - required if not unit"
                    },
                    "userId": {
                      "type": "integer",
                      "description": "ID for User"
                    },
                    "reservationId": {
                      "type": "integer",
                      "description": "ID for Reservation"
                    },
                    "vendorId": {
                      "type": "integer",
                      "description": "ID for Vendor"
                    },
                    "isTurn": {
                      "type": "boolean"
                    },
                    "isManual": {
                      "type": "boolean"
                    },
                    "chargeOwner": {
                      "type": "boolean"
                    },
                    "comments": {
                      "type": "string"
                    },
                    "cost": {
                      "type": "number",
                      "format": "float"
                    },
                    "nextReservationId": {
                      "type": "number",
                      "description": "Will provide the reservation ID of the next reservation scheduled after this WO."
                    },
                    "completedAt": {
                      "type": "string",
                      "format": "date",
                      "description": "Date due in ISO-8601 format"
                    },
                    "completedBy": {
                      "type": "integer"
                    },
                    "processedAt": {
                      "type": "string",
                      "format": "date",
                      "description": "Date due in ISO-8601 format"
                    },
                    "processedBy": {
                      "type": "integer"
                    },
                    "createdAt": {
                      "type": "string",
                      "format": "date",
                      "description": "Date Created in ISO-8601 format"
                    },
                    "createdBy": {
                      "type": "string",
                      "description": "Created by this user"
                    },
                    "updatedAt": {
                      "type": "string",
                      "format": "date",
                      "description": "Date Updated in ISO-8601 format"
                    },
                    "updatedBy": {
                      "type": "string",
                      "description": "Updated by this user"
                    },
                    "_embedded": {
                      "type": "object",
                      "properties": {
                        "assignees": {
                          "type": "object"
                        },
                        "vendor": {
                          "type": "object"
                        },
                        "status": {
                          "type": "object"
                        },
                        "cleanType": {
                          "type": "object"
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
                        },
                        "contacts": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          }
                        },
                        "licences": {
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
                    "title",
                    "priority"
                  ],
                  "x-readme-ref-name": "HousekeepingWorkOrderResponse"
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
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "title": "Housekeeping Work Order Request",
                "type": "object",
                "description": "This supports creation of tasks.",
                "properties": {
                  "isInspection": {
                    "type": "boolean",
                    "description": "Is this an inspection - required if not clean type"
                  },
                  "cleanTypeId": {
                    "type": "integer",
                    "description": "Type of Cleaning - required if not inspeciton"
                  },
                  "scheduledAt": {
                    "type": "string",
                    "format": "date",
                    "description": "Date due in ISO-8601 format"
                  },
                  "unitId": {
                    "type": "integer",
                    "description": "ID for Unit - retuired if not unit block"
                  },
                  "unitBlockId": {
                    "type": "integer",
                    "description": "ID for Unit Blocking - required if not unit"
                  },
                  "userId": {
                    "type": "integer",
                    "description": "ID for User"
                  },
                  "reservationId": {
                    "type": "integer",
                    "description": "ID for Reservation"
                  },
                  "vendorId": {
                    "type": "integer",
                    "description": "ID for Vendor"
                  },
                  "isTurn": {
                    "type": "boolean"
                  },
                  "chargeOwner": {
                    "type": "boolean"
                  },
                  "comments": {
                    "type": "string"
                  },
                  "cost": {
                    "type": "number",
                    "format": "float"
                  }
                },
                "required": [
                  "unitId",
                  "scheduledAt",
                  "status"
                ],
                "x-readme-ref-name": "HousekeepingWorkOrderRequest"
              }
            }
          }
        },
        "security": [
          {
            "hmac": []
          },
          {
            "basic": []
          }
        ],
        "description": "Create a new housekeeping work order.",
        "tags": [
          "Work Order"
        ]
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
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": true
  }
}
```