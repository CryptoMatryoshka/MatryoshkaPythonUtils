import pyautogui
import time
import logging


def click_on_image(image_path, confidence=0.9, max_processing_sec=3, wait_time=3):
    """
    Находит заданную картинку на экране и кликает по ней.

    :param image_path: Путь к файлу картинки
    :param confidence: Уверенность в совпадении (по умолчанию 0.9)
    :param max_processing_sec: Время ожидания в секундах (по умолчанию 10)
    """
    start_time = time.time()
    while time.time() - start_time < max_processing_sec:
        try:
            # Поиск картинки на экране
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location is not None:
                # Получение центра найденной области
                center = pyautogui.center(location)
                # Клик по центру найденной области
                pyautogui.click(center)
                logging.info(f"Клик по картинке {image_path} выполнен.")

                time.sleep(wait_time)
                return True
        except Exception as e:
            logging.error(f"Ошибка при поиске картинки: {e}", e)

        time.sleep(1)

    logging.warning(f"Картинка {image_path} не найдена в течение {max_processing_sec} секунд.")
    return False


def is_image_existed_on_screen(image_path, confidence=0.9, max_processing_sec=3):
    """
    Проверяет наличие заданной картинки на экране.

    :param image_path: Путь к файлу картинки
    :param confidence: Уверенность в совпадении (по умолчанию 0.9)
    :param max_processing_sec: Время ожидания в секундах (по умолчанию 10)
    :return: True, если картинка найдена, иначе False
    """
    start_time = time.time()
    while time.time() - start_time < max_processing_sec:
        try:
            # Поиск картинки на экране
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location is not None:
                logging.info(f"Картинка {image_path} найдена на экране.")
                return True
        except Exception as e:
            logging.warning(f"Ошибка при поиске картинки: {e}")
        time.sleep(1)
    logging.warning(f"Картинка {image_path} не найдена в течение {max_processing_sec} секунд.")
    return False
