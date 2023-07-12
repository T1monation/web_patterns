class AppRoute:
    def __init__(self, routes, url):
        """
        Сохраняем значение переданного параметра
        """
        if not url.endswith("/"):
            url = f"{url}/"
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        """
        Сам декоратор
        """
        self.routes[self.url] = cls()


class SimpleTemplateRoute:
    """
    Класс для обработки простых шаблонов
    """

    def __init__(self, routes_storage: dict, register_routes: dict) -> None:
        """

        Args:
            routes_storage (dict): Переменная-словарь  вида {"путь": "вьюха"}
            register_routes (dict): Переменная-словарь вида {"путь": "файл шаблона"}
        """
        for key, value in register_routes.items():
            if not key.endswith("/"):
                key = f"{key}/"
            routes_storage[key] = BasicView(value)


class Debug:
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        """
        сам декоратор
        """

        # это вспомогательная функция будет декорировать каждый отдельный метод класса, см. ниже
        def timeit(method):
            """
            нужен для того, чтобы декоратор класса wrapper обернул в timeit
            каждый метод декорируемого класса
            """

            def timed(*args, **kw):
                ts = time()
                result = method(*args, **kw)
                te = time()
                delta = te - ts

                print(f"debug --> {self.name} выполнялся {delta:2.2f} ms")
                return result

            return timed

        return timeit(cls)
