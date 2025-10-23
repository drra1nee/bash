"""Работа с ZIP-архивами: создание и распаковка"""

import zipfile
import os
from .resolve_path import resolve_path


def zip_cmd(folder, archive):
    """
    Создаёт ZIP-архив из указанной папки
    """
    src = resolve_path(folder)

    # Автоматически добавляем расширение .zip если его нет
    if not archive.endswith('.zip'):
        archive += '.zip'

    # Если указано только имя файла архива, сохраняем в текущей директории
    if ('/' not in archive) and ('\\' not in archive):
        dst = src.parent / archive
    else:
        # Если указан путь, используем его как есть
        dst = resolve_path(archive)

    if not src.exists():
        raise FileNotFoundError(f"zip: {folder}: No such file or directory")
    if not src.is_dir():
        raise ValueError(f"zip: {folder}: Not a directory")
    if not os.access(src, os.R_OK):
        raise PermissionError(f"zip: Cannot read '{folder}': Permission denied")
    if not os.access(dst.parent, os.W_OK):
        raise PermissionError(f"zip: Cannot write to directory '{src.parent}': Permission denied")

    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Сохраняем структуру: архив будет содержать саму папку folder/
        for file_path in src.rglob('*'):
            # Относительный путь от родителя folder
            arcname = file_path.relative_to(src.parent)
            zf.write(file_path, arcname)
        # Добавляем саму папку, если она пустая
        if not any(src.iterdir()):
            zf.writestr(f"{src.name}/", "")


def unzip_cmd(archive):
    """
    Распаковывает ZIP-архив в текущий рабочий каталог
    """
    arc = resolve_path(archive)

    if not arc.exists():
        raise FileNotFoundError(f"unzip: {archive}: No such file or directory")
    if not zipfile.is_zipfile(arc):
        raise ValueError(f"unzip: {archive}: not a zip file")
    if not os.access(arc, os.R_OK):
        raise PermissionError(f"unzip: Cannot read '{archive}': Permission denied")
    if not os.access(arc.parent, os.W_OK):
        raise PermissionError(f"unzip: Cannot write to directory '{arc.parent}': Permission denied")

    with zipfile.ZipFile(arc, 'r') as zf:
        zf.extractall(path=arc.parent)
