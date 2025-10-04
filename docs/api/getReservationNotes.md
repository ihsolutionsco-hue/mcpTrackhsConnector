Get Reservation Notes

# OpenAPI definition
```json
{
  "_id": "/branches/1.0/apis/channel-api.json",
  "openapi": "3.0.0",
  "info": {
    "title": "Channel API",
    "version": "1.0",
    "description": "This API is intended to be used in channel (OTA, channel managers, websites and other similar sites) integrations.\n\nAn account can limit which data is visible in this API to any given channel.",
    "contact": {
      "name": "Track Support",
      "email": "support@trackhs.com",
      "url": "https://support.trackhs.com"
    }
  },
  "tags": [
    {
      "name": "Reservations",
      "description": "Endpoints which provide reservation notes data and information."
    }
  ],
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
    "/pms/reservations/{reservationId}/notes": {
      "parameters": [
        {
          "schema": {
            "type": "string"
          },
          "name": "reservationId",
          "in": "path",
          "required": true,
          "description": "The ID of the reservation to get notes for"
        }
      ],
      "get": {
        "summary": "Get Reservation Notes",
        "tags": [
          "Reservations"
        ],
        "parameters": [
          {
            "name": "page",
            "in": "query",
            "schema": {
              "type": "integer",
              "minimum": 0,
              "default": 0
            },
            "description": "Page number of result set"
          },
          {
            "name": "size",
            "in": "query",
            "schema": {
              "type": "integer",
              "minimum": 1,
              "maximum": 100,
              "default": 20
            },
            "description": "Size of page (max 100)"
          },
          {
            "name": "isInternal",
            "in": "query",
            "schema": {
              "type": "boolean"
            },
            "description": "Filter by internal notes (true) or external notes (false)"
          },
          {
            "name": "noteType",
            "in": "query",
            "schema": {
              "type": "string"
            },
            "description": "Filter by note type"
          },
          {
            "name": "priority",
            "in": "query",
            "schema": {
              "type": "string",
              "enum": ["low", "medium", "high"]
            },
            "description": "Filter by note priority"
          },
          {
            "name": "author",
            "in": "query",
            "schema": {
              "type": "string"
            },
            "description": "Filter by note author"
          },
          {
            "name": "sortBy",
            "in": "query",
            "schema": {
              "type": "string",
              "enum": ["createdAt", "updatedAt", "author", "priority"],
              "default": "createdAt"
            },
            "description": "Field to sort notes by"
          },
          {
            "name": "sortDirection",
            "in": "query",
            "schema": {
              "type": "string",
              "enum": ["asc", "desc"],
              "default": "desc"
            },
            "description": "Sort direction"
          },
          {
            "name": "search",
            "in": "query",
            "schema": {
              "type": "string"
            },
            "description": "Search in note content"
          },
          {
            "name": "dateFrom",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date-time"
            },
            "description": "Filter notes from this date (ISO 8601 format)"
          },
          {
            "name": "dateTo",
            "in": "query",
            "schema": {
              "type": "string",
              "format": "date-time"
            },
            "description": "Filter notes to this date (ISO 8601 format)"
          }
        ],
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Reservation Notes Response",
                  "type": "object",
                  "properties": {
                    "_embedded": {
                      "type": "object",
                      "properties": {
                        "notes": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "id": {
                                "type": "integer",
                                "description": "Unique identifier for the note"
                              },
                              "reservationId": {
                                "type": "integer",
                                "description": "ID of the reservation this note belongs to"
                              },
                              "content": {
                                "type": "string",
                                "description": "The note content"
                              },
                              "author": {
                                "type": "string",
                                "description": "Author of the note"
                              },
                              "createdAt": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Date and time when the note was created (ISO 8601 format)"
                              },
                              "updatedAt": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Date and time when the note was last updated (ISO 8601 format)"
                              },
                              "isInternal": {
                                "type": "boolean",
                                "description": "Whether the note is internal (true) or external (false)"
                              },
                              "noteType": {
                                "type": "string",
                                "description": "Type of the note (optional)"
                              },
                              "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "Priority level of the note (optional)"
                              },
                              "tags": {
                                "type": "array",
                                "items": {
                                  "type": "string"
                                },
                                "description": "Tags associated with the note (optional)"
                              }
                            },
                            "required": ["id", "reservationId", "content", "author", "createdAt", "updatedAt", "isInternal"]
                          }
                        }
                      }
                    },
                    "page": {
                      "type": "integer",
                      "description": "Current page number"
                    },
                    "page_count": {
                      "type": "integer",
                      "description": "Total number of pages"
                    },
                    "page_size": {
                      "type": "integer",
                      "description": "Number of items per page"
                    },
                    "total_items": {
                      "type": "integer",
                      "description": "Total number of notes"
                    },
                    "_links": {
                      "type": "object",
                      "properties": {
                        "self": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string",
                              "description": "Link to current page"
                            }
                          }
                        },
                        "first": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string",
                              "description": "Link to first page"
                            }
                          }
                        },
                        "last": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string",
                              "description": "Link to last page"
                            }
                          }
                        },
                        "next": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string",
                              "description": "Link to next page"
                            }
                          }
                        },
                        "prev": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string",
                              "description": "Link to previous page"
                            }
                          }
                        }
                      },
                      "required": ["self"]
                    }
                  },
                  "required": ["_embedded", "_links"]
                }
              }
            }
          },
          "400": {
            "description": "Bad Request",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Api Problem Response",
                  "type": "object",
                  "description": "In an error situation, we will return a json object with details of the error. This response is based on the following specification: https://tools.ietf.org/html/rfc7807",
                  "properties": {
                    "code": {
                      "type": "string",
                      "description": "New code structure to track errors for endpoints rather than matching description strings."
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
                      "example": 400,
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
          "401": {
            "description": "Unauthorized",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Api Problem Response",
                  "type": "object",
                  "description": "In an error situation, we will return a json object with details of the error. This response is based on the following specification: https://tools.ietf.org/html/rfc7807",
                  "properties": {
                    "code": {
                      "type": "string",
                      "description": "New code structure to track errors for endpoints rather than matching description strings."
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
                      "example": 401,
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
                  "description": "In an error situation, we will return a json object with details of the error. This response is based on the following specification: https://tools.ietf.org/html/rfc7807",
                  "properties": {
                    "code": {
                      "type": "string",
                      "description": "New code structure to track errors for endpoints rather than matching description strings."
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
                      "example": 403,
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
          "404": {
            "description": "Not Found",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Api Problem Response",
                  "type": "object",
                  "description": "In an error situation, we will return a json object with details of the error. This response is based on the following specification: https://tools.ietf.org/html/rfc7807",
                  "properties": {
                    "code": {
                      "type": "string",
                      "description": "New code structure to track errors for endpoints rather than matching description strings."
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
                      "example": 404,
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
                  "description": "In an error situation, we will return a json object with details of the error. This response is based on the following specification: https://tools.ietf.org/html/rfc7807",
                  "properties": {
                    "code": {
                      "type": "string",
                      "description": "New code structure to track errors for endpoints rather than matching description strings."
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
                      "example": 500,
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
        "operationId": "getReservationNotes",
        "description": "This endpoint will return all notes for the specified reservation with optional filtering and pagination."
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
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": true
  }
}
```
