import requests
import asyncio
from bs4 import BeautifulSoup
import re
from telethon import TelegramClient
from config import API_ID, API_HASH, BOT_TOKEN

client = TelegramClient('new_bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Хранение последних обработанных новостей
processed_announcements = set()
latest_announcement = None  # Хранит информацию о последней новости

# Функция для парсинга страницы и получения анонсов с Binance (ru)
def fetch_binance_announcements_ru():
    BINANCE_URL_RU = "https://www.binance.com/ru/support/announcement/%D0%BD%D0%BE%D0%B2%D0%BE%D0%B5-%D0%BB%D0%B8%D1%81%D1%82%D0%B8%D0%BD%D0%B3%D0%B8-%D0%BA%D1%80%D0%B8%D0%BF%D1%82%D0%BE%D0%B2%D0%B0%D0%BB%D1%8E%D1%82%D1%8B?c=48&navId=48"
    response = requests.get(BINANCE_URL_RU)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Поиск всех ссылок на анонсы
    links = soup.find_all('a', href=True)
    announcements = []

    for link in links:
        if '/ru/support/announcement/' in link['href']:
            announcements.append(link['href'])

    return announcements

# Функция для парсинга страницы и получения анонсов с Binance (en)
def fetch_binance_announcements_en():
    BINANCE_URL_EN = "https://www.binance.com/en/support/announcement/new-cryptocurrency-listing?c=48&navId=48"
    response = requests.get(BINANCE_URL_EN)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Поиск всех ссылок на анонсы
    links = soup.find_all('a', href=True)
    announcements = []

    for link in links:
        if '/en/support/announcement/' in link['href']:
            announcements.append(link['href'])

    return announcements

# Функция для парсинга тикеров из анонсов
def extract_tickers(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Ищем текст анонса
    text = soup.get_text()
    tickers = re.findall(r'\b[A-Z0-9]{6,}\b', text)
    return tickers

# Мониторинг новых листингов на Binance (ru)
async def monitor_new_listings_binance_ru():
    global latest_announcement

    while True:
        try:
            announcements = fetch_binance_announcements_ru()
            for announcement in announcements:
                if announcement not in processed_announcements:
                    processed_announcements.add(announcement)
                    url = f"https://www.binance.com{announcement}"
                    tickers = extract_tickers(url)

                    if tickers:
                        latest_announcement = (url, tickers)
                        message = f"Новый листинг на Binance (RU)!\nТикеры: {', '.join(tickers)}\nПодробнее: {url}"
                        await client.send_message('me', message)  # Отправка в личные сообщения
        except Exception as e:
            print(f"Ошибка: {e}")
        await asyncio.sleep(10)  # Проверка каждые 10 секунд

# Мониторинг новых листингов на Binance (en)
async def monitor_new_listings_binance_en():
    global latest_announcement

    while True:
        try:
            announcements = fetch_binance_announcements_en()
            for announcement in announcements:
                if announcement not in processed_announcements:
                    processed_announcements.add(announcement)
                    url = f"https://www.binance.com{announcement}"
                    tickers = extract_tickers(url)

                    if tickers:
                        latest_announcement = (url, tickers)
                        message = f"Новый листинг на Binance (EN)!\nТикеры: {', '.join(tickers)}\nПодробнее: {url}"
                        await client.send_message('me', message)  # Отправка в личные сообщения
        except Exception as e:
            print(f"Ошибка: {e}")
        await asyncio.sleep(10)  # Проверка каждые 10 секунд
