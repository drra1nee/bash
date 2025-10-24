"""
Копирование файлов и каталогов
"""

import shutil
from .resolve_path import resolve_path
import os

def get_writable_base(path):
    """Возвращает ближайший существующий родительский каталог для path"""
    p = path.resolve()
    # Идем до корня
    while p != p.parent:
        if p.exists():
            return p
        p = p.parent
    return p

def cp(sources, destination, recursive=False):
    # Путь назначения только один
    dst = resolve_path(destination)

    # При нескольких источниках destination должен быть каталогом
    if len(sources) > 1 and not dst.is_dir():
        raise NotADirectoryError(f"cp: target '{destination}' is not a directory")

    for src_str in sources:
        src = resolve_path(src_str)
        if not src.exists():
            raise FileNotFoundError(f"cp: Cannot stat '{src_str}': No such file or directory")
        if not os.access(src, os.R_OK):
            raise PermissionError(f"cp: Cannot read '{src.name}' permission denied")
        write_base = get_writable_base(dst)
        if not os.access(write_base, os.W_OK):
            raise PermissionError(f"cp: Cannot create '{write_base}': Permission denied")

        # src - каталог
        if src.is_dir():
            if not recursive:
                raise IsADirectoryError(f"cp: -r not specified; omitting directory '{src_str}'")
            # Определяем целевой путь
            if dst.is_dir():
                if not os.access(dst, os.W_OK):
                    raise PermissionError(f"cp: '{dst.name}' permission denied")
                target = dst / src.name
            else:
                # Если мы копируем в несуществующий каталог, делаем новый
                target = dst
            shutil.copytree(src, target, dirs_exist_ok=True)
        # src - файл
        else:
            if not os.access(write_base, os.W_OK):
                raise PermissionError(f"cp: '{dst.name}' permission denied")
            shutil.copy2(src, dst)
