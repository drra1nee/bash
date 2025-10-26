"""
Модуль для логирования всех действий пользователя
"""

import logging

def setup_logger(log_file="shell.log"):
    """
    Настраивает логгер
    """
    logger = logging.getLogger()
    # utf-8 для того, чтобы в файле логирования русские буквы нормально отображались
    handler = logging.FileHandler(log_file, encoding='utf-8')
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

def log_command(command):
    """Логирует введённую команду"""
    logging.info(f"{command}")

def log_output_line(line):
    """Логирует строку вывода команды"""
    if line.strip() != "":
        logging.info(f"{line}")

def log_error(message):
    """Логирует ошибку"""
    logging.error(message)
