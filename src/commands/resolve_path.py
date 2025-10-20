"""
Модуль для преобразования строки пути в абсолютный путь с поддержкой специальных символов
"""

from pathlib import Path

def resolve_path(path_str) :
    if not path_str or path_str == "~":
        return Path.home()
    elif path_str.startswith("~/"):
        return Path.home() / path_str[2:]
    else:
        return Path(path_str).resolve()
