"""
Удаляет файл или каталог.
"""

import os
import shutil
from pathlib import Path
from .resolve_path import resolve_path

def _is_root_path(path):
    """Проверяет, является ли путь корнем диска на Windows или / на Unix."""
    resolved = str(path.resolve())
    if os.name == 'nt':  # Windows
        return len(resolved) == 3 and (resolved[1:] == ":\\" or resolved[1:] == ":/")
    else:  # Unix
        return resolved == "/" or resolved == "\\"

def rm(path, recursive=False):
    p = resolve_path(path)
    if not p.exists():
        raise FileNotFoundError(f"rm: cannot remove '{path}': No such file or directory")

    # Защита от удаления корня, домашней и родительской папки
    if _is_root_path(p) or str(p) in [str(Path.home()), str(Path.cwd().parent)]:
        raise PermissionError(f"rm: cannot remove '{path}': Permission denied")

    # Удаление папки
    if p.is_dir():
        if not recursive:
            raise OSError(f"rm: cannot remove '{path}': Is a directory")
        confirm = input(f"Remove directory '{p}'? (y/n): ")
        if confirm.lower() != 'y':
            return []
        shutil.rmtree(p)
    # Удаление файла
    else:
        p.unlink()
