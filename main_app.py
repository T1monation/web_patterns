from templator import render
from views import View


class FrameWorkApp:
    def __init__(self, views: View, fronts):
        self.fronts = fronts
        self.views = views

    def __call__(self, environ, start_response):
        method = environ["REQUEST_METHOD"]
        print("method", method)
        data = self.get_wsgi_input_data(environ)
        print(data)
        path = environ["PATH_INFO"]
        request = {}
        # front controller
        for front in self.fronts:
            front(request)
        print(request)
        code, body = self.views.get_view(path, request)
        start_response(code, [("Content-Type", "text/html")])
        return body

    @staticmethod
    def get_wsgi_input_data(env: dict) -> dict:
        request = {}
        if env["REQUEST_METHOD"] == "GET":
            data = env["QUERY_STRING"]
            if data:
                data_str = data
            else:
                return request

        if env["REQUEST_METHOD"] == "POST":
            # получаем длину тела, они приходит в строковом формате
            content_length_data = env.get("CONTENT_LENGTH")
            # приводим к int, если тело есть, иначе возвращаем 0
            content_length = int(content_length_data) if content_length_data else 0
            # считываем данные если они есть
            if content_length > 0:
                data = env["wsgi.input"].read(content_length)
                data_str = data.decode(encoding="utf-8")
                print(data_str)
            else:
                return request

        print(data_str)
        params = data_str.split("&")
        for item in params:
            # делим ключ и значение через =
            k, v = item.split("=")
            request[k] = v
        return request
