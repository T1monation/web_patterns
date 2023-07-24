# Файл с пользовательскими вьюхами
from patterns.decorators import render
from patterns.decorators import AppRoute, Debug
from patterns.creation import Engine, Logger, MapperRegistry, Product
from patterns.behavior import SmsNotifier, EmailNotifier, BaseSerializer
from patterns.unit_of_work import UnitOfWork


engine = Engine()
routes = dict()
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
logger = Logger("framework")
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


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
                # engine.categories.append(new_category)
                new_category.mark_new()
                try:
                    UnitOfWork.get_current().commit()
                except Exception as e:
                    return "500 OK", render(
                        "admin_message_template.html", message=f"Ошибка: {e}"
                    )
                else:
                    logger.log(f"категория {name} созданна")
                    return "200 OK", render(
                        "admin_message_template.html",
                        message=f"Категория {name} созданна!",
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
            print(MapperRegistry.get_current_mapper("category").all())
            return "200 OK", render(
                "admin_create_product.html",
                categories=MapperRegistry.get_current_mapper("category").all(),
            )
        if request["method"] == "POST":
            if not engine.get_product(request["product_name"]):
                new_product = Product(
                    request["product_name"],
                    request["selected_category"],
                    request["product_prise"],
                )
                new_product.observers.append(email_notifier)
                new_product.observers.append(sms_notifier)
                new_product.mark_new()
                try:
                    UnitOfWork.get_current().commit()
                except Exception as e:
                    return "500 OK", render(
                        "admin_message_template.html", message=f"Ошибка: {e}"
                    )
                else:
                    logger.log(f"товар {request['product_name']} добавлен в каталог")
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
        mapper = MapperRegistry.get_current_mapper("category")
        categories = mapper.all()
        if len(categories) == 0:
            return "200 OK", render(
                "message_template.html",
                message=f"В каталоге пока пусто!",
            )
        else:
            if request["method"] == "GET":
                return "200 OK", render("shop.html", categories=categories)
            if request["method"] == "POST":
                mapper = MapperRegistry.get_current_mapper("product")
                try:
                    product_list = mapper.find_by_category_name(
                        request["find_category"]
                    )
                except Exception as e:
                    return "200 OK", render(
                        "admin_message_template.html",
                        message=f"В категории {request['find_category']} товаров еще нет",
                    )
                else:
                    return "200 OK", render(
                        "shop.html", categories=categories, product_list=product_list
                    )


@AppRoute(routes=routes, url="/admin/create_tree")
class MakeTree:
    @Debug(name="MakeTree")
    def __call__(self, request):
        if request["method"] == "GET":
            if len(engine.categories) == 0:
                return "200 OK", render(
                    "admin_message_template.html",
                    message=f"Категории еще  не созданны.",
                )
            parrent_categories = engine.categories
            child_categories = [
                el for el in engine.categories if el.id not in engine.category_tree
            ]
            return "200 OK", render(
                "admin_create_tree.html",
                parrent_categories=parrent_categories,
                child_categories=child_categories,
            )
        if request["method"] == "POST":
            if request["parrent_category"] == request["child_category"]:
                return "200 OK", render(
                    "admin_message_template.html",
                    message=f"Родительская и дочерняя категории не могут быть одинаковыми",
                )
            if request["child_category"] in engine.category_tree:
                return "200 OK", render(
                    "admin_message_template.html",
                    message=f"Категория {request['child_category']} уже добавленна в дерево как родительская.",
                )
            if request["parrent_category"]:
                engine.add_to_tree(
                    engine.find_category_by_name(request["parrent_category"]),
                    engine.find_category_by_name(request["child_category"]),
                )
                return "200 OK", render(
                    "admin_message_template.html",
                    message=f"Элемент дерева успешно добавлен",
                )
            return "500", render(
                "admin_message_template.html",
                message=f"что-то пошло не так(",
            )


@AppRoute(routes=routes, url="/admin/sale/")
class Sale:
    @Debug(name="Sale")
    def __call__(self, request):
        if request["method"] == "GET":
            return "200 OK", render(
                "admin_sale.html",
                products=engine.products,
            )
        if request["method"] == "POST":
            find_product_name = request["product_on_sale"]
            for el in engine.products:
                if el.name == find_product_name:
                    el.set_price(request["sale_value"])
                    logger.log(
                        f"установленна скидка {request['sale_value']}% для товара {el.name}"
                    )
                    return "200 OK", render(
                        "admin_message_template.html",
                        message=f"Скидка на товар {el.name} составит {request['sale_value']}% итоговая цена - {el.price}",
                    )
            else:
                return "200 OK", render(
                    "admin_message_template.html",
                    message=f"товар с названием {request['product_name']} уже существует!",
                )


@AppRoute(routes=routes, url="/api/categories")
class CourseApi:
    @Debug(name="CourseApi")
    def __call__(self, request):
        print(request)
        return "200 OK", BaseSerializer(engine.categories).save()
