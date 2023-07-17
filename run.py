from wsgiref.simple_server import make_server
from patterns.decorators import SimpleTemplateRoute
from frponts import Front
from main_app import FrameWorkApp
from views import routes


# Пользовательские фронт-контроллеры
def secret_front(request):
    request["secret"] = "some secret"


def other_front(request):
    request["key"] = "key"


def find_message(request: dict):
    if ("login" and "title" and "text") in request:
        request["message"] = (
            request["login"],
            request["title"],
            request["text"],
        )

        request.pop("login")
        request.pop("title")
        request.pop("text")


# Пользовательская Вьюха
def show_message(request):
    if "stored_messages" in request:
        return request["stored_messages"]
    else:
        return None


# создаем хранилище фронтов и наполняем его пользовательсекими фронтами
fronts = Front()
fronts.add_front(secret_front)
fronts.add_front(other_front)
fronts.add_front(find_message)


simple_routes_templates = {
    "/": "index.html",
    "/authors": "authors.html",
    "/contact_us/": "contact_us.html",
    "/admin": "admin_start.html",
}
SimpleTemplateRoute(routes, simple_routes_templates)

app = FrameWorkApp(routes, fronts)


with make_server("", 8000, app) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
