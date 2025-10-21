"""Копирование файлов и каталогов"""

import shutil
from .resolve_path import resolve_path


def cp(sources, destination, recursive=False):
    """
    Sources: пути к исходным файлам/каталогам
    destination: путь назначения
    recursive: копировать каталоги рекурсивно
    """

    # Путь назначения только один
    dst = resolve_path(destination)

    # При нескольких источниках destination должен быть каталогом
    if len(sources) > 1:
        if not dst.exists() or not dst.is_dir():
            raise NotADirectoryError(f"Destination is not a directory: {destination}")

    for src_str in sources:
        src = resolve_path(src_str)
        if not src.exists():
            raise FileNotFoundError(f"Source does not exist: {src_str}")

        # src - каталог
        if src.is_dir():
            if not recursive:
                raise IsADirectoryError(f"Source is a directory: {src_str} (use -r for recursive copy)")
            # Определяем целевой путь
            if dst.exists() and dst.is_dir():
                target = dst / src.name
            else:
                target = dst
            shutil.copytree(src, target, dirs_exist_ok=True)
        # src - файл
        else:
            # Определяем целевой путь
            if dst.exists() and dst.is_dir():
                target = dst / src.name
            else:
                target = dst
            shutil.copy2(src, target)
