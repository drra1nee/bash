"""Модуль для ведения журнала (логирования) всех действий пользователя"""

import logging

def setup_logger(log_file="shell.log"):
    """
    Настраивает логгер с поддержкой UTF-8 для корректного отображения русских букв.
    """
    logger = logging.getLogger()
    logger.handlers.clear()
    handler = logging.FileHandler(log_file, encoding='utf-8')
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

def log_command(command):
    """Логирует введённую команду"""
    logging.info(f"INFO: {command}")

def log_output_line(line):
    """Логирует строку вывода команды"""
    if line.strip() != "":
        logging.info(f"INFO: {line}")

def log_error(message):
    """Логирует ошибку"""
    logging.info(f"ERROR: {message}")
