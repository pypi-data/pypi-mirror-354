import os
import json
import asyncio
from datetime import datetime, timedelta
from .google_docs_processor import GoogleDocsProcessor
import logging

class GoogleDocsCacheManager:
    _shared_memory_cache = {}  # Глобальный кэш в памяти для всех экземпляров

    def __init__(self, credentials_info=None, credentials_file=None, cache_directory: str = None, max_concurrent_tasks: int = 10, cache_ttl_seconds: int = 1800, logger: logging.Logger = None, dev_mode: bool = True):
        """
        Инициализация менеджера кэша для Google Docs.

        :param credentials_info: JSON-словарь с учетными данными сервисного аккаунта.
        :param credentials_file: Путь к файлу с учетными данными Google API.
        :param cache_directory: Директория для хранения кэша. Если None, то кэш только в памяти.
        :param max_concurrent_tasks: Максимальное количество одновременных задач.
        :param cache_ttl_seconds: Время жизни кэша в секундах.
        :param logger: Логгер для записи событий.
        :param dev_mode: Разрешает использование GoogleDocsProcessor (True - разрешен, False - только кеш).
        """
        self.logger = logger if logger else logging.getLogger(__name__) if logger is not None else None
        self.cache_directory = cache_directory
        self.cache_ttl = timedelta(seconds=cache_ttl_seconds) if dev_mode else None
        self.dev_mode = dev_mode
        self.processor = GoogleDocsProcessor(
            credentials_info=credentials_info,
            credentials_file=credentials_file,
            max_concurrent_tasks=max_concurrent_tasks,
            logger=self.logger
        ) if dev_mode else None

        if cache_directory:
            os.makedirs(cache_directory, exist_ok=True)

    def _get_cached_file_path(self, document_id: str) -> str:
        return os.path.join(self.cache_directory, f"{document_id}.json") if self.cache_directory else None

    def _is_cache_valid(self, file_path: str) -> bool:
        if not file_path or not os.path.exists(file_path):
            return False
        if not self.dev_mode:
            return True  # В продакшн-режиме кеш не устаревает
        file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        return datetime.now() - file_mod_time <= self.cache_ttl

    def _validate_cached_file(self, document_id: str) -> bool:
        file_path = self._get_cached_file_path(document_id)
        if not file_path or not os.path.exists(file_path):
            return False
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                json.load(file)
            return True
        except (IOError, json.JSONDecodeError):
            return False

    def get_cached_document(self, document_id: str) -> dict | None:
        """
        Возвращает документ из кэша, сначала проверяя память, затем диск.

        :param document_id: ID документа Google Docs.
        :return: JSON-структура документа или None, если кэш отсутствует или устарел.
        """
        # Проверяем кэш в памяти (глобальный)
        cache_entry = GoogleDocsCacheManager._shared_memory_cache.get(document_id)
        if cache_entry and (not self.dev_mode or datetime.now() - cache_entry["timestamp"] <= self.cache_ttl):
            return cache_entry["data"]

        # Проверяем кэш на диске
        file_path = self._get_cached_file_path(document_id)
        if file_path and os.path.exists(file_path):
            if not self.dev_mode or self._is_cache_valid(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        GoogleDocsCacheManager._shared_memory_cache[document_id] = {"data": data, "timestamp": datetime.now()}
                        return data
                except (IOError, json.JSONDecodeError):
                    return None
        return None

    async def update_cache(self, document_ids: list[str], forced_reload: bool = False) -> dict:
        """
        Обновляет кэш документов, которые устарели, отсутствуют или требуют перезагрузки.
        
        :param document_ids: Список ID документов Google Docs.
        :param forced_reload: Принудительная перезагрузка документов.
        :return: Словарь с результатами обновления.
        """
        documents_to_update = []
        results = {}

        for document_id in document_ids:
            cached_data = self.get_cached_document(document_id)
            if forced_reload or cached_data is None:
                if not self.dev_mode:
                    results[document_id] = {
                        'status': {
                            'error_code': 3,
                            'from_cache': False,
                            'next_update': None
                        }
                    }
                    continue
                documents_to_update.append(document_id)
            else:
                results[document_id] = {
                    'status': {
                        'error_code': 0,
                        'from_cache': True,
                        'next_update': "Never" if not self.dev_mode else (datetime.now() + self.cache_ttl).strftime("%Y-%m-%d %H:%M:%S")
                    }
                }

        if self.dev_mode and documents_to_update:
            if self.logger:
                self.logger.info("Обновляем следующие документы: %s", documents_to_update)
            try:
                docs_loaded = await self.processor.process_documents(documents_to_update)
                for doc_loaded in docs_loaded:
                    doc_id = doc_loaded['document_id']
                    # Если в результате содержится ошибка, передаем её сквозным образом
                    if "status" in doc_loaded and doc_loaded["status"]["error_code"] != 0:
                        results[doc_id] = doc_loaded
                        continue

                    # Обновляем кэш для успешно загруженных документов
                    GoogleDocsCacheManager._shared_memory_cache[doc_id] = {"data": doc_loaded, "timestamp": datetime.now()}
                    if self.cache_directory:
                        file_path = self._get_cached_file_path(doc_id)
                        try:
                            with open(file_path, 'w', encoding='utf-8') as file:
                                json.dump(doc_loaded, file, ensure_ascii=False, indent=2)
                        except IOError:
                            pass
                    results[doc_id] = {
                        'status': {
                            'error_code': 0,
                            'from_cache': False,
                            'next_update': "Never" if not self.dev_mode else (datetime.now() + self.cache_ttl).strftime("%Y-%m-%d %H:%M:%S")
                        }
                    }
            except Exception as e:
                if self.logger:
                    self.logger.error("❌ Общая ошибка при обновлении кэша: %s", str(e))
                for document_id in documents_to_update:
                    results[document_id] = {
                        'status': {
                            'error_code': 2,
                            'from_cache': False,
                            'next_update': None
                        }
                    }

        return results
