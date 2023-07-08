# Файл с пользовательскими вьюхами
from views import AppRoute, Debug, render
from patterns.creation import Engine


engine = Engine()
routes = dict()


@AppRoute(routes=routes, url="/messages/")
class MessageReader:
    @Debug(name="MessageReader")
    def __call__(self, request):
        if request["stored_messages"] == []:
            return "200 OK", render("message_template.html", message="Сообщений нет")
        else:
            return "200 OK", render(
                "messages.html", object_list=request["stored_messages"]
            )


@AppRoute(routes=routes, url="/admin/create_category/")
class CreateCategory:
    @Debug(name="CreateCategory")
    def __call__(self, request):
        if request["method"] == "GET":
            return "200 OK", render("admin_create_category.html")
        if request["method"] == "POST":
            # метод пост

            name = request["product_category"]
            name = engine.decode_value(name)

            # Проверяем на уникальность:
            find_category = engine.find_category_by_name(name)

            if not find_category:
                new_category = engine.create_category(name)
                engine.categories.append(new_category)
                return "200 OK", render(
                    "admin_message_template.html", message=f"Категория {name} созданна!"
                )

            else:
                return "200 OK", render(
                    "admin_message_template.html",
                    message=f"Категория с названием {name} уже существует!",
                )


@AppRoute(routes=routes, url="/admin/create_product/")
class CreateProduct:
    @Debug(name="CreateProduct")
    def __call__(self, request):
        if request["method"] == "GET":
            return "200 OK", render(
                "admin_create_product.html",
                categories=engine.categories,
                product_types=engine.get_product_type(),
            )
        if request["method"] == "POST":
            if not engine.get_product(request["product_name"]):
                new_product = engine.create_product(
                    request["selected_product_type"],
                    request["product_name"],
                    request["selected_category"],
                    request["product_prise"],
                )
                engine.products.append(new_product)
                return "200 OK", render(
                    "admin_message_template.html",
                    message=f"Товар {request['product_name']} добавлен в каталог",
                )
            else:
                return "200 OK", render(
                    "admin_message_template.html",
                    message=f"товар с названием {request['product_name']} уже существует!",
                )


@AppRoute(routes=routes, url="/shop/")
class ShowShop:
    @Debug(name="ShowShop")
    def __call__(self, request):
        if len(engine.categories) == 0:
            return "200 OK", render(
                "message_template.html",
                message=f"В каталоге пока пусто!",
            )
        else:
            all_categories = []
            for category in engine.categories:
                all_categories.append(category.name)
            if request["method"] == "GET":
                return "200 OK", render("shop.html", categories=all_categories)
            if request["method"] == "POST":
                find_category = request["find_category"]
                product_list = [
                    el for el in engine.products if el.category == find_category
                ]
                return "200 OK", render(
                    "shop.html", categories=all_categories, product_list=product_list
                )
