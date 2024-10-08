import pyautogui
import time
import logging
from random import randint


def scroll(scroll_clicks, wait_time=3):
    screen_size_x, screen_size_y = pyautogui.size()
    screen_center_x = screen_size_x / 2
    screen_center_y = screen_size_y / 2
    pyautogui.moveTo(screen_center_x, screen_center_y)
    pyautogui.scroll(scroll_clicks)
    time.sleep(wait_time)


def click_on_center(wait_time=3):
    screen_size_x, screen_size_y = pyautogui.size()
    screen_center_x = screen_size_x / 2
    screen_center_y = screen_size_y / 2
    pyautogui.click(screen_center_x, screen_center_y)
    time.sleep(wait_time)

def scroll_down_by_dragdrop(shift_px):
    screen_size_x, screen_size_y = pyautogui.size()
    screen_center_x = screen_size_x / 2
    screen_center_y = screen_size_y / 2
    pyautogui.moveTo(screen_center_x, screen_center_y)
    pyautogui.dragTo(screen_center_x, screen_center_y - shift_px, button='left', duration=2)
    time.sleep(3)


def count_of_images_on_screen(image_path, confidence=0.9, max_processing_sec=3, wait_time=3):
    start_time = time.time()
    while time.time() - start_time < max_processing_sec:
        try:
            # Поиск всех вхождений картинки на экране
            locations = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))
            return len(locations)
        except Exception as e:
            logging.error(f"Ошибка при поиске картинки: {e}, path: {image_path}")
        time.sleep(1)
    return 0

def click_on_image(image_path, confidence=0.9, max_processing_sec=3, wait_time=3, is_bottom=True):
    start_time = time.time()
    while time.time() - start_time < max_processing_sec:
        try:
            # Поиск всех вхождений картинки на экране
            locations = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))
            if locations:
                if is_bottom:
                    # Найти нижнее вхождение (с максимальной координатой y)
                    location = max(locations, key=lambda loc: loc.top)
                else:
                    location = min(locations, key=lambda loc: loc.top)

                # Получение центра найденной области
                center = pyautogui.center(location)
                # Клик по центру найденной области
                pyautogui.click(center)
                logging.info(f"Клик по нижней картинке {image_path} выполнен.")

                time.sleep(wait_time)
                return True
        except Exception as e:
            logging.error(f"Ошибка при поиске картинки: {e}")

        time.sleep(1)

    logging.info(f"Картинка {image_path} не найдена за отведенное время.")
    return False


def move_to_image(image_path, confidence=0.9, max_processing_sec=3, wait_time=3):
    start_time = time.time()
    while time.time() - start_time < max_processing_sec:
        try:
            # Поиск картинки на экране
            location_matches = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))
            if not location_matches:
                logging.warning("Изображения не найдены.")
                return None

            # Найти изображение с наибольшей координатой y (самое нижнее)
            location = max(location_matches, key=lambda x: x.top)

            # Получение центра найденной области
            center = pyautogui.center(location)
            # Клик по центру найденной области
            pyautogui.moveTo(center)
            logging.info(f"Навели мыш на картинку {image_path}.")

            time.sleep(wait_time)
            return center
        except Exception as e:
            logging.error(f"Ошибка при поиске картинки: {e}")

        time.sleep(1)

    logging.warning(f"Картинка {image_path} не найдена в течение {max_processing_sec} секунд.")
    return None


def click_on_image_and_hold(image_path, confidence=0.9, max_processing_sec=3, wait_time=3, hold_time=1):
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
                # Смещение координат центра на рандомное значение от -15 до 15 по обеим осям
                random_offset_x = randint(-15, 15)
                random_offset_y = randint(-15, 15)

                # Новая позиция с учетом смещения
                new_x = center.x + random_offset_x
                new_y = center.y + random_offset_y

                new_center = (new_x, new_y)

                # Клик по центру найденной области
                logging.info(f"Зажали картинку {image_path} выполнен.")
                pyautogui.mouseDown(new_center)
                time.sleep(hold_time)
                pyautogui.mouseUp(new_center)

                time.sleep(wait_time)
                return True
        except Exception as e:
            logging.error(f"Ошибка при поиске картинки: {e}")

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


