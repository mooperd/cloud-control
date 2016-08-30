Endpoints
=========

/v1/user
--------

This endpoint will redirect you to the current authenticated user.
Please read further.


/v1/user/[:userId]
--------------

### Entry

```
{
    "id": 1234,
    "groupId": 12,
    "alternativeGroupIds": [
        1,
        2,
        3
    ],
    "username": "m.bennewitz",
    "permissions": [
        "own.r",
        "own.w",
        "user.r",
        "user.w",
        "app.r",
        "app.w",
        "station.r"
    ],
    "email": "m.bennewitz@dcmn.com",
    "firstName": "Marc",
    "lastName": "Bennewitz",
    "status": "verified"
}
```

### GET

#### Query params:

NONE

### GET collection

#### Query params

 * `limit`:      Limit the number of entries in the collection (default=10)
 * `offset`:     Retrieve entries of the collection at this offset (default=0)
 * `userGroup`:  `,` separated list of user group IDs
 * `status`:     `,` separated list of status (`unverified`, `verified` or `disabled`)


### POST

#### JSON request

```
{
    "groupId": 12,
    "alternativeGroupIds": [
        1,
        2,
        3
    ],
    "username": "m.bennewitz",
    "permissions": [
        "own.r",
        "own.w",
        "user.r",
        "user.w",
        "app.r",
        "app.w",
        "station.r"
    ],
    "email": "m.bennewitz@dcmn.com",
    "firstName": "Marc",
    "lastName": "Bennewitz",
    "status": "unverified"  (optional)
}
```

#### Response

Status 201

The standard entry of this endpoint

### PATCH

#### JSON request

```
{
    "groupId": 12,
    "alternativeGroupIds": [
        1,
        2,
        3
    ],
    "username": "m.bennewitz",
    "permissions": [
        "own.r",
        "own.w",
        "user.r",
        "user.w",
        "app.r",
        "app.w",
        "station.r"
    ],
    "email": "m.bennewitz@dcmn.com",
    "firstName": "Marc",
    "lastName": "Bennewitz",
    "status": "verified"
}
```

#### Response

The standard entry of this endpoint

### DELETE

#### JSON request

empty

#### Response

Status 204

Empty response on success


/v1/userGroup/[:userGroupId]
----------------------------

#### Entry

```
{
    "id": 1234,
    "name": "DCMN"
}
```

### GET

#### Query params:

NONE

### GET collection

#### Query params

 * `limit`:  Limit the number of entries in the collection (default=10)
 * `offset`: Retrieve entries of the collection at this offset (default=0)

### POST

#### JSON request

```
{
    "name": "DCMN"
}
```

#### Response

Status 201

The standard entry of this endpoint

### PATCH

#### JSON request

```
{
    "name": "DCMN"
}
```

#### Response

The standard entry of this endpoint

### DELETE

#### JSON request

empty

#### Response

Status 204

Empty response on success


/v1/app/[:appId]
-------------

### Entry

```
{
    "id": 1234,
    "userGroupId": 1234,
    "name": "Stayfriends",
    "uri": "http://stayfriends.de/",
    "types": [
        "desktop",
        "web",
        "mobile"
    ],
    "brandUtmParams": {
        "utm_source": [
            "google"
        ],
        "utm_medium": [
            "cpc",
            "cpm"
        ],
        "utm_campaign": [
            "Branding Campaign 1",
            "Branding Campaign 2"
        ],
        "utm_term": [
            "stayfriend",
            "stayfriends",
            "stay-friend"
        ],
        "utm_content": [
            "banner_300x250"
        ]
    },
    "cTime": "2015-09-24T12:34:56Z"
}
```

### GET

#### Query params

NONE

### GET collection

#### Query params

 * `limit`:     Limit the number of entries in the collection (default=10)
 * `offset`:    Retrieve entries of the collection at this offset (default=0)
 * `userGroup`: `,` separated list of user group IDs


### POST

#### JSON request

```
{
    "userGroupId": 1234,
    "name": "Stayfriends",
    "uri": "http://stayfriends.de/",
    "types": [
        "web"
    ],
    "brandUtmParams": {
        "utm_source": [
            "google"
        ],
        "utm_medium": [
            "cpc",
            "cpm"
        ],
        "utm_campaign": [
            "Branding Campaign 1",
            "Branding Campaign 2"
        ],
        "utm_term": [
            "stayfriend",
            "stayfriends",
            "stay-friend"
        ],
        "utm_content": [
            "banner_300x250"
        ]
    }
}
```

#### Response

Status 201

The standard entry of this endpoint

### PATCH

#### JSON request

```
{
    "userGroupId": 1234,
    "name": "Stayfriends",
    "uri": "http://stayfriends.de/",
    "types": [
        "web"
    ],
    "brandUtmParams": {
        "utm_source": [
            "google"
        ],
        "utm_medium": [
            "cpc",
            "cpm"
        ],
        "utm_campaign": [
            "Branding Campaign 1",
            "Branding Campaign 2"
        ],
        "utm_term": [
            "stayfriend",
            "stayfriends",
            "stay-friend"
        ],
        "utm_content": [
            "banner_300x250"
        ]
    }
}
```

#### Response

Status 200

The standard entry of this endpoint

### DELETE

#### JSON request

empty

#### Response

Status 204

Empty response on success


/v1/app/:appId/goal/[:goalId]
--------------

### Entry

```
{
    "id": 1234,
    "appId" 1234,
    "name": "Name of the goal"
    "revenue": 2.99
}
```

### GET

#### Query params

NONE

### GET collection

#### Query params

 * `limit`:      Limit the number of entries in the collection (default=10)
 * `offset`:     Retrieve entries of the collection at this offset (default=0)
 * `userGroup`:  `,` separated list of user group IDs


/v1/app/stats
-------------

Contains app related statistics:

### GET

#### Query params

 * `tz`:       Time zone offset in format `±hh[:mm]`
               or an identifier defined by [IANA Time Zone Database](https://www.iana.org/time-zones)
               or UTC if not provided
 * `range`:    *required* Date and time range in ISO-8601, e.g. 2015-01-01/2016-01-01
 * `interval`: The interval how the statistical entries are listed, e.g. `P1D` for one day
 * `group`:    Group by `app`, `goal`, `country`
 * `app`:      `,` separated list of app IDs
 * `country`:  `,` separated list of country codes in ISO-3166-1 ALPHA-2

#### All stats for the year 2015 (without group or interval)

##### Request

`/v1/app/stats?range=2015-01-01/2016-01-01&tz=Europe/Berlin`

##### Response

```
{
    "timezone": "Europe/Berlin",
    "range": "2015-02-01/2015-10-26",
    "entries": {
        "2015-02-01": {
            "visits": 1234,
            "pageviews": 34,
            "conversions": 2,
            "conversionRevenue": 123.456
        }
    }
}
```

#### All stats per day of year 2015

##### Request

`/v1/app/stats?range=2015-01-01/2016-01-01&tz=Europe/Berlin&interval=P1D`

##### Response

```
{
    "timezone": "Europe/Berlin",
    "range": "2015-02-01/2015-10-26",
    "entries": {
        "2015-02-01": {
            "visits": 1234,
            "pageviews": 34,
            "conversions": 2,
            "conversionRevenue": 123.456
        }, "...": { ... }
    }
}
```

#### All stats grouped by app with interval of 1 day of year 2015

##### Request

`/v1/app/stats?range=2015-01-01/2016-01-01&tz=Europe/Berlin&group=app&interval=P1D`

##### Response

```
{
    "timezone": "Europe/Berlin",
    "range": "2015-02-01/2015-10-26",
    "group": "appId",
    "entries": {
        "12345": {
            "2015-02-01": {
                "visits": 1234,
                "pageviews": 34,
                "conversions": 2,
                "conversionRevenue": 123.456
            }, "...": { ... }
        }, "...": { ... }
    }
}
```


/v1/campaign/[:campaignId]
------------------

### Entry

```
{
    "id": 1234,
    "appId" 1234,
    "name": "Name of the campaign",
    "timezone": "Europe/Berlin",
    "countryCodes": ["DE", "US"],
    "costCurrencyCode": "EUR",
    "conversionAttributionWindow": 604800
}
```

### GET

#### Query params

NONE

### GET collection

#### Query params

 * `limit`:      Limit the number of entries in the collection (default=10)
 * `offset`:     Retrieve entries of the collection at this offset (default=0)
 * `app`:        `,` separated list of app IDs
 * `userGroup`:  `,` separated list of user group IDs

### POST

#### JSON request

```
{
    "appId": 1234,
    "name": "Name of the campaign",
    "timezone": "Europe/Berlin",
    "countryCodes": ["DE", "US"],
    "costCurrencyCode": "EUR",
    "conversionAttributionWindow": 604800
}
```

Possible UTM Parameters are: `utm_campaign`, `utm_source`, `utm_medium`, `utm_term`, `utm_content`.

#### Response

Status 201

The standard entry of this endpoint

### PATCH

#### JSON request

```
{
    "appId" 1234,
    "name": "Name of the campaign",
    "timezone": "Europe/Berlin",
    "countryCodes": ["DE", "US"],
    "costCurrencyCode": "EUR",
    "conversionAttributionWindow": 604800
}
```

Possible UTM Parameters are: `utm_campaign`, `utm_source`, `utm_medium`, `utm_term`, `utm_content`.

#### Response

The standard entry of this endpoint

### DELETE

#### JSON request

empty

#### Response

Status 204

Empty response on success

/v1/spot/[:spotId]
------------------

### Entry

```
{
    "id": 1234,
    "appId" 1234,
    "name": "Name of the spot",
    "length": 10
}
```

### GET

#### Query params

NONE

### GET collection

#### Query params

 * `limit`:      Limit the number of entries in the collection (default=10)
 * `offset`:     Retrieve entries of the collection at this offset (default=0)
 * `app`:        `,` separated list of app IDs
 * `userGroup`:  `,` separated list of user group IDs


/v1/spot/airing/[:spotAiringId]
-------------------------------

### Entry

```
{
    "id": 1234,
    "spotId": 1234,
    "campaignId": 1234,
    "stationId": 12,
    "time": "2014-07-06T14:57:20+00:00",
    "programName": "Name of the current show",
    "grossMedia": 10.50,
    "netMedia": 4.78,
    "grossReach": 120000,
    "grossRatingPoints": 1.234
}
```

### GET

#### Query params

NONE

### GET collection

#### Query params

 * `limit`:    Limit the number of entries in the collection (default=10)
 * `offset`:   Retrieve entries of the collection at this offset (default=0)
 * `range`:    Date and time range in ISO-8601
 * `app`:      `,` separated list of app IDs
 * `campaign`  `,` separated list of campaign IDs

#### TVSpots aired in 2015 in given campaignid 3

##### Request

`/v1/spot/airing/?range=2015-01-01/2016-01-01&campaign=3`

##### Response

```
{
    "count": 123,
    "limit": 10,
    "offset": 0,
    "entries": [
        {
            "id": 1234,
            "spotId": 1234,
            "campaignId": 1234,
            "stationId": 12,
            "time": "2014-07-06T14:57:20+00:00",
            "programName": "Name of the current show",
            "grossMedia": 12.50,
            "netMedia": 5.67
            "grossReach": 150000,
            "grossRatingPoints": 0.45
        }, { ... }
    ]
}
```

### POST

#### JSON request

```
{
    "start": "2015-09-24T02:00:00Z",
    "end": "2015-10-24T02:00:00Z",
    "campaignId": 1234,
    "entries": [
        {
            "spotId": 74,
            "stationId": 5,
            "time": "2014-07-12T14:57:20Z",
            "programName": "Name of the current show",
            "grossMedia": 10000,
            "netMedia":100,
            "grossReach": 120000,
            "grossRatingPoints": 1.91
        }, { ... }
    ]
}
```

#### Response

Status 201

The standard entry of this endpoint


/v1/spot/airing/:spotAiringId/peak
--------------

### Entry

```
{
    "2016-06-09 15:04:00": {
        "grossUplift": 5,
        "baseline": 55,
        "threshold": 60,
    }, "..." : { ... }
}
```

### GET

#### Params

NONE


/v1/spot/stats
--------------

Spot related statistics:

### GET

#### Query params

 * `tz`:       Time zone offset in format `±hh[:mm]`
               or an identifier defined by [IANA Time Zone Database](https://www.iana.org/time-zones)
               or UTC if not provided
 * `range`:    *required* Date and time range in ISO-8601
 * `interval`: The interval how the statistical entries are listed, e.g. `P1D` for one day
 * `group`:    `,` separated list of `station`, `app`, `goal`, `campaign`, `spot`,  `spotAiring`
 * `app`:      `,` separated list of app IDs
 * `campaign`  `,` separated list of campaign IDs

#### Stats of year 2015

##### Request

`/v1/spot/stats?range=2015-01-01/2016-01-01&tz=Europe/Berlin`

##### Response

```
{
    "timezone": "Europe/Berlin",
    "range": "2015-02-01/2015-10-26",
    "entries": {
        "2015-02-01": {
            "upliftVisits": 61728,
            "upliftShortTermConversions": 123,
            "upliftLongTermConversions": 1234
        }
    }
}
```

#### Stats with interval of 1 day of year 2015

##### Request

`/v1/spot/stats?range=2015-01-01/2016-01-01&tz=Europe/Berlin&interval=P1D`

##### Response

```
{
    "timezone": "Europe/Berlin",
    "range": "2015-02-01/2015-10-26",
    "entries": {
        "2015-02-01": {
            "upliftVisits": 456789,
            "upliftShortTermConversions": 123,
            "upliftLongTermConversions": 1234
        }, "...": { ... }
    }
}
```

#### Stats grouped by spot with interval of 1 day of year 2015

##### Request

`/v1/spot/stats?range=2015-01-01/2016-01-01&tz=Europe/Berlin&interval=P1D&group=spot`

##### Response

```
{
    "timezone": "Europe/Berlin",
    "range": "2015-02-01/2015-10-26",
    "group": "spotId",
    "entries": {
        "{SpotId}": {
            "2015-02-01": {
                "upliftVisits": 456789,
                "upliftShortTermConversions": 123,
                "upliftLongTermConversions": 1234
            }, "...": { ... }
        }, "...": { ... }
    }
}
```


/v1/spot/stats/build/[:buildId]
--------------

Getting the status of a running build is currently not supported

Make the job build

### POST

{
    "campaignId": 1234,
    "range": "2016-01-01/2016-02-01"
    "email": "m.bennewitz@dcmn.com"
}

#### Response

Status 201

The standard entry of this endpoint


/v1/brand/stats
--------------

Brand traffic statistics:

### GET

#### Query params

 * `tz`:       Time zone offset in format `±hh[:mm]`
               or an identifier defined by [IANA Time Zone Database](https://www.iana.org/time-zones)
               or UTC if not provided
 * `range`:    *required* Date and time range in ISO-8601
 * `interval`: The interval how the statistical entries are listed, e.g. `P1D` for one day
 * `group`:    `,` separated list of `app`, `goal`, `campaign`, `sourceType`
 * `app`:      `,` separated list of app IDs
 * `campaign`  `,` separated list of campaign IDs

#### Stats of year 2015

##### Request

`/v1/brand/stats?range=2015-01-01/2016-01-01&tz=Europe/Berlin`

##### Response

```
{
    "timezone": "Europe/Berlin",
    "range": "2015-02-01/2015-10-26",
    "entries": {
        "2015-02-01": {
            "visits": 1728,
            "visitors": 1234,
            "shortTermConversions": 34
            "longTermConversions": 56
        }
    }
}
```

#### Stats with interval of 1 day of year 2015

##### Request

`/v1/brand/stats?range=2015-01-01/2016-01-01&tz=Europe/Berlin&interval=P1D`

##### Response

```
{
    "timezone": "Europe/Berlin",
    "range": "2015-02-01/2015-10-26",
    "entries": {
        "2015-02-01": {
            "visits": 1728,
            "visitors": 1234,
            "shortTermConversions": 34
            "longTermConversions": 56
        }, "...": { ... }
    }
}
```

#### Stats grouped by goal with interval of 1 day of year 2015

##### Request

`/v1/brand/stats?range=2015-01-01/2016-01-01&tz=Europe/Berlin&interval=P1D&group=spot`

##### Response

```
{
    "timezone": "Europe/Berlin",
    "range": "2015-02-01/2015-10-26",
    "group": "appId,goalId",
    "entries": {
        "{appId},{goalId}": {
            "2015-02-01": {
                "visits": 1728,
                "visitors": 1234,
                "shortTermConversions": 34
                "longTermConversions": 56
            }, "...": { ... }
        }, "...": { ... }
    }
}
```


/v1/station/[:stationId]
-----------------

This endpoint doesn't need authentication for read operations
and therefore can be cached over different users.

### Entry

```
{
    "id": 1234,
    "name": "13TH STREET",
    "aliases": [
        "13th",
        "13thstr",
        "13thstreet"
    ],
    "countryCode": "DE",
    "clusterId": 8
}
```

### GET

#### Query params

NONE

### GET collection

#### Query params

 * `country`: `,` separated list of country codes in ISO-3166-1 ALPHA-2
 * `limit`:   Limit the number of entries in the collection (default=10)
 * `offset`:  Retrieve entries of the collection at this offset (default=0)

### POST

#### JSON request

```
{
    "name": "13TH STREET",
    "aliases": [
        "13th",
        "13thstr",
        "13thstreet"
    ],
    "countryCode": "DE",
    "clusterId": 8
}
```

#### Response

Status 201

The standard entry of this endpoint

### PATCH

#### JSON request

```
{
    "name": "13TH STREET",
    "aliases": [
        "13th",
        "13thstr",
        "13thstreet"
    ],
    "countryCode": "DE",
    "clusterId": 1234
}
```

#### Response

Status 200

The standard entry of this endpoint

### DELETE

#### JSON request

empty

#### Response

Status 204

Empty response on success


/v1/station/cluster/[:clusterId]
-----------------

### Entry

```
{
    "id": 1234,
    "name": "Performance Driver Channels"
    "countryCode": "DE"
}
```

### GET

#### Query params

NONE

### GET collection

#### Query params

 * `country`:  `,` separated list of country codes in ISO-3166-1 ALPHA-2
 * `limit`:    Limit the number of entries in the collection (default=10)
 * `offset`:   Retrieve entries of the collection at this offset (default=0)

### POST

#### JSON request

```
{
    "name": "Performance Driver Channels",
    "countryCode": "DE"
}
```

#### Response

Status 201

The standard entry of this endpoint

### PATCH

#### JSON request

```
{
    "name": "Volume Driver Channels"
}
```

#### Response

Status 200

The standard entry of this endpoint


/v1/campaign/:campaignId/flight/[:flightId]
-----------------

Flights endpoint

### Entry
```
{
    "campaignId": 1234,
    "id": 2,
    "name": "Flight Name",
    "start": "2015-09-24T02:00:00Z",
    "end": "2015-10-24T02:00:00Z"
}
```

### GET

#### Query params

NONE

### GET collection

#### Query params

 * `limit`:    Limit the number of entries in the collection (default=10)
 * `offset`:   Retrieve entries of the collection at this offset (default=0)
 * `range`:    Date and time range in ISO-8601. Will be included flights that have any time in common with the passed one


### POST

#### JSON request

```
{
    "name": "Flight Name",
    "start": "2015-09-24T02:00:00Z",
    "end": "2015-10-24T02:00:00Z"
}
```

#### Response

Status 201

The standard entry of this endpoint

### PATCH

#### JSON request

```
{
    "name": "New Flight Name",
    "start": "2015-09-24T02:00:00Z",
    "end": "2015-10-24T02:00:00Z"
}
```

#### Response

Status 200

The standard entry of this endpoint

### DELETE

#### JSON request

empty

#### Response

Status 204

Empty response on success

