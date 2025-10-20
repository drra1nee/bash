"""Смена текущей рабочей директории"""

import os
from pathlib import Path

def cd(path):
    if path == "~" or path == "":
        target = Path.home()
    elif path.startswith("~/"):
        target = Path.home() / path[2:]
    else:
        target = Path(path).resolve()

    if not target.exists() or not target.is_dir():
        raise FileNotFoundError(f"No such directory: {path}")

    os.chdir(target)
