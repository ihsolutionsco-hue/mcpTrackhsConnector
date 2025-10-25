Reservation

# OpenAPI definition
```json
{
  "_id": "/branches/1.0/apis/pms-reservations-api.json",
  "openapi": "3.0.0",
  "info": {
    "title": "PMS Reservations API",
    "version": "1.0",
    "description": "The full PMS API is large, as such we have broken down the files into related components. Since some of the components may share model files, models are referenced instead of embedded.\n\nThis API covers all endpoints related to unit, unit type and node configuration.\n\nWhen used externally, this API requires a server context key.\n\nWhen used in user context, endpoints may be restricted based on role.\n",
    "contact": {
      "name": "Track Support",
      "email": "support@trackhs.com",
      "url": "https://support.trackhs.com"
    }
  },
  "tags": [
    {
      "name": "Reservations"
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
  "paths": {
    "/pms/reservations/{reservationId}": {
      "parameters": [
        {
          "schema": {
            "type": "string"
          },
          "name": "reservationId",
          "in": "path",
          "required": true
        }
      ],
      "get": {
        "summary": "Reservation",
        "tags": [
          "Reservations"
        ],
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Reservation Response - Server",
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "integer",
                      "description": "ID"
                    },
                    "altConf": {
                      "type": "string",
                      "nullable": true
                    },
                    "unitId": {
                      "type": "integer"
                    },
                    "isUnitLocked": {
                      "type": "boolean"
                    },
                    "isUnitAssigned": {
                      "type": "boolean"
                    },
                    "isUnitTypeLocked": {
                      "type": "boolean"
                    },
                    "unitTypeId": {
                      "type": "integer"
                    },
                    "arrivalDate": {
                      "type": "string",
                      "format": "date",
                      "description": "Date as ISO 8601 format (no timestamp)"
                    },
                    "departureDate": {
                      "type": "string",
                      "format": "date",
                      "description": "Date as ISO 8601 format (no timestamp)"
                    },
                    "earlyArrival": {
                      "type": "boolean"
                    },
                    "lateDeparture": {
                      "type": "boolean"
                    },
                    "arrivalTime": {
                      "type": "string",
                      "format": "date-time",
                      "description": "Date as ISO 8601 format"
                    },
                    "departureTime": {
                      "type": "string",
                      "format": "date-time",
                      "description": "Date as ISO 8601 format"
                    },
                    "nights": {
                      "type": "number"
                    },
                    "status": {
                      "type": "string",
                      "enum": [
                        "Hold",
                        "Confirmed",
                        "Checked Out",
                        "Checked In",
                        "Cancelled"
                      ]
                    },
                    "cancelledAt": {
                      "type": "string",
                      "nullable": true,
                      "format": "date-time",
                      "description": "Date as ISO 8601 format"
                    },
                    "occupants": {
                      "type": "object",
                      "additionalProperties": {
                        "oneOf": [
                          {
                            "type": "string"
                          },
                          {
                            "type": "integer"
                          }
                        ]
                      },
                      "example": {
                        "adults": 2,
                        "children": 2,
                        "pets": 0
                      }
                    },
                    "requiredSecurityDeposit": {
                      "type": "number",
                      "format": "float"
                    },
                    "remainingSecurityDeposit": {
                      "type": "number",
                      "format": "float"
                    },
                    "quoteBreakdown": {
                      "type": "object",
                      "properties": {
                        "currency": {
                          "type": "string"
                        },
                        "totalRent": {
                          "type": "number",
                          "format": "float"
                        },
                        "adr": {
                          "type": "number",
                          "format": "float",
                          "description": "average daily rate"
                        },
                        "rates": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "date": {
                                "type": "string",
                                "format": "date",
                                "description": "Date as ISO 8601 format"
                              },
                              "rate": {
                                "type": "number",
                                "format": "float"
                              },
                              "nights": {
                                "type": "number"
                              }
                            }
                          }
                        },
                        "discount": {
                          "type": "number",
                          "format": "float"
                        },
                        "extraRates": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "id": {
                                "type": "integer",
                                "description": "ID"
                              },
                              "quantity": {
                                "type": "number"
                              },
                              "charge": {
                                "type": "number",
                                "format": "float"
                              }
                            }
                          }
                        },
                        "totalFees": {
                          "type": "number",
                          "format": "float"
                        },
                        "fees": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "label": {
                                "type": "string"
                              },
                              "value": {
                                "type": "number",
                                "format": "float"
                              },
                              "display": {
                                "type": "string"
                              }
                            }
                          }
                        },
                        "subTotal": {
                          "type": "number",
                          "format": "float"
                        },
                        "totalTaxes": {
                          "type": "number",
                          "format": "float"
                        },
                        "taxes": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "name": {
                                "type": "string"
                              },
                              "total": {
                                "type": "number",
                                "format": "float"
                              }
                            }
                          }
                        },
                        "total": {
                          "type": "number",
                          "format": "float"
                        },
                        "insurance": {
                          "type": "number",
                          "format": "float"
                        },
                        "grandTotal": {
                          "type": "number",
                          "format": "float"
                        },
                        "payments": {
                          "type": "number",
                          "format": "float"
                        },
                        "balance": {
                          "type": "number",
                          "format": "float"
                        }
                      }
                    },
                    "folioBreakdown": {
                      "type": "object",
                      "properties": {
                        "currency": {
                          "type": "string"
                        },
                        "totalRent": {
                          "type": "number",
                          "format": "float"
                        },
                        "adr": {
                          "type": "number",
                          "format": "float",
                          "description": "average daily rate"
                        },
                        "rates": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "date": {
                                "type": "string",
                                "format": "date",
                                "description": "Date as ISO 8601 format"
                              },
                              "rate": {
                                "type": "number",
                                "format": "float"
                              },
                              "nights": {
                                "type": "number"
                              }
                            }
                          }
                        },
                        "totalFees": {
                          "type": "number",
                          "format": "float"
                        },
                        "totalCharges": {
                          "type": "number",
                          "format": "float"
                        },
                        "fees": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "label": {
                                "type": "string"
                              },
                              "value": {
                                "type": "number",
                                "format": "float"
                              },
                              "display": {
                                "type": "string"
                              }
                            }
                          }
                        },
                        "subTotal": {
                          "type": "number",
                          "format": "float"
                        },
                        "totalTaxes": {
                          "type": "number",
                          "format": "float"
                        },
                        "taxes": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "name": {
                                "type": "string"
                              },
                              "total": {
                                "type": "number",
                                "format": "float"
                              }
                            }
                          }
                        },
                        "total": {
                          "type": "number",
                          "format": "float"
                        },
                        "grandTotal": {
                          "type": "number",
                          "format": "float"
                        },
                        "payments": {
                          "type": "number",
                          "format": "float"
                        },
                        "transfers": {
                          "type": "number",
                          "format": "float"
                        },
                        "insurance": {
                          "type": "number",
                          "format": "float"
                        },
                        "balance": {
                          "type": "number",
                          "format": "float"
                        }
                      }
                    },
                    "contactId": {
                      "type": "integer"
                    },
                    "channelId": {
                      "type": "integer",
                      "nullable": true
                    },
                    "channel": {
                      "type": "string",
                      "nullable": true
                    },
                    "folioId": {
                      "type": "integer"
                    },
                    "guaranteePolicyId": {
                      "type": "integer",
                      "nullable": true,
                      "description": "if an approved and active policy, otherwise defaults to automated selection of guarantee policy"
                    },
                    "subChannel": {
                      "type": "string",
                      "nullable": true,
                      "description": "Subchannel where the reservation came from"
                    },
                    "cancellationPolicyId": {
                      "type": "integer"
                    },
                    "cancellationReasonId": {
                      "type": "integer"
                    },
                    "userId": {
                      "type": "integer",
                      "nullable": true
                    },
                    "user": {
                      "type": "string",
                      "nullable": true
                    },
                    "travelAgentId": {
                      "type": "integer",
                      "nullable": true
                    },
                    "travelAgent": {
                      "type": "string",
                      "nullable": true
                    },
                    "campaignId": {
                      "type": "integer",
                      "nullable": true
                    },
                    "campaign": {
                      "type": "string",
                      "nullable": true
                    },
                    "typeId": {
                      "type": "integer"
                    },
                    "typeInline": {
                      "deprecated": true,
                      "type": "object",
                      "properties": {
                        "id": {
                          "type": "integer"
                        },
                        "name": {
                          "type": "string"
                        },
                        "code": {
                          "type": "string"
                        }
                      }
                    },
                    "rateTypeId": {
                      "type": "integer"
                    },
                    "unitCodeId": {
                      "type": "integer",
                      "nullable": true
                    },
                    "cancelledById": {
                      "type": "integer",
                      "nullable": true
                    },
                    "cancelledBy": {
                      "type": "string",
                      "nullable": true
                    },
                    "paymentMethodId": {
                      "type": "integer",
                      "nullable": true
                    },
                    "holdExpiration": {
                      "type": "string",
                      "format": "date-time",
                      "description": "Date time in ISO 8601 format"
                    },
                    "isTaxable": {
                      "type": "boolean"
                    },
                    "inviteUuid": {
                      "type": "string",
                      "nullable": true
                    },
                    "uuid": {
                      "type": "string"
                    },
                    "source": {
                      "type": "string"
                    },
                    "agreementStatus": {
                      "type": "string"
                    },
                    "automatePayment": {
                      "type": "boolean"
                    },
                    "promoCodeId": {
                      "type": "integer",
                      "nullable": true,
                      "description": "promotional code ID AKA coupon code ID"
                    },
                    "promoCode": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 16,
                      "nullable": true,
                      "description": "promotional code AKA coupon code"
                    },
                    "updatedBy": {
                      "type": "string"
                    },
                    "createdBy": {
                      "type": "string"
                    },
                    "updatedAt": {
                      "type": "string",
                      "format": "date-time",
                      "description": "Date time in ISO 8601 format"
                    },
                    "createdAt": {
                      "type": "string",
                      "format": "date-time",
                      "description": "Date time in ISO 8601 format"
                    },
                    "_embedded": {
                      "type": "object",
                      "properties": {
                        "contact": {
                          "type": "object",
                          "properties": {
                            "firstName": {
                              "type": "string",
                              "description": "First Name",
                              "maxLength": 32
                            },
                            "lastName": {
                              "type": "string",
                              "description": "Last Name",
                              "maxLength": 32
                            },
                            "name": {
                              "type": "string",
                              "description": "Full Name",
                              "maxLength": 64
                            },
                            "primaryEmail": {
                              "type": "string",
                              "format": "email",
                              "description": "Primary email assigned to contact. Must be unique from primary and secondary email addresses.",
                              "maxLength": 100
                            },
                            "secondaryEmail": {
                              "type": "string",
                              "nullable": true,
                              "format": "email",
                              "description": "Alternative or secondary email assigned to contact. Must be unique from primary and secondary email addresses.",
                              "maxLength": 100
                            },
                            "homePhone": {
                              "type": "string",
                              "nullable": true,
                              "description": "Use E.164 Format, non complaint numbers will be processed within US locale.",
                              "maxLength": 16
                            },
                            "cellPhone": {
                              "type": "string",
                              "nullable": true,
                              "description": "Use E.164 Format, non complaint numbers will be processed within US locale.",
                              "maxLength": 16
                            },
                            "workPhone": {
                              "type": "string",
                              "nullable": true,
                              "description": "Use E.164 Format, non complaint numbers will be processed within US locale.",
                              "maxLength": 16
                            },
                            "otherPhone": {
                              "type": "string",
                              "nullable": true,
                              "description": "Use E.164 Format, non complaint numbers will be processed within US locale.",
                              "maxLength": 16
                            },
                            "fax": {
                              "type": "string",
                              "nullable": true,
                              "description": "Use E.164 Format, non complaint numbers will be processed within US locale.",
                              "maxLength": 16
                            },
                            "streetAddress": {
                              "type": "string",
                              "nullable": true,
                              "maxLength": 255
                            },
                            "extendedAddress": {
                              "type": "string",
                              "nullable": true,
                              "maxLength": 255
                            },
                            "locality": {
                              "type": "string",
                              "nullable": true
                            },
                            "region": {
                              "type": "string",
                              "nullable": true
                            },
                            "postalCode": {
                              "type": "string",
                              "nullable": true,
                              "maxLength": 16
                            },
                            "country": {
                              "type": "string",
                              "example": "US",
                              "minLength": 2,
                              "maxLength": 2,
                              "description": "ISO 2 Character Country Code"
                            },
                            "notes": {
                              "type": "string",
                              "nullable": true,
                              "maxLength": 4000
                            },
                            "anniversary": {
                              "type": "string",
                              "nullable": true,
                              "pattern": "^(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|30|31)$"
                            },
                            "birthdate": {
                              "type": "string",
                              "nullable": true,
                              "pattern": "^(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|30|31)$"
                            },
                            "noIdentity": {
                              "type": "boolean",
                              "nullable": true
                            },
                            "isVip": {
                              "type": "boolean",
                              "nullable": true
                            },
                            "isBlacklist": {
                              "type": "boolean",
                              "nullable": true
                            },
                            "tags": {
                              "type": "array",
                              "items": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "number"
                                  }
                                }
                              }
                            },
                            "references": {
                              "type": "array",
                              "items": {
                                "type": "object",
                                "properties": {
                                  "reference": {
                                    "type": "string"
                                  },
                                  "salesLinkId": {
                                    "type": "integer",
                                    "nullable": true
                                  },
                                  "channelId": {
                                    "type": "integer",
                                    "nullable": true
                                  }
                                }
                              }
                            },
                            "custom": {
                              "type": "object",
                              "description": "Keys are determinied by customer. Values are either string or array depending on type",
                              "properties": {
                                "custom_n": {
                                  "oneOf": [
                                    {
                                      "type": "string"
                                    },
                                    {
                                      "type": "array"
                                    }
                                  ],
                                  "items": {}
                                }
                              }
                            },
                            "updatedBy": {
                              "type": "string"
                            },
                            "createdBy": {
                              "type": "string"
                            },
                            "updatedAt": {
                              "type": "string",
                              "format": "date-time",
                              "description": "Date time in ISO 8601 format"
                            },
                            "createdAt": {
                              "type": "string",
                              "format": "date-time",
                              "description": "Date time in ISO 8601 format"
                            },
                            "isOwnerContact": {
                              "type": "boolean"
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
                          }
                        },
                        "folio": {
                          "type": "object",
                          "properties": {
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
                                "logs": {
                                  "type": "object",
                                  "properties": {
                                    "href": {
                                      "type": "string"
                                    }
                                  }
                                }
                              }
                            },
                            "id": {
                              "type": "integer",
                              "minimum": 1
                            },
                            "type": {
                              "type": "string",
                              "enum": [
                                "guest",
                                "master"
                              ]
                            },
                            "status": {
                              "type": "string",
                              "enum": [
                                "open",
                                "closed"
                              ]
                            },
                            "contactId": {
                              "type": "integer",
                              "description": "Id of the guest",
                              "minimum": 1
                            },
                            "companyId": {
                              "type": "integer",
                              "description": "Id of the company",
                              "nullable": true,
                              "minimum": 1
                            },
                            "company": {
                              "type": "object",
                              "description": "Company",
                              "nullable": true
                            },
                            "taxExempt": {
                              "type": "boolean",
                              "description": "Flag that indicates if the tax exempted for the folio"
                            },
                            "startDate": {
                              "type": "string",
                              "format": "date",
                              "description": "Date when the folio starts, in ISO-8601 format"
                            },
                            "endDate": {
                              "type": "string",
                              "format": "date",
                              "description": "Date when the folio ends, in ISO-8601 format"
                            },
                            "closedDate": {
                              "type": "string",
                              "format": "date",
                              "nullable": true,
                              "description": "Date when the folio got closed, in ISO-8601 format"
                            },
                            "realizedBalance": {
                              "type": "number"
                            },
                            "currentBalance": {
                              "type": "number"
                            },
                            "createdBy": {
                              "type": "string"
                            },
                            "createdAt": {
                              "type": "string",
                              "format": "date-time",
                              "description": "Date as ISO 8601 format"
                            },
                            "updatedBy": {
                              "type": "string"
                            },
                            "updatedAt": {
                              "type": "string",
                              "format": "date-time",
                              "description": "Date as ISO 8601 format"
                            },
                            "name": {
                              "type": "string",
                              "description": "Name, visible for certain folio types only"
                            },
                            "reservationId": {
                              "type": "integer",
                              "description": "Id of the relevant reservation, visible for certain folio types only",
                              "minimum": 1
                            },
                            "travelAgentId": {
                              "type": "integer",
                              "nullable": true,
                              "description": "Id of the travel agent, visible for certain folio types only",
                              "minimum": 1
                            },
                            "travelAgent": {
                              "type": "object",
                              "nullable": true,
                              "description": "Travel agent"
                            },
                            "hasException": {
                              "type": "boolean",
                              "description": "Flag that indicates if the folio has an exception, visible for certain folio types only"
                            },
                            "exceptionMessage": {
                              "type": "string",
                              "nullable": true,
                              "description": "Exception message if exists, visible for certain folio types only"
                            },
                            "checkInDate": {
                              "type": "string",
                              "format": "date",
                              "nullable": true,
                              "description": "Date in ISO-8601 format, visible for certain folio types only"
                            },
                            "checkOutDate": {
                              "type": "string",
                              "format": "date",
                              "nullable": true,
                              "description": "Date in ISO-8601 format, visible for certain folio types only"
                            },
                            "ownerRevenue": {
                              "type": "number",
                              "description": "Owner revenue, visible for certain folio types only"
                            },
                            "ownerCommission": {
                              "type": "number",
                              "description": "Owner commission, visible for certain folio types only"
                            },
                            "agentCommission": {
                              "type": "number",
                              "description": "Travel agent commission, visible for certain folio types only"
                            },
                            "masterFolioId": {
                              "type": "integer",
                              "nullable": true,
                              "description": "Id of the relevant master folio if exists, visible for certain folio types only",
                              "minimum": 1
                            },
                            "masterFolio": {
                              "type": "object",
                              "nullable": true,
                              "description": "master folio",
                              "minimum": 1
                            },
                            "masterFolioRuleId": {
                              "type": "integer",
                              "nullable": true,
                              "description": "Id of the relevant master folio rule mapping if exists, visible for certain folio types only",
                              "minimum": 1
                            },
                            "masterFolioRule": {
                              "type": "object",
                              "nullable": true,
                              "description": "folio rule"
                            },
                            "_embedded": {
                              "type": "object",
                              "properties": {
                                "contact": {
                                  "type": "object",
                                  "properties": {
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
                                  }
                                },
                                "reservation": {
                                  "type": "object",
                                  "properties": {
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
                                        "logs": {
                                          "type": "object",
                                          "properties": {
                                            "href": {
                                              "type": "string"
                                            }
                                          }
                                        },
                                        "notes": {
                                          "type": "object",
                                          "properties": {
                                            "href": {
                                              "type": "string"
                                            }
                                          }
                                        },
                                        "fees": {
                                          "type": "object",
                                          "properties": {
                                            "href": {
                                              "type": "string"
                                            }
                                          }
                                        },
                                        "cancel": {
                                          "type": "object",
                                          "properties": {
                                            "href": {
                                              "type": "string"
                                            }
                                          }
                                        },
                                        "tags": {
                                          "type": "object",
                                          "properties": {
                                            "href": {
                                              "type": "string"
                                            }
                                          }
                                        },
                                        "rates": {
                                          "type": "object",
                                          "properties": {
                                            "href": {
                                              "type": "string"
                                            }
                                          }
                                        },
                                        "discount": {
                                          "type": "object",
                                          "properties": {
                                            "href": {
                                              "type": "string"
                                            }
                                          }
                                        }
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        },
                        "unit": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "integer",
                              "description": "ID of the unit"
                            },
                            "name": {
                              "type": "string",
                              "description": "Name"
                            },
                            "longitude": {
                              "type": "number",
                              "description": "Location longitude"
                            },
                            "latitude": {
                              "type": "number",
                              "description": "Location latitude"
                            },
                            "isActive": {
                              "type": "boolean",
                              "description": "Unit is active"
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
                          }
                        },
                        "cancellationReason": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "integer",
                              "description": "ID of the unit"
                            },
                            "name": {
                              "type": "string",
                              "description": "Name"
                            },
                            "isActive": {
                              "type": "boolean",
                              "description": "Unit is active"
                            },
                            "handle": {
                              "type": "string",
                              "description": "Handle"
                            },
                            "cancelledByGuest": {
                              "type": "boolean",
                              "description": "Was Canceled By Guest"
                            },
                            "airbnbType": {
                              "type": "integer",
                              "nullable": true,
                              "description": "Airbnb Type ID"
                            },
                            "updatedBy": {
                              "type": "string"
                            },
                            "createdBy": {
                              "type": "string"
                            },
                            "updatedAt": {
                              "type": "string",
                              "format": "date-time",
                              "description": "Date time in ISO 8601 format"
                            },
                            "createdAt": {
                              "type": "string",
                              "nullable": true,
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
                          }
                        },
                        "unitType": {
                          "type": "object",
                          "properties": {
                            "unitType": {
                              "title": "Unit Type Response",
                              "type": "object",
                              "description": "Unit Type Response",
                              "properties": {
                                "id": {
                                  "type": "integer"
                                },
                                "isActive": {
                                  "type": "boolean"
                                },
                                "roles": {
                                  "type": "array",
                                  "description": "Default roles when this unit type is used. Inherits to unit."
                                },
                                "bedTypes": {
                                  "type": "array",
                                  "description": "Specify what bed types are available in this unit type. Inherits to unit."
                                },
                                "custom": {
                                  "type": "object",
                                  "description": "Lists out the custom fields applied to unit types, and their current value on this specific type."
                                },
                                "updated": {
                                  "type": "object",
                                  "description": "Specifies when each part of the type was updated in ISO 8601 dateTime format.",
                                  "properties": {
                                    "availability": {
                                      "type": "string"
                                    },
                                    "content": {
                                      "type": "string"
                                    },
                                    "pricing": {
                                      "type": "string"
                                    }
                                  }
                                },
                                "createdAt": {
                                  "type": "string",
                                  "description": "DateTime that this was created, in ISO 8601 dateTime format."
                                },
                                "createdBy": {
                                  "type": "string"
                                },
                                "updatedAt": {
                                  "type": "string",
                                  "description": "DateTime that this was updated, in ISO 8601 dateTime format."
                                },
                                "updatedBy": {
                                  "type": "string"
                                },
                                "name": {
                                  "type": "string"
                                },
                                "shortName": {
                                  "type": "string"
                                },
                                "typeCode": {
                                  "type": "string"
                                },
                                "maxPets": {
                                  "type": "integer"
                                },
                                "minimumAgeLimit": {
                                  "type": "integer"
                                },
                                "phone": {
                                  "type": "string"
                                },
                                "streetAddress": {
                                  "type": "string"
                                },
                                "extendedAddress": {
                                  "type": "string"
                                },
                                "locality": {
                                  "type": "string"
                                },
                                "region": {
                                  "type": "string"
                                },
                                "postal": {
                                  "type": "string"
                                },
                                "country": {
                                  "type": "string"
                                },
                                "maxDiscount": {
                                  "type": "string",
                                  "description": "Should be a percentage number value."
                                },
                                "area": {
                                  "type": "string",
                                  "description": "area of the unit in sq. ft."
                                },
                                "websiteUrl": {
                                  "type": "string"
                                },
                                "floors": {
                                  "type": "integer",
                                  "description": "Number of floors / level in unit type."
                                },
                                "maxOccupancy": {
                                  "type": "integer"
                                },
                                "bedrooms": {
                                  "type": "integer"
                                },
                                "fullBathrooms": {
                                  "type": "integer"
                                },
                                "threeQuarterBathroom": {
                                  "type": "integer"
                                },
                                "halfBathrooms": {
                                  "type": "integer"
                                },
                                "timezone": {
                                  "type": "string",
                                  "description": "timezone string."
                                },
                                "longitude": {
                                  "type": "string",
                                  "description": "longitude in coordinate format."
                                },
                                "latitude": {
                                  "type": "string",
                                  "description": "longitude in coordinate format."
                                },
                                "maintenanceMessage": {
                                  "type": "string"
                                },
                                "housekeepingMessage": {
                                  "type": "string"
                                },
                                "housekeepingNotes": {
                                  "type": "string"
                                },
                                "oversellLimit": {
                                  "type": "integer"
                                },
                                "securityDeposit": {
                                  "type": "string",
                                  "description": "should be a decimal number value."
                                },
                                "petFriendly": {
                                  "type": "boolean"
                                },
                                "smokingAllowed": {
                                  "type": "boolean"
                                },
                                "childrenAllowed": {
                                  "type": "boolean"
                                },
                                "eventsAllowed": {
                                  "type": "boolean"
                                },
                                "isAccessible": {
                                  "type": "boolean"
                                },
                                "hasEarlyCheckin": {
                                  "type": "boolean"
                                },
                                "hasLateCheckout": {
                                  "type": "boolean"
                                },
                                "quickCheckin": {
                                  "type": "boolean"
                                },
                                "quickCheckout": {
                                  "type": "boolean"
                                },
                                "useRoomConfiguration": {
                                  "type": "boolean"
                                },
                                "isBookable": {
                                  "type": "boolean"
                                },
                                "allowUnitRates": {
                                  "type": "boolean"
                                },
                                "allowOversell": {
                                  "type": "boolean"
                                },
                                "folioException": {
                                  "type": "boolean"
                                },
                                "checkinTime": {
                                  "type": "string"
                                },
                                "checkoutTime": {
                                  "type": "string"
                                },
                                "earlyCheckinTime": {
                                  "type": "string"
                                },
                                "lateCheckoutTime": {
                                  "type": "string"
                                },
                                "nodeId": {
                                  "type": "integer"
                                },
                                "lodgingTypeId": {
                                  "type": "integer"
                                },
                                "calendarGroupId": {
                                  "type": "integer"
                                },
                                "housekeepingZoneId": {
                                  "type": "integer"
                                },
                                "maintenanceZoneId": {
                                  "type": "integer"
                                },
                                "travelInsuranceProductId": {
                                  "type": "integer"
                                },
                                "localOfficeId": {
                                  "type": "integer"
                                },
                                "taxDistrictId": {
                                  "type": "integer"
                                },
                                "taxId": {
                                  "type": "integer"
                                },
                                "cancellationPoliciesIds": {
                                  "type": "array",
                                  "items": {
                                    "type": "integer"
                                  }
                                },
                                "guaranteePoliciesIds": {
                                  "type": "array",
                                  "items": {
                                    "type": "integer"
                                  }
                                },
                                "documentsIds": {
                                  "type": "array",
                                  "items": {
                                    "type": "integer"
                                  }
                                },
                                "gatewaysIds": {
                                  "type": "array",
                                  "items": {
                                    "type": "integer"
                                  }
                                },
                                "amenitiesIds": {
                                  "type": "array",
                                  "items": {
                                    "type": "integer"
                                  }
                                },
                                "_embedded": {
                                  "type": "object",
                                  "properties": {
                                    "lodgingType": {
                                      "title": "Lodging Types Response",
                                      "type": "object",
                                      "description": "Bed types entity model",
                                      "properties": {
                                        "id": {
                                          "type": "number"
                                        },
                                        "name": {
                                          "type": "string"
                                        },
                                        "code": {
                                          "type": "string",
                                          "description": "Abbreviation / Code for this lodging type"
                                        },
                                        "airbnbTypeCategory": {
                                          "type": "string",
                                          "enum": [
                                            "aparthotel",
                                            "apartment",
                                            "barn",
                                            "bnb",
                                            "boat",
                                            "boutique_hotel",
                                            "bungalow",
                                            "cabin",
                                            "campsite",
                                            "castle",
                                            "cave",
                                            "chalet",
                                            "condominium",
                                            "cottage",
                                            "dome_house",
                                            "earthhouse",
                                            "farm_stay",
                                            "guest_suite",
                                            "guesthouse",
                                            "hostel",
                                            "hotel",
                                            "house",
                                            "houseboat",
                                            "hut",
                                            "igloo",
                                            "island",
                                            "lighthouse",
                                            "lodge",
                                            "loft",
                                            "plane",
                                            "resort",
                                            "rv",
                                            "serviced_apartment",
                                            "tent",
                                            "tiny_house",
                                            "tipi",
                                            "townhouse",
                                            "train",
                                            "treehouse",
                                            "villa",
                                            "windmill",
                                            "yurt"
                                          ],
                                          "description": "Required if the bed type will be published to airbnb."
                                        },
                                        "airbnbTypeGroup": {
                                          "type": "string",
                                          "enum": [
                                            "apartments",
                                            "bnb",
                                            "boutique_hotels_and_more",
                                            "houses",
                                            "secondary_units",
                                            "unique_homes"
                                          ],
                                          "description": "Required if the bed type will be published to airbnb."
                                        },
                                        "airbnbRoomType": {
                                          "type": "string",
                                          "enum": [
                                            "private_room",
                                            "shared_room",
                                            "hotel_room",
                                            "entire_home"
                                          ],
                                          "description": "Required for Airbnb. Note that only certain room types will be compatible with airbnb type categories."
                                        },
                                        "homeawayType": {
                                          "type": "string",
                                          "description": "Required if bed type is published to Homeaway/VRBO",
                                          "enum": [
                                            "PROPERTY_TYPE_APARTMENT",
                                            "PROPERTY_TYPE_BARN",
                                            "PROPERTY_TYPE_BED_AND_BREAKFAST",
                                            "PROPERTY_TYPE_BOAT",
                                            "PROPERTY_TYPE_BUILDING",
                                            "PROPERTY_TYPE_BUNGALOW",
                                            "PROPERTY_TYPE_CABIN",
                                            "PROPERTY_TYPE_CAMPGROUND",
                                            "PROPERTY_TYPE_CARAVAN",
                                            "PROPERTY_TYPE_CASTLE",
                                            "PROPERTY_TYPE_CHACARA",
                                            "PROPERTY_TYPE_CHALET",
                                            "PROPERTY_TYPE_CHATEAU",
                                            "PROPERTY_TYPE_CONDO",
                                            "PROPERTY_TYPE_CORPORATE_APARTMENT",
                                            "PROPERTY_TYPE_COTTAGE",
                                            "PROPERTY_TYPE_ESTATE",
                                            "PROPERTY_TYPE_FARMHOUSE",
                                            "PROPERTY_TYPE_GUESTHOUSE",
                                            "PROPERTY_TYPE_HOSTEL",
                                            "PROPERTY_TYPE_HOTEL",
                                            "PROPERTY_TYPE_HOUSE",
                                            "PROPERTY_TYPE_HOUSE_BOAT",
                                            "PROPERTY_TYPE_LODGE",
                                            "PROPERTY_TYPE_MAS",
                                            "PROPERTY_TYPE_MILL",
                                            "PROPERTY_TYPE_MOBILE_HOME",
                                            "PROPERTY_TYPE_RECREATIONAL_VEHICLE",
                                            "PROPERTY_TYPE_RESORT",
                                            "PROPERTY_TYPE_RIAD",
                                            "PROPERTY_TYPE_STUDIO",
                                            "PROPERTY_TYPE_SUITES",
                                            "PROPERTY_TYPE_TOWER",
                                            "PROPERTY_TYPE_TOWNHOME",
                                            "PROPERTY_TYPE_VILLA",
                                            "PROPERTY_TYPE_YACHT"
                                          ]
                                        },
                                        "tripadvisorType": {
                                          "type": "string",
                                          "enum": [
                                            "APARTMENT",
                                            "B_AND_B",
                                            "BARN",
                                            "BEACH_HUT",
                                            "BOATHOUSE",
                                            "BUNGALOW",
                                            "CAMPER_VAN",
                                            "CARAVAN_MOBILE_HOME",
                                            "CASTLE",
                                            "CAVE_HOUSE",
                                            "CHALET",
                                            "CHATEAU",
                                            "CONDO",
                                            "CONVERTED_CHAPEL",
                                            "COTTAGE",
                                            "FARMHOUSE",
                                            "FINCA",
                                            "FORT",
                                            "GITE",
                                            "GUEST_HOUSE",
                                            "HOTEL_APARTMENT",
                                            "HOUSE",
                                            "HOUSEBOAT",
                                            "LIGHT_HOUSE",
                                            "LODGE",
                                            "LOG_CABIN",
                                            "MANOR_HOUSE",
                                            "NARROWBOAT",
                                            "PENT_HOUSE",
                                            "ROOM",
                                            "RIAD",
                                            "SHEPHERDS_HUT",
                                            "SKI_CHALET",
                                            "STUDIO",
                                            "TENTED_CAMP",
                                            "TIPI_TEEPEE",
                                            "TOWER",
                                            "TOWNHOUSE",
                                            "TREE_HOUSE",
                                            "TRULLO",
                                            "VILLA",
                                            "WATERMILL",
                                            "WINDMILL",
                                            "YACHT",
                                            "YURT"
                                          ],
                                          "description": "Required if bed type is published to Tripadvisor."
                                        },
                                        "marriottTypeGroup": {
                                          "type": "string",
                                          "enum": [
                                            "house",
                                            "apt",
                                            "condo",
                                            "loft",
                                            "bungalow",
                                            "cottage",
                                            "cabin",
                                            "townhouse"
                                          ]
                                        },
                                        "isFilterable": {
                                          "type": "boolean"
                                        },
                                        "isActive": {
                                          "type": "boolean"
                                        },
                                        "createdBy": {
                                          "type": "string"
                                        },
                                        "createdAt": {
                                          "type": "string",
                                          "format": "date-time",
                                          "description": "Date as ISO 8601 format"
                                        },
                                        "updatedBy": {
                                          "type": "string"
                                        },
                                        "updatedAt": {
                                          "type": "string",
                                          "format": "date-time",
                                          "description": "Date as ISO 8601 format"
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
                                        "airbnbType",
                                        "isFilterable",
                                        "isActive",
                                        "name",
                                        "createdBy",
                                        "createdAt",
                                        "updatedBy",
                                        "updatedAt"
                                      ]
                                    },
                                    "node": {
                                      "title": "Nodes Response",
                                      "type": "object",
                                      "properties": {
                                        "id": {
                                          "type": "integer",
                                          "description": "ID"
                                        },
                                        "name": {
                                          "type": "string",
                                          "description": "Name of Node Type"
                                        },
                                        "maxPets": {
                                          "type": "integer"
                                        },
                                        "phone": {
                                          "type": "string"
                                        },
                                        "websiteUrl": {
                                          "type": "string"
                                        },
                                        "streetAddress": {
                                          "type": "string"
                                        },
                                        "extendedAddress": {
                                          "type": "string"
                                        },
                                        "locality": {
                                          "type": "string"
                                        },
                                        "region": {
                                          "type": "string"
                                        },
                                        "postal": {
                                          "type": "string"
                                        },
                                        "country": {
                                          "type": "string"
                                        },
                                        "maxDiscount": {
                                          "type": "number"
                                        },
                                        "timezone": {
                                          "type": "string"
                                        },
                                        "longitude": {
                                          "type": "number"
                                        },
                                        "latitude": {
                                          "type": "number"
                                        },
                                        "housekeepingNotes": {
                                          "type": "string"
                                        },
                                        "petFriendly": {
                                          "type": "boolean"
                                        },
                                        "smokingAllowed": {
                                          "type": "boolean"
                                        },
                                        "childrenAllowed": {
                                          "type": "boolean"
                                        },
                                        "eventsAllowed": {
                                          "type": "boolean"
                                        },
                                        "isAccessible": {
                                          "type": "boolean"
                                        },
                                        "hasEarlyCheckin": {
                                          "type": "boolean"
                                        },
                                        "hasLateCheckout": {
                                          "type": "boolean"
                                        },
                                        "quickCheckin": {
                                          "type": "boolean"
                                        },
                                        "quickCheckout": {
                                          "type": "boolean"
                                        },
                                        "checkinTime": {
                                          "type": "string",
                                          "format": "date-time",
                                          "description": "Date time in ISO 8601 format"
                                        },
                                        "checkoutTime": {
                                          "type": "string",
                                          "format": "date-time",
                                          "description": "Date time in ISO 8601 format"
                                        },
                                        "earlyCheckinTime": {
                                          "type": "string",
                                          "format": "date-time",
                                          "description": "Date time in ISO 8601 format"
                                        },
                                        "lateCheckoutTime": {
                                          "type": "string",
                                          "format": "date-time",
                                          "description": "Date time in ISO 8601 format"
                                        },
                                        "description": {
                                          "type": "string",
                                          "nullable": true,
                                          "description": "Description for Node Type."
                                        },
                                        "shortDescription": {
                                          "type": "string"
                                        },
                                        "longDescription": {
                                          "type": "string"
                                        },
                                        "directions": {
                                          "type": "string"
                                        },
                                        "checkinDetails": {
                                          "type": "string"
                                        },
                                        "houseRules": {
                                          "type": "string"
                                        },
                                        "parentId": {
                                          "type": "integer",
                                          "description": "required if not top node (#1)"
                                        },
                                        "typeId": {
                                          "type": "integer"
                                        },
                                        "taxDistrictId": {
                                          "type": "integer"
                                        },
                                        "checkinOfficeId": {
                                          "type": "integer"
                                        },
                                        "cancellationPolicyId": {
                                          "type": "integer"
                                        },
                                        "housekeepingZoneId": {
                                          "type": "integer"
                                        },
                                        "maintenanceZoneId": {
                                          "type": "integer"
                                        },
                                        "isReservations": {
                                          "type": "boolean",
                                          "nullable": true
                                        },
                                        "isHousekeeping": {
                                          "type": "boolean",
                                          "nullable": true
                                        },
                                        "isMaintenance": {
                                          "type": "boolean",
                                          "nullable": true
                                        },
                                        "isOnline": {
                                          "type": "boolean",
                                          "nullable": true
                                        },
                                        "isOwners": {
                                          "type": "boolean",
                                          "nullable": true
                                        },
                                        "isActive": {
                                          "type": "boolean",
                                          "nullable": true
                                        },
                                        "roles": {
                                          "type": "array",
                                          "nullable": true,
                                          "items": {
                                            "type": "object",
                                            "properties": {
                                              "roleId": {
                                                "type": "integer"
                                              },
                                              "userId": {
                                                "type": "integer"
                                              }
                                            }
                                          }
                                        },
                                        "custom": {
                                          "type": "object",
                                          "description": "custom per install `pms_nodes_*`"
                                        },
                                        "guaranteePoliciesIds": {
                                          "type": "array"
                                        },
                                        "amenitiesIds": {
                                          "type": "array"
                                        },
                                        "documentsIds": {
                                          "type": "array"
                                        },
                                        "gatewaysIds": {
                                          "type": "array"
                                        }
                                      }
                                    },
                                    "localOffice": {
                                      "title": "local office Response",
                                      "type": "object",
                                      "properties": {
                                        "name": {
                                          "type": "string"
                                        },
                                        "directions": {
                                          "type": "string"
                                        },
                                        "email": {
                                          "type": "string"
                                        },
                                        "phone": {
                                          "type": "string",
                                          "description": "Street Address of unit."
                                        },
                                        "extendedAddress": {
                                          "type": "string",
                                          "nullable": true,
                                          "description": "Extended Address of unit."
                                        },
                                        "locality": {
                                          "type": "string",
                                          "description": "City/Locality of unit."
                                        },
                                        "region": {
                                          "type": "string",
                                          "description": "State/Region of unit."
                                        },
                                        "postalCode": {
                                          "type": "string",
                                          "description": "Postal Code of unit."
                                        },
                                        "country": {
                                          "type": "string",
                                          "example": "US",
                                          "minLength": 2,
                                          "maxLength": 2,
                                          "description": "ISO 2 Character Country Code"
                                        },
                                        "latitude": {
                                          "type": "number",
                                          "nullable": true,
                                          "format": "double",
                                          "description": "Latitude of unit."
                                        },
                                        "longitude": {
                                          "type": "number",
                                          "nullable": true,
                                          "format": "double",
                                          "description": "Longitude of unit."
                                        }
                                      }
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
                              }
                            }
                          }
                        },
                        "rateType": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "integer",
                              "description": "ID of the unit"
                            },
                            "type": {
                              "type": "string",
                              "description": "Name"
                            },
                            "code": {
                              "type": "string",
                              "description": "Name"
                            },
                            "name": {
                              "type": "string",
                              "description": "Name"
                            },
                            "isAllChannels": {
                              "type": "boolean",
                              "description": "Unit is active"
                            },
                            "channelId": {
                              "type": "array",
                              "items": {
                                "type": "integer"
                              },
                              "nullable": true,
                              "description": "Channel Ids"
                            },
                            "isActive": {
                              "type": "boolean",
                              "description": "Unit is active"
                            },
                            "updatedBy": {
                              "type": "string"
                            },
                            "createdBy": {
                              "type": "string"
                            },
                            "updatedAt": {
                              "type": "string",
                              "format": "date-time",
                              "description": "Date time in ISO 8601 format"
                            },
                            "createdAt": {
                              "type": "string",
                              "nullable": true,
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
                          }
                        },
                        "user": {
                          "title": "General User Object",
                          "type": "object",
                          "description": "used by server for multiple instances of user definition (user, createdBy)",
                          "properties": {
                            "id": {
                              "type": "integer"
                            },
                            "isActive": {
                              "type": "boolean"
                            },
                            "name": {
                              "type": "string"
                            },
                            "phone": {
                              "type": "string"
                            },
                            "email": {
                              "type": "string"
                            },
                            "username": {
                              "type": "string"
                            },
                            "roleId": {
                              "type": "integer"
                            },
                            "teamId": {
                              "nullable": true,
                              "type": "integer"
                            },
                            "vendorId": {
                              "nullable": true,
                              "type": "integer"
                            },
                            "assignable": {
                              "type": "array",
                              "items": {
                                "type": "string"
                              }
                            },
                            "createdAt": {
                              "type": "string",
                              "nullable": true,
                              "format": "date-time",
                              "description": "Date time in ISO 8601 format"
                            },
                            "createdBy": {
                              "type": "string"
                            },
                            "updatedAt": {
                              "type": "string",
                              "nullable": true,
                              "format": "date-time",
                              "description": "Date time in ISO 8601 format"
                            },
                            "updatedBy": {
                              "type": "string"
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
                          }
                        },
                        "canceledBy": {
                          "title": "General User Object",
                          "type": "object",
                          "description": "used by server for multiple instances of user definition (user, createdBy)",
                          "properties": {
                            "id": {
                              "type": "integer"
                            },
                            "isActive": {
                              "type": "boolean"
                            },
                            "name": {
                              "type": "string"
                            },
                            "phone": {
                              "type": "string"
                            },
                            "email": {
                              "type": "string"
                            },
                            "username": {
                              "type": "string"
                            },
                            "roleId": {
                              "type": "integer"
                            },
                            "teamId": {
                              "nullable": true,
                              "type": "integer"
                            },
                            "vendorId": {
                              "nullable": true,
                              "type": "integer"
                            },
                            "assignable": {
                              "type": "array",
                              "items": {
                                "type": "string"
                              }
                            },
                            "createdAt": {
                              "type": "string",
                              "nullable": true,
                              "format": "date-time",
                              "description": "Date time in ISO 8601 format"
                            },
                            "createdBy": {
                              "type": "string"
                            },
                            "updatedAt": {
                              "type": "string",
                              "nullable": true,
                              "format": "date-time",
                              "description": "Date time in ISO 8601 format"
                            },
                            "updatedBy": {
                              "type": "string"
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
                          }
                        },
                        "paymentMethod": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "integer",
                              "description": "ID of the unit"
                            },
                            "type": {
                              "type": "string",
                              "description": "Name"
                            },
                            "isDefault": {
                              "type": "boolean",
                              "description": "Default Payment Method"
                            },
                            "cardNumber": {
                              "type": "string",
                              "nullable": true,
                              "description": "Card Number",
                              "example": "4111111111111111"
                            },
                            "cardExpiration": {
                              "type": "string",
                              "nullable": true,
                              "pattern": "^(0|1)([0-9]{1})[-\\/]([0-9]{2,4})$",
                              "description": "Expiration Date as MM-YY or MM-YYYY"
                            },
                            "cardType": {
                              "type": "string",
                              "nullable": true,
                              "description": "Credit Card Type"
                            },
                            "routingNumber": {
                              "type": "string",
                              "example": "021000021",
                              "description": "Bank routing number - spreedly test example"
                            },
                            "accountNumber": {
                              "type": "string",
                              "example": "9876543210",
                              "description": "Bank routing number - spreedly test example"
                            },
                            "accountType": {
                              "type": "string",
                              "enum": [
                                "business-checking",
                                "business-savings",
                                "personal-checking",
                                "personal-savings"
                              ],
                              "example": "personal-checking",
                              "description": "Bank account type"
                            },
                            "name": {
                              "type": "string",
                              "example": "personal-checking",
                              "description": "Payment Method Name"
                            },
                            "isRedacted": {
                              "type": "boolean",
                              "description": "Payment Method is Redacted"
                            },
                            "isVirtual": {
                              "type": "boolean",
                              "description": "Payment Method is Virtual"
                            },
                            "effectiveDate": {
                              "type": "string",
                              "nullable": true,
                              "format": "date",
                              "description": "Date in ISO 8601 format"
                            },
                            "updatedBy": {
                              "type": "string"
                            },
                            "createdBy": {
                              "type": "string"
                            },
                            "updatedAt": {
                              "type": "string",
                              "format": "date-time",
                              "description": "Date time in ISO 8601 format"
                            },
                            "createdAt": {
                              "type": "string",
                              "nullable": true,
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
                          }
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
                        "logs": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          }
                        },
                        "notes": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          }
                        },
                        "fees": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          }
                        },
                        "cancel": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          }
                        },
                        "tags": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          }
                        },
                        "rates": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          }
                        },
                        "discount": {
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
                    "id"
                  ],
                  "x-readme-ref-name": "ReservationSchemaResponse"
                },
                "examples": {
                  "Example Response": {
                    "value": {
                      "id": 1,
                      "altConf": "null or string with alternate confirmation number",
                      "unitId": 6,
                      "arrivalDate": "2019-11-25",
                      "departureDate": "2019-11-28",
                      "earlyArrival": false,
                      "lateDeparture": false,
                      "arrivalTime": "2019-11-25T23:00:00+00:00",
                      "departureTime": "2019-11-28T17:00:00+00:00",
                      "nights": 3,
                      "status": "Checked Out",
                      "cancelledAt": null,
                      "occupants": {
                        "1": 7,
                        "2": 0
                      },
                      "requiredSecurityDeposit": 0,
                      "remainingSecurityDeposit": 0,
                      "quoteBreakdown": {
                        "currency": "USD",
                        "totalRent": 1627,
                        "adr": 363.36,
                        "discount": -536.91,
                        "rates": [
                          {
                            "date": "2019-11-25",
                            "rate": 466,
                            "nights": 1
                          },
                          {
                            "date": "2019-11-26",
                            "rate": 534,
                            "nights": 1
                          },
                          {
                            "date": "2019-11-27",
                            "rate": 627,
                            "nights": 1
                          }
                        ],
                        "extraRates": [],
                        "totalFees": 306.76,
                        "fees": [
                          {
                            "label": "Check Out Clean",
                            "value": 185,
                            "display": "itemize"
                          },
                          {
                            "label": "KNC Fee",
                            "value": 5.45,
                            "display": "taxes"
                          },
                          {
                            "label": "Sandbox Booking Fee",
                            "value": 76.31,
                            "display": "itemize"
                          },
                          {
                            "label": "Damage Fee",
                            "value": 60,
                            "display": "itemize"
                          },
                          {
                            "label": "Cleaning Fee - Guest Check Out Clean",
                            "value": 10,
                            "display": "itemize"
                          },
                          {
                            "label": "Damage Fee",
                            "value": -30,
                            "display": "itemize"
                          }
                        ],
                        "subTotal": 1396.85,
                        "totalTaxes": 69.49,
                        "taxes": [
                          {
                            "name": "WI State Sales Tax - 2.9%",
                            "total": 31.61
                          },
                          {
                            "name": "Sandbox County Sales Tax - 3.475%",
                            "total": 37.88
                          }
                        ],
                        "total": 1466.34,
                        "insurance": 103.3,
                        "grandTotal": 1569.64,
                        "payments": 179.61,
                        "balance": 1390.03
                      },
                      "folioBreakdown": {
                        "currency": "USD",
                        "totalRent": 0,
                        "adr": 0,
                        "rates": [],
                        "totalFees": 0,
                        "totalCharges": 0,
                        "fees": [
                          {
                            "label": "Cancellation Charge",
                            "total": 10
                          }
                        ],
                        "subTotal": 10,
                        "totalTaxes": 1.4,
                        "taxes": [
                          {
                            "name": "Georgia Sales Tax -Chatham County",
                            "total": 0.7
                          },
                          {
                            "name": "Tybee Hotel Tax",
                            "total": 0.7
                          }
                        ],
                        "total": 11.39,
                        "grandTotal": 11.39,
                        "payments": 0,
                        "transfers": 0,
                        "insurance": 0,
                        "balance": 0
                      },
                      "contactId": 41151,
                      "channelId": null,
                      "channel": null,
                      "folioId": 118,
                      "guaranteePolicyId": 8,
                      "subChannel": "unknown, Google, Booking, Online, other - this is a string",
                      "cancellationPolicyId": 16,
                      "cancellationReasonId": 1,
                      "userId": null,
                      "user": null,
                      "travelAgentId": null,
                      "travelAgent": null,
                      "campaignId": 1,
                      "campaign": null,
                      "typeId": 1,
                      "typeInline": {
                        "deprecated": true,
                        "id": 1,
                        "name": "Guest Direct",
                        "code": "G"
                      },
                      "rateTypeId": 1,
                      "unitCodeId": null,
                      "cancelledById": null,
                      "cancelledBy": null,
                      "paymentMethodId": 37,
                      "holdExpiration": "2020-09-30T13:41:20+00:00",
                      "isTaxable": true,
                      "inviteUuid": null,
                      "uuid": "5cec40da-7874-4df0-bf9f-9fe42111a638",
                      "source": "channel",
                      "agreementStatus": "not-sent",
                      "automatePayment": true,
                      "promoCodeId": null,
                      "promoCode": null,
                      "updatedBy": "system",
                      "createdBy": "system",
                      "updatedAt": "2019-11-26T22:09:06+00:00",
                      "createdAt": "2019-09-11T03:40:52+00:00",
                      "_embedded": {
                        "unit": {
                          "id": 1544,
                          "name": "Beach Racquet A126",
                          "longitude": -80.858145,
                          "latitude": 32.022724,
                          "isActive": true,
                          "_links": {
                            "self": {
                              "href": "https://api-integration-example.tracksandbox.io/api/pms/units/1544/"
                            }
                          }
                        },
                        "contact": {
                          "id": 41151,
                          "firstName": "AaronB",
                          "lastName": "Bachman123",
                          "name": "AaronB Bachman123",
                          "primaryEmail": "test1234@test.com",
                          "secondaryEmail": null,
                          "homePhone": null,
                          "workPhone": null,
                          "cellPhone": null,
                          "otherPhone": null,
                          "fax": null,
                          "streetAddress": null,
                          "extendedAddress": null,
                          "locality": null,
                          "region": null,
                          "postalCode": null,
                          "country": "US",
                          "notes": null,
                          "anniversary": null,
                          "birthdate": null,
                          "noIdentity": false,
                          "isVip": false,
                          "isBlacklist": false,
                          "tags": [],
                          "references": [],
                          "custom": {
                            "custom_20": null
                          },
                          "createdAt": "2020-09-30T08:57:31-04:00",
                          "createdBy": "system",
                          "updatedAt": "2020-09-30T08:57:31-04:00",
                          "updatedBy": "system",
                          "isOwnerContact": false,
                          "_links": {
                            "self": {
                              "href": "https://api-integration-example.tracksandbox.io/api/crm/contacts/41151/"
                            }
                          }
                        },
                        "folio": {
                          "id": 118,
                          "type": "guest",
                          "status": "closed",
                          "contactId": 41151,
                          "companyId": null,
                          "company": null,
                          "taxExempt": false,
                          "startDate": "2020-11-29",
                          "endDate": "2020-12-01",
                          "closedDate": "2020-09-30",
                          "realizedBalance": -88.61,
                          "currentBalance": -88.61,
                          "createdAt": "2020-09-30T09:41:20-04:00",
                          "createdBy": "system",
                          "updatedAt": "2020-09-30T10:52:07-04:00",
                          "updatedBy": "system",
                          "name": "Folio",
                          "reservationId": 122,
                          "travelAgentId": null,
                          "travelAgent": null,
                          "hasException": false,
                          "exceptionMessage": null,
                          "checkInDate": null,
                          "checkOutDate": null,
                          "ownerRevenue": 0,
                          "ownerCommission": 0,
                          "agentCommission": 0,
                          "masterFolioId": null,
                          "masterFolio": null,
                          "masterFolioRuleId": null,
                          "masterFolioRule": null,
                          "_embedded": {
                            "contact": {
                              "_links": {
                                "self": {
                                  "href": "https://api-integration-example.tracksandbox.io/api/crm/contacts/41151/"
                                }
                              }
                            },
                            "reservation": {
                              "_links": {
                                "self": {
                                  "href": "https://api-integration-example.tracksandbox.io/api/pms/reservations/122/"
                                },
                                "logs": {
                                  "href": "https://api-integration-example.tracksandbox.io/api/pms/reservations/122/logs/"
                                },
                                "notes": {
                                  "href": "https://api-integration-example.tracksandbox.io/api/pms/reservations/122/notes/"
                                },
                                "fees": {
                                  "href": "https://api-integration-example.tracksandbox.io/api/pms/reservations/122/fees/"
                                },
                                "cancel": {
                                  "href": "https://api-integration-example.tracksandbox.io/api/pms/reservations/122/cancel/"
                                },
                                "tags": {
                                  "href": "https://api-integration-example.tracksandbox.io/api/pms/reservations/122/tags/"
                                },
                                "rates": {
                                  "href": "https://api-integration-example.tracksandbox.io/api/pms/reservations/122/rates/"
                                },
                                "discount": {
                                  "href": "https://api-integration-example.tracksandbox.io/api/pms/reservations/122/discount/"
                                }
                              }
                            }
                          },
                          "_links": {
                            "self": {
                              "href": "https://api-integration-example.tracksandbox.io/api/pms/folios/118/"
                            }
                          }
                        },
                        "cancellationReason": {
                          "id": 1,
                          "name": "Guest No longer able to take vacation",
                          "isActive": true,
                          "handle": "DEFAULT_CANCEL",
                          "cancelledByGuest": false,
                          "airbnbType": null,
                          "createdAt": "2020-05-12T01:05:46-04:00",
                          "createdBy": "system",
                          "updatedAt": "2020-08-15T14:25:52-04:00",
                          "updatedBy": "9-kmacgeorge",
                          "_links": {
                            "self": {
                              "href": "https://api-integration-example.tracksandbox.io/api/pms/reservations/cancellation-reasons/1/"
                            }
                          }
                        },
                        "rateType": {
                          "id": 1,
                          "type": "flat",
                          "code": "RR",
                          "name": "Rack Rate",
                          "isAllChannels": false,
                          "channelId": [
                            1,
                            6,
                            7,
                            8
                          ],
                          "isActive": true,
                          "createdAt": null,
                          "createdBy": "system",
                          "updatedAt": "2020-08-18T17:41:29-04:00",
                          "updatedBy": "6-kmurray",
                          "_links": {
                            "self": {
                              "href": "https://api-integration-example.tracksandbox.io/api/pms/rates/types/1/"
                            }
                          }
                        },
                        "paymentMethod": {
                          "id": 37,
                          "type": "credit",
                          "isDefault": false,
                          "cardNumber": "1111",
                          "cardExpiration": "05-2024",
                          "cardType": "visa",
                          "name": "raja test card",
                          "isRedacted": false,
                          "isVirtual": false,
                          "effectiveDate": null,
                          "limit": null,
                          "createdAt": "2020-09-30T09:41:20-04:00",
                          "createdBy": "system",
                          "updatedAt": "2020-09-30T09:41:20-04:00",
                          "updatedBy": "system",
                          "contactId": 41151,
                          "_links": {
                            "self": {
                              "href": "https://api-integration-example.tracksandbox.io/api/pms/payment-methods/37/"
                            }
                          }
                        }
                      },
                      "_links": {
                        "self": {
                          "href": "https://api-integration-example.tracksandbox.io/api/pms/reservations/1/"
                        },
                        "cancel": {
                          "href": "https://api-integration-example.tracksandbox.io/api/pms/reservations/1/cancel/"
                        }
                      }
                    }
                  }
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
          "404": {
            "description": "Not Found",
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
        "operationId": "getReservation",
        "description": "This endpoint will return all reservation of reservationId provided."
      }
    }
  },
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": true
  }
}
```