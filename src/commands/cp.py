"""Копирование файлов и каталогов"""

import shutil
from .resolve_path import resolve_path


def cp(sources, destination, recursive=False):
    """
    sources: список строк — пути к исходным файлам/каталогам
    destination: строка — путь назначения
    recursive: копировать каталоги рекурсивно
    """

    # Разрешаем путь назначения один раз
    dst = resolve_path(destination)

    # Если источник один, dst может быть файлом или каталогом
    if len(sources) == 1:
        src = resolve_path(sources[0])
        if not src.exists():
            raise FileNotFoundError(f"Source does not exist: {sources[0]}")

        if src.is_dir():
            if not recursive:
                raise IsADirectoryError(f"Source is a directory: {sources[0]} (use -r for recursive copy)")

            if dst.exists() and dst.is_file():
                raise NotADirectoryError(f"Destination is not a directory: {destination}")

            # Копируем каталог внутрь dst (если dst существует и это каталог) или создаём его
            target = dst / src.name if (dst.exists() and dst.is_dir()) else dst
            shutil.copytree(src, target, dirs_exist_ok=True)
        else:
            # Копируем файл
            target = dst / src.name if (dst.exists() and dst.is_dir()) else dst
            shutil.copy2(src, target)
    else:
        # Несколько источников: destination должен быть каталогом
        if not dst.exists():
            raise FileNotFoundError(f"Destination directory does not exist: {destination}")
        if not dst.is_dir():
            raise NotADirectoryError(f"Destination is not a directory (multiple sources provided): {destination}")

        for src_str in sources:
            src = resolve_path(src_str)
            if not src.exists():
                raise FileNotFoundError(f"Source does not exist: {src_str}")
            if src.is_dir():
                if not recursive:
                    raise IsADirectoryError(f"Source is a directory: {src_str} (use -r for recursive copy)")
                shutil.copytree(src, dst / src.name, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
