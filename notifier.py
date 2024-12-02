from telethon import TelegramClient, events
from config import API_ID, API_HASH, BOT_TOKEN

# Уникальное имя для сессии, чтобы избежать блокировок базы данных
client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

latest_announcement = None


@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("Бот запущен и следит за новыми листингами Binance!")
    raise events.StopPropagation


@client.on(events.NewMessage(pattern='/last'))
async def last(event):
    if latest_announcement:
        url, tickers = latest_announcement
        message = f"Последняя новость на Binance:\nТикеры: {', '.join(tickers)}\nПодробнее: {url}"
        await event.respond(message)
    else:
        await event.respond("На данный момент нет обработанных новостей.")
