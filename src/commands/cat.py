"""
Возвращает список строк — содержимое одного или нескольких файлов
"""

from .resolve_path import resolve_path


def cat(paths):
    all_lines = []

    for path in paths:
        p = resolve_path(path)

        if not p.exists():
            raise FileNotFoundError(f"cat: {path}: No such file or directory")
        if p.is_dir():
            raise IsADirectoryError(f"cat: {path}: Is a directory")

        # Список кодировок для перебора
        encodings = ['utf-8', 'utf-16']
        decoded = False

        # Перебор кодировок для правильного чтения файла
        for encoding in encodings:
            try:
                with open(p, 'r', encoding=encoding) as f:
                    content = f.read()
                all_lines.extend(content.splitlines(keepends=True))
                decoded = True
                break
            except (UnicodeDecodeError, UnicodeError):
                continue

        # Если ни одна не подошла
        if not decoded:
            raise ValueError(f"cat: {path}: Cannot decode file (unsupported encoding)")

    return all_lines
