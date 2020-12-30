import logging
import os

import psycopg2
from telethon import events, TelegramClient

logging.basicConfig(level=logging.INFO)
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
telephone = os.getenv('TELEPHONE')
client = TelegramClient('alex', api_id, api_hash)

# user = os.getenv("DB_USER")
# password = os.getenv("DB_PASSWORD")
# host = os.getenv("DB_HOST")
# port = os.getenv("DB_PORT")
# database_name = os.getenv("DATABASE_NAME")
# connection = psycopg2.connect(user=user,
#                               password=password,
#                               host=host,
#                               port=port,
#                               database=database_name)
# cursor = connection.cursor()
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS statistic (
#         id serial PRIMARY KEY,
#         message TEXT,
#         chat TEXT,
#         created_at TIMESTAMP NOT NULL
#     );
# """)
# connection.commit()


@client.on(events.NewMessage(outgoing=True))
async def handler(event):
    if event.raw_text != '/ping':
        logging.info("triggered in chat %s\n on message: %s\n", event.chat.title, event.raw_text)
        cursor.execute("""
            INSERT INTO statistic ( 
                message,
                chat,
                created_at
            ) 
            VALUES ( '{}', '{}', current_timestamp );""".format(event.raw_text,
                                                                event.chat.title))
        connection.commit()


client.connect()
client.start(phone=telephone)
client.run_until_disconnected()
