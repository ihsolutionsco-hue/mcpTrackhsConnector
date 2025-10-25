Unit

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
    "/pms/units/{unitId}": {
      "parameters": [
        {
          "name": "unitId",
          "in": "path",
          "required": true,
          "schema": {
            "type": "number"
          },
          "description": "Unit ID"
        }
      ],
      "get": {
        "summary": "Unit",
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
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
                },
                "examples": {
                  "Example Response": {
                    "value": {
                      "id": 7,
                      "name": "Townhomes 444",
                      "shortName": "TH444",
                      "unitCode": "TH444",
                      "headline": "",
                      "shortDescription": "Short description of your unit!",
                      "houseRules": "Rules for this unit are as follows:\nPets are allowed (ONE DOG ONLY)\n*Additional pet fees apply\nSmoking is not permitted.\nChildren are allowed.\nThe minimum age limit for this unit is 25.",
                      "nodeId": 81,
                      "unitType": {
                        "id": 32,
                        "name": "3 - NW"
                      },
                      "lodgingType": {
                        "id": 3,
                        "name": "Townhome"
                      },
                      "directions": "1) Exit parking lot toward Lanes Ave. 2) Follow Lanes Ave for 4 miles and turn right on Kings Street. 3) Follow Kings Street for 1 mile until you reach the New Richmond sign. Turn right at the sign, and you have reached your destination.",
                      "checkinDetails": "Wifi Information:\nSSID: wifiName\nPassword: wifiPassword",
                      "timezone": "America/Denver",
                      "checkinTime": "16:00:00",
                      "hasEarlyCheckin": true,
                      "earlyCheckinTime": "12:00:00",
                      "checkoutTime": "10:00:00",
                      "hasLateCheckout": true,
                      "lateCheckoutTime": "12:00:00",
                      "website": "https://www.sandbox.com/rentals/townhomes-444-at-north-sandbox",
                      "phone": "5557778888",
                      "streetAddress": "444 Ave.",
                      "extendedAddress": null,
                      "locality": "New Richmond",
                      "region": "WI",
                      "postal": "54017",
                      "country": "US",
                      "latitude": null,
                      "longitude": null,
                      "petsFriendly": true,
                      "maxPets": 1,
                      "eventsAllowed": false,
                      "smokingAllowed": false,
                      "childrenAllowed": true,
                      "minimumAgeLimit": 25,
                      "isAccessible": false,
                      "area": 1637,
                      "floors": null,
                      "maxOccupancy": 12,
                      "bedrooms": 3,
                      "fullBathrooms": 3,
                      "threeQuarterBathrooms": null,
                      "halfBathrooms": 0,
                      "bedTypes": [
                        {
                          "id": 3,
                          "name": "King Bed",
                          "count": 2
                        },
                        {
                          "id": 4,
                          "name": "Full Bed",
                          "count": 2
                        },
                        {
                          "id": 6,
                          "name": "Queen Sofa Sleeper",
                          "count": 1
                        },
                        {
                          "id": 23,
                          "name": "Queen Futon",
                          "count": 1
                        }
                      ],
                      "rooms": [],
                      "amenities": [
                        {
                          "id": 4,
                          "name": "Fridge - Full Size",
                          "group": {
                            "id": 1,
                            "name": "Kitchen & Cooking"
                          }
                        },
                        {
                          "id": 16,
                          "name": "Range - Electric",
                          "group": {
                            "id": 1,
                            "name": "Kitchen & Cooking"
                          }
                        },
                        {
                          "id": 120,
                          "name": "DVDs",
                          "group": {
                            "id": 5,
                            "name": "Entertainment"
                          }
                        }
                      ],
                      "amenityDescription": "1st Floor",
                      "custom": {
                        "22": "Parking is unassigned outside in the parking lot. Only one vehicle is allowed per townhome. Overflow parking is available in the Keystone Lodge and Spa Lot on Highway 6. Vehicles parking without a parking permit will be ticketed or towed at the owner's expense.",
                        "27": "The outdoor pool, covered hot tub and sauna are located on the south side of the complex near the tennis center. Follow the walkway towards the tennis center and lodge parking lot. Changing rooms and showers are available and towels are provided. Hours are from 8am to 10pm.",
                        "33": "From November through April, a free Keystone Resort shuttle picks up three times per hour at the shuttle stops on either side of the Tennis Townhomes complex. You are on the silver route. For more information or to request an on call shuttle please call Keystone Transportation at 970-496-4200."
                      },
                      "taxId": null,
                      "updatedAt": "2020-05-21T22:30:18-06:00",
                      "_links": {
                        "self": {
                          "href": "https://api-integration-example.tracksandbox.io/api/pms/units/7/"
                        },
                        "images": {
                          "href": "https://api-integration-example.tracksandbox.io/api/pms/units/7/images/"
                        },
                        "policies": {
                          "href": "https://api-integration-example.tracksandbox.io/api/pms/units/7/policies/"
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
        "description": "This will return a single unit based on the unitId provided in the path.",
        "operationId": "getChannelUnit",
        "tags": [
          "Units"
        ],
        "parameters": [
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
            "name": "includeDescriptions",
            "description": "Return descriptions of units, may be inherited from node if set to inherited. 1 == true, 0 == false. If using channel keys, descriptions will always be returned."
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
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": true
  }
}
```