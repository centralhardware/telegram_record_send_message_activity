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

## analyze data with SQL

### pretty print table

```sql
SELECT
    id, substring(message from 0 for 150), chat, created_at 
FROM "statistic";
```

### message count per channel

```sql
SELECT
    count(*), chat 
FROM "statistic" 
GROUP BY chat 
ORDER BY count DESC;
```

### evg message length per chat

```sql
SELECT 
    chat, round(avg(length(message))) as len
FROM "statistic"
GROUP BY chat 
ORDER BY len DESC;
```

### top message by length

```sql
SELECT chat, message, length(message) as len 
FROM "statistic" 
ORDER BY len DESC 
LIMIT 10;
```

###  most used word

```sql
SELECT 
    word, count(word) as count 
FROM (
    SELECT regexp_split_to_table(s.message, ' ') AS word 
    FROM "statistic" s) AS words 
GROUP BY word 
ORDER BY count DESC 
LIMIT 51;
```

