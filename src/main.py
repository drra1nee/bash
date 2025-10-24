"""
Главный модуль оболочки - точка входа в программу
"""

from src.logger import setup_logger
from src.shell import ShellEmulator

def main():
    setup_logger()
    shell = ShellEmulator()
    shell.run()

if __name__ == "__main__":
    main()
