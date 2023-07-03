from templator import render


class View:
    routes = dict()

    def add_route(self, route: str, template: str):
        """
        Метод добавления роута и файла шаблона для этого роута
        Шаблоны должны храниться в папке /templates
        Args:
            route (str): роут
            template (str): имя файла шаблона
        """
        if not route.endswith("/"):
            route = route + "/"
        self.routes[route] = template

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
            path = path + "/"
        if path in self.routes:
            print(request)
            return "200 OK", [bytes(render(self.routes[path]), "utf-8")]
        else:
            return "404 WHAT", [b"404 PAGE Not Found"]
