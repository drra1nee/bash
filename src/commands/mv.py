"""
Перемещает один или несколько файлов/каталогов или переименовывает файл/каталог
"""

import shutil
from .resolve_path import resolve_path
import os

def mv(sources, destination):
    dst = resolve_path(destination)

    if len(sources) > 1 and not dst.is_dir():
        raise NotADirectoryError(f"mv: target '{destination}' is not a directory")

    for src_str in sources:
        src = resolve_path(src_str)
        if not src.exists():
            raise FileNotFoundError(f"mv: cannot stat '{src_str}': No such file or directory")
        if not os.access(src, os.R_OK):
            raise PermissionError(f"cp: '{src.name}' permission denied")
        if not os.access(dst, os.W_OK):
            raise PermissionError(f"cp: '{dst.name}' permission denied")

        shutil.move(src, dst)
