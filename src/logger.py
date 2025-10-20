"""Модуль для ведения журнала (логирования) всех действий пользователя"""

import logging

def setup_logger(log_file="shell.log"):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='[%(asctime)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def log_command(command: str):
    """Логирует введённую команду"""
    logging.info(command)

def log_output_line(line: str):
    """Логирует строку вывода команды"""
    if line.strip() != "":
        logging.info(line)

def log_error(message: str):
    """Логирует ошибку"""
    logging.info(f"ERROR: {message}")
