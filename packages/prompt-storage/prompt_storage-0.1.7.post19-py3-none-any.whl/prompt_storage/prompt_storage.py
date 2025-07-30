import traceback
from .google_docs_cache_manager import GoogleDocsCacheManager
from .logger import LoggerManager
from .template_processor import TemplateProcessor
import copy
import logging

# Время жизни кэша по умолчанию (1 месяц)
CACHE_TIMEOUT = 60 * 60 * 24 * 30

class PromptStorage:
    def __init__(self,
            credentials_info=None,
            credentials_file=None,
            cache_directory=None,
            log_directory=None,
            max_concurrent_tasks=10,
            cache_ttl_seconds=CACHE_TIMEOUT,
            dev_mode=False,
            file_log_level=logging.INFO,
            console_log_level=logging.INFO,
        ):
        """
        Инициализация PromptStorage.

        :param credentials_info: JSON-словарь с учетными данными сервисного аккаунта.
        :param credentials_file: Путь к файлу с учетными данными Google API.
        :param cache_directory: Директория для хранения кэшированных документов.
        :param max_concurrent_tasks: Максимальное количество одновременных задач.
        :param cache_ttl_seconds: Время жизни кэша в секундах.
        :param logger: Логгер, переданный из PromptStorage. Если None, логирование отключается.
        :param dev_mode: Разрешает использование GoogleDocsProcessor (True - разрешен, False - только кеш).
        """
        self.dev_mode = dev_mode

        # Инициализируем логгер
        self.logger_manager = LoggerManager(log_dir=log_directory, file_log_level=file_log_level, console_log_level=console_log_level)
        self.logger = self.logger_manager.get_logger()

        if self.logger:
            self.logger.info("⏳ Инициализация PromptStorage...")

        self.cache_manager = GoogleDocsCacheManager(
            credentials_info=credentials_info,
            credentials_file=credentials_file,
            cache_directory=cache_directory,
            max_concurrent_tasks=max_concurrent_tasks,
            cache_ttl_seconds=cache_ttl_seconds,
            logger=self.logger,
            dev_mode=self.dev_mode
        )

        if self.logger:
            self.logger.info("✅ PromptStorage успешно инициализирован.")

    async def update_documents(self, document_ids, forced_reload=False):
        if self.logger:
            self.logger.info("Запуск обновления документов: %s", document_ids)
        return await self.cache_manager.update_cache(document_ids, forced_reload=forced_reload)

    def get_cached_document(self, document_id):
        return self.cache_manager.get_cached_document(document_id)

    async def get_document_info(self, document_id, group_titles=None, tab_title=None, forced_reload=False):
        await self.update_documents([document_id], forced_reload=forced_reload)
        cached_document = self.get_cached_document(document_id)
        if not cached_document:
            return {"status": "failure", "tabs": []}
        
        tabs = cached_document.get("tabs", [])
        if group_titles:
            tabs = [tab for tab in tabs if tab.get("title") in group_titles]
        if tab_title:
            tabs = [tab for tab in tabs if tab.get("title") == tab_title]
        
        return {"tabs": tabs}  # Убрали status для совместимости с PromptStorage

    async def get_document_part(self, document_id, path="/", forced_reload=False):
        await self.update_documents([document_id], forced_reload=forced_reload)
        cached_document = self.get_cached_document(document_id)
        if not cached_document:
            return {"status": "failure", "tabs": []}
        
        tabs = cached_document.get("tabs", [])
        
        if not path or path == "/":
            return {"tabs": tabs}  # Убрали status

        path_parts = [part for part in path.split("/") if part]

        def find_tab_by_path(tabs, parts):
            if not parts:
                return None
            current_part = parts[0]
            for tab in tabs:
                if tab.get("title") == current_part:
                    if len(parts) == 1:
                        return tab
                    return find_tab_by_path(tab.get("children", []), parts[1:])
            return None

        matching_tab = find_tab_by_path(tabs, path_parts)
        if matching_tab:
            return {"tabs": [matching_tab]}  # Убрали status
        return {"tabs": []}  # Теперь всегда соответствует формату


    async def render_document_part_recursively(self, doc_id, path, parse_mode='text', template_vars=None, forced_reload=False):
        """
        Получение содержимого вкладки документа с рендерингом.

        :param doc_id: ID документа.
        :param path: Путь к вкладке.
        :param parse_mode: 'text' (по умолчанию), 'jinja2' или другой движок.
        :param template_vars: Переменные для рендеринга.
        :param forced_reload: Принудительная перезагрузка документа.
        :return: Содержимое вкладки.
        """
        def render_tabs_recursively(tabs, template_processor, template_vars):
            for tab in tabs:
                tab["tab_text"] = template_processor.render(tab["tab_text"], template_vars)
                if "children" in tab and tab["children"]:
                    render_tabs_recursively(tab["children"], template_processor, template_vars)

        found_part = await self.get_document_part(doc_id, path, forced_reload=forced_reload)

        if found_part and "tabs" in found_part:
            # Создаем глубокую копию, чтобы не менять оригинал
            rendered_part = copy.deepcopy(found_part)
            template_processor = TemplateProcessor(engine=parse_mode)
            render_tabs_recursively(rendered_part["tabs"], template_processor, template_vars)
            return rendered_part

        return found_part

    async def render_document_part(self, doc_id, path, parse_mode='text', template_vars=None, forced_reload=False):
        doc_part = await self.get_document_part(doc_id, path, forced_reload=forced_reload)
        try:
            if len(doc_part['tabs']) > 0:
                template = doc_part['tabs'][0]['tab_text']
                template_processor = TemplateProcessor(engine=parse_mode)
                return template_processor.render(template, template_vars)
            else:
                self.logger.error(f"Не удалось получить часть документа по пути: '{path}' для документа: '{doc_id}'. Ответ от сервиса: {doc_part!r}")
                return None
        except Exception as e:
            self.logger.error(f"Ошибка при рендеринге документа: {e}")
            self.logger.debug(traceback.format_exc())
            return None
