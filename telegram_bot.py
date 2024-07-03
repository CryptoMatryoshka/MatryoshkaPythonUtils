import logging
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv
import os
import asyncio

# Количество попыток отправки сообщения в случае ошибки
ERROR_MESSAGE_RETRY_COUNT = 3
RETRY_DELAY_SECONDS = 5

# Загрузка переменных окружения из .env файла
load_dotenv()
# Получение токена из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHANNEL = os.getenv('TELEGRAM_CHANNEL')

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Токен бота не найден в переменных окружения. "
                     "Проверьте наличие TELEGRAM_BOT_TOKEN переменной в .env файле.")

if not TELEGRAM_CHANNEL:
    raise ValueError("Адрес канала для отправки сообщений не найден в переменных окружения. "
                     "Проверьте наличие TELEGRAM_CHANNEL переменной в .env файле.")

# Инициализация бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def _send_message(text):
    """
    Отправка текстового сообщения в Telegram.
    :param chat_id: ID чата, куда отправлять сообщение
    :param text: Текст сообщения
    :param retry_delay: Задержка между попытками в секундах
    """
    for attempt in range(ERROR_MESSAGE_RETRY_COUNT):
        try:
            await bot.send_message(chat_id=TELEGRAM_CHANNEL, text=text)
            logging.info(f"Сообщение отправлено в чат {TELEGRAM_CHANNEL}")
            break
        except TelegramError as e:
            logging.error(f"Ошибка при отправке сообщения: {e}")
            if attempt < ERROR_MESSAGE_RETRY_COUNT - 1:
                await asyncio.sleep(RETRY_DELAY_SECONDS)
            else:
                logging.error("Не удалось отправить сообщение после нескольких попыток")


def send_message(text):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_send_message(text))


async def _send_photo(photo_path, caption=None):
    """
    Отправка картинки в Telegram.
    :param chat_id: ID чата, куда отправлять картинку
    :param photo_path: Путь к файлу картинки
    :param caption: Подпись к картинке
    """
    if not os.path.isfile(photo_path):
        error_msg = f"ERROR: Файл картинки не найден: {photo_path}"
        logging.error(error_msg)
        error_msg = error_msg if caption is None else caption + " " + error_msg
        send_message(error_msg)
        return

    for attempt in range(ERROR_MESSAGE_RETRY_COUNT):

        try:
            with open(photo_path, 'rb') as photo:
                await bot.send_photo(chat_id=TELEGRAM_CHANNEL, photo=photo, caption=caption)
            logging.info(f"Картинка отправлена в чат {TELEGRAM_CHANNEL}")
            break
        except TelegramError as e:
            logging.warning(f"Ошибка при отправке картинки: {e}")
            if attempt < ERROR_MESSAGE_RETRY_COUNT - 1:
                await asyncio.sleep(RETRY_DELAY_SECONDS)
            else:
                logging.warning("Не удалось отправить картинку после нескольких попыток")


def send_photo(photo_path, caption=None):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_send_photo(photo_path, caption))