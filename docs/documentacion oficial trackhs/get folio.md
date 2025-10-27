Get a Folio

# OpenAPI definition
```json
{
  "_id": "/branches/1.0/apis/pms-folios-api.json",
  "openapi": "3.0.0",
  "info": {
    "title": "PMS Folios API",
    "version": "1.0",
    "description": "The full PMS API is large, as such we have broken down the files into related components. Since some of the components may share model files, models are referenced instead of embedded.\n\nThis API covers all endpoints related to folios.\n\nWhen used externally, this API requires a server context key.\n\nWhen used in user context, endpoints may be restricted based on role.\n",
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
    "/pms/folios/{folioId}": {
      "parameters": [
        {
          "schema": {
            "type": "integer",
            "minimum": 1
          },
          "name": "folioId",
          "in": "path",
          "description": "Folio id",
          "required": true
        }
      ],
      "get": {
        "summary": "Get a Folio",
        "tags": [
          "Folio"
        ],
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Folio response",
                  "type": "object",
                  "description": "Get to see some additional fields depending on the folio type.",
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
                    "updatedAt": {
                      "type": "string",
                      "format": "date-time",
                      "description": "Date time in ISO 8601 format"
                    },
                    "updatedBy": {
                      "type": "string"
                    },
                    "createdAt": {
                      "type": "string",
                      "format": "date-time",
                      "description": "Date time in ISO 8601 format"
                    },
                    "createdBy": {
                      "type": "string"
                    },
                    "id": {
                      "type": "integer",
                      "minimum": 1
                    },
                    "masterFolioRuleId": {
                      "type": "integer",
                      "description": "Id of the relevant master folio rule mapping if exists, visible for certain folio types only",
                      "minimum": 1
                    },
                    "masterFolioId": {
                      "type": "integer",
                      "description": "Id of the relevant master folio if exists, visible for certain folio types only",
                      "minimum": 1
                    },
                    "agentCommission": {
                      "type": "number",
                      "description": "Travel agent commission, visible for certain folio types only"
                    },
                    "ownerCommission": {
                      "type": "number",
                      "description": "Owner commission, visible for certain folio types only"
                    },
                    "ownerRevenue": {
                      "type": "number",
                      "description": "Owner revenue, visible for certain folio types only"
                    },
                    "checkOutDate": {
                      "type": "string",
                      "format": "date",
                      "description": "Date in ISO-8601 format, visible for certain folio types only"
                    },
                    "checkInDate": {
                      "type": "string",
                      "format": "date",
                      "description": "Date in ISO-8601 format, visible for certain folio types only"
                    },
                    "exceptionMessage": {
                      "type": "string",
                      "description": "Exception message if exists, visible for certain folio types only"
                    },
                    "hasException": {
                      "type": "boolean",
                      "description": "Flag that indicates if the folio has an exception, visible for certain folio types only"
                    },
                    "travelAgentId": {
                      "type": "integer",
                      "description": "Id of the travel agent, visible for certain folio types only",
                      "minimum": 1
                    },
                    "reservationId": {
                      "type": "integer",
                      "description": "Id of the relevant reservation, visible for certain folio types only",
                      "minimum": 1
                    },
                    "name": {
                      "type": "string",
                      "description": "Name, visible for certain folio types only"
                    },
                    "currentBalance": {
                      "type": "number"
                    },
                    "realizedBalance": {
                      "type": "number"
                    },
                    "closedDate": {
                      "type": "string",
                      "format": "date",
                      "description": "Date when the folio got closed, in ISO-8601 format"
                    },
                    "endDate": {
                      "type": "string",
                      "format": "date",
                      "description": "Date when the folio ends, in ISO-8601 format"
                    },
                    "startDate": {
                      "type": "string",
                      "format": "date",
                      "description": "Date when the folio starts, in ISO-8601 format"
                    },
                    "taxEmpty": {
                      "type": "boolean",
                      "description": "Flag that indicates if the tax exempted for the folio"
                    },
                    "companyId": {
                      "type": "integer",
                      "description": "Id of the company",
                      "nullable": true,
                      "minimum": 1
                    },
                    "contactId": {
                      "type": "integer",
                      "description": "Id of the guest",
                      "minimum": 1
                    },
                    "status": {
                      "type": "string",
                      "enum": [
                        "open",
                        "closed"
                      ]
                    },
                    "type": {
                      "type": "string",
                      "enum": [
                        "guest",
                        "master"
                      ]
                    },
                    "_embedded": {
                      "type": "object",
                      "properties": {
                        "contact": {
                          "title": "Contact Response",
                          "type": "object",
                          "description": "",
                          "properties": {
                            "id": {
                              "type": "integer",
                              "description": "ID"
                            },
                            "firstName": {
                              "type": "string",
                              "description": "Name of policy",
                              "minLength": 1,
                              "maxLength": 64
                            },
                            "lastName": {
                              "type": "string"
                            },
                            "primaryEmail": {
                              "type": "string",
                              "format": "email",
                              "description": "Primary email assigned to contact. Must be unique."
                            },
                            "secondaryEmail": {
                              "type": "string",
                              "format": "email",
                              "description": "Alternative or secondary email assigned to contact. Must be unique."
                            },
                            "homePhone": {
                              "type": "string",
                              "description": "Use E.164 Format, non complaint numbers will be processed within US locale."
                            },
                            "cellPhone": {
                              "type": "string",
                              "description": "Use E.164 Format, non complaint numbers will be processed within US locale."
                            },
                            "workPhone": {
                              "type": "string",
                              "description": "Use E.164 Format, non complaint numbers will be processed within US locale."
                            },
                            "otherPhone": {
                              "type": "string",
                              "description": "Use E.164 Format, non complaint numbers will be processed within US locale."
                            },
                            "fax": {
                              "type": "string",
                              "description": "Use E.164 Format, non complaint numbers will be processed within US locale."
                            },
                            "streetAddress": {
                              "type": "string"
                            },
                            "country": {
                              "type": "string",
                              "example": "US",
                              "minLength": 2,
                              "maxLength": 2,
                              "description": "ISO 2 Character Country Code"
                            },
                            "postalCode": {
                              "type": "string"
                            },
                            "region": {
                              "type": "string"
                            },
                            "locality": {
                              "type": "string"
                            },
                            "extendedAddress": {
                              "type": "string",
                              "nullable": true
                            },
                            "notes": {
                              "type": "string"
                            },
                            "anniversary": {
                              "type": "string",
                              "pattern": "^(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|30|31)$"
                            },
                            "birthdate": {
                              "type": "string",
                              "pattern": "^(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|30|31)$"
                            },
                            "isVip": {
                              "type": "boolean"
                            },
                            "isBlacklist": {
                              "type": "boolean"
                            },
                            "taxId": {
                              "type": "string",
                              "nullable": true,
                              "description": "1099 Tax Id (Restricted)"
                            },
                            "paymentType": {
                              "type": "string",
                              "description": "Payment type, used for ACH or Check payments. (Restricted)",
                              "deprecated": true,
                              "enum": [
                                "print",
                                "direct"
                              ]
                            },
                            "achAccountNumber": {
                              "type": "string",
                              "description": "ACH Account Number (Restricted)",
                              "deprecated": true
                            },
                            "achRoutingNumber": {
                              "type": "string",
                              "description": "ACH Routing Number (Restricted)",
                              "deprecated": true,
                              "minLength": 9,
                              "maxLength": 9,
                              "pattern": "^[0-9]{9}$"
                            },
                            "achAccountType": {
                              "type": "string",
                              "enum": [
                                "business-checking",
                                "business-savings",
                                "personal-checking",
                                "personal-savings"
                              ],
                              "deprecated": true,
                              "description": "Used if payment type is ACH. (Restricted)"
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
                                    "type": "integer"
                                  },
                                  "channelId": {
                                    "type": "integer"
                                  }
                                }
                              }
                            },
                            "tags": {
                              "type": "array",
                              "items": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "integer",
                                    "description": "ID"
                                  },
                                  "name": {
                                    "type": "string"
                                  }
                                }
                              }
                            },
                            "customValues": {
                              "type": "object",
                              "description": "Keys are determined by customer. Values are either string or array depending on type",
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
                            },
                            "updatedAt": {
                              "type": "string",
                              "format": "date-time",
                              "description": "Date as ISO 8601 format"
                            },
                            "updatedBy": {
                              "type": "string"
                            },
                            "createdAt": {
                              "type": "string",
                              "format": "date-time",
                              "description": "Date as ISO 8601 format"
                            },
                            "createdBy": {
                              "type": "string"
                            },
                            "noIdentity": {
                              "type": "boolean",
                              "description": "Contacts that do not have identity information"
                            }
                          }
                        },
                        "travelAgent": {
                          "title": "Company Response",
                          "type": "object",
                          "description": "Response contains fields for all company types.\n\nSeveral field types are restricted to specific user permissions when accessed as a user. Those are indicated below.\n\nOther specific fields are only visible or available with certian company types.\n\nOwners cannot be created or updated via this API. Instead the owner API should be used instead.\n",
                          "properties": {
                            "id": {
                              "type": "integer",
                              "description": "ID"
                            },
                            "type": {
                              "type": "string",
                              "enum": [
                                "company",
                                "agent",
                                "vendor",
                                "owner"
                              ]
                            },
                            "isActive": {
                              "type": "boolean"
                            },
                            "name": {
                              "type": "string",
                              "description": "Name of the company."
                            },
                            "streetAddress": {
                              "type": "string"
                            },
                            "extendedAddress": {
                              "type": "string",
                              "nullable": true
                            },
                            "locality": {
                              "type": "string"
                            },
                            "region": {
                              "type": "string"
                            },
                            "postal": {
                              "type": "string",
                              "description": "Postal Code of company."
                            },
                            "country": {
                              "type": "string",
                              "example": "US",
                              "minLength": 2,
                              "maxLength": 2,
                              "description": "ISO 2 Character Country Code"
                            },
                            "taxType": {
                              "type": "string",
                              "enum": [
                                "rents",
                                "other",
                                "none",
                                "non_employee_compensation"
                              ],
                              "description": "(Restricted) 1099 Income classification"
                            },
                            "taxName": {
                              "type": "string",
                              "description": "(Restricted) 1099 Tax Payee Name, If different"
                            },
                            "taxId": {
                              "type": "string",
                              "nullable": true,
                              "description": "1099 Tax Id (Restricted)"
                            },
                            "achAccountNumber": {
                              "type": "string",
                              "description": "ACH Account Number (Restricted)"
                            },
                            "achRoutingNumber": {
                              "type": "string",
                              "minLength": 9,
                              "maxLength": 9,
                              "pattern": "^[0-9]{9}$",
                              "description": "ACH Routing Number (Restricted)"
                            },
                            "achAccountType": {
                              "deprecated": true,
                              "type": "string",
                              "enum": [
                                "business-checking",
                                "business-savings",
                                "personal-checking",
                                "personal-savings"
                              ],
                              "description": "Used if payment type is ACH. (Restricted)"
                            },
                            "achVerifiedAt": {
                              "type": "string",
                              "description": "Date as ISO 8601 format, When ACH information was prenoted (Restricted)",
                              "deprecated": true,
                              "format": "date-time"
                            },
                            "paymentType": {
                              "type": "string",
                              "description": "Payment type, used for ACH or Check payments. Restricted.",
                              "deprecated": true,
                              "enum": [
                                "print",
                                "direct"
                              ]
                            },
                            "glExpirationDate": {
                              "type": "string",
                              "format": "date",
                              "deprecated": true,
                              "description": "Date as ISO 8601 format, General libality insurance expriation date"
                            },
                            "glInsurancePolicy": {
                              "type": "string",
                              "deprecated": true,
                              "description": "General liablity insurance policy"
                            },
                            "wcExpirationDate": {
                              "type": "string",
                              "format": "date",
                              "deprecated": true,
                              "description": "Date as ISO 8601 format, Workers comp insurance expiration date. "
                            },
                            "wcInsurancePolicy": {
                              "type": "string",
                              "deprecated": true,
                              "description": "Workers comp insurnace policy number."
                            },
                            "travelAgentDeductCommission": {
                              "type": "boolean",
                              "description": "(Travel Agent and PMS) Enable travel agent commission. Value is set with travelAgentCommission."
                            },
                            "travelAgentCommission": {
                              "type": "number",
                              "description": "(Travel Agent and PMS) Commission value of between 0 and 100%. Used if commission is enabled.",
                              "minimum": 0,
                              "maximum": 100
                            },
                            "travelAgentIataNumber": {
                              "type": "string",
                              "description": "(Travel Agent) Requied for all travel agents."
                            },
                            "enableWorkOrderApproval": {
                              "type": "boolean",
                              "description": "(Vendor and PMS) Allow vendor to approve assigned work orders."
                            },
                            "notes": {
                              "type": "string"
                            },
                            "website": {
                              "type": "string",
                              "format": "uri"
                            },
                            "email": {
                              "type": "string",
                              "format": "email"
                            },
                            "fax": {
                              "type": "string",
                              "description": "Use E.164 Format, non complaint numbers will be processed within US locale."
                            },
                            "phone": {
                              "type": "string",
                              "description": "Use E.164 Format, non complaint numbers will be processed within US locale."
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
                            "tags": {
                              "type": "array",
                              "items": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "integer",
                                    "description": "ID"
                                  },
                                  "name": {
                                    "type": "string"
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
                            "type",
                            "name"
                          ]
                        },
                        "company": {
                          "title": "Company Response",
                          "type": "object",
                          "description": "Response contains fields for all company types.\n\nSeveral field types are restricted to specific user permissions when accessed as a user. Those are indicated below.\n\nOther specific fields are only visible or available with certian company types.\n\nOwners cannot be created or updated via this API. Instead the owner API should be used instead.\n",
                          "properties": {
                            "id": {
                              "type": "integer",
                              "description": "ID"
                            },
                            "type": {
                              "type": "string",
                              "enum": [
                                "company",
                                "agent",
                                "vendor",
                                "owner"
                              ]
                            },
                            "isActive": {
                              "type": "boolean"
                            },
                            "name": {
                              "type": "string",
                              "description": "Name of the company."
                            },
                            "streetAddress": {
                              "type": "string"
                            },
                            "extendedAddress": {
                              "type": "string",
                              "nullable": true
                            },
                            "locality": {
                              "type": "string"
                            },
                            "region": {
                              "type": "string"
                            },
                            "postal": {
                              "type": "string",
                              "description": "Postal Code of company."
                            },
                            "country": {
                              "type": "string",
                              "example": "US",
                              "minLength": 2,
                              "maxLength": 2,
                              "description": "ISO 2 Character Country Code"
                            },
                            "taxType": {
                              "type": "string",
                              "enum": [
                                "rents",
                                "other",
                                "none",
                                "non_employee_compensation"
                              ],
                              "description": "(Restricted) 1099 Income classification"
                            },
                            "taxName": {
                              "type": "string",
                              "description": "(Restricted) 1099 Tax Payee Name, If different"
                            },
                            "taxId": {
                              "type": "string",
                              "nullable": true,
                              "description": "1099 Tax Id (Restricted)"
                            },
                            "achAccountNumber": {
                              "type": "string",
                              "description": "ACH Account Number (Restricted)"
                            },
                            "achRoutingNumber": {
                              "type": "string",
                              "minLength": 9,
                              "maxLength": 9,
                              "pattern": "^[0-9]{9}$",
                              "description": "ACH Routing Number (Restricted)"
                            },
                            "achAccountType": {
                              "deprecated": true,
                              "type": "string",
                              "enum": [
                                "business-checking",
                                "business-savings",
                                "personal-checking",
                                "personal-savings"
                              ],
                              "description": "Used if payment type is ACH. (Restricted)"
                            },
                            "achVerifiedAt": {
                              "type": "string",
                              "description": "Date as ISO 8601 format, When ACH information was prenoted (Restricted)",
                              "deprecated": true,
                              "format": "date-time"
                            },
                            "paymentType": {
                              "type": "string",
                              "description": "Payment type, used for ACH or Check payments. Restricted.",
                              "deprecated": true,
                              "enum": [
                                "print",
                                "direct"
                              ]
                            },
                            "glExpirationDate": {
                              "type": "string",
                              "format": "date",
                              "deprecated": true,
                              "description": "Date as ISO 8601 format, General libality insurance expriation date"
                            },
                            "glInsurancePolicy": {
                              "type": "string",
                              "deprecated": true,
                              "description": "General liablity insurance policy"
                            },
                            "wcExpirationDate": {
                              "type": "string",
                              "format": "date",
                              "deprecated": true,
                              "description": "Date as ISO 8601 format, Workers comp insurance expiration date. "
                            },
                            "wcInsurancePolicy": {
                              "type": "string",
                              "deprecated": true,
                              "description": "Workers comp insurnace policy number."
                            },
                            "travelAgentDeductCommission": {
                              "type": "boolean",
                              "description": "(Travel Agent and PMS) Enable travel agent commission. Value is set with travelAgentCommission."
                            },
                            "travelAgentCommission": {
                              "type": "number",
                              "description": "(Travel Agent and PMS) Commission value of between 0 and 100%. Used if commission is enabled.",
                              "minimum": 0,
                              "maximum": 100
                            },
                            "travelAgentIataNumber": {
                              "type": "string",
                              "description": "(Travel Agent) Requied for all travel agents."
                            },
                            "enableWorkOrderApproval": {
                              "type": "boolean",
                              "description": "(Vendor and PMS) Allow vendor to approve assigned work orders."
                            },
                            "notes": {
                              "type": "string"
                            },
                            "website": {
                              "type": "string",
                              "format": "uri"
                            },
                            "email": {
                              "type": "string",
                              "format": "email"
                            },
                            "fax": {
                              "type": "string",
                              "description": "Use E.164 Format, non complaint numbers will be processed within US locale."
                            },
                            "phone": {
                              "type": "string",
                              "description": "Use E.164 Format, non complaint numbers will be processed within US locale."
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
                            "tags": {
                              "type": "array",
                              "items": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "integer",
                                    "description": "ID"
                                  },
                                  "name": {
                                    "type": "string"
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
                            "type",
                            "name"
                          ]
                        },
                        "masterFolioRule": {
                          "title": "Folio rule mapping",
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "integer",
                              "minimum": 1
                            },
                            "ruleId": {
                              "type": "integer",
                              "minimum": 1,
                              "description": "Id of the folio rule"
                            },
                            "startDate": {
                              "type": "string",
                              "format": "date",
                              "description": "Date in ISO-8601 format when the mapping becomes effective, null indicates effective till end date"
                            },
                            "endDate": {
                              "type": "string",
                              "format": "date",
                              "description": "Date in ISO-8601 format after which the mapping no loner stays effective, null indicates always in effect"
                            },
                            "minNights": {
                              "type": "integer",
                              "minimum": 1,
                              "description": "Minimum number of nights"
                            },
                            "maxNights": {
                              "type": "integer",
                              "minimum": 1,
                              "description": "Maximum number of nights applicable"
                            },
                            "maxSpend": {
                              "type": "number",
                              "description": "Max amount to be spent"
                            },
                            "createdBy": {
                              "type": "string"
                            },
                            "createdAt": {
                              "type": "string",
                              "format": "date-time",
                              "description": "Date time in ISO 8601 format"
                            },
                            "updatedBy": {
                              "type": "string"
                            },
                            "updatedAt": {
                              "type": "string",
                              "format": "date-time",
                              "description": "Date time in ISO 8601 format"
                            },
                            "_embedded": {
                              "type": "object",
                              "properties": {
                                "rule": {
                                  "title": "Folio rule response",
                                  "type": "object",
                                  "description": "Get to see additional fields depending on the type of rule.",
                                  "properties": {
                                    "id": {
                                      "type": "integer",
                                      "description": "ID",
                                      "minimum": 1
                                    },
                                    "name": {
                                      "type": "string",
                                      "description": "Name of the rule"
                                    },
                                    "code": {
                                      "type": "string",
                                      "description": "Short code"
                                    },
                                    "isActive": {
                                      "type": "boolean",
                                      "description": "Flag that indicates if the rule is active"
                                    },
                                    "type": {
                                      "type": "string",
                                      "enum": [
                                        "percent",
                                        "breakdown"
                                      ],
                                      "description": "Type of the rule"
                                    },
                                    "createdBy": {
                                      "type": "string"
                                    },
                                    "createdAt": {
                                      "type": "string",
                                      "format": "date-time",
                                      "description": "Date time in ISO 8601 format"
                                    },
                                    "updatedBy": {
                                      "type": "string"
                                    },
                                    "updatedAt": {
                                      "type": "string",
                                      "format": "date-time",
                                      "description": "Date time in ISO 8601 format"
                                    },
                                    "percentAmount": {
                                      "type": "number",
                                      "maximum": 100,
                                      "description": "Amount of percentage. Will be set for certain types only, 0 for others"
                                    },
                                    "breakdownRentMode": {
                                      "type": "string",
                                      "enum": [
                                        "percent",
                                        "nights"
                                      ],
                                      "description": "Will be set for certain types only, empty for others"
                                    },
                                    "breakdownRentIncludeTax": {
                                      "type": "boolean",
                                      "description": "Flag that indicates if the rent includes tax. Will be set for certain types only, empty for others"
                                    },
                                    "breakdownRentPercent": {
                                      "type": "number",
                                      "maximum": 100,
                                      "description": "Amount of percentage. Will be set for certain break down rent modes only, 0 for others"
                                    },
                                    "breakdownRentNights": {
                                      "type": "integer",
                                      "description": "Will be set for certain break down rent modes only, 0 for others"
                                    },
                                    "breakdownFeeMode": {
                                      "type": "string",
                                      "enum": [
                                        "percent",
                                        "required"
                                      ],
                                      "description": "Will be set for certain types only, empty for others"
                                    },
                                    "breakdownFeeIncludeTax": {
                                      "type": "boolean",
                                      "description": "Flag that indicates if the fee includes tax. Will be set for certain types only, empty for others"
                                    },
                                    "breakdownFeePercent": {
                                      "type": "number",
                                      "maximum": 100,
                                      "description": "Amount of percentage. Will be set for certain break down fee modes only, 0 for others"
                                    },
                                    "breakdownChargesMode": {
                                      "type": "string",
                                      "enum": [
                                        "percent",
                                        "required"
                                      ],
                                      "description": "Will be set for certain types only, empty for others"
                                    },
                                    "breakdownChargesIncludeTax": {
                                      "type": "boolean",
                                      "description": "Flag that indicates if the charges include tax. Will be set for certain types only, empty for others"
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
                                    "name",
                                    "code",
                                    "isActive",
                                    "type"
                                  ]
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
                            "ruleId"
                          ]
                        },
                        "masterFolio": {
                          "type": "object",
                          "description": "this folio response without master"
                        }
                      }
                    }
                  },
                  "required": [
                    "id",
                    "status"
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
        "operationId": "getFolio",
        "description": "Get a single Folio, can be used with any folio type.",
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
      "name": "Folio"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": true
  }
}
```