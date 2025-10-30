"""
Поиск строк, соответствующий шаблону в файлах
"""

from .resolve_path import resolve_path
import os
import re

def collect_files(paths, recursive):
    """
    Собирает список файлов для поиска в них
    """
    file_list = []
    for path_str in paths:
        p = resolve_path(path_str)
        if not p.exists():
            raise FileNotFoundError(f"grep: {path_str}: No such file or directory")
        if p.is_dir():
            if not recursive:
                raise ValueError(f"grep: {path_str}: Is a directory")
            # Рекурсивно собираем все файлы в подкаталогах
            file_list.extend(f for f in p.rglob('*') if f.is_file())
        else:
            file_list.append(p)
    return file_list

def search_file(file, pattern):
    """
    Выполняет поиск по шаблону в файле, возвращая список строк в формате: "файл:номер:строка"
    """
    if not os.access(file, os.R_OK):
        raise PermissionError(f"cp: Cannot read '{file.name}' permission denied")
    # Список кодировок для перебора
    encodings = ['utf-8', 'utf-16']
    lines = None
    # Перебор кодировок для правильного чтения файла
    for encoding in encodings:
        try:
            with open(file, 'r', encoding=encoding) as f:
                lines = f.readlines()
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    # Если ни одна не подошла
    if lines is None:
        return []

    results = []
    # Пробегаемся по строкам файла и ищем подходящие по шаблону строки
    for line_num, line in enumerate(lines, start=1):
        if pattern.search(line):
            # Убираем завершающие символы для чистоты вывода
            clean_line = line.rstrip('\n\r')
            results.append(f"{file} : {line_num} : {clean_line}")
    return results

def grep(pattern, paths, recursive, ignore_case):
    """
    Основная функция поиска текста по файлам
    """
    files_search = collect_files(paths, recursive)

    # Обработка флага -i
    flags = re.IGNORECASE if ignore_case else 0
    # Компилируем регулярное выражение
    try:
        compiled = re.compile(pattern, flags)
    except re.error as e:
        raise ValueError(f"grep: invalid pattern: {e}")

    # Выполняем поиск по каждому файлу
    all_results = []
    for file in files_search:
        matches = search_file(file, compiled)
        all_results.extend(matches)

    return all_results
