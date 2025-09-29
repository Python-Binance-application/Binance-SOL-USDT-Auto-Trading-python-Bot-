import asyncio
from telegram import Bot
import config

async def scrivi_bot(data):
    bot = Bot(token=config.BOT_TOKEN)
    await bot.send_message(chat_id=config.CHAT_ID, text=data)


def bot_telegram(data):
    asyncio.run(scrivi_bot(data))
