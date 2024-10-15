import logging
import os

from datetime import datetime


class Logs:
    def __init__(self):
        base_filename = 'Logs/' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_filename = self.get_unique_log_filename(base_filename)
        
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            filename = log_filename,
                            filemode='a')

    @staticmethod
    def get_unique_log_filename(base_filename: str, extension: str = "log"):
        """
        Генерирует уникальное имя файла для логов. Если файл с таким именем уже существует,
        добавляется суффикс (_1, _2, ...).

        Параметры:
            base_filename (str) : Базовое имя файла (например, с меткой времени)
            extension (str) : Расширение (по умолчанию 'log').

        Возвращает:
            str: Уникальное имя файла
        """

        i = 1
        filename = f"{base_filename}.{extension}"

        """ Проверка на существование такого файла """
        while os.path.exists(filename):
            filename = f"{base_filename}_{i}.{extension}"
            i += 1

        return filename
