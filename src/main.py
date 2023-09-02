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
clickhouse = clickhouse_connect.get_client(host=host, port=8123, username=user, password=password)
clickhouse.command("""
    CREATE TABLE IF NOT EXISTS telegram_messages (
                                                 date_time DateTime,
                                                 message String,
                                                 chat String)
    ENGINE MergeTree ORDER BY date_time
""")

@client.on(events.NewMessage(outgoing=True))
async def handler(event):
    if hasattr(event.chat, "title"):
        title = event.chat.title
    elif event.chat.username is not None:
        title = event.chat.username
    else:
        return
    if event.raw_text != '':
        logging.info("triggered in chat %s\n on message: %s\n", title, event.raw_text)
        data = [[datetime.now(), event.raw_text, title],]
        clickhouse.insert('telegram_messages', data, ['date_time', 'message', 'chat'])
        logging.info("insert new message")
    else:
        logging.info("ignore empty message")

client.connect()
client.start(phone=telephone)
client.run_until_disconnected()
