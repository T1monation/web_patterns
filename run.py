from wsgiref.simple_server import make_server
from views import View
from main_app import FrameWorkApp


def secret_front(request):
    request["secret"] = "some secret"


def other_front(request):
    request["key"] = "key"


fronts = [secret_front, other_front]

# создаем "хранилище" путей и вьюх
vievs = View()
vievs.add_route("/", "authors.html")
vievs.add_route("/a_page", "simplestyle_horizon_a_page.html")
vievs.add_route("/contacts", "simplestyle_horizon_contact_us.html")
vievs.add_route("/another", "simplestyle_horizon_another_page.html")

app = FrameWorkApp(vievs, fronts)


with make_server("", 8000, app) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
