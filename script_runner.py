import subprocess
import time
import logging
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение списка скриптов из переменной окружения
SCRIPTS_ENV = os.getenv('SCRIPTS')
if not SCRIPTS_ENV:
    raise ValueError("Список скриптов не найден в переменных окружения. "
                     "Проверьте наличие SCRIPTS переменной в .env файле.")

# Преобразование строки скриптов в список
scripts = SCRIPTS_ENV.split(',')

# Проверяем лежит ли python в .venv
python_exec_file_1 = "./venv/Scripts/python"
python_exec_file_2 = "../venv/Scripts/python"
if os.path.isfile(python_exec_file_1):
    python_exec_file = python_exec_file_1
elif os.path.isfile(python_exec_file_2):
    python_exec_file = python_exec_file_2
else:
    python_exec_file = "python"

logging.info(f"Используем python скрипт {python_exec_file}")


def run_script(script_path):
    logging.info(f"Стартуем скрипт: {script_path}...")
    subprocess.run([python_exec_file, script_path], check=True)


def run_scripts_in_infinite_loop():
    iteration = 0
    while True:
        iteration += 1
        logging.info(f"Начинаем пускать скрипты, итерация: {iteration}...")
        try:
            for script_conf in scripts:
                # Путь до скрипта
                script_path = script_conf.split(':')[0]
                # Интервал проверки в секундах
                check_interval_seconds = script_conf.split(':')[1]
                run_script(script_path)
                time.sleep(5)
            # Таймаут перед следующим запуском
            logging.info(f"*** Закончили проверку, ожидаем {check_interval_seconds} секунд...")
            time.sleep(int(check_interval_seconds))
        except subprocess.CalledProcessError:
            logging.error(f"Скрипт {script_path} упал. Перезапускаем...")
            # Задержка перед перезапуском
            time.sleep(1)
