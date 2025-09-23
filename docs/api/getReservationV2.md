Get Reservation V2

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
      "description": "Endpoints which provide unit type data and information."
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
    "/v2/pms/reservations/{reservationId}": {
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
        "summary": "Get Reservation V2",
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
                    "alternates": {
                      "type": "array",
                      "description": "Alternate Confirmation ID's"
                    },
                    "currency": {
                      "type": "string",
                      "description": "Currency that this reservation uses."
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
                      "description": "Date as ISO 8601 format with timestamp"
                    },
                    "departureTime": {
                      "type": "string",
                      "format": "date-time",
                      "description": "Date as ISO 8601 format with timestamp"
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
                      "description": "Date as ISO 8601 format with timestamp."
                    },
                    "occupants": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "typeId": {
                            "type": "integer"
                          },
                          "name": {
                            "type": "string"
                          },
                          "handle": {
                            "type": "string"
                          },
                          "quantity": {
                            "type": "number"
                          },
                          "included": {
                            "type": "boolean",
                            "description": "How many of this occupant are included in rent price."
                          },
                          "extraQuantity": {
                            "type": "number",
                            "description": "How many extra occupants are allowed on top of included number."
                          },
                          "ratePerPersonPerStay": {
                            "type": "string",
                            "description": "Rate (in local currency) that will be charged per extra occupant per night per occupant."
                          },
                          "ratePerStay": {
                            "type": "string",
                            "description": "Rate (in local currency) that will be charged for the stay if any extra occupants (up to max) are added."
                          }
                        }
                      }
                    },
                    "securityDeposit": {
                      "type": "object",
                      "properties": {
                        "required": {
                          "type": "string"
                        }
                      }
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
                    "bookedAt": {
                      "type": "string",
                      "format": "date-time",
                      "description": "Date time in ISO 8601 format"
                    },
                    "guestBreakdown": {
                      "type": "object",
                      "properties": {
                        "grossRent": {
                          "type": "string",
                          "description": "Value in number format (X.XX), overall rent value, before discounts."
                        },
                        "guestGrossDisplayRent": {
                          "type": "string",
                          "description": "Value in number format (X.XX), rent value that will be displayed to guest."
                        },
                        "discount": {
                          "type": "string",
                          "description": "Value in number format (X.XX), overall discount value applied to reservation. Displays as negative value."
                        },
                        "promoValue": {
                          "type": "string",
                          "description": "Value in number format (X.XX), overall promo code value applied to reservation. Displays as positive value."
                        },
                        "discountTotal": {
                          "type": "number",
                          "description": "Sum of discount + promo values. Displays as negative value."
                        },
                        "netRent": {
                          "type": "string",
                          "description": "Value in number format (X.XX), Rent after discounts or credits."
                        },
                        "guestNetDisplayRent": {
                          "type": "string",
                          "description": "Value in number format (X.XX), Net rent value displayed to guest."
                        },
                        "actualAdr": {
                          "type": "string",
                          "description": "Value in number format (X.XX), actual Average Daily Rate."
                        },
                        "guestAdr": {
                          "type": "string",
                          "description": "Value in number format (X.XX), guest Average Daily Rate."
                        },
                        "totalGuestFees": {
                          "type": "string",
                          "description": "Value in number format (X.XX), Combined value of guest fees."
                        },
                        "totalRentFees": {
                          "type": "string",
                          "description": "Value in number format (X.XX), Combined value of rent fees."
                        },
                        "totalItemizedFees": {
                          "type": "string",
                          "description": "Value in number format (X.XX), Combined value of itemized fees."
                        },
                        "totalTaxFees": {
                          "type": "string",
                          "description": "Value in number format (X.XX), Combined value of tax fees."
                        },
                        "totalServiceFees": {
                          "type": "string",
                          "description": "Value in number format (X.XX). Combined value of service fee."
                        },
                        "folioCharges": {
                          "type": "string",
                          "description": "Value in number format (X.XX)."
                        },
                        "subtotal": {
                          "type": "string",
                          "description": "Value in number format (X.XX)."
                        },
                        "guestSubtotal": {
                          "type": "string",
                          "description": "Value in number format (X.XX), Subtotal that will be displayed to guest."
                        },
                        "totalTaxes": {
                          "type": "string",
                          "description": "Value in number format (X.XX)."
                        },
                        "totalGuestTaxes": {
                          "type": "string",
                          "description": "Value in number format (X.XX)."
                        },
                        "total": {
                          "type": "string",
                          "description": "Value in number format (X.XX)."
                        },
                        "grandTotal": {
                          "type": "string",
                          "description": "Value in number format (X.XX)."
                        },
                        "netPayments": {
                          "type": "string",
                          "description": "Value in number format (X.XX)."
                        },
                        "payments": {
                          "type": "string",
                          "description": "Value in number format (X.XX)."
                        },
                        "refunds": {
                          "type": "string",
                          "description": "Value in number format (X.XX)."
                        },
                        "netTransfers": {
                          "type": "string",
                          "description": "Value in number format (X.XX). Overall value of transfers into or out of this folio to other folios."
                        },
                        "balance": {
                          "type": "string",
                          "description": "Value in number format (X.XX). Balance of reservation / folio. Negative value signifies overpayment that should be refunded."
                        },
                        "rates": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "date": {
                                "type": "string",
                                "format": "date",
                                "description": "Date in ISO 8601 date format. No Timestamp."
                              },
                              "rate": {
                                "type": "string",
                                "description": "Value in number format (X.XX)."
                              },
                              "nights": {
                                "type": "integer",
                                "description": "number of nights this rate is applied for."
                              },
                              "isQuoted": {
                                "type": "boolean"
                              }
                            }
                          }
                        },
                        "guestFees": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "id": {
                                "type": "string",
                                "description": "ID of fee."
                              },
                              "name": {
                                "type": "string"
                              },
                              "displayAs": {
                                "type": "string",
                                "enum": [
                                  "itemize",
                                  "rent",
                                  "tax",
                                  "service"
                                ]
                              },
                              "quantity": {
                                "type": "string"
                              },
                              "unitValue": {
                                "type": "string",
                                "description": "Value in number format (X.XX). Value per fee."
                              },
                              "value": {
                                "type": "string",
                                "description": "Value in number format (X.XX). Total value of fee, unitValue * quantity."
                              }
                            }
                          }
                        },
                        "taxes": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "id": {
                                "type": "integer"
                              },
                              "name": {
                                "type": "string"
                              },
                              "amount": {
                                "type": "string",
                                "description": "Value in number format (X.XX)."
                              }
                            }
                          }
                        }
                      }
                    },
                    "type": {
                      "type": "object",
                      "properties": {
                        "id": {
                          "type": "integer"
                        },
                        "name": {
                          "type": "string"
                        }
                      }
                    },
                    "guaranteePolicy": {
                      "type": "object",
                      "properties": {
                        "id": {
                          "type": "integer"
                        },
                        "name": {
                          "type": "string"
                        },
                        "type": {
                          "type": "string",
                          "enum": [
                            "Hold",
                            "Guarantee",
                            "FullDeposit"
                          ]
                        },
                        "hold": {
                          "type": "object",
                          "properties": {
                            "limit": {
                              "type": "integer"
                            }
                          }
                        }
                      }
                    },
                    "cancellationPolicy": {
                      "type": "object",
                      "properties": {
                        "id": {
                          "type": "integer"
                        },
                        "name": {
                          "type": "string"
                        },
                        "time": {
                          "type": "string",
                          "description": "Time in HH:MM format."
                        },
                        "timezone": {
                          "type": "string",
                          "description": "Timezone in format \"Country/Locality\""
                        },
                        "breakpoints": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "start": {
                                "type": "integer"
                              },
                              "end": {
                                "type": "integer"
                              },
                              "nonRefundable": {
                                "type": "boolean"
                              },
                              "nonCancelable": {
                                "type": "boolean"
                              },
                              "penaltyNights": {
                                "type": "integer"
                              },
                              "penaltyPercent": {
                                "type": "string",
                                "description": "Percentage in format (6% == 6.00)."
                              },
                              "penaltyFlat": {
                                "type": "string",
                                "description": "Value in number format (X.XX)."
                              },
                              "description": {
                                "type": "string"
                              }
                            }
                          }
                        }
                      }
                    },
                    "paymentPlan": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "date": {
                            "type": "string",
                            "format": "date",
                            "description": "Date in ISO 8601 format, no timestamp."
                          },
                          "amount": {
                            "type": "string",
                            "description": "Value in number format (X.XX)."
                          }
                        }
                      }
                    },
                    "rateType": {
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
                    "travelInsuranceProducts": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "integer"
                          },
                          "status": {
                            "type": "string",
                            "enum": [
                              "optin",
                              "funded",
                              "cancelled"
                            ]
                          },
                          "type": {
                            "type": "string",
                            "enum": [
                              "Travel Insurance",
                              "Master Cancel",
                              "Damage Deposit"
                            ]
                          },
                          "provider": {
                            "type": "string"
                          },
                          "providerId": {
                            "type": "integer"
                          },
                          "amount": {
                            "type": "string"
                          }
                        }
                      }
                    },
                    "_embedded": {
                      "type": "object",
                      "properties": {
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
                            "shortName": {
                              "type": "string"
                            },
                            "unitCode": {
                              "type": "string"
                            },
                            "headline": {
                              "type": "string",
                              "nullable": true
                            },
                            "shortDescription": {
                              "type": "string"
                            },
                            "longDescription": {
                              "type": "string"
                            },
                            "houseRules": {
                              "type": "string",
                              "nullable": true
                            },
                            "nodeId": {
                              "type": "integer"
                            },
                            "unitType": {
                              "type": "object",
                              "properties": {
                                "id": {
                                  "type": "integer"
                                },
                                "name": {
                                  "type": "string"
                                }
                              }
                            },
                            "lodgingType": {
                              "type": "object",
                              "properties": {
                                "id": {
                                  "type": "integer"
                                },
                                "name": {
                                  "type": "string"
                                }
                              }
                            },
                            "directions": {
                              "type": "string",
                              "nullable": true
                            },
                            "checkinDetails": {
                              "type": "string",
                              "nullable": true
                            },
                            "timezone": {
                              "type": "string",
                              "description": "Timezone in format \"Country/Locality\""
                            },
                            "checkinTime": {
                              "type": "string",
                              "description": "Default check-in time (in unit timezone)"
                            },
                            "hasEarlyCheckin": {
                              "type": "boolean",
                              "description": "If unit allows early checkin."
                            },
                            "earlyCheckinTime": {
                              "type": "string",
                              "description": "Requires hasEarlyCheckin. Time in unit timezone. Format \"HH:MM\""
                            },
                            "checkoutTime": {
                              "type": "string",
                              "description": "Default check-in time (in unit timezone)"
                            },
                            "hasLateCheckout": {
                              "type": "boolean",
                              "description": "If unit allows late checkout."
                            },
                            "lateCheckoutTime": {
                              "type": "string",
                              "description": "Requires hasEarlyCheckin. Time in unit timezone. Format \"HH:MM\""
                            },
                            "minBookingWindow": {
                              "type": "integer"
                            },
                            "maxBookingWindow": {
                              "type": "integer"
                            },
                            "website": {
                              "type": "string",
                              "description": "Custom URL provided that directs to unit website.",
                              "nullable": true
                            },
                            "phone": {
                              "type": "string",
                              "nullable": true
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
                            "postalCode": {
                              "type": "string"
                            },
                            "country": {
                              "type": "string",
                              "description": "In 2 character format. Ex- \"US\""
                            },
                            "longitude": {
                              "type": "number",
                              "description": "Location longitude"
                            },
                            "latitude": {
                              "type": "number",
                              "description": "Location latitude"
                            },
                            "petsFriendly": {
                              "type": "boolean"
                            },
                            "maxPets": {
                              "type": "integer"
                            },
                            "eventsAllowed": {
                              "type": "boolean"
                            },
                            "smokingAllowed": {
                              "type": "boolean"
                            },
                            "childrenAllowed": {
                              "type": "boolean"
                            },
                            "minimumAgeLimit": {
                              "type": "integer",
                              "nullable": true
                            },
                            "isAccessible": {
                              "type": "boolean"
                            },
                            "area": {
                              "type": "number",
                              "nullable": true
                            },
                            "floors": {
                              "type": "number",
                              "nullable": true
                            },
                            "maxOccupancy": {
                              "type": "integer"
                            },
                            "securityDeposit": {
                              "type": "string",
                              "description": "Default security deposit amount for unit."
                            },
                            "bedrooms": {
                              "type": "integer"
                            },
                            "fullBathrooms": {
                              "type": "integer"
                            },
                            "threeQuarterBathrooms": {
                              "type": "integer"
                            },
                            "halfBathrooms": {
                              "type": "integer"
                            },
                            "bedTypes": {
                              "type": "array",
                              "description": "If roomConfiguration is true.",
                              "items": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "integer"
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
                              "items": {
                                "type": "object",
                                "properties": {
                                  "name": {
                                    "type": "string"
                                  },
                                  "type": {
                                    "type": "string"
                                  },
                                  "sleeps": {
                                    "type": "integer"
                                  },
                                  "description": {
                                    "type": "string"
                                  },
                                  "hasAttachedBathroom": {
                                    "type": "boolean"
                                  },
                                  "order": {
                                    "type": "integer",
                                    "nullable": true
                                  },
                                  "airbnbType": {
                                    "type": "string"
                                  },
                                  "marriottType": {
                                    "type": "string"
                                  },
                                  "homeawayType": {
                                    "type": "string"
                                  },
                                  "bedTypes": {
                                    "type": "array",
                                    "items": {
                                      "type": "object",
                                      "properties": {
                                        "id": {
                                          "type": "integer"
                                        },
                                        "name": {
                                          "type": "string"
                                        },
                                        "count": {
                                          "type": "integer"
                                        },
                                        "airbnbType": {
                                          "type": "string"
                                        },
                                        "marriottType": {
                                          "type": "string"
                                        },
                                        "homeawayType": {
                                          "type": "string"
                                        }
                                      }
                                    }
                                  }
                                }
                              }
                            },
                            "amenities": {
                              "type": "array",
                              "items": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "integer"
                                  },
                                  "name": {
                                    "type": "string"
                                  },
                                  "group": {
                                    "type": "object",
                                    "properties": {
                                      "id": {
                                        "type": "integer"
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
                              "type": "string"
                            },
                            "coverImage": {
                              "type": "string",
                              "description": "Link to image"
                            },
                            "taxId": {
                              "type": "integer"
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
                              "items": {
                                "type": "object",
                                "properties": {
                                  "body": {
                                    "type": "string"
                                  },
                                  "params": {
                                    "type": "string"
                                  }
                                }
                              }
                            },
                            "updated": {
                              "type": "object",
                              "properties": {
                                "availability": {
                                  "type": "string",
                                  "format": "date-time",
                                  "description": "Date-time in ISO 8601 format."
                                },
                                "content": {
                                  "type": "string",
                                  "format": "date-time",
                                  "description": "Date-time in ISO 8601 format."
                                },
                                "pricing": {
                                  "type": "string",
                                  "format": "date-time",
                                  "description": "Date-time in ISO 8601 format."
                                }
                              }
                            },
                            "updatedAt": {
                              "type": "string",
                              "format": "date-time",
                              "description": "Date-time in ISO 8601 format."
                            },
                            "createdAt": {
                              "type": "string",
                              "format": "date-time",
                              "description": "Date-time in ISO 8601 format."
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
                        "contact": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "integer"
                            },
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
                            "isDNR": {
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
                        "cancel": {
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
        "operationId": "getChannelReservationV2",
        "description": "This endpoint will return all reservation of reservationId provided."
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