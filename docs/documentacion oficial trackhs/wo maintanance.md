Create Maintenance Work Order

# OpenAPI definition
```json
{
  "_id": "/branches/1.0/apis/pms-maintenance-api.json",
  "openapi": "3.0.0",
  "info": {
    "title": "PMS Maintenance API",
    "version": "1.0",
    "description": "The full PMS API is large, as such we have broken down the files into related components. Since some of the components may share model files, models are referenced instead of embedded.\n\nThis API covers all endpoints related to Maintenance.\n\nWhen used externally, this API requires a server context key.\n\nWhen used in user context, endpoints may be restricted based on role.\n",
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
  "tags": [
    {
      "name": "Work Order"
    }
  ],
  "paths": {
    "/pms/maintenance/work-orders": {
      "post": {
        "summary": "Create Maintenance Work Order",
        "operationId": "createMaintenanceWorkOrder",
        "responses": {
          "201": {
            "description": "Created",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Maintenance Work Order Response",
                  "type": "object",
                  "description": "Response.",
                  "properties": {
                    "id": {
                      "type": "integer",
                      "description": "ID"
                    },
                    "dateReceived": {
                      "type": "string",
                      "format": "date",
                      "description": "Date as ISO 8601 format"
                    },
                    "priority": {
                      "type": "number",
                      "enum": [
                        5,
                        3,
                        1
                      ],
                      "description": "Priority Level -- High=5, Medium=3, Low=1"
                    },
                    "status": {
                      "type": "string",
                      "enum": [
                        "open",
                        "not-started",
                        "in-progress",
                        "completed",
                        "processed",
                        "vendor-not-start",
                        "vendor-assigned",
                        "vendor-declined",
                        "vendor-completed",
                        "user-completed",
                        "cancelled"
                      ]
                    },
                    "assignees": {
                      "type": "array",
                      "nullable": true,
                      "items": {
                        "type": "object"
                      }
                    },
                    "summary": {
                      "type": "string"
                    },
                    "problems": {
                      "type": "array",
                      "nullable": true,
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "number"
                          },
                          "name": {
                            "type": "string"
                          }
                        }
                      }
                    },
                    "estimatedCost": {
                      "type": "number",
                      "format": "float"
                    },
                    "estimatedTime": {
                      "type": "integer",
                      "description": "Time in minutes."
                    },
                    "actualTime": {
                      "type": "integer",
                      "description": "Time in minutes. Requires time tracking BETA."
                    },
                    "dateCompleted": {
                      "type": "string",
                      "format": "date",
                      "description": "Date in ISO 8601 format."
                    },
                    "completedById": {
                      "type": "number"
                    },
                    "dateProcessed": {
                      "type": "string",
                      "format": "date",
                      "description": "Date as ISO 8601 format"
                    },
                    "processedById": {
                      "type": "number"
                    },
                    "userId": {
                      "type": "number"
                    },
                    "vendorId": {
                      "type": "number"
                    },
                    "unitId": {
                      "type": "number"
                    },
                    "ownerId": {
                      "type": "number"
                    },
                    "reservationId": {
                      "type": "number"
                    },
                    "referenceNumber": {
                      "type": "string"
                    },
                    "description": {
                      "type": "string"
                    },
                    "workPerformed": {
                      "type": "string"
                    },
                    "source": {
                      "type": "string"
                    },
                    "sourceName": {
                      "type": "string"
                    },
                    "sourcePhone": {
                      "type": "string"
                    },
                    "blockCheckin": {
                      "type": "boolean"
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
                        "unit": {
                          "type": "object"
                        },
                        "vendor": {
                          "type": "object"
                        },
                        "owner": {
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
                  ]
                }
              }
            }
          },
          "401": {
            "description": "Unauthorized",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Api Problem Response",
                  "type": "object",
                  "x-examples": {
                    "Invalid Authentication": {
                      "type": "http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html",
                      "title": "Forbidden",
                      "status": 403,
                      "detail": "Forbidden"
                    }
                  },
                  "description": "In an error situation, we will return a json object with details of the error. This response is based on the following specification: https://tools.ietf.org/html/rfc7807",
                  "properties": {
                    "code": {
                      "type": "string",
                      "description": "New code structure to track errors for endpoints rather than matching description strings.\nThese will start to appear in all endpoints starting March 2021.\n"
                    },
                    "type": {
                      "type": "string",
                      "format": "uri",
                      "example": "http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html",
                      "description": "A URI reference that identifies the problem type."
                    },
                    "title": {
                      "type": "string",
                      "description": "A short, human-readable summary of the problem type."
                    },
                    "status": {
                      "example": 200,
                      "description": "HTTP status code",
                      "type": "integer"
                    },
                    "detail": {
                      "type": "string",
                      "description": "A human-readable explanation specific to this occurrence of the problem."
                    },
                    "validation_messages": {
                      "type": "array",
                      "description": "We use this to send validation message, often in conjunction with 400 or 422 status codes.",
                      "items": {
                        "type": "string"
                      }
                    }
                  },
                  "required": [
                    "type",
                    "title",
                    "status",
                    "detail"
                  ]
                }
              }
            }
          },
          "403": {
            "description": "Forbidden",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Api Problem Response",
                  "type": "object",
                  "x-examples": {
                    "Invalid Authentication": {
                      "type": "http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html",
                      "title": "Forbidden",
                      "status": 403,
                      "detail": "Forbidden"
                    }
                  },
                  "description": "In an error situation, we will return a json object with details of the error. This response is based on the following specification: https://tools.ietf.org/html/rfc7807",
                  "properties": {
                    "code": {
                      "type": "string",
                      "description": "New code structure to track errors for endpoints rather than matching description strings.\nThese will start to appear in all endpoints starting March 2021.\n"
                    },
                    "type": {
                      "type": "string",
                      "format": "uri",
                      "example": "http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html",
                      "description": "A URI reference that identifies the problem type."
                    },
                    "title": {
                      "type": "string",
                      "description": "A short, human-readable summary of the problem type."
                    },
                    "status": {
                      "example": 200,
                      "description": "HTTP status code",
                      "type": "integer"
                    },
                    "detail": {
                      "type": "string",
                      "description": "A human-readable explanation specific to this occurrence of the problem."
                    },
                    "validation_messages": {
                      "type": "array",
                      "description": "We use this to send validation message, often in conjunction with 400 or 422 status codes.",
                      "items": {
                        "type": "string"
                      }
                    }
                  },
                  "required": [
                    "type",
                    "title",
                    "status",
                    "detail"
                  ]
                }
              }
            }
          },
          "422": {
            "description": "Unprocessable Entity",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Api Problem Response",
                  "type": "object",
                  "x-examples": {
                    "Invalid Authentication": {
                      "type": "http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html",
                      "title": "Forbidden",
                      "status": 403,
                      "detail": "Forbidden"
                    }
                  },
                  "description": "In an error situation, we will return a json object with details of the error. This response is based on the following specification: https://tools.ietf.org/html/rfc7807",
                  "properties": {
                    "code": {
                      "type": "string",
                      "description": "New code structure to track errors for endpoints rather than matching description strings.\nThese will start to appear in all endpoints starting March 2021.\n"
                    },
                    "type": {
                      "type": "string",
                      "format": "uri",
                      "example": "http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html",
                      "description": "A URI reference that identifies the problem type."
                    },
                    "title": {
                      "type": "string",
                      "description": "A short, human-readable summary of the problem type."
                    },
                    "status": {
                      "example": 200,
                      "description": "HTTP status code",
                      "type": "integer"
                    },
                    "detail": {
                      "type": "string",
                      "description": "A human-readable explanation specific to this occurrence of the problem."
                    },
                    "validation_messages": {
                      "type": "array",
                      "description": "We use this to send validation message, often in conjunction with 400 or 422 status codes.",
                      "items": {
                        "type": "string"
                      }
                    }
                  },
                  "required": [
                    "type",
                    "title",
                    "status",
                    "detail"
                  ]
                }
              }
            }
          },
          "500": {
            "description": "Internal Server Error",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Api Problem Response",
                  "type": "object",
                  "x-examples": {
                    "Invalid Authentication": {
                      "type": "http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html",
                      "title": "Forbidden",
                      "status": 403,
                      "detail": "Forbidden"
                    }
                  },
                  "description": "In an error situation, we will return a json object with details of the error. This response is based on the following specification: https://tools.ietf.org/html/rfc7807",
                  "properties": {
                    "code": {
                      "type": "string",
                      "description": "New code structure to track errors for endpoints rather than matching description strings.\nThese will start to appear in all endpoints starting March 2021.\n"
                    },
                    "type": {
                      "type": "string",
                      "format": "uri",
                      "example": "http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html",
                      "description": "A URI reference that identifies the problem type."
                    },
                    "title": {
                      "type": "string",
                      "description": "A short, human-readable summary of the problem type."
                    },
                    "status": {
                      "example": 200,
                      "description": "HTTP status code",
                      "type": "integer"
                    },
                    "detail": {
                      "type": "string",
                      "description": "A human-readable explanation specific to this occurrence of the problem."
                    },
                    "validation_messages": {
                      "type": "array",
                      "description": "We use this to send validation message, often in conjunction with 400 or 422 status codes.",
                      "items": {
                        "type": "string"
                      }
                    }
                  },
                  "required": [
                    "type",
                    "title",
                    "status",
                    "detail"
                  ]
                }
              }
            }
          }
        },
        "parameters": [
          {
            "schema": {
              "type": "string",
              "enum": [
                "application/json"
              ],
              "default": "application/json"
            },
            "in": "header",
            "name": "Content-Type"
          }
        ],
        "tags": [
          "Work Order"
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "title": "Maintenance Work Order Request",
                "type": "object",
                "description": "This supports creation of tasks.",
                "properties": {
                  "dateReceived": {
                    "type": "string",
                    "format": "date",
                    "description": "Date as ISO 8601 format"
                  },
                  "priority": {
                    "type": "number",
                    "enum": [
                      5,
                      3,
                      1
                    ],
                    "description": "Priority Level -- High=5, Medium=3, Low=1"
                  },
                  "summary": {
                    "type": "string"
                  },
                  "estimatedCost": {
                    "type": "number",
                    "format": "float"
                  },
                  "estimatedTime": {
                    "type": "integer",
                    "description": "Estimated time in minutes."
                  },
                  "dateScheduled": {
                    "type": "string",
                    "format": "date",
                    "description": "Date as ISO 8601 format"
                  },
                  "userId": {
                    "type": "number",
                    "nullable": true
                  },
                  "vendorId": {
                    "type": "number",
                    "nullable": true
                  },
                  "unitId": {
                    "type": "number",
                    "nullable": true
                  },
                  "reservationId": {
                    "type": "number",
                    "nullable": true
                  },
                  "referenceNumber": {
                    "type": "string"
                  },
                  "description": {
                    "type": "string"
                  },
                  "workPerformed": {
                    "type": "string"
                  },
                  "source": {
                    "type": "string"
                  },
                  "sourceName": {
                    "type": "string"
                  },
                  "sourcePhone": {
                    "type": "string"
                  },
                  "actualTime": {
                    "type": "number",
                    "description": "Total Time Spent In Minutes"
                  },
                  "blockCheckin": {
                    "type": "boolean",
                    "description": "Set whether this work order will prevent reservation check-ins for scheduled date provided."
                  }
                },
                "required": [
                  "dateReceived",
                  "priority",
                  "status",
                  "summary",
                  "estimatedCost",
                  "estimatedTime"
                ]
              }
            }
          }
        },
        "description": "This endpoint will allow you to create a new maintenance work-order.",
        "security": [
          {
            "hmac": []
          },
          {
            "basic": []
          }
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