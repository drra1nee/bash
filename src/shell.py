"""Обрабатывает ввод пользователя, разбирает команды и вызывает нужные функции"""

from pathlib import Path
import shlex
from .logger import log_command, log_output_line, log_error
from src.commands import ls, cd, cat
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
            except (KeyboardInterrupt, EOFError):
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
                long = "-l" in args
                path = ' '.join(args[1:]) if long and len(args) > 1 else (' '.join(args) if not long and args else ".")
                output_lines = ls(path, long=long)

            elif cmd == "cd":
                cd(' '.join(args))
                self.current_dir = Path.cwd()
                output_lines = []

            elif cmd == "cat":
                output_lines = cat(' '.join(args))

            elif cmd == "exit":
                sys.exit(0)

            else:
                raise ValueError(f"command not found: {cmd}")

            # Выводим в консоль и логируем каждую строку результата
            for line in output_lines:
                clean_line = line.rstrip('\n\r')
                print(clean_line)
                log_output_line(clean_line)

        except Exception as e:
            error_msg = str(e)
            print(f"ERROR: {error_msg}")
            log_error(error_msg)
