# Файл с пользовательскими вьюхами
from views import ViewRegister
from patterns.creation import Engine

engine = Engine()


class MessageReader:
    def __call__(self, template, request):
        if request["stored_messages"] == []:
            return ViewRegister.render("message_template.html", message="Сообщений нет")
        else:
            return ViewRegister.render(template, object_list=request["stored_messages"])


class CreateCategory:
    def __call__(self, template, request):
        if request["method"] == "GET":
            return ViewRegister.render(template)
        if request["method"] == "POST":
            # метод пост

            name = request["product_category"]
            name = engine.decode_value(name)

            # Проверяем на уникальность:
            find_category = engine.find_category_by_name(name)

            if not find_category:
                new_category = engine.create_category(name)
                engine.categories.append(new_category)
                return ViewRegister.render(
                    "admin_message_template.html", message=f"Категория {name} созданна!"
                )

            else:
                return ViewRegister.render(
                    "admin_message_template.html",
                    message=f"Категория с названием {name} уже существует!",
                )


class CreateProduct:
    def __call__(self, template, request):
        if request["method"] == "GET":
            return ViewRegister.render(
                template,
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
                return ViewRegister.render(
                    "admin_message_template.html",
                    message=f"Товар {request['product_name']} добавлен в каталог",
                )
            else:
                return ViewRegister.render(
                    "admin_message_template.html",
                    message=f"товар с названием {request['product_name']} уже существует!",
                )


class ShowShop:
    def __call__(self, template, request):
        if len(engine.categories) == 0:
            return ViewRegister.render(
                "message_template.html",
                message=f"В каталоге пока пусто!",
            )
        else:
            all_categories = []
            for category in engine.categories:
                all_categories.append(category.name)
            if request["method"] == "GET":
                return ViewRegister.render(template, categories=all_categories)
            if request["method"] == "POST":
                find_category = request["find_category"]
                product_list = [
                    el for el in engine.products if el.category == find_category
                ]
                return ViewRegister.render(
                    template, categories=all_categories, product_list=product_list
                )
