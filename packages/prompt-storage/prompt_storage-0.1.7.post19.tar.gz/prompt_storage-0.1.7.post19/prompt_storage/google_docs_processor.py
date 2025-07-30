import asyncio
import json
import os
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import logging
import traceback

class GoogleDocsProcessor:
    def __init__(self, credentials_info=None, credentials_file=None, max_concurrent_tasks=10, logger=None):
        """
        Инициализация процессора для работы с Google Docs.

        :param credentials_info: JSON-словарь с учетными данными сервисного аккаунта.
        :param credentials_file: Путь к файлу с учетными данными Google API.
        :param max_concurrent_tasks: Максимальное количество одновременных задач.
        :param logger: Логгер. Если None, создаётся новый логгер.
        """
        self.credentials_info = credentials_info
        self.credentials_file = credentials_file
        self.max_concurrent_tasks = max_concurrent_tasks

        # Настраиваем логгер
        self.logger = logger or logging.getLogger(__name__)
        if logger is None:
            logging.basicConfig(level=logging.INFO)
            self.logger.addHandler(logging.StreamHandler())

        self.logger.info("✅ GoogleDocsProcessor успешно инициализирован.")

    def _get_fresh_credentials(self):
        """Загружает учетные данные и обновляет токен, если необходимо."""
        scopes = ["https://www.googleapis.com/auth/documents.readonly"]

        try:
            if self.credentials_info:
                self.logger.info("🔑 Используется авторизация через JSON-словарь.")
                creds = Credentials.from_service_account_info(self.credentials_info, scopes=scopes)
            elif self.credentials_file and os.path.exists(self.credentials_file):
                self.logger.info("📂 Используется авторизация через файл: %s", self.credentials_file)
                creds = Credentials.from_service_account_file(self.credentials_file, scopes=scopes)
            else:
                raise ValueError("Не удалось загрузить учетные данные. Укажите credentials_info или путь к credentials_file.")

            # Обновляем токен, если истёк
            if creds.expired and creds.valid:
                self.logger.info("🔄 Обновление устаревшего токена...")
                creds.refresh(Request())

            return creds
        except Exception as e:
            self.logger.error("❌ Ошибка при получении учетных данных: %s", str(e))
            raise

    def fetch_document_sync(self, document_id):
        """
        Синхронное получение содержимого документа Google Docs.

        :param document_id: ID документа Google Docs.
        :return: JSON-структура документа или информация об ошибке.
        """
        # Получаем учетные данные с обработкой ошибок
        try:
            creds = self._get_fresh_credentials()
        except Exception as e:
            self.logger.error("❌ Ошибка при получении учетных данных для документа %s: %s", document_id, str(e))
            return {
                "document_id": document_id,
                "status": {
                    "error_code": 2,
                    "error_message": str(e),
                    "traceback": traceback.format_exc()
                }
            }

        # Создаем сервис Google Docs с обработкой ошибок
        try:
            service = build("docs", "v1", credentials=creds, cache_discovery=False)
        except Exception as e:
            self.logger.error("❌ Ошибка при создании сервиса Google Docs для документа %s: %s", document_id, str(e))
            return {
                "document_id": document_id,
                "status": {
                    "error_code": 2,
                    "error_message": str(e),
                    "traceback": traceback.format_exc()
                }
            }

        # Загружаем документ с обработкой ошибок
        try:
            self.logger.debug("🔍 Загрузка документа %s", document_id)
            document = service.documents().get(documentId=document_id, includeTabsContent=True).execute()
        except Exception as e:
            self.logger.error("❌ Ошибка при загрузке документа %s: %s", document_id, str(e))
            return {
                "document_id": document_id,
                "status": {
                    "error_code": 2,
                    "error_message": str(e),
                    "traceback": traceback.format_exc()
                }
            }

        return {
            "document_id": document_id,
            "title": document.get("title", "Unknown title"),
            "tabs": document.get("tabs", []) or []
        }

    async def extract_tab_content(self, tab):
        """Извлечение текста из вкладки документа."""
        content = tab.get('documentTab', {}).get('body', {}).get('content', []) or []
        return ''.join(
            text_element['textRun']['content']
            for element in content if 'paragraph' in element
            for text_element in element['paragraph'].get('elements', [])
            if 'textRun' in text_element
        )

    async def process_tabs(self, tabs):
        """Рекурсивная обработка вкладок и их преобразование в JSON."""
        async def process_single_tab(tab):
            tab_data = {
                "title": tab.get('tabProperties', {}).get('title', 'Untitled Tab'),
                "tab_id": tab.get('tabProperties', {}).get('tabId', 'Unknown'),
                "index": tab.get('tabProperties', {}).get('index', 'No Index'),
                "tab_text": await self.extract_tab_content(tab),
                "children": []
            }
            if 'childTabs' in tab:
                tab_data["children"] = await self.process_tabs(tab.get('childTabs', []))
            return tab_data

        return await asyncio.gather(*(process_single_tab(tab) for tab in tabs))

    async def process_document(self, document_id):
        """
        Асинхронная обработка одного документа и сохранение результата.

        :param document_id: ID документа Google Docs.
        :return: JSON-структура обработанного документа или информация об ошибке.
        """
        try:
            self.logger.info("📄 Начата обработка документа %s", document_id)
            document = await asyncio.to_thread(self.fetch_document_sync, document_id)

            # Если fetch_document_sync вернул ошибку, пробрасываем её далее
            if "status" in document and document["status"]["error_code"] != 0:
                self.logger.error("❌ Ошибка при загрузке документа %s: %s", document_id, document["status"]["error_message"])
                return document

            # Если ошибок при загрузке нет, проверяем наличие вкладок
            if 'tabs' in document and document['tabs']:
                tabs_json = await self.process_tabs(document['tabs'])
                return {
                    "document_id": document_id,
                    "title": document.get("title", "Unknown title"),
                    "tabs": tabs_json,
                    "status": {"error_code": 0, "error_message": None, "traceback": None}
                }
            else:
                self.logger.warning("⚠️ Документ %s не содержит вкладок", document_id)
                return {
                    "document_id": document_id,
                    #"title": document.get("title", "Unknown title"),
                    "status": {"error_code": 1, "error_message": "Документ не содержит вкладок", "traceback": None}
                }
        except Exception as e:
            self.logger.error("❌ Ошибка при обработке документа %s: %s", document_id, str(e))
            return {
                "document_id": document_id,
                "status": {"error_code": 2, "error_message": str(e), "traceback": traceback.format_exc()}
            }

    async def process_documents(self, document_ids):
        """
        Асинхронная обработка нескольких документов с ограничением на количество задач.

        :param document_ids: Список ID документов Google Docs.
        :return: Список загруженных документов (с данными или ошибками).
        """
        semaphore = asyncio.Semaphore(self.max_concurrent_tasks)

        async def process_with_semaphore(doc_id):
            async with semaphore:
                try:
                    return await self.process_document(doc_id)
                except Exception as e:
                    self.logger.error("❌ Ошибка при обработке документа %s: %s", doc_id, str(e))
                    return {
                        "document_id": doc_id,
                        "status": {"error_code": 3, "error_message": str(e), "traceback": traceback.format_exc()}
                    }

        self.logger.info("📂 Начата обработка %d документов", len(document_ids))
        results = await asyncio.gather(*[process_with_semaphore(doc_id) for doc_id in document_ids], return_exceptions=True)

        # Преобразование исключений в словари, если таковые возникли
        for idx, result in enumerate(results):
            if isinstance(result, Exception):
                self.logger.error("❌ Ошибка при обработке %s: %s", document_ids[idx], str(result))
                results[idx] = {
                    "document_id": document_ids[idx],
                    "status": {
                        "error_code": 3,
                        "error_message": str(result),
                        "traceback": ""
                    }
                }

        self.logger.info("✅ Обработка всех документов завершена")
        return results
