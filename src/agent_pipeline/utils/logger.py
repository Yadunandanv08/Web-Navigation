import time
from colorama import Fore, Style


class Logger:
    def __init__(self):
        self.start_time = time.time()

    def log(self, message: str, level: str = "INFO", color: str = ""):
        elapsed_time = time.time() - self.start_time
        formatted_message = f"{color}[{elapsed_time:.2f}s] {level}: {message}{Style.RESET_ALL}"
        print(formatted_message)

    def info(self, message: str):
        self.log(message, "INFO", Fore.GREEN)

    def warning(self, message: str):
        self.log(message, "WARNING", Fore.YELLOW)

    def error(self, message: str):
        self.log(message, "ERROR", Fore.RED)

    def thought(self, message: str):
        self.log(message, "THOUGHT", Fore.CYAN)

    def reflection(self, message: str):
        self.log(message, "REFLECTION", Fore.MAGENTA)
