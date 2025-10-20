"""
Реализация команды 'ls', вывод списка файлов и каталогов
"""

import os
import stat
from pathlib import Path
from datetime import datetime

def format_permissions(path: Path):
    """
    Возвращает строку прав доступа в формате '-rwxr-xr-x'
    """
    try:
        st = path.stat()
    except (OSError, AttributeError):
        return "----------"  # заглушка при ошибке

    # На Unix/Linux/macOS — настоящие права
    if os.name != 'nt':
        return stat.filemode(st.st_mode)

    # На Windows — эмуляция, так как Windows не использует Unix права напрямую
    is_dir = path.is_dir()

    # Владелец (user)
    user_r = 'r'
    user_w = 'w' if os.access(path, os.W_OK) else '-'  # проверка на запись
    user_x = 'x' if is_dir else '-'  # каталоги — исполняемые

    # Группа и остальные
    group_r = other_r = 'r'
    group_w = other_w = '-'
    group_x = other_x = 'x' if is_dir else '-'

    type_char = 'd' if is_dir else '-'
    return f"{type_char}{user_r}{user_w}{user_x}{group_r}{group_w}{group_x}{other_r}{other_w}{other_x}"

def format_time(timestamp):
    """Преобразует временную метку в читаемую дату и время"""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')

def ls(path=".", long=False):
    """
    Выводит содержимое указанного пути
    - path: путь к файлу или каталогу (по умолчанию — текущая директория)
    - long: если True — вывод в подробном формате (-l)
    """
    # Обработка домашней директории
    if path == "~":
        path = Path.home()
    elif path.startswith("~/"):
        path = Path.home() / path[2:]

    p = Path(path).resolve()
    if not p.exists():
        raise FileNotFoundError(f"No such file or directory: {path}")

    items = sorted(p.iterdir()) if p.is_dir() else [p]
    output_lines = []

    if long:
        for item in items:
            perms = format_permissions(item)  # передаём сам Path
            st = item.stat()
            size = st.st_size
            mtime = format_time(st.st_mtime)
            output_lines.append(f"{perms} {size:>10} {mtime} {item.name}")
    else:
        # Вывод без -l: по 5 файлов/папок в строке
        names = [item.name for item in items]
        for i in range(0, len(names), 5):
            line = "  ".join(names[i:i + 5])
            output_lines.append(line)

    return output_lines
