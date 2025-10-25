"""
Копирование файлов и каталогов
"""

import shutil
from .resolve_path import resolve_path
import os

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
        if (not os.access(dst, os.W_OK) and dst.exists()) or (not os.access(dst.parent, os.W_OK) and not dst.exists()):
            raise PermissionError(f"cp: Cannot create '{dst.name}': Permission denied")

        # src - каталог
        if src.is_dir():
            if not recursive:
                raise IsADirectoryError(f"cp: -r not specified; omitting directory '{src_str}'")
            # Если dst существует и является папкой
            if dst.is_dir():
                target = dst / src.name
            # Если dst не существует
            else:
                target = dst
            shutil.copytree(src, target, dirs_exist_ok=True)
        # src - файл
        else:
            shutil.copy2(src, dst)
