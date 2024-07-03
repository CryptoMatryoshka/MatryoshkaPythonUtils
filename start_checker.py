import subprocess
import time
import logging
from dotenv import load_dotenv
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Загрузка переменных окружения из .env файла
load_dotenv()
# Интервал проверки в секундах
CHECK_INTERVAL_SECONDS = os.getenv('CHECK_INTERVAL_SECONDS')
if not CHECK_INTERVAL_SECONDS:
    raise ValueError("Интервал проверки не найден в переменных окружения. "
                     "Проверьте наличие CHECK_INTERVAL_SECONDS переменной в .env файле.")

# Получение списка скриптов из переменной окружения
SCRIPTS_ENV = os.getenv('SCRIPTS')
if not SCRIPTS_ENV:
    raise ValueError("Список скриптов не найден в переменных окружения. "
                     "Проверьте наличие SCRIPTS переменной в .env файле.")

# Преобразование строки скриптов в список
scripts = SCRIPTS_ENV.split(',')

def run_script(script_path):
    logging.info(f"Стартуем скрипт: {script_path}...")
    subprocess.run(["./venv/Scripts/python", script_path], check=True)


if __name__ == '__main__':
    iteration = 0
    while True:
        iteration += 1
        logging.info(f"Начинаем пускать скрипты, итерация: {iteration}...")
        try:
            for script_path in scripts:

                run_script(script_path)
                time.sleep(5)
            # Таймаут перед следующим запуском
            logging.info(f"*** Закончили проверку, ожидаем {CHECK_INTERVAL_SECONDS} секунд...")
            time.sleep(int(CHECK_INTERVAL_SECONDS))
        except subprocess.CalledProcessError:
            logging.error(f"Скрипт {script_path} упал. Перезапускаем...")
            # Задержка перед перезапуском
            time.sleep(1)
            run_script(script_path)
