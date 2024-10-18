import logging
import os

from datetime import datetime

from numpy import log

"""
Command: 
    logger.debug('Это сообщение для отладки (DEBUG)')
    logger.info('Это информационное сообщение (INFO)')
    logger.warning('Это предупреждающее сообщение (WARNING)')
    logger.error('Это сообщение об ошибке (ERROR)')
    logger.critical('Это критическое сообщение (CRITICAL)')
"""


class ColoredFormatter(logging.Formatter):
    # ANSI escape codes for colors
    COLORS = {
        'DEBUG': '\033[94m',  # Blue
        'INFO': '\033[92m',   # Green
        'WARNING': '\033[93m',# Yellow
        'ERROR': '\033[33m',  # Orange
        'CRITICAL': '\033[91m', # Red background
    }
    RESET = '\033[0m'  # Reset to default color

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        record.msg = f"{color}{record.msg}{self.RESET}"
        return super().format(record)


class Logs:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logs, cls).__new__(cls)
            cls._instance.__init__()
        
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'logger'):
            base_filename = 'Logs/' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            log_filename = self.get_unique_log_filename(base_filename)
               
            self.logger = logging.getLogger('my_logger')
            self.logger.setLevel(logging.DEBUG)

            file_handler = logging.FileHandler(log_filename)
            console_handler = logging.StreamHandler()

            file_handler.setLevel(logging.DEBUG)
            console_handler.setLevel(logging.DEBUG)

            formatter = ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            if not any(isinstance(h, logging.StreamHandler) for h in self.logger.handlers):
                self.logger.addHandler(file_handler)
                self.logger.addHandler(console_handler)       
            
    def getLogger(self):
        return self.logger

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
