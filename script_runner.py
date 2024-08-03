import subprocess
import time
import logging
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from random import randint, seed

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
python_exec_file_1 = "./venv/Scripts/python.exe"
python_exec_file_2 = "../venv/Scripts/python.exe"
if os.path.isfile(python_exec_file_1):
    python_exec_file = python_exec_file_1
elif os.path.isfile(python_exec_file_2):
    python_exec_file = python_exec_file_2
else:
    python_exec_file = "python"

def run_script(script_path):
    logging.info(f"Используем python скрипт {python_exec_file}")
    logging.info(f"Стартуем скрипт: {script_path}...")
    try:
        subprocess.run([python_exec_file, script_path], check=True)

        logging.info(f"Скрипт отработал успешно: {script_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка при выполнении скрипта {script_path}: {e}")
        raise

def run_scripts_in_infinite_loop():
    seed(datetime.now().timestamp())

    iteration = 0
    # Словарь для хранения времени последнего запуска script_conf:datetime
    script_execution_dict = {script_conf: datetime.now() for script_conf in scripts}

    logging.info(f"Ждем 10 сек, и начинаем запускать скрипты!")
    time.sleep(10)

    while True:
        iteration += 1
        try:
            for script_conf in scripts:
                # Путь до скрипта
                script_path, check_interval_seconds = script_conf.split(':')
                check_interval_seconds = int(check_interval_seconds)

                # Считаем сколько времени прошло
                if datetime.now() > script_execution_dict[script_conf]:
                    # Сохраняем время запуска
                    # Добавляем случайное время, чтобы не палиться как робот
                    script_execution_dict[script_conf] = datetime.now() + timedelta(seconds=(check_interval_seconds + randint(0, 720)))
                    logging.info(f"Скрипт: {script_path} Время запуска, {script_execution_dict[script_conf]}"
                                 f" check_interval_seconds {check_interval_seconds}")

                    logging.info(f"Запускаем скрипт: {script_path}")
                    run_script(script_path)
                    logging.info(f"Скрипт отработал: {script_path}")

            # Таймаут перед следующей итерацией
            time.sleep(1)
        except subprocess.CalledProcessError as e:
            logging.error(f"Скрипт {script_path} упал. Перезапускаем... {e}")
            # Задержка перед перезапуском
            time.sleep(5)
        except Exception as e:
            logging.error(f"Неожиданная ошибка: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_scripts_in_infinite_loop()
