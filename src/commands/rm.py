"""
Удаляет файл или каталог
"""

import os
import shutil
from pathlib import Path
from .resolve_path import resolve_path


def is_root_path(path):
    """Проверяет, является ли путь корнем диска на Windows или / на Unix."""
    resolved = str(path.resolve())
    if os.name == 'nt':  # Windows
        return len(resolved) == 3 and (resolved[1:] == ":\\" or resolved[1:] == ":/")
    else:  # Unix
        return resolved == "/" or resolved == "\\"


def rm(paths, recursive=False):
    for path in paths:
        p = resolve_path(path)
        if not p.exists():
            raise FileNotFoundError(f"rm: cannot remove '{path}': No such file or directory")

        # Защита от удаления корня, домашней и родительской папки
        if is_root_path(p) or str(p) in [str(Path.home()), str(Path.cwd().parent)]:
            raise PermissionError(f"rm: cannot remove '{path}': Permission denied")

        # Если удаляем папку
        if p.is_dir():
            if not recursive:
                raise IsADirectoryError(f"rm: cannot remove '{path}': Is a directory")
            # Запрашиваем подтверждение для каждого каталога отдельно
            confirm = input(f"Remove directory '{p}'? (y/n): ")
            if confirm.lower() != 'y':
                continue
            shutil.rmtree(p)
        # Если удаляем файл
        else:
            p.unlink()
