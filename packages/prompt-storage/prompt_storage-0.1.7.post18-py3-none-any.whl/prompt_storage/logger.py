import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

class BriefFormatter(logging.Formatter):
    def formatException(self, exc_info):
        # Получаем стандартную трассировку и возвращаем только первую строку
        result = super().formatException(exc_info)
        if result:
            return result.splitlines()[0]
        return ""

class LoggerManager:
    def __init__(self, log_dir=None, max_log_files=3,
                 logger_level=logging.DEBUG, file_log_level=logging.INFO, console_log_level=logging.INFO):
        """
        Менеджер логирования для prompt-storage.
        
        :param log_dir: Директория для хранения логов. Если None или "", файловый обработчик отключается.
        :param max_log_files: Максимальное количество файлов логов.
        :param logger_level: Общий уровень логирования для логгера.
        :param file_log_level: Уровень логирования для файлового обработчика.
        :param console_log_level: Уровень логирования для консольного обработчика.
        """
        self.log_dir = log_dir
        self.max_log_files = max_log_files
        self.logger_level = logger_level
        self.file_log_level = file_log_level
        self.console_log_level = console_log_level

        self.logger = logging.getLogger("prompt_storage_logger")
        self.logger.setLevel(self.logger_level)
        self.logger.propagate = False

        # Настраиваем консольный обработчик всегда
        self._setup_console_handler()

        # Если директория логов указана, настраиваем файловый обработчик
        if self.log_dir:
            os.makedirs(self.log_dir, exist_ok=True)
            self._cleanup_old_logs()
            self._setup_file_handler()

    def _cleanup_old_logs(self):
        """Удаляет старые лог-файлы, если их количество превышает max_log_files."""
        log_files = sorted(
            [os.path.join(self.log_dir, f) for f in os.listdir(self.log_dir)
             if f.startswith("app_") and f.endswith(".log")],
            key=os.path.getctime
        )
        while len(log_files) > self.max_log_files:
            oldest_file = log_files.pop(0)
            os.remove(oldest_file)
            #print(f"🗑 Удален старый лог-файл: {oldest_file}")

    def _setup_file_handler(self):
        """Настраивает файловый обработчик логирования с ротацией."""
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(module)s.%(funcName)s - %(message)s"
        log_filename = os.path.join(self.log_dir, f"app_{datetime.now().strftime('%Y-%m-%d')}.log")
        file_handler = RotatingFileHandler(log_filename, maxBytes=5 * 1024 * 1024, backupCount=self.max_log_files)
        file_handler.setLevel(self.file_log_level)
        file_handler.setFormatter(logging.Formatter(log_format))
        self.logger.addHandler(file_handler)

    def _setup_console_handler(self):
        """Настраивает консольный обработчик логирования с кратким форматом."""
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.console_log_level)
        # Используем BriefFormatter для вывода краткой информации об ошибках
        brief_formatter = BriefFormatter("%(asctime)s - %(levelname)s - %(module)s.%(funcName)s - %(message)s")
        console_handler.setFormatter(brief_formatter)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        """Возвращает настроенный логгер."""
        return self.logger
