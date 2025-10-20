"""Смена текущей рабочей директории"""

import os
from pathlib import Path

def cd(path):
    """
    Меняет текущую рабочую директорию
    """
    if path == "~" or path == "":
        target = Path.home()
    elif path == "..":
        target = Path.cwd().parent
    else:
        target = Path(path).resolve()

    if not target.exists() or not target.is_dir():
        raise FileNotFoundError(f"No such directory: {path}")

    os.chdir(target)
    return []  # ничего не выводим
