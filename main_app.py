from quopri import decodestring
from templator import render
from views import ViewRegister
from frponts import Front


class FrameWorkApp:
    message_storage = list()

    def __init__(self, views: ViewRegister, fronts: Front):
        self.fronts = fronts
        self.views = views

    def __call__(self, environ, start_response):
        method = environ["REQUEST_METHOD"]
        print("method", method)
        request = self.get_wsgi_input_data(environ)
        request["method"] = environ["REQUEST_METHOD"]
        print(request)
        path = environ["PATH_INFO"]

        processed_request = self.fronts.processing_request(request)
        if "message" in processed_request:
            self.message_storage.append(processed_request["message"])
        processed_request["stored_messages"] = self.message_storage
        print(request)
        code, body = self.views.get_view(path, processed_request)
        start_response(code, [("Content-Type", "text/html")])
        return body

    @staticmethod
    def get_wsgi_input_data(env: dict) -> dict:
        """
        Функция для парсинга значений параметров из форм и адресной строки браузера
        при запросах "GET" и "POST"
        Args:
            env (dict): словарь environ

        Returns:
            dict: словарь полученных параметров
        """
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
        returned_request = FrameWorkApp.decode_value(request)

        return returned_request

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace("%", "=").replace("+", " "), "UTF-8")
            val_decode_str = decodestring(val).decode("UTF-8")
            new_data[k] = val_decode_str
        return new_data
