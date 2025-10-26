"""Смена текущей рабочей директории"""

import os
from .resolve_path import resolve_path

def cd(path):
    p = resolve_path(path)

    if not p.exists():
        raise FileNotFoundError(f"cd: {path}: No such file or directory")
    if not p.is_dir():
        raise NotADirectoryError(f"cd: {path}: Not a directory")

    os.chdir(p)
