"""
Вывод списка файлов и каталогов
"""

import os
import stat
from datetime import datetime
from .resolve_path import resolve_path

def format_permissions(path):
    """
    Возвращает строку прав доступа в формате '-rwxr-xr-x'
    """
    try:
        st = path.stat()
    except (OSError, AttributeError):
        # заглушка при ошибке
        return "----------"

    # На Linux - настоящие права
    if os.name != 'nt':
        return stat.filemode(st.st_mode)

    # На Windows - эмуляция, так как Windows не использует Unix права напрямую
    is_dir = path.is_dir()

    # Владелец
    user_r = 'r'
    # Проверка на запись
    user_w = 'w' if os.access(path, os.W_OK) else '-'
    # Каталоги - исполняемые
    user_x = 'x' if is_dir else '-'

    # Группа и остальные
    group_r = other_r = 'r'
    group_w = other_w = '-'
    group_x = other_x = 'x' if is_dir else '-'

    type_char = 'd' if is_dir else '-'
    return f"{type_char}{user_r}{user_w}{user_x}{group_r}{group_w}{group_x}{other_r}{other_w}{other_x}"

def format_time(time):
    """Форматирование даты и времени"""
    return datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M')

def ls(paths, long):
    """
    Выводит содержимое одного или нескольких путей
    """
    resolved_paths = [resolve_path(p) for p in paths]

    output_lines = []
    multiple = len(resolved_paths) > 1

    for p, orig in zip(resolved_paths, paths):
        if not p.exists():
            raise FileNotFoundError(f"ls: Cannot access '{orig}': No such file or directory")

        # Получаем содержимое каталога
        if p.is_dir():
            try:
                items = p.iterdir()
            except PermissionError:
                raise PermissionError(f"ls: Cannot open directory '{orig}': Permission denied")

            # Подробное отображение
            if long:
                # Если больше одного пути, записываем название каталога
                if multiple:
                    output_lines.append(f"'{orig}':")
                for item in items:
                    # Получение данных о файле и запись их в нужном формате
                    perms = format_permissions(item)
                    st = item.stat()
                    size = st.st_size
                    mtime = format_time(st.st_mtime)
                    output_lines.append(f"{perms} {size:>10} {mtime} {item.name}")
            else:
                # Короткий формат
                if multiple:
                    output_lines.append(f"'{orig}':")
                for item in items:
                    output_lines.append(item.name)
        else:
            # Это файл
            if long:
                perms = format_permissions(p)
                st = p.stat()
                size = st.st_size
                mtime = format_time(st.st_mtime)
                output_lines.append(f"{perms} {size:>10} {mtime} {p.name}")
            else:
                output_lines.append(p.name)

    return output_lines
