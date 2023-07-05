from jinja2 import Template
from jinja2 import FileSystemLoader
from jinja2.environment import Environment


class View:
    """
    Класс page-controller
    """

    routes = dict()

    def add_route(self, route: str, template: str, view=None):
        """
        Метод добавления роута и файла шаблона для этого роута
        Шаблоны должны храниться в папке /templates
        Args:
            route (str): роут
            template (str): имя файла шаблона
            view : пользовательская функция для обработки данных, по умалчанию None
        """
        if not route.endswith("/"):
            route = f"{route}/"
        self.routes[route] = (template, view)

    def get_view(self, path: str, request: dict):
        """
        Метод, который ищет и возвращает view по роуту,
        или возвращает 404
        Args:
            path (str): роут для поиска
            request (dict): словарь с параметрами

        Returns:
            (tuple): строка с кодом ответа, view  в байтах
        """
        if not path.endswith("/"):
            path = f"{path}/"
        if path in self.routes:
            # если не была добавленна пользовательская вьюха:
            if not self.routes[path][1]:
                return "200 OK", [bytes(self.render(self.routes[path][0]), "utf-8")]
            else:
                # если была добавленна пользовательская вьюха, вызываем ее, и результат отдаем как
                # именнованный параметр
                return "200 OK", [
                    bytes(
                        self.render(
                            self.routes[path][0],
                            object_list=self.routes[path][1](request),
                        ),
                        "utf-8",
                    )
                ]
        else:
            return "404 WHAT", [b"404 PAGE Not Found"]

    @staticmethod
    def render(template_name, folder="templates", **kwargs):
        env = Environment()
        env.loader = FileSystemLoader(folder)
        template = env.get_template(template_name)
        return template.render(**kwargs)
