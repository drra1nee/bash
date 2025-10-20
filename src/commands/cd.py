"""Смена текущей рабочей директории"""

import os
from .resolve_path import resolve_path

def cd(path):
    target = resolve_path(path)

    if not target.exists() or not target.is_dir():
        raise FileNotFoundError(f"No such directory: {path}")

    os.chdir(target)
