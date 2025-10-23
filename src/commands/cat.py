"""
Возвращает список строк — содержимое файла.
"""

from .resolve_path import resolve_path

def cat(path):
    p = resolve_path(path)

    if not p.exists():
        raise FileNotFoundError(f"cat: {path}: No such file or directory")
    if p.is_dir():
        raise IsADirectoryError(f"cat: {path}: Is a directory")

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
    raise ValueError(f"cat: {path}: Cannot decode file (unsupported encoding)")
