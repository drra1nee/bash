"""Смена текущей рабочей директории"""

import os
from .resolve_path import resolve_path

def cd(path):
    target = resolve_path(path)

    if not target.exists():
        raise FileNotFoundError(f"cd: {path}: No such file or directory")
    if not target.is_dir():
        raise NotADirectoryError(f"cd: {path}: Not a directory")

    os.chdir(target)
