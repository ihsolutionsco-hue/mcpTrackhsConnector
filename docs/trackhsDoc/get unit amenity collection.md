Unit Amenity Collection

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
    "/pms/units/amenities": {
      "get": {
        "summary": "Unit Amenity Collection",
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
                                "type": "integer"
                              },
                              "groupName": {
                                "type": "string"
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
                },
                "examples": {
                  "Example Response": {
                    "value": {
                      "_links": {
                        "self": {
                          "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/?page=1"
                        },
                        "first": {
                          "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/"
                        },
                        "last": {
                          "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/?page=8"
                        },
                        "next": {
                          "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/?page=2"
                        }
                      },
                      "_embedded": {
                        "amenities": [
                          {
                            "id": 1,
                            "name": "Air Conditioning",
                            "groupId": 1,
                            "groupName": "Additional Amenities",
                            "homeawayType": "AMENITIES_AIR_CONDITIONING",
                            "airbnbType": "ac",
                            "tripadvisorType": "AIR_CONDITIONING",
                            "updatedAt": "2020-08-25T12:41:07-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/1/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/1/"
                              }
                            }
                          },
                          {
                            "id": 2,
                            "name": "Fenced Yard",
                            "groupId": 4,
                            "groupName": "Outdoor",
                            "homeawayType": "",
                            "airbnbType": "",
                            "tripadvisorType": "",
                            "updatedAt": "2020-05-05T16:39:06-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/2/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/4/"
                              }
                            }
                          },
                          {
                            "id": 3,
                            "name": "Ground Level",
                            "groupId": 1,
                            "groupName": "Additional Amenities",
                            "homeawayType": "",
                            "airbnbType": "single_level_home",
                            "tripadvisorType": "",
                            "updatedAt": "2020-05-12T10:00:19-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/3/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/1/"
                              }
                            }
                          },
                          {
                            "id": 4,
                            "name": "Pool",
                            "groupId": 2,
                            "groupName": "Pool",
                            "homeawayType": "POOL_SPA_PRIVATE_POOL",
                            "airbnbType": "pool",
                            "tripadvisorType": "UNHEATED_OUTDOOR_POOL_PRIVATE",
                            "updatedAt": "2020-05-12T10:27:41-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/4/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/2/"
                              }
                            }
                          },
                          {
                            "id": 5,
                            "name": "Hot Tub",
                            "groupId": 2,
                            "groupName": "Pool",
                            "homeawayType": "POOL_SPA_HOT_TUB",
                            "airbnbType": "",
                            "tripadvisorType": "",
                            "updatedAt": "2020-05-07T07:40:02-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/5/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/2/"
                              }
                            }
                          },
                          {
                            "id": 6,
                            "name": "Elevator",
                            "groupId": 1,
                            "groupName": "Additional Amenities",
                            "homeawayType": "AMENITIES_ELEVATOR",
                            "airbnbType": "elevator",
                            "tripadvisorType": "ELEVATOR_IN_BUILDING",
                            "updatedAt": "2020-04-04T21:36:59-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/6/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/1/"
                              }
                            }
                          },
                          {
                            "id": 7,
                            "name": "Fireplace",
                            "groupId": 1,
                            "groupName": "Additional Amenities",
                            "homeawayType": "AMENITIES_FIREPLACE",
                            "airbnbType": "fireplace",
                            "tripadvisorType": "FIREPLACE",
                            "updatedAt": "2020-04-04T22:36:37-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/7/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/1/"
                              }
                            }
                          },
                          {
                            "id": 8,
                            "name": "Coin-Operated Washer Dryer",
                            "groupId": 6,
                            "groupName": "Bathroom & Laundry",
                            "homeawayType": "ATTRACTIONS_COIN_LAUNDRY",
                            "airbnbType": "washer",
                            "tripadvisorType": "WASHING_MACHINE",
                            "updatedAt": "2020-05-12T10:23:18-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/8/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/6/"
                              }
                            }
                          },
                          {
                            "id": 9,
                            "name": "In Unit Washer & Dryer",
                            "groupId": 6,
                            "groupName": "Bathroom & Laundry",
                            "homeawayType": "AMENITIES_WASHER",
                            "airbnbType": "washer",
                            "tripadvisorType": "WASHING_MACHINE",
                            "updatedAt": "2020-05-07T07:41:54-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/9/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/6/"
                              }
                            }
                          },
                          {
                            "id": 10,
                            "name": "Shared Washer Dryer",
                            "groupId": 6,
                            "groupName": "Bathroom & Laundry",
                            "homeawayType": "AMENITIES_WASHER",
                            "airbnbType": "washer",
                            "tripadvisorType": "WASHING_MACHINE",
                            "updatedAt": "2020-05-12T10:04:36-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/10/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/6/"
                              }
                            }
                          },
                          {
                            "id": 11,
                            "name": "Television",
                            "groupId": 7,
                            "groupName": "Entertainment",
                            "homeawayType": "ENTERTAINMENT_TELEVISION",
                            "airbnbType": "tv",
                            "tripadvisorType": "TV",
                            "updatedAt": "2020-05-07T07:42:42-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/11/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/7/"
                              }
                            }
                          },
                          {
                            "id": 12,
                            "name": "Smart Television",
                            "groupId": 7,
                            "groupName": "Entertainment",
                            "homeawayType": "ENTERTAINMENT_TELEVISION",
                            "airbnbType": "tv",
                            "tripadvisorType": "TV",
                            "updatedAt": "2020-05-07T07:43:02-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/12/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/7/"
                              }
                            }
                          },
                          {
                            "id": 14,
                            "name": "WIFI",
                            "groupId": 1,
                            "groupName": "Additional Amenities",
                            "homeawayType": "AMENITIES_INTERNET",
                            "airbnbType": "wireless_internet",
                            "tripadvisorType": "WIFI",
                            "updatedAt": "2020-05-07T07:43:25-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/14/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/1/"
                              }
                            }
                          },
                          {
                            "id": 15,
                            "name": "Exercise Room",
                            "groupId": 1,
                            "groupName": "Additional Amenities",
                            "homeawayType": "AMENITIES_FITNESS_ROOM",
                            "airbnbType": "gym",
                            "tripadvisorType": "GYM",
                            "updatedAt": "2020-04-04T22:57:22-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/15/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/1/"
                              }
                            }
                          },
                          {
                            "id": 16,
                            "name": "Air Hockey Table",
                            "groupId": 7,
                            "groupName": "Entertainment",
                            "homeawayType": "ENTERTAINMENT_GAMES",
                            "airbnbType": "",
                            "tripadvisorType": "",
                            "updatedAt": "2020-05-19T10:41:02-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/16/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/7/"
                              }
                            }
                          },
                          {
                            "id": 17,
                            "name": "Basketball Hoop",
                            "groupId": 7,
                            "groupName": "Entertainment",
                            "homeawayType": "SPORTS_BASKETBALL_COURT",
                            "airbnbType": "",
                            "tripadvisorType": "",
                            "updatedAt": "2020-05-12T10:09:36-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/17/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/7/"
                              }
                            }
                          },
                          {
                            "id": 18,
                            "name": "Cornhole Set",
                            "groupId": 7,
                            "groupName": "Entertainment",
                            "homeawayType": "ENTERTAINMENT_GAMES",
                            "airbnbType": "",
                            "tripadvisorType": "",
                            "updatedAt": "2020-05-19T11:22:39-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/18/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/7/"
                              }
                            }
                          },
                          {
                            "id": 19,
                            "name": "Darts",
                            "groupId": 7,
                            "groupName": "Entertainment",
                            "homeawayType": "ENTERTAINMENT_GAMES",
                            "airbnbType": "",
                            "tripadvisorType": "",
                            "updatedAt": "2020-05-19T13:33:29-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/19/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/7/"
                              }
                            }
                          },
                          {
                            "id": 20,
                            "name": "Bocce Ball",
                            "groupId": 7,
                            "groupName": "Entertainment",
                            "homeawayType": "ENTERTAINMENT_GAMES",
                            "airbnbType": "",
                            "tripadvisorType": "",
                            "updatedAt": "2020-05-19T11:20:19-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/20/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/7/"
                              }
                            }
                          },
                          {
                            "id": 22,
                            "name": "Foosball",
                            "groupId": 7,
                            "groupName": "Entertainment",
                            "homeawayType": "ENTERTAINMENT_FOOSBALL",
                            "airbnbType": "",
                            "tripadvisorType": "",
                            "updatedAt": "2020-05-12T10:12:07-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/22/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/7/"
                              }
                            }
                          },
                          {
                            "id": 23,
                            "name": "Ping Pong",
                            "groupId": 7,
                            "groupName": "Entertainment",
                            "homeawayType": "ENTERTAINMENT_PING_PONG_TABLE",
                            "airbnbType": "",
                            "tripadvisorType": "PING_PONG_TABLE",
                            "updatedAt": "2020-05-12T10:12:32-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/23/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/7/"
                              }
                            }
                          },
                          {
                            "id": 24,
                            "name": "Pool Table",
                            "groupId": 7,
                            "groupName": "Entertainment",
                            "homeawayType": "ENTERTAINMENT_POOL_TABLE",
                            "airbnbType": "",
                            "tripadvisorType": "POOL_TABLE",
                            "updatedAt": "2020-05-12T10:13:01-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/24/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/7/"
                              }
                            }
                          },
                          {
                            "id": 25,
                            "name": "X-Box",
                            "groupId": 7,
                            "groupName": "Entertainment",
                            "homeawayType": "ENTERTAINMENT_VIDEO_GAMES",
                            "airbnbType": "",
                            "tripadvisorType": "",
                            "updatedAt": "2020-05-12T10:13:56-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/25/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/7/"
                              }
                            }
                          },
                          {
                            "id": 26,
                            "name": "Putting Green",
                            "groupId": 7,
                            "groupName": "Entertainment",
                            "homeawayType": "",
                            "airbnbType": "",
                            "tripadvisorType": "",
                            "updatedAt": "2020-05-12T10:14:28-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/26/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/7/"
                              }
                            }
                          },
                          {
                            "id": 27,
                            "name": "Game Room",
                            "groupId": 7,
                            "groupName": "Entertainment",
                            "homeawayType": "AMENITIES_GAME_ROOM",
                            "airbnbType": "",
                            "tripadvisorType": "",
                            "updatedAt": "2020-05-12T10:15:19-04:00",
                            "_links": {
                              "self": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenities/27/"
                              },
                              "group": {
                                "href": "https://api-integration-example.tracksandbox.io/api/pms/units/amenity-groups/7/"
                              }
                            }
                          }
                        ]
                      },
                      "page_count": 8,
                      "page_size": 25,
                      "total_items": 185,
                      "page": 1
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
        "operationId": "getUnitamenities",
        "description": "Return all amenities assigned to a given unit. The computed flag will return a set of amenities that encompasses the entire tree.",
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