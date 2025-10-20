"""
Модуль для преобразования строки пути в абсолютный путь
"""

from pathlib import Path
import os

def resolve_path(path_str) :
    # Обработка символа "~" в path
    if not path_str or path_str == "~":
        return Path.home()
    elif path_str.startswith("~/"):
        return Path.home() / path_str[2:]
    # Обработка path состоящих только из названия диска в Windows
    elif os.name == 'nt' and len(path_str) == 2 and path_str[1] == ':':
        return Path(path_str + '\\').resolve()
    # Обработка всех остальных path
    else:
        return Path(path_str).resolve()
