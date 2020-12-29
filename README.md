## telegram record send message activity

just writes to the database every time the user writes something in a telegram

environments variable:
- API_ID
- API_HASH
- TELEPHONE
- DB_USER
- DB_PASSWORD
- DB_HOST
- DB_PORT
- DATABASE_NAME

table structure:

| field name     | type                        |      
| -------------  |:-------------:              | 
| id             | integer                     | 
| message        | text                        | 
| chat | are neat| text                        |
| created_at     | timestamp without time zone | 

### note

bot ignore `/ping` because [telegram_bot_alive_checker](https://github.com/centralhardware/telegram_bot_alive_checker) 
on the same account 