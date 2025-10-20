"""
Возвращает список строк — содержимое файла.
"""

from pathlib import Path

def cat(path):
    if path.startswith("~/"):
        p = Path.home() / path[2:]
    else:
        p = Path(path).resolve()

    if p.is_dir():
        raise IsADirectoryError(f"Is a directory: {path}")
    if not p.exists():
        raise FileNotFoundError(f"No such file: {path}")

    # Список кодировок для перебора
    encodings = ['utf-8', 'cp1251', 'utf-16', 'koi8-r', 'iso-8859-1']

    for encoding in encodings:
        try:
            with open(p, 'r', encoding=encoding) as f:
                content = f.read()
            return content.splitlines(keepends=True)
        except (UnicodeDecodeError, UnicodeError):
            continue  # пробуем следующую кодировку

    # Если ни одна не подошла
    raise ValueError(f"Cannot decode file '{path}' (unsupported encoding)")
