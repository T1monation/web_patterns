from wsgiref.simple_server import make_server
from views import ViewRegister
from frponts import Front
from main_app import FrameWorkApp
from user_views import MessageReader, CreateCategory, CreateProduct, ShowShop


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
views = ViewRegister()
views.add_route("/", "index.html")
views.add_route("/authors", "authors.html")
views.add_route("/contact_us", "contact_us.html")
views.add_route("/messages", "messages.html", MessageReader())
views.add_route("/admin", "admin_start.html")
views.add_route(
    "/admin/create_category", "admin_create_category.html", CreateCategory()
)
views.add_route("/admin/create_product", "admin_create_product.html", CreateProduct())
views.add_route("/shop", "shop.html", ShowShop())


app = FrameWorkApp(views, fronts)


with make_server("", 8000, app) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
