from datetime import datetime
import logging
import os

import clickhouse_connect
from telethon import events, TelegramClient

logging.basicConfig(level=logging.INFO)

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
telephone = os.getenv('TELEPHONE')
client = TelegramClient('alex', api_id, api_hash)

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_DATABASE")
clickhouse = clickhouse_connect.get_client(host=host, database=database, port=8123, username=user, password=password)
clickhouse.command("""
    CREATE TABLE IF NOT EXISTS telegram_messages (
                                                 date_time DateTime,
                                                 message String,
                                                 chat String)
    ENGINE MergeTree ORDER BY date_time
""")
clickhouse.command("""
    ALTER TABLE telegram_messages
    ADD COLUMN IF NOT EXISTS chat_id String
""")

@client.on(events.NewMessage(outgoing=True))
async def handler(event):
    chat_title = ''
    chat_id= ''
    if hasattr(event.chat, "title"):
        chat_title = event.chat.title
    if event.chat.username is not None:
        chat_id = event.chat.username

    if chat_title == '':
        chat_title = chat_id

    if event.raw_text != '':
        logging.info("triggered in chat %s\n on message: %s\n", chat_title, event.raw_text)
        data = [[datetime.now(), event.raw_text, chat_title, chat_id],]
        clickhouse.insert('telegram_messages', data, ['date_time', 'message', 'chat', 'chat_id'])
        logging.info("insert new message")
    else:
        logging.info("ignore empty message")

client.connect()
client.start(phone=telephone)
client.run_until_disconnected()
