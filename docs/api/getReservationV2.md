Get Reservation V2

# OpenAPI definition
```json
{
  "_id": "/branches/1.0/apis/pms-reservations-v2-api.json",
  "openapi": "3.0.0",
  "info": {
    "title": "PMS Reservations V2 API",
    "version": "2.0",
    "description": "The full PMS API is large, as such we have broken down the files into related components. Since some of the components may share model files, models are referenced instead of embedded.\n\nThis API covers all endpoints related to unit, unit type and node configuration.\n\nCertain functions of this endpoint are limited in channel and certain user contexts (based on roles)\n\nAll functions will be available to server key contexts.\n",
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
                  "title": "Reservation Response V2 - Server",
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
                    "clientIPAddress": {
                      "type": "string",
                      "description": "IP address for client user making the reservation, this is used for fraud detection"
                    },
                    "session": {
                      "type": "string",
                      "description": "session data use [seon v6 agent](https://docs.seon.io/api-reference/fraud-api#javascript-agent-v6) to create system fingerprint, this is used for fraud detection"
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
                      "description": "Details of the security deposit for the reservation.",
                      "properties": {
                        "required": {
                          "type": "string",
                          "description": "Total required security deposit amount.",
                          "example": "1.00"
                        },
                        "remaining": {
                          "type": "number",
                          "description": "Remaining amount of the security deposit.",
                          "example": 1
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
                          "description": "Value in number format (X.XX). This is the total rent paid by the guest prior to any adjustment or discounts. Will be referred to Gross Rent in most cases."
                        },
                        "guestGrossDisplayRent": {
                          "type": "string",
                          "description": "Value in number format (X.XX). Some fees can be configured to part of rent, as such, those are included in “Guest Gross Display Rent” in addition to “Guest Gross Rent”. Guest Gross Display Rent = Guest Gross Rent + Guest Fees in Rent"
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
                          "description": "Value in number format (X.XX). Rent paid by the guest after any promo codes or discounts. May also be referred to as “discounted rent”. Guest Net Rent = Guest Gross Rent - Adjustment - Promo Value."
                        },
                        "guestNetDisplayRent": {
                          "type": "string",
                          "description": "Value in number format (X.XX). Some fees can be configured to part of rent, as such, those are included in “Guest Net Display Rent” in addition to “Guest Net Rent”. Guest Net Display Rent = Guest Net Rent + Guest Fees in Rent."
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
                          "description": "Value in number format (X.XX). This is a collection of all guest fees charged to the guest. Total guest feels is considered a sum of this this collection. It is however, not displayed to the guest. Total Guest Fees = Sum (Guest Fees)."
                        },
                        "totalRentFees": {
                          "type": "string",
                          "description": "Value in number format (X.XX). Sum of “Guest Fees” with a display as property set to “rent”. This value will be added to rent values when display to the guest with “Guest Gross Display Rent” and “Guest Net Display Rent”. Total Guest Fees = SUM (Guest Fees with Display As \"rent\")."
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
                    "ownerBreakdown": {
                      "type": "object",
                      "properties": {
                        "grossRent": {
                          "type": "string",
                          "description": "Value in number format (X.XX). “Owner Gross Rent” is calculated from “Guest Net Rent” with Travel Agent Commission - If “Deduct from Gross Rent” is enabled and booking fees removed."
                        },
                        "feeRevenue": {
                          "type": "string",
                          "description": "Value in number format (X.XX)."
                        },
                        "grossRevenue": {
                          "type": "string",
                          "description": "Value in number format (X.XX)."
                        },
                        "managerCommission": {
                          "type": "string",
                          "description": "Value in number format (X.XX)."
                        },
                        "agentCommission": {
                          "type": "string",
                          "description": "Value in number format (X.XX). Travel agent commission only applies if the reservation related to a travel agent that receives commission, otherwise this is 0.\n\nTravel agent commission is based on “Guest Net Rent” as far as the value of this is concerned. However, there are a number of settings that may affect how this applies to owner revenue."
                        },
                        "netRevenue": {
                          "type": "string",
                          "description": "Value in number format (X.XX)."
                        },
                        "ownerFees": {
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
                        }
                      }
                    },
                    "discountReasonId": {
                      "type": "integer"
                    },
                    "discountNotes": {
                      "type": "string",
                      "nullable": true
                    },
                    "contactId": {
                      "type": "integer"
                    },
                    "channelId": {
                      "type": "integer"
                    },
                    "subChannel": {
                      "type": "string"
                    },
                    "folioId": {
                      "type": "integer"
                    },
                    "guaranteePolicyId": {
                      "type": "integer"
                    },
                    "cancellationPolicyId": {
                      "type": "integer"
                    },
                    "cancellationReasonId": {
                      "type": "integer"
                    },
                    "userId": {
                      "type": "integer"
                    },
                    "travelAgentId": {
                      "type": "integer"
                    },
                    "campaignId": {
                      "type": "integer"
                    },
                    "typeId": {
                      "type": "integer"
                    },
                    "rateTypeId": {
                      "type": "integer"
                    },
                    "unitCodeId": {
                      "type": "integer"
                    },
                    "cancelledById": {
                      "type": "integer"
                    },
                    "paymentMethodId": {
                      "type": "integer"
                    },
                    "quoteId": {
                      "type": "integer"
                    },
                    "holdExpiresAt": {
                      "type": "string",
                      "format": "date-time",
                      "description": "Date-time in ISO 8601 format."
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
                    "isChannelLocked": {
                      "type": "boolean"
                    },
                    "agreementStatus": {
                      "type": "string",
                      "enum": [
                        "not-needed",
                        "not-sent",
                        "sent",
                        "viewed",
                        "received"
                      ]
                    },
                    "automatePayment": {
                      "type": "boolean"
                    },
                    "revenueRealizedMethod": {
                      "type": "string"
                    },
                    "scheduleType1": {
                      "type": "string"
                    },
                    "schedulePercentage1": {
                      "type": "number"
                    },
                    "scheduleType2": {
                      "type": "string"
                    },
                    "schedulePercentage2": {
                      "type": "number"
                    },
                    "promoCodeId": {
                      "type": "integer"
                    },
                    "updatedBy": {
                      "type": "string"
                    },
                    "createdBy": {
                      "type": "string"
                    },
                    "groupId": {
                      "type": "integer"
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
                        },
                        "guaranteePolicy": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "integer"
                            },
                            "isActive": {
                              "type": "boolean"
                            },
                            "isDefault": {
                              "type": "boolean"
                            },
                            "name": {
                              "type": "string"
                            },
                            "description": {
                              "type": "string"
                            },
                            "beforeArrivalStart": {
                              "type": "integer"
                            },
                            "beforeArrivalEnd": {
                              "type": "integer"
                            },
                            "type": {
                              "type": "string",
                              "enum": [
                                "Hold",
                                "Guarantee",
                                "FullDeposit"
                              ]
                            },
                            "holdLimit": {
                              "type": "integer"
                            },
                            "depositType": {
                              "type": "string"
                            },
                            "amount": {
                              "type": "string",
                              "description": "Value in number format (X.XX)."
                            },
                            "includeTax": {
                              "type": "boolean"
                            },
                            "includeFees": {
                              "type": "boolean"
                            },
                            "includeTravelInsurance": {
                              "type": "boolean"
                            },
                            "travelInsuranceWithFirstPayment": {
                              "type": "boolean"
                            },
                            "isAutomaticCancel": {
                              "type": "boolean"
                            },
                            "includeFolioCharges": {
                              "type": "boolean"
                            },
                            "hasPaymentSchedule": {
                              "type": "boolean"
                            },
                            "priority": {
                              "type": "integer"
                            },
                            "breakpoints": {
                              "type": "array",
                              "items": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "integer"
                                  },
                                  "dueType": {
                                    "type": "string",
                                    "enum": [
                                      "at-checkin",
                                      "before-checkin",
                                      "at-booking",
                                      "after-booking"
                                    ]
                                  },
                                  "stop": {
                                    "type": "integer"
                                  },
                                  "percent": {
                                    "type": "number"
                                  },
                                  "amount": {
                                    "type": "string",
                                    "description": "Value in number format (X.XX)."
                                  },
                                  "isRemaining": {
                                    "type": "boolean"
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
                        },
                        "cancellationPolicy": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "integer"
                            },
                            "isDefault": {
                              "type": "boolean"
                            },
                            "isActive": {
                              "type": "boolean"
                            },
                            "name": {
                              "type": "string"
                            },
                            "code": {
                              "type": "string"
                            },
                            "chargeAs": {
                              "type": "string",
                              "enum": [
                                "fee",
                                "split"
                              ]
                            },
                            "canExceedBalance": {
                              "type": "boolean"
                            },
                            "cancelTime": {
                              "type": "string",
                              "description": "Format \"HH:MM\""
                            },
                            "cancelTimezone": {
                              "type": "string",
                              "description": "Timezone in format \"Country/Locality\""
                            },
                            "postDate": {
                              "type": "string",
                              "enum": [
                                "now",
                                "checkin",
                                "checkout"
                              ]
                            },
                            "airbnbType": {
                              "type": "string"
                            },
                            "marriottType": {
                              "type": "string"
                            },
                            "tripadvisorType": {
                              "type": "string"
                            },
                            "homeawayType": {
                              "type": "string"
                            },
                            "breakpoints": {
                              "type": "array",
                              "items": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "integer"
                                  },
                                  "rangeStart": {
                                    "type": "integer"
                                  },
                                  "rangeEnd": {
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
                            },
                            "priority": {
                              "type": "integer"
                            },
                            "createdBy": {
                              "type": "string"
                            },
                            "createdAt": {
                              "type": "string",
                              "format": "date-time",
                              "description": "Date as ISO 8601 format with timestamp"
                            },
                            "updatedBy": {
                              "type": "string"
                            },
                            "updatedAt": {
                              "type": "string",
                              "format": "date-time",
                              "description": "Date as ISO 8601 format with timestamp"
                            },
                            "dateGroupId": {
                              "type": "integer"
                            },
                            "dateRangeType": {
                              "type": "string"
                            },
                            "startDate": {
                              "type": "string",
                              "format": "date-time",
                              "description": "Date as ISO 8601 format"
                            },
                            "endDate": {
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
                          }
                        },
                        "user": {
                          "type": "object",
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
                              "type": "integer"
                            },
                            "vendorId": {
                              "type": "integer"
                            },
                            "assignable": {
                              "type": "array",
                              "items": {
                                "type": "string"
                              }
                            },
                            "createdBy": {
                              "type": "string"
                            },
                            "createdAt": {
                              "type": "string",
                              "format": "date-time",
                              "description": "Date as ISO 8601 format with timestamp"
                            },
                            "updatedBy": {
                              "type": "string"
                            },
                            "updatedAt": {
                              "type": "string",
                              "format": "date-time",
                              "description": "Date as ISO 8601 format with timestamp"
                            },
                            "_embedded": {
                              "type": "object",
                              "properties": {
                                "vendor": {
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
                        },
                        "type": {
                          "title": "Reservation Type Response",
                          "type": "object",
                          "description": "Expected response when receiving an OK response from the API.",
                          "properties": {
                            "id": {
                              "type": "integer",
                              "description": "ID of the reservation type."
                            },
                            "name": {
                              "type": "string",
                              "description": "System name of the reservation type."
                            },
                            "publicName": {
                              "type": "string",
                              "description": "Public name of the reservation type."
                            },
                            "code": {
                              "type": "string",
                              "description": "Code that is assigned to the reservation type. Should be unique, can be alphanumeric."
                            },
                            "description": {
                              "type": "string",
                              "description": "Description of the reservation type, should convey when it should be used / what its purpose is."
                            },
                            "isActive": {
                              "type": "boolean",
                              "description": "Is this reservation type active, will default to true."
                            },
                            "isCommissionable": {
                              "type": "boolean",
                              "description": "Choose if commission can be used in this reservation type."
                            },
                            "typeColor": {
                              "type": "string",
                              "description": "6 digit hex string. Will set the color of this reservation type in the tape chart."
                            },
                            "chargeRates": {
                              "type": "boolean",
                              "description": "Deprecated, do not worry about this.",
                              "deprecated": true
                            },
                            "chargeRent": {
                              "type": "string",
                              "enum": [
                                "owner",
                                "guest",
                                "none"
                              ],
                              "description": "Who wil be charged the value of the rest, either Owner, Guest, or None."
                            },
                            "rentEarned": {
                              "type": "string",
                              "enum": [
                                "owner",
                                "account",
                                "auto"
                              ],
                              "description": "Either the Owner or Revenue account will be credited with the rent value. Can be set to Auto to choose itself."
                            },
                            "requiresAgreement": {
                              "type": "boolean",
                              "description": "Wether reservation type requires agreements to be signed in order to check in reservations."
                            },
                            "requirePayment": {
                              "type": "boolean",
                              "description": "Wether reservation type requires full payment in order to realize & post rent to a reservation."
                            },
                            "cleaningOptionsId": {
                              "type": "integer",
                              "description": "The default cleaning type applied to this reservation type. This will cahnge what type of clean will be requuested upon reservation check-out."
                            },
                            "realizeRates": {
                              "type": "string",
                              "enum": [
                                "nightly",
                                "checkin",
                                "checkout",
                                "monthly"
                              ],
                              "description": "Choose when the rent will be realized in the reservation folio."
                            },
                            "isLocked": {
                              "type": "boolean",
                              "description": "If reservation type is locked, you should NOT make any major changes to the type. The only types to have this attribute will be the first 3 reservation types of the system."
                            },
                            "sendPortalInvited": {
                              "type": "boolean",
                              "description": "whether guest portal invites will be sent automatically to the contact on the reservation."
                            },
                            "portalReservationBreakdown": {
                              "type": "boolean",
                              "description": "Whether payment breakdown will be visible in guest portal."
                            },
                            "showFolioTransactions": {
                              "type": "boolean",
                              "description": "Determine if folio transactions is visibe on the guest portal."
                            },
                            "isOwner": {
                              "type": "boolean",
                              "description": "Owner can book this unit in the owner portal. (as an owner reservation))"
                            },
                            "scheduleType1": {
                              "type": "string"
                            },
                            "schedulePercentage1": {
                              "type": "integer"
                            },
                            "scheduleType2": {
                              "type": "string"
                            },
                            "schedulePercentage2": {
                              "type": "integer"
                            },
                            "ownerStay": {
                              "type": "boolean"
                            },
                            "personalUse": {
                              "type": "boolean"
                            },
                            "autoSelect": {
                              "type": "boolean"
                            },
                            "securityDepositType": {
                              "type": "string"
                            },
                            "deferDisbursement": {
                              "type": "boolean"
                            },
                            "deferDisbursementDate": {
                              "type": "string",
                              "description": "Date in IISO 8601 format."
                            },
                            "posDefaultAllow": {
                              "type": "boolean"
                            },
                            "posDefaultLimit": {
                              "type": "string"
                            },
                            "createdAt": {
                              "type": "string",
                              "format": "date-time",
                              "description": "DateTime in ISO 8601 format."
                            },
                            "createdBy": {
                              "type": "string",
                              "description": "Which user created this."
                            },
                            "updatedAt": {
                              "type": "string",
                              "format": "date-time",
                              "description": "DateTime in ISO 8601 format."
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
                          },
                          "required": [
                            "isActive"
                          ]
                        },
                        "rateType": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "integer"
                            },
                            "type": {
                              "type": "string"
                            },
                            "code": {
                              "type": "string"
                            },
                            "name": {
                              "type": "string"
                            },
                            "isAutoSelect": {
                              "type": "boolean"
                            },
                            "occupancyPricingByType": {
                              "type": "boolean"
                            },
                            "isAllChannels": {
                              "type": "boolean"
                            },
                            "channelIds": {
                              "type": "array",
                              "items": {
                                "type": "integer"
                              }
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
                              "description": "Date as ISO 8601 format with timestamp"
                            },
                            "updatedBy": {
                              "type": "string"
                            },
                            "updatedAt": {
                              "type": "string",
                              "format": "date-time",
                              "description": "Date as ISO 8601 format with timestamp"
                            },
                            "parentRateId": {
                              "type": "integer"
                            },
                            "rentType": {
                              "type": "string"
                            },
                            "rentAmount": {
                              "type": "string"
                            },
                            "minLosType": {
                              "type": "string"
                            },
                            "minLosAmount": {
                              "type": "number"
                            },
                            "maxLosType": {
                              "type": "string"
                            },
                            "maxLosAmount": {
                              "type": "number"
                            },
                            "ctaOverride": {
                              "type": "boolean"
                            },
                            "cta": {
                              "type": "object",
                              "properties": {
                                "monday": {
                                  "type": "boolean"
                                },
                                "tuesday": {
                                  "type": "boolean"
                                },
                                "wednesday": {
                                  "type": "boolean"
                                },
                                "thursday": {
                                  "type": "boolean"
                                },
                                "friday": {
                                  "type": "boolean"
                                },
                                "saturday": {
                                  "type": "boolean"
                                },
                                "sunday": {
                                  "type": "boolean"
                                }
                              }
                            },
                            "ctdOverride": {
                              "type": "boolean"
                            },
                            "ctd": {
                              "type": "object",
                              "properties": {
                                "monday": {
                                  "type": "boolean"
                                },
                                "tuesday": {
                                  "type": "boolean"
                                },
                                "wednesday": {
                                  "type": "boolean"
                                },
                                "thursday": {
                                  "type": "boolean"
                                },
                                "friday": {
                                  "type": "boolean"
                                },
                                "saturday": {
                                  "type": "boolean"
                                },
                                "sunday": {
                                  "type": "boolean"
                                }
                              }
                            }
                          }
                        },
                        "_embedded": {
                          "type": "object",
                          "properties": {
                            "parentRate": {
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
                        "checkin": {
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