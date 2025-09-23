Get All Contacts

# OpenAPI definition
```json
{
  "_id": "/branches/1.0/apis/crm-api.json",
  "openapi": "3.0.0",
  "info": {
    "title": "CRM API",
    "version": "1.0",
    "contact": {
      "name": "Track Support",
      "email": "support@trackhs.com",
      "url": "https://support.trackhs.com"
    },
    "description": "This provides access to the core entities which make up the CRM component of the platform.\n\nThis requires a server or user key conext to accesss."
  },
  "tags": [
    {
      "name": "Contact"
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
    "/crm/contacts": {
      "get": {
        "summary": "Get All Contacts",
        "tags": [
          "Contact"
        ],
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "_embedded": {
                      "type": "object",
                      "properties": {
                        "contacts": {
                          "type": "array",
                          "items": {
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
                            },
                            "x-readme-ref-name": "ContactsResponse"
                          }
                        }
                      }
                    }
                  },
                  "required": [
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
        "operationId": "getContacts",
        "security": [
          {
            "basic": []
          },
          {
            "hmac": []
          }
        ],
        "description": "Contacts include guests, owners, or vendor employees. This endpoint will return all contacts. ",
        "parameters": [
          {
            "schema": {
              "type": "string",
              "enum": [
                "id",
                "name",
                "email",
                "cellPhone",
                "homePhone",
                "otherPhone",
                "vip"
              ]
            },
            "in": "query",
            "name": "sortColumn",
            "description": "Sorted by id, name, email, mobile phone, home phone, other phone, vip"
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
            "name": "sortDirection",
            "description": "Sort ascending or descending"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "search",
            "description": "Search by first name, last name, email, mobile phone, home phone, other phone with a right side wild card (this-search-plus*)\n\nIf is numeric and starts with a '1', then it will search for that number\n\nif numeric and not a 1, it will search for a number prefixed with a 1 and  (phone numbers saved with 1 at beginning)\n\notherwise it will search for the string\n\n## how does it search\n\nThe search parameter with explode on spaces and use each word to do an ANDing query with each word as a parameter. It MUST match against all provided strings, but not in the same column.\n\n`search=Griselda Peters` will do a search that includes 2 names but could match against any of the 7 fields.\n\n*NOTE:* this is a wildcard search, so it searches for a “start of string” with these words.\n\n_Possible Issues_: searching for `Peter James`, which may match\n\n- First name James\n- Last name Peter, Peters, Peterson\n- First name Peter\n- Last name James\n\nSo, it is not perfect, but you could include phone number in there as well and the odds of overlapping a multiple contacts are drastically reduced.\n"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "term",
            "description": "Locate contact based on a precise value such as ID or name"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "email",
            "description": "Search contact by primary or secondary email address"
          },
          {
            "schema": {
              "type": "number"
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
              "format": "date",
              "description": "Date as ISO 8601 format"
            },
            "in": "query",
            "name": "updatedSince",
            "description": "Date in ISO 8601 format. Will return all contacts updated since timestamp."
          }
        ]
      }
    }
  },
  "components": {
    "securitySchemes": {
      "basic": {
        "type": "http",
        "scheme": "basic",
        "description": "Authentication is unique to each customer. Please request authorization keys from the customer you are integrating with."
      },
      "hmac": {
        "type": "http",
        "scheme": "bearer",
        "description": "HMAC Authentication based on https://github.com/acquia/http-hmac-spec/tree/2.0"
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