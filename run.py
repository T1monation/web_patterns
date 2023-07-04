from wsgiref.simple_server import make_server
from views import View
from frponts import Front
from main_app import FrameWorkApp


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
    print(1)
    if "stored_messages" in request:
        print(2)
        return request["stored_messages"]
    else:
        return None


# создаем хранилище фронтов и наполняем его пользовательсекими фронтами
fronts = Front()
fronts.add_front(secret_front)
fronts.add_front(other_front)
fronts.add_front(find_message)

# создаем "хранилище" путей и вьюх
vievs = View()
vievs.add_route("/", "index.html")
vievs.add_route("/authors", "authors.html")
vievs.add_route("/contact_us", "contact_us.html")
vievs.add_route("/messages", "messages.html", show_message)


app = FrameWorkApp(vievs, fronts)


with make_server("", 8000, app) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
