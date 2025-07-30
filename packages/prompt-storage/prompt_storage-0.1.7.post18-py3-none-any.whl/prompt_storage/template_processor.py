from jinja2 import Environment, Template, DebugUndefined
from mako.template import Template as MakoTemplate

class TemplateProcessor:
    def __init__(self, engine="text"):
        """
        Универсальный обработчик шаблонов.

        :param engine: Название движка ('jinja2', 'mako', 'text' - без обработки).
        """
        self.engine = engine.lower()
        if self.engine == "jinja2":
            self.env = Environment(undefined=DebugUndefined)  # Сохраняем неизвестные переменные

    def render(self, text, variables=None):
        """
        Рендерит текст с использованием указанного движка.

        :param text: Исходный текст.
        :param variables: Словарь переменных для шаблона.
        :return: Отрендеренный текст.
        """
        variables = variables or {}

        if self.engine == "jinja2":
            try:
                template = self.env.from_string(text)
                return template.render(**variables)
            except Exception as e:
                return f"Ошибка рендеринга Jinja2: {str(e)}"

        elif self.engine == "mako":
            try:
                template = MakoTemplate(text)
                return template.render(**variables)
            except Exception as e:
                return f"Ошибка рендеринга Mako: {str(e)}"

        elif self.engine == "text":
            return text  # Просто возвращаем текст без обработки

        return f"Ошибка: Неизвестный движок шаблонов '{self.engine}'"
