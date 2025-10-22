"""
Перемещает один или несколько файлов/каталогов или переименовывает файл/каталог
"""

import shutil
from .resolve_path import resolve_path
import os

def mv(sources, destination):
    dst = resolve_path(destination)

    if len(sources) > 1 and not dst.is_dir():
        raise NotADirectoryError(f"Destination is not a directory: {destination}")

    for src_str in sources:
        src = resolve_path(src_str)
        if not src.exists():
            raise FileNotFoundError(f"Source not found: {src_str}")
        if not os.access(src, os.R_OK) or not os.access(dst, os.W_OK):
            raise PermissionError("mv: permission denied")
        shutil.move(src, dst)
