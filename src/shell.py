"""Обрабатывает ввод пользователя, разбирает команды и вызывает нужные функции"""

from pathlib import Path
import shlex
from .logger import log_command, log_output_line, log_error
from src.commands import ls, cd, cat, cp, mv, rm, zip_cmd, unzip_cmd, tar_cmd, untar_cmd

import sys

class ShellEmulator:
    """Класс интерактивной оболочки"""

    def __init__(self):
        """Инициализирует оболочку с текущей рабочей директорией"""
        self.current_dir = Path.cwd()

    def run(self):
        """Запускает бесконечный цикл обработки команд"""
        while True:
            try:
                # Формируем приглашение вида: /home/user$
                prompt = f"{self.current_dir}$ "
                user_input = input(prompt).strip()
                if not user_input:
                    continue

                log_command(user_input)  # Сразу логирует введённую команду
                self.execute(user_input)
            except KeyboardInterrupt:
                print("\nExit")
                break

    def execute(self, cmd_line):
        """Разбирает и выполняет команду"""
        parts = shlex.split(cmd_line)
        if not parts:
            return
        cmd = parts[0]
        args = parts[1:]

        try:
            if cmd == "ls":
                # Проверяем, используется ли флаг -l
                long = "-l" in args
                if long and len(args) > 1:
                    path = ' '.join(args[1:])
                elif not long and args:
                    path = ' '.join(args)
                else:
                    path = "."
                output_lines = ls(path, long=long)

            elif cmd == "cd":
                cd(' '.join(args))
                self.current_dir = Path.cwd()
                output_lines = []

            elif cmd == "cat":
                output_lines = cat(' '.join(args))

            elif cmd == "cp":
                if len(args) < 2:
                    raise ValueError("cp: missing file operand")
                # Проверяем, используется ли флаг -r и стоит ли он сразу после cp
                recursive = False
                if len(args) >= 3 and args[0] == "-r":
                    recursive = True
                    sources = args[1:-1]
                    destination = args[-1]
                else:
                    sources = args[:-1]
                    destination = args[-1]
                cp(sources, destination, recursive=recursive)
                output_lines = []

            elif cmd == "mv":
                if len(args) < 2:
                    raise ValueError("mv: missing file operand")
                sources = args[:-1]
                destination = args[-1]
                mv(sources, destination)
                output_lines = []

            elif cmd == "rm":
                recursive = "-r" in args
                if recursive:
                    path = ' '.join(args[1:])
                else:
                    path = ' '.join(args)
                if len(path) == 0:
                    raise ValueError("rm: missing operand")
                rm(path, recursive=recursive)
                output_lines = []

            elif cmd == "zip":
                if len(args) != 2:
                    raise ValueError("zip: wrong number of arguments")
                zip_cmd(args[0], args[1])
                output_lines = []

            elif cmd == "unzip":
                    if len(args) != 1:
                        raise ValueError("unzip: wrong number of arguments")
                    unzip_cmd(args[0])
                    output_lines = []

            elif cmd == "tar":
                if len(args) != 2:
                    raise ValueError("tar: wrong number of arguments")
                tar_cmd(args[0], args[1])
                output_lines = []

            elif cmd == "untar":
                if len(args) != 1:
                    raise ValueError("untar: wrong number of arguments")
                untar_cmd(args[0])
                output_lines = []

            elif cmd == "exit":
                sys.exit(0)

            else:
                raise ValueError(f"command not found: {cmd}")

            # Выводим в консоль и логируем каждую строку результата
            if len(output_lines) == 0:
                log_output_line("Success")
            else:
                log_output_line("Success, result:")
            for line in output_lines:
                clean_line = line.rstrip('\n\r')
                print(clean_line)
                log_output_line(clean_line)

        except Exception as e:
            error_msg = str(e)
            print(f"ERROR: {error_msg}")
            log_error(error_msg)
