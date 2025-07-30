# PromptStorage 🚀

**Назначение**

Библиотека prompt-storage предназначена для ускорения разработки проектов путем распараллеливания процессов создания кода и работы промпт-инженеров.

**Элегантное решение для управления промптами из Google Docs с кешированием и шаблонизацией**

PromptStorage – это мощная и гибкая библиотека, которая превращает Google Docs в вашу персональную базу промптов для работы с языковыми моделями. Забудьте о хардкоде промптов в коде или о сложных системах управления контентом – используйте знакомый всем Google Docs для создания, редактирования и управления промптами в удобном интерфейсе!

## 🌟 Основные преимущества

- **Интеграция с Google Docs** – храните промпты там, где их удобно редактировать
- **Интеллектуальное кеширование** – мгновенный доступ к промптам даже без интернета
- **Гибкая шаблонизация** – поддержка Jinja2 и Mako для динамического контента
- **Встроенная интеграция с FastAPI** – создавайте API для промптов за минуты
- **Простота использования** – получение и обработка промптов всего за несколько строк кода
- **Оптимизация производительности** – кеширование минимизирует запросы к API

## 📦 Установка

### Базовая установка
```bash
pip install prompt-storage
```

### Установка с поддержкой API (FastAPI)
```bash
pip install "prompt-storage[api]"
```

### Установка в Google Colab (избегая конфликтов)
```python
!pip install --no-dependencies prompt-storage
!pip install google-api-python-client google-auth google-auth-oauthlib python-docx jinja2 mako
# Для работы с API:
# !pip install fastapi
```

## 🚀 Быстрый старт

```python
from prompt_storage import PromptStorage
from prompt_storage.template_processor import TemplateProcessor

# Инициализация хранилища промптов
storage = PromptStorage(
    credentials_path="credentials.json",
    token_path="token.json",
    cache_dir="./cache"
)

# Получение промпта по ID документа
prompt = storage.get_prompt("your_google_doc_id")

# Обработка промпта как шаблона
template_processor = TemplateProcessor()
processed_prompt = template_processor.process_template(
    prompt, 
    {"variable": "value", "user_name": "Иван"},
    template_engine="jinja2"
)

print(processed_prompt)
```

## 💡 Ключевые возможности

### Google Docs Processor

```python
from prompt_storage import GoogleDocsProcessor

# Инициализация процессора Google Docs
processor = GoogleDocsProcessor(
    credentials_path="credentials.json",
    token_path="token.json"
)

# Загрузка документа
document = processor.get_document("your_google_doc_id")

# Извлечение текста
text = processor.extract_text(document)
```

### Управление кешем

```python
from prompt_storage import GoogleDocsCacheManager

# Инициализация менеджера кеша
cache_manager = GoogleDocsCacheManager(cache_dir="./cache")

# Сохранение в кеш
cache_manager.save_to_cache("doc_id", "document_content")

# Проверка наличия в кеше
is_cached = cache_manager.is_cached("doc_id")

# Получение из кеша
content = cache_manager.get_from_cache("doc_id")
```

### Шаблонизация

```python
from prompt_storage import TemplateProcessor

# Инициализация процессора шаблонов
template_processor = TemplateProcessor()

# Jinja2 шаблонизация
jinja_result = template_processor.process_template(
    "Привет, {{ user_name }}! Ваш баланс: {{ balance }}.",
    {"user_name": "Иван", "balance": "1000₽"},
    "jinja2"
)

# Mako шаблонизация
mako_result = template_processor.process_template(
    "Привет, ${user_name}! Ваш баланс: ${balance}.",
    {"user_name": "Иван", "balance": "1000₽"},
    "mako"
)
```

## 🔧 Настройка доступа к Google API

1. Создайте проект в [Google Cloud Console](https://console.cloud.google.com/)
2. Включите Google Docs API для вашего проекта
3. Создайте учетные данные OAuth2 и скачайте файл credentials.json
4. При первом запуске библиотеки, будет запрошена авторизация через браузер

## 📊 Варианты использования

- **Управление промптами для LLM** – централизованное хранение и версионирование промптов
- **Создание многоязычных интерфейсов** – шаблоны с поддержкой переменных для локализации
- **Системы генерации контента** – динамические промпты для создания разнообразного контента
- **Автоматизация рутинных задач** – промпты для различных бизнес-процессов

## 📜 Лицензия

MIT

---

**Упростите управление промптами уже сегодня!** 🚀
