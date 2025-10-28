Unit Collection

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
      "name": "Units",
      "description": "Endpoints which provide unit data and information."
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
    "/pms/units": {
      "get": {
        "summary": "Unit Collection",
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
                        "units": {
                          "type": "array",
                          "items": {
                            "title": "Unit Response - Channel",
                            "type": "object",
                            "description": "The data will be returned with a collection lookup and with a single entity lookup.\n\nDue to planned changes, the following fields should be considered unstable: unitType and customData. All other fields should be considered stable.",
                            "properties": {
                              "id": {
                                "type": "integer",
                                "description": "ID"
                              },
                              "name": {
                                "type": "string",
                                "description": "Name"
                              },
                              "shortName": {
                                "type": "string",
                                "description": "Short name of unit."
                              },
                              "unitCode": {
                                "type": "string"
                              },
                              "headline": {
                                "type": "string",
                                "description": "Will be set if configured for channel."
                              },
                              "shortDescription": {
                                "type": "string",
                                "nullable": true,
                                "description": "Short Description of unit."
                              },
                              "longDescription": {
                                "type": "string",
                                "nullable": true,
                                "description": "Long Description of unit."
                              },
                              "houseRules": {
                                "type": "string",
                                "description": "Freeform version of what the rules are for the house. Combined rules for association, quiet hours, what's allowed, what isn't, etc."
                              },
                              "nodeId": {
                                "type": "integer",
                                "description": "Returns which node the unit is associated with."
                              },
                              "unitType": {
                                "type": "object",
                                "description": "Channel - Object with id and name. Other contexts will have link with unitTypeId field. Consider this value unstable. Will be replaced with a unit types API link.",
                                "deprecated": true,
                                "properties": {
                                  "id": {
                                    "type": "integer",
                                    "description": "ID"
                                  },
                                  "name": {
                                    "type": "string"
                                  }
                                }
                              },
                              "lodgingType": {
                                "type": "object",
                                "description": "Channel - Object with id and name. Other contexts will have link with lodgingTypeId field.",
                                "properties": {
                                  "id": {
                                    "type": "integer",
                                    "description": "ID"
                                  },
                                  "name": {
                                    "type": "string"
                                  }
                                }
                              },
                              "directions": {
                                "type": "string",
                                "nullable": true,
                                "description": "Directions to the unit location."
                              },
                              "checkinDetails": {
                                "type": "string",
                                "nullable": true,
                                "description": "Checkin details, if applicable to unit."
                              },
                              "timezone": {
                                "type": "string",
                                "description": "Timezone used for checkin/checkout times."
                              },
                              "checkinTime": {
                                "type": "string",
                                "description": "Checkin time set at unit level. Format \"HH:MM\""
                              },
                              "hasEarlyCheckin": {
                                "type": "boolean",
                                "description": "Whether or not unit has early checkin."
                              },
                              "earlyCheckinTime": {
                                "type": "string",
                                "description": "Early checkin time if supported. Format \"HH:MM\""
                              },
                              "checkoutTime": {
                                "type": "string",
                                "description": "Checkout time set at the unit level. Format \"HH:MM\""
                              },
                              "hasLateCheckout": {
                                "type": "boolean",
                                "description": "Whether or not unit allows late checkout."
                              },
                              "lateCheckoutTime": {
                                "type": "string",
                                "description": "Late checkout time if supported. Format \"HH:MM\""
                              },
                              "minBookingWindow": {
                                "type": "integer"
                              },
                              "maxBookingWindow": {
                                "type": "integer"
                              },
                              "website": {
                                "type": "string",
                                "format": "uri",
                                "description": "Website to site that represents unit."
                              },
                              "phone": {
                                "type": "string",
                                "nullable": true,
                                "description": "Phone to number that represents unit."
                              },
                              "streetAddress": {
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
                              "postal": {
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
                              },
                              "petsFriendly": {
                                "type": "boolean",
                                "description": "Return pet friendly or not pet friendly units."
                              },
                              "maxPets": {
                                "type": "integer",
                                "nullable": true,
                                "description": "Max number of pets allowed in a unit."
                              },
                              "eventsAllowed": {
                                "type": "boolean",
                                "description": "Whether or not events are allowed in the unit."
                              },
                              "smokingAllowed": {
                                "type": "boolean",
                                "description": "Whether or not smoking is allowed in the unit."
                              },
                              "childrenAllowed": {
                                "type": "boolean",
                                "description": "Whether or not children are allowed in the unit."
                              },
                              "minimumAgeLimit": {
                                "type": "integer",
                                "description": "What is the minimum limit of the primary guest."
                              },
                              "isAccessible": {
                                "type": "boolean",
                                "description": "Is the unit handicap accessible."
                              },
                              "area": {
                                "type": "integer",
                                "description": "Unit area in local unit of measurement."
                              },
                              "floors": {
                                "type": "integer",
                                "nullable": true,
                                "description": "Floors of the unit."
                              },
                              "maxOccupancy": {
                                "type": "integer",
                                "description": "Max occupancy of the unit."
                              },
                              "securityDeposit": {
                                "type": "string",
                                "description": "Requires the security deposit beta."
                              },
                              "bedrooms": {
                                "type": "integer",
                                "description": "Count of bedrooms."
                              },
                              "fullBathrooms": {
                                "type": "integer",
                                "description": "Count of full bathrooms."
                              },
                              "threeQuarterBathrooms": {
                                "type": "integer",
                                "nullable": true,
                                "description": "Count of three quarter baths."
                              },
                              "halfBathrooms": {
                                "type": "integer",
                                "description": "Count of half baths."
                              },
                              "bedTypes": {
                                "type": "array",
                                "description": "Count of each bed type. This will return a summary of bed types that are available in the unit.\n\nif unit or unitType is set to useRoomConfiguration then the bedTypes are nested under the rooms attribute\n",
                                "items": {
                                  "type": "object",
                                  "properties": {
                                    "id": {
                                      "type": "integer",
                                      "description": "ID"
                                    },
                                    "name": {
                                      "type": "string"
                                    },
                                    "count": {
                                      "type": "integer"
                                    }
                                  }
                                }
                              },
                              "rooms": {
                                "type": "array",
                                "description": "If unit or unitType is set to useRoomConfiguration\nthen this will contain array of all room configurations.\n",
                                "items": {
                                  "type": "object",
                                  "properties": {
                                    "name": {
                                      "type": "string"
                                    },
                                    "type": {
                                      "type": "string",
                                      "enum": [
                                        "bedroom",
                                        "half_bathroom",
                                        "three_quarter_bathroom",
                                        "full_bathroom",
                                        "kitchen",
                                        "common",
                                        "outside"
                                      ]
                                    },
                                    "sleeps": {
                                      "type": "integer"
                                    },
                                    "description": {
                                      "type": "string"
                                    },
                                    "hasAttachedBathroom": {
                                      "type": "boolean",
                                      "description": "Maps to airbnb room amenity"
                                    },
                                    "beds": {
                                      "type": "array",
                                      "description": "Bed types and number of each bed type.",
                                      "items": {
                                        "type": "object",
                                        "properties": {
                                          "id": {
                                            "type": "integer",
                                            "description": "ID"
                                          },
                                          "name": {
                                            "type": "string"
                                          },
                                          "count": {
                                            "type": "string"
                                          },
                                          "homeawayType": {
                                            "type": "string",
                                            "description": "This may be used to assist in mapping bed types value.",
                                            "enum": [
                                              "AMENITY_BUNK_BED",
                                              "AMENITY_CHILD_BED",
                                              "AMENITY_BABY_CRIB",
                                              "AMENITY_DOUBLE",
                                              "AMENITY_KING",
                                              "AMENITY_MURPHY_BED",
                                              "AMENITY_QUEEN",
                                              "AMENITY_SLEEP_SOFA",
                                              "AMENITY_TWIN_SINGLE"
                                            ]
                                          },
                                          "airbnbType": {
                                            "type": "string",
                                            "enum": [
                                              "king_bed",
                                              "queen_bed",
                                              "double_bed",
                                              "single_bed",
                                              "sofa_bed",
                                              "couch",
                                              "air_mattress",
                                              "bunk_bed",
                                              "floor_mattress",
                                              "toddler_bed",
                                              "crib",
                                              "water_bed",
                                              "hammock"
                                            ],
                                            "description": "This may be used to assist in mapping bed types value."
                                          },
                                          "marriottType": {
                                            "type": "string",
                                            "enum": [
                                              "TWIN_XL_BED",
                                              "SINGLE_BED",
                                              "SINGLE_XL_BED",
                                              "FULL_BED",
                                              "FULL_XL_BED",
                                              "DOUBLE_BED",
                                              "QUEEN_NA_BED",
                                              "QUEEN_EU_BED",
                                              "CAL_KING_BED",
                                              "GRAND_KING_BED",
                                              "BUNK_BED",
                                              "SOFA_BED",
                                              "MURPHY_BED",
                                              "TODDLER_BED",
                                              "FUTON",
                                              "CRIB",
                                              "AIR_MATTRESS",
                                              "FLOOR_MATTRESS"
                                            ],
                                            "description": "This may be used to assist in mapping bed types value."
                                          }
                                        }
                                      }
                                    },
                                    "order": {
                                      "type": "integer",
                                      "nullable": true
                                    },
                                    "homeawayType": {
                                      "type": "string",
                                      "enum": [
                                        "BEDROOM",
                                        "LIVING_SLEEPING_COMBO",
                                        "OTHER_SLEEPING_AREA",
                                        "FULL_BATH",
                                        "HALF_BATH",
                                        "SHOWER_INDOOR_OR_OUTDOOR"
                                      ],
                                      "description": "This can be used to assist with mapping of the room value."
                                    },
                                    "airbnbType": {
                                      "type": "string",
                                      "enum": [
                                        "backyard",
                                        "basement",
                                        "bedroom",
                                        "common_space",
                                        "common_spaces",
                                        "dining_room",
                                        "entrance_to_home",
                                        "entry",
                                        "exterior",
                                        "front_yard",
                                        "family_room",
                                        "full_bathroom",
                                        "half_bathroom",
                                        "hot_tub",
                                        "garage",
                                        "gym",
                                        "kitchen",
                                        "kitchenette",
                                        "laundry_room",
                                        "living_room",
                                        "office",
                                        "other",
                                        "outdoor_common_area",
                                        "outdoor_space",
                                        "pool",
                                        "recreation_area",
                                        "study",
                                        "studio"
                                      ],
                                      "description": "This can be used to assist with mapping of the room value."
                                    }
                                  }
                                }
                              },
                              "amenities": {
                                "type": "array",
                                "description": "Amenities including the linked group for each amenity. This will include public unit amenities.",
                                "items": {
                                  "type": "object",
                                  "properties": {
                                    "id": {
                                      "type": "integer",
                                      "description": "ID"
                                    },
                                    "name": {
                                      "type": "string"
                                    },
                                    "group": {
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
                                  }
                                }
                              },
                              "amenityDescription": {
                                "type": "string",
                                "description": "Description of amenities, covers anything not in structured set."
                              },
                              "custom": {
                                "type": "object",
                                "nullable": true,
                                "description": "Properties will vary by customer. This will display all fields available with channel distribution. Each property will have a different data type depending on the property."
                              },
                              "coverImage": {
                                "type": "string",
                                "format": "uri",
                                "deprecated": true,
                                "description": "Deprectated, use images api"
                              },
                              "taxId": {
                                "type": "string",
                                "nullable": true,
                                "description": "Unit Local Tax ID, may be used for compliance."
                              },
                              "localOffice": {
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
                                    "type": "string"
                                  },
                                  "latitude": {
                                    "type": "string"
                                  },
                                  "longitude": {
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
                                  "postalCode": {
                                    "type": "string"
                                  },
                                  "country": {
                                    "type": "string"
                                  }
                                }
                              },
                              "regulations": {
                                "type": "array",
                                "deprecated": true,
                                "items": {
                                  "type": "object"
                                }
                              },
                              "updatedAt": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Timestamp of when this unit was last updated at. Date as ISO 8601 format"
                              }
                            }
                          }
                        }
                      }
                    },
                    "page": {
                      "type": "number"
                    },
                    "page_count": {
                      "type": "number"
                    },
                    "page_size": {
                      "type": "number"
                    },
                    "total_items": {
                      "type": "number"
                    },
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
                    }
                  },
                  "required": [
                    "_embedded",
                    "page",
                    "page_count",
                    "page_size",
                    "total_items",
                    "_links"
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
        "operationId": "getChannelUnits",
        "description": "The units available on this endpoint will either be determined by the channel setting of show all units, or enabling specific units.\n\nThe data will be flattened to show the node and the inherited values.\n\nFor query parameters, any \"boolean\" values (true / false), the system wil instead take 1 or 0, with 1 == true, and 0 == false.\n",
        "parameters": [
          {
            "schema": {
              "type": "integer",
              "maximum": 0,
              "minimum": 0
            },
            "in": "query",
            "name": "page",
            "description": "Page number of result set - Limited to 10k total results (page * size)"
          },
          {
            "schema": {
              "type": "integer"
            },
            "in": "query",
            "name": "size",
            "description": "Size of page - Limited to 10k total results (page * size)"
          },
          {
            "schema": {
              "type": "string",
              "default": "name",
              "enum": [
                "id",
                "name",
                "nodeName",
                "unitTypeName"
              ]
            },
            "in": "query",
            "name": "sortColumn",
            "description": "Column to sort the result set."
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
            "description": "Direction to sort result set."
          },
          {
            "schema": {
              "oneOf": [
                {
                  "title": "Single Node",
                  "type": "integer"
                },
                {
                  "title": "Multiple Nodes",
                  "type": "array",
                  "items": {
                    "type": "integer"
                  }
                }
              ]
            },
            "in": "query",
            "name": "nodeId",
            "description": "Return all units that are descendants of the specific node ID(s). Can be single value or array."
          },
          {
            "schema": {
              "oneOf": [
                {
                  "title": "Single Amenity",
                  "type": "integer"
                },
                {
                  "title": "Multiple Amenities",
                  "type": "array",
                  "items": {
                    "type": "integer"
                  }
                }
              ]
            },
            "in": "query",
            "name": "amenityId",
            "description": "Return all units that have these amenity ID(s). Can be single value or array."
          },
          {
            "schema": {
              "oneOf": [
                {
                  "title": "Single Unit Type",
                  "type": "integer"
                },
                {
                  "title": "Multiple Unit Types",
                  "type": "array",
                  "items": {
                    "type": "integer"
                  }
                }
              ]
            },
            "in": "query",
            "name": "unitTypeId",
            "description": "Return all units of the specific unit type(s). Can be single value or array."
          },
          {
            "schema": {
              "type": "string",
              "format": "date-time"
            },
            "in": "query",
            "name": "contentUpdatedSince",
            "description": "Date in ISO 8601 format. Will return all units with content changes since timestamp."
          },
          {
            "schema": {
              "type": "string",
              "format": "date"
            },
            "in": "query",
            "name": "updatedSince",
            "deprecated": true,
            "description": "Date in ISO 8601 format. Will return all units updated since timestamp. @deprecated use contentUpdatedSince."
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "search",
            "description": "substring search matching on name or descriptions"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "term",
            "description": "substring search matching on term"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "unitCode",
            "description": "search on unitCode, exact match or add % for wildcard"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "shortName",
            "description": "search on shortName, exact match or add % for wildcard"
          },
          {
            "schema": {
              "type": "integer"
            },
            "in": "query",
            "name": "minBedrooms",
            "description": "Return all units with this or more number of bedrooms"
          },
          {
            "schema": {
              "type": "integer"
            },
            "in": "query",
            "name": "maxBedrooms",
            "description": "Return all units with this or less number of bedrooms"
          },
          {
            "schema": {
              "type": "integer"
            },
            "in": "query",
            "name": "bedrooms",
            "description": "Return all units with this exact number of bedrooms."
          },
          {
            "schema": {
              "type": "integer"
            },
            "in": "query",
            "name": "minBathrooms",
            "description": "Return all units with this exact number of bathrooms."
          },
          {
            "schema": {
              "type": "integer"
            },
            "in": "query",
            "name": "maxBathrooms",
            "description": "Return all units with this exact number of bathrooms."
          },
          {
            "schema": {
              "type": "integer"
            },
            "in": "query",
            "name": "bathrooms",
            "description": "Return all units with this exact number of bathrooms."
          },
          {
            "schema": {
              "type": "integer"
            },
            "in": "query",
            "name": "calendarId",
            "description": "Return all units matching this unit's type with calendar group id"
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
            "name": "petsFriendly",
            "description": "Return all units that are pet friendly"
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
            "name": "allowUnitRates",
            "description": "Return all units who's type allows unit rates"
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
            "name": "computed",
            "description": "Return additional computed values attributes based on inherited attributes. 1 == true, 0 == false."
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
            "name": "inherited",
            "description": "Return additional inherited attributes. 1 == true, 0 == false."
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
            "name": "limited",
            "description": "Return very limited attributes ( id, name, longitude latitude, isActive )"
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
            "name": "isBookable",
            "description": "Return all bookable units"
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
            "name": "includeDescriptions",
            "description": "Return descriptions of units, may be inherited from node if set to inherited. 1 == true, 0 == false. If using channel keys, descriptions will always be returned."
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
            "name": "isActive",
            "description": "Return active (true), inactive (false), or all (null) units"
          },
          {
            "schema": {
              "type": "string",
              "format": "date"
            },
            "in": "query",
            "name": "arrival",
            "description": "Date in ISO 8601 format. Will return all units available between this and departure"
          },
          {
            "schema": {
              "type": "string",
              "format": "date"
            },
            "in": "query",
            "name": "departure",
            "description": "Date in ISO 8601 format. Will return all units available between this and arrival"
          },
          {
            "schema": {
              "type": "integer"
            },
            "in": "query",
            "name": "roleId",
            "description": "Return units by is a specific roleId is being used."
          },
          {
            "schema": {
              "type": "array",
              "items": {
                "type": "integer"
              }
            },
            "in": "query",
            "name": "id",
            "description": "Filter by Unit IDs."
          },
          {
            "schema": {
              "type": "string",
              "enum": [
                "clean",
                "dirty",
                "occupied",
                "inspection",
                "inprogress"
              ]
            },
            "in": "query",
            "name": "unitStatus",
            "description": "filter by unit status"
          }
        ],
        "tags": [
          "Units"
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
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": true
  }
}
```


