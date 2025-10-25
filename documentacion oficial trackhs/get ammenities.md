Get Amenities

# OpenAPI definition
```json
{
  "_id": "/branches/1.0/apis/pms-amenities-api.json",
  "openapi": "3.0.0",
  "info": {
    "title": "PMS Amenities API",
    "version": "1.0",
    "description": "The full PMS API is large, as such we have broken down the files into related components. Since some of the components may share model files, models are referenced instead of embedded.\n\nThis API covers all endpoints related to unit, unit type and node configuration.\n\nWhen used externally, this API requires a server context key. \n\nWhen used in user context, endpoints may be restricted based on role.",
    "contact": {
      "name": "Track Support",
      "email": "support@trackhs.com",
      "url": "https://support.trackhs.com"
    }
  },
  "tags": [
    {
      "name": "Amenity"
    },
    {
      "name": "Unit BETA"
    }
  ],
  "paths": {
    "/pms/units/amenities": {
      "get": {
        "summary": "Get Amenities",
        "tags": [
          "Amenity",
          "Unit BETA"
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
                        "amenities": {
                          "type": "array",
                          "items": {
                            "title": "Amenities Response",
                            "type": "object",
                            "description": "Amenities Response",
                            "x-examples": {},
                            "properties": {
                              "id": {
                                "type": "integer",
                                "description": "ID"
                              },
                              "name": {
                                "type": "string"
                              },
                              "groupId": {
                                "type": "string"
                              },
                              "group": {
                                "type": "object",
                                "properties": {
                                  "name": {
                                    "type": "string"
                                  }
                                }
                              },
                              "homeawayType": {
                                "type": "string"
                              },
                              "airbnbType": {
                                "type": "string"
                              },
                              "tripadvisorType": {
                                "type": "string"
                              },
                              "marriottType": {
                                "type": "string",
                                "enum": [
                                  "AIR_CONDITION",
                                  "AIR_CONDITION_WINDOW",
                                  "BABY_CRIB",
                                  "BABYSIT_AVAILABLE",
                                  "BABYSIT_FEE",
                                  "BABYSIT_ONREQUEST",
                                  "BARTENDER",
                                  "BARTENDER_FEE",
                                  "BARTENDER_ONREQUEST",
                                  "BASKETBL_COMMUNITY",
                                  "BASKETBL_PRIVATE",
                                  "BATHTUB",
                                  "BEACH_ACCESS",
                                  "BEACH_ESSENTIALS",
                                  "BEACHFRONT",
                                  "BILLIARDS",
                                  "BUTLER_AVAILABLE",
                                  "BUTLER_FEE",
                                  "BUTLER_ONREQUEST",
                                  "CABLE",
                                  "CARBON_MONO_ALARM",
                                  "CHEF_AVAILABLE",
                                  "CHEF_FEE",
                                  "CHEF_ONREQUEST",
                                  "CHLD_BKS_TOYS",
                                  "CHLD_PLAY_AREA",
                                  "CITY_VIEW",
                                  "COFFEE_TEA_MAKER",
                                  "CONCIERGE",
                                  "COURTYARD_COMMUNITY",
                                  "COURTYARD_PRIVATE",
                                  "DAILYHOUSEKEEP_AVAILABLE",
                                  "DAILYHOUSEKEEP_FEE",
                                  "DAILYHOUSEKEEP_ONREQUEST",
                                  "DISHWASHER",
                                  "DRYCLEAN_AVAILABLE",
                                  "DRYCLEAN_FEE",
                                  "DRYCLEAN_ONREQUEST",
                                  "DRYER_IN_HOME",
                                  "DRYER_ON_PROPERTY",
                                  "ELEVATOR",
                                  "FIRE_EXTINGUISH",
                                  "FIREPLACE",
                                  "FIRST_AID",
                                  "FITNESS_COMMUNITY",
                                  "FITNESS_EQUIPMENT",
                                  "FITNESS_PRIVATE",
                                  "FREE_PARKING_OFF_SITE",
                                  "FREE_PARKING_ON_SITE",
                                  "GAME_ROOM",
                                  "GAMES",
                                  "GARDEN_VIEW",
                                  "GRILL_CHARCOAL",
                                  "GRILL_GAS",
                                  "GROCERY_AVAILABLE",
                                  "GROCERY_FEE",
                                  "GROCERY_ONREQUEST",
                                  "GROUND_FLOOR",
                                  "HAIR_DRYER",
                                  "HANDICAP_PARKING",
                                  "HEATING",
                                  "HIGH_CHAIR",
                                  "HOT_TUB",
                                  "INDOOR_PARKING",
                                  "INPERSON_CHECKIN",
                                  "IRON",
                                  "JET_SKIS",
                                  "KIDS_AMENITIES",
                                  "LAUNDRY_AVAILABLE",
                                  "LAUNDRY_FEE",
                                  "LAUNDRY_ONREQUEST",
                                  "MEAL_INCLUDED",
                                  "MICROWAVE",
                                  "MOUNTAIN_VIEW",
                                  "NO_PETS_ALLOWED",
                                  "OCEAN_VIEW",
                                  "OUTDOOR_DINING",
                                  "OUTDOOR_FIREPIT",
                                  "OUTDOOR_FURNITURE",
                                  "OUTDOOR_SUNLOUNGERS",
                                  "OVEN",
                                  "PARKING_OFF_SITE_FEE",
                                  "PARKING_ON_SITE_FEE",
                                  "PATIO_BALCONY",
                                  "PETS_ALLOWED",
                                  "POOL_COMMUNITY",
                                  "POOL_HEATED",
                                  "POOL_PRIVATE",
                                  "PRIVATE_DOCK",
                                  "PRIVATE_PARKING",
                                  "REFRIGERATOR",
                                  "SAFE",
                                  "SAUNA_COMMUNITY",
                                  "SAUNA_PRIVATE",
                                  "SECURITY_SYSTEM",
                                  "SITESTAFF_AVAILABLE",
                                  "SITESTAFF_FEE",
                                  "SITESTAFF_ONREQUEST",
                                  "SKI_IN_OUT",
                                  "SKI_RENTAL",
                                  "SKI_STORAGE",
                                  "SMOKE_ALARM",
                                  "STEP_FREE_ACCESS",
                                  "STOVE",
                                  "TABLE_TENNIS",
                                  "TENNIS_COMMUNITY",
                                  "TENNIS_PRIVATE",
                                  "THEATER",
                                  "TODDLER_BED",
                                  "VALET_PARKING",
                                  "VALET_PARKING_FEE",
                                  "VALET_PARKING_ONREQUEST",
                                  "WASHER_IN_HOME",
                                  "WASHER_ON_PROPERTY",
                                  "WATER_SPORTS",
                                  "WATER_SPORTS_FEE",
                                  "WATER_SPORTS_ONREQUEST",
                                  "WATER_VIEW",
                                  "WATERFRONT",
                                  "WHEELCHAIR_ACCESS",
                                  "WIDE_HALLWAY_CLEARANCE",
                                  "WIDE_HOME_DOORWAY"
                                ]
                              },
                              "isFilterable": {
                                "type": "boolean"
                              },
                              "isPublic": {
                                "type": "boolean"
                              },
                              "publicSearchable": {
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
                                  },
                                  "group": {
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
                              "name"
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
        "operationId": "getUnitAmenities",
        "description": "Return all amenities assigned to a given unit. The computed flag will return a set of amenities that encompasses the entire tree.",
        "security": [
          {
            "basic": []
          },
          {
            "hmac": []
          }
        ],
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
              "enum": [
                "id",
                "order",
                "isPublic",
                "publicSearchable",
                "isFilterable",
                "createdAt"
              ],
              "default": "order"
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
            "description": "search on id and/or name"
          },
          {
            "schema": {
              "type": "integer"
            },
            "in": "query",
            "name": "groupId",
            "description": "filter on group id"
          },
          {
            "schema": {
              "type": "integer",
              "enum": [
                1,
                0
              ]
            },
            "in": "query",
            "name": "isPublic"
          },
          {
            "schema": {
              "type": "integer",
              "enum": [
                1,
                0
              ]
            },
            "in": "query",
            "name": "publicSearchable"
          },
          {
            "schema": {
              "type": "integer",
              "enum": [
                1,
                0
              ]
            },
            "in": "query",
            "name": "isFilterable"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "homeawayType",
            "description": "search on homeawayType and allow % for wildcard matching"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "airbnbType",
            "description": "search on airbnbType and allow % for wildcard matching"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "tripadvisorType",
            "description": "search on tripadvisorType and allow % for wildcard matching"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "marriottType",
            "description": "search on marriottType and allow % for wildcard matching"
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
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": true
  }
}
```