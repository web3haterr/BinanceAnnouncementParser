import logging
from telethon import TelegramClient, events
from fetcher import monitor_new_listings_binance_ru, monitor_new_listings_binance_en, latest_announcement
from config import API_ID, API_HASH, BOT_TOKEN
import asyncio

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация клиента
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Команда /start
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    user = event.sender
    await event.respond(f"Привет, {user.first_name}! Я бот для мониторинга листингов Binance.")

# Команда /last
@client.on(events.NewMessage(pattern='/last'))
async def last(event):
    if latest_announcement:
        url, tickers = latest_announcement
        message = f"Последняя новость на Binance:\nТикеры: {', '.join(tickers)}\nПодробнее: {url}"
        await event.respond(message)
    else:
        await event.respond("На данный момент нет обработанных новостей.")

# Запуск мониторинга новых листингов на двух сайтах параллельно
async def start_monitoring():
    # Запуск мониторинга двух сайтов
    task1 = asyncio.create_task(monitor_new_listings_binance_ru())
    task2 = asyncio.create_task(monitor_new_listings_binance_en())
    
    # Ожидание завершения всех задач
    await asyncio.gather(task1, task2)

# Основной запуск
if __name__ == "__main__":
    print("Бот запущен...")
    loop = asyncio.get_event_loop()
    loop.create_task(start_monitoring())  # Запуск мониторинга на двух сайтах
    loop.run_until_complete(client.run_until_disconnected())  # Ожидание сообщений и команд
