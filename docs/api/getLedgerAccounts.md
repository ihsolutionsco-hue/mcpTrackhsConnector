Get Ledger Accounts

# OpenAPI definition
```json
{
  "_id": "/branches/1.0/apis/pms-accounting-api.json",
  "openapi": "3.0.0",
  "info": {
    "title": "PMS Accounting API",
    "version": "1.0",
    "contact": {
      "name": "Track Support",
      "email": "support@trackhs.com",
      "url": "https://support.trackhs.com"
    },
    "description": "The full PMS API is large, as such we have broken down the files into related components. Since some of the components may share model files, models are referenced instead of embedded.\n\nThis API covers all endpoints related to finances and accounting.\n\nWhen used externally, this API requires a server context key. \n\nWhen used in user context, endpoints may be restricted based on role."
  },
  "tags": [
    {
      "name": "Accounts"
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
    "/pms/accounting/accounts": {
      "get": {
        "summary": "Get Ledger Accounts",
        "tags": [
          "Accounts"
        ],
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "title": "Payment Account Response",
                    "type": "object",
                    "description": "Object",
                    "properties": {
                      "id": {
                        "type": "integer"
                      },
                      "code": {
                        "type": "string"
                      },
                      "name": {
                        "type": "string"
                      },
                      "description": {
                        "type": "string"
                      },
                      "category": {
                        "type": "string",
                        "enum": [
                          "revenue",
                          "asset",
                          "equity",
                          "expense",
                          "liability"
                        ]
                      },
                      "accountType": {
                        "type": "string",
                        "enum": [
                          "bank",
                          "current",
                          "fixed",
                          "other-asset",
                          "receivable"
                        ]
                      },
                      "parentId": {
                        "nullable": true,
                        "type": "integer"
                      },
                      "isActive": {
                        "type": "boolean"
                      },
                      "externalId": {
                        "type": "integer"
                      },
                      "externalName": {
                        "type": "string"
                      },
                      "bankName": {
                        "type": "string"
                      },
                      "achEnabled": {
                        "type": "boolean"
                      },
                      "allowOwnerPayments": {
                        "type": "boolean"
                      },
                      "achOrginId": {
                        "type": "integer"
                      },
                      "routingNumber": {
                        "type": "integer"
                      },
                      "accountNumber": {
                        "type": "integer"
                      },
                      "currency": {
                        "type": "string"
                      },
                      "currentBalance": {
                        "type": "number"
                      },
                      "recursiveBalance": {
                        "type": "number"
                      },
                      "immediateDestination": {
                        "type": "integer"
                      },
                      "immediateDestinationName": {
                        "type": "string"
                      },
                      "immediateOriginName": {
                        "type": "string"
                      },
                      "companyName": {
                        "type": "string"
                      },
                      "companyIdentification": {
                        "type": "integer"
                      },
                      "stakeholderId": {
                        "type": "integer"
                      },
                      "enableRefunds": {
                        "type": "boolean"
                      },
                      "defaultRefundAccount": {
                        "type": "integer"
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
                          "parent": {
                            "type": "object",
                            "description": "This will return another account property in full."
                          },
                          "stakeholder": {
                            "type": "object",
                            "properties": {
                              "href": {
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
        "operationId": "getLedgerAccounts",
        "description": "Returns an array of ledger accounts.\n\nRequires Server Keys.",
        "parameters": [
          {
            "schema": {
              "type": "number",
              "maximum": 0,
              "minimum": 0
            },
            "in": "query",
            "name": "page",
            "description": "Page Number"
          },
          {
            "schema": {
              "type": "number"
            },
            "in": "query",
            "name": "size",
            "description": "Page Size"
          },
          {
            "schema": {
              "type": "string",
              "default": "name",
              "enum": [
                "id",
                "name",
                "type",
                "relativeOrder",
                "isActive"
              ]
            },
            "in": "query",
            "name": "sortColumn",
            "description": ""
          },
          {
            "schema": {
              "type": "string",
              "enum": [
                "asc",
                "desc"
              ],
              "default": "asc"
            },
            "in": "query",
            "name": "sortDirection"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "search",
            "description": "Search gateways with a string."
          },
          {
            "schema": {
              "type": "integer"
            },
            "in": "query",
            "name": "isActive"
          },
          {
            "schema": {
              "type": "string",
              "enum": [
                "Revenue",
                "Asset",
                "Equity",
                "Liability",
                "Expense"
              ]
            },
            "in": "query",
            "name": "category"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "accountType",
            "description": "Options vary based on what the category is."
          },
          {
            "schema": {
              "type": "integer"
            },
            "in": "query",
            "name": "parentId"
          },
          {
            "schema": {
              "type": "integer"
            },
            "in": "query",
            "name": "includeRestricted"
          },
          {
            "schema": {
              "type": "integer"
            },
            "in": "query",
            "name": "sortByCategoryValue"
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