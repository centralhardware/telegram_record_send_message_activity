## telegram record send message activity

just writes to the clickhouse every time the user writes something in a telegram

environments variable:
- API_ID
- API_HASH
- TELEPHONE
- DB_USER
- DB_PASSWORD
- DB_HOST

table structure:

| field name |            type             |      
|------------|:---------------------------:| 
| date_time  | timestamp without time zone |
| message    |            text             | 
| chat       |         are neat            |