"""
Работа с TAR.GZ-архивами: создание и распаковка
"""

import tarfile
import os
from .resolve_path import resolve_path


def tar_cmd(folder, archive):
    """
    Создаёт TAR.GZ-архив из указанной папки
    """
    src = resolve_path(folder)

    # Автоматически добавляем расширение .tar.gz если его нет
    if not archive.endswith('.tar.gz'):
        archive += '.tar.gz'

    # Если указано только имя файла архива, сохраняем в текущей директории
    if '/' not in archive and '\\' not in archive:
        dst = src.parent / archive
    else:
        # Если указан путь, используем его как есть
        dst = resolve_path(archive)

    if not src.exists():
        raise FileNotFoundError(f"tar: {folder}: No such file or directory")
    if not src.is_dir():
        raise ValueError(f"tar: {folder}: Not a directory")
    if not os.access(src, os.R_OK):
        raise PermissionError(f"tar: Cannot read '{folder}': Permission denied")
    if not os.access(dst.parent, os.W_OK):
        raise PermissionError(f"tar: Cannot write to directory '{src.parent}': Permission denied")

    with tarfile.open(dst, "w:gz") as tf:
        tf.add(src, arcname=src.name)


def untar_cmd(archive):
    """
    Распаковывает TAR.GZ-архив в каталог, в котором находится архив
    """
    arc = resolve_path(archive)

    if not arc.exists():
        raise FileNotFoundError(f"untar: {archive}: No such file or directory")
    if not tarfile.is_tarfile(arc):
        raise ValueError(f"untar: {archive}: not a tar.gz file")
    if not os.access(arc, os.R_OK):
        raise PermissionError(f"untar: Cannot read '{archive}': Permission denied")
    if not os.access(arc.parent, os.W_OK):
        raise PermissionError(f"untar: Cannot write to directory '{arc.parent}': Permission denied")

    with tarfile.open(arc, "r:gz") as tf:
        tf.extractall(path=arc.parent, filter='tar')
