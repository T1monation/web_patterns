from copy import deepcopy
from quopri import decodestring


class User:
    pass


# Клиент условного интернет-магазина
class Client(User):
    pass


# Персонал условного интернет-магазина
class Staff(User):
    pass


class UserFactory:
    """
    Класс-фабрика по созданию пользователей
    roles: словарь, в котором храняться пользовательские роли
    """

    roles = {
        "client": Client,
        "staff": Staff,
    }

    @classmethod
    def create(cls, role: str):
        """
        Метод создает экземпляр пользовательского класса с заданной ролью
        Args:
            role (str): роль пользователя

        Returns:
            User-class: возвращает экземпляр пользовательского класса
        """
        return cls.roles[role]()


class ProductPrototype:
    def clone(self):
        return deepcopy(self)


class Product(ProductPrototype):
    def __init__(self, name: str, category: str, prise: str):
        """
        Экземпляр класса Product
        Args:
            name (str): наименование товара
            category (str): категория товара
            prise (str): цена товара
        """
        self.name = name
        self.category = category
        self.prise = prise
        self.category = category


class Ram(Product):
    pass


class Cpu(Product):
    pass


class Gpu(Product):
    pass


class ProductFactory:
    product_types = {
        "ram": Ram,
        "cpu": Cpu,
        "gpu": Gpu,
    }

    @classmethod
    def create(cls, product_type: str, name: str, categoty: str, prise: str):
        """
        Создание экземпляра класса товара
        Args:
            product_type (str): тип товара
            name (str): имя товара
            categoty (str): категория товара
            prise (str): цена товара

        Returns:
            class: экземпляр класса товара
        """
        return cls.product_types[product_type](name, categoty, prise)


class Category:
    auto_id = 0

    def __init__(self, name: str, category: str):
        """
        Инициализация класса Category
        Args:
            name (str): название категории
            category (str): [description]
        """
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.products = []

    def products_count(self):
        result = len(self.products)
        if self.category:
            result += self.category.products_count()
        return result


class Engine:
    def __init__(self):
        self.clients = []
        self.stuff = []
        self.products = []
        self.categories = []

    @staticmethod
    def create_user(role: str):
        """
        Создание пользователя
        Args:
            role (str): пользовательская роль

        Returns:
            class: Экземпляр класа пользователя
        """
        return UserFactory.create(role)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id: int):
        """
        Метод поиска категории по id
        Args:
            id (int): id категории

        Raises:
            Exception: не найдена категория с заданным id

        Returns:
            [type]: найденная категория товара
        """
        for item in self.categories:
            print("item", item.id)
            if item.id == id:
                return item
        raise Exception(f"Нет категории с id = {id}")

    def find_category_by_name(self, name: str):
        """
        Метод поиска категории по названию
        Args:
            name (str): название категории

        Returns:
            [type]: найденная категория товара или None
        """
        for item in self.categories:
            print("item", item.name)
            if item.name == name:
                return item
        return None

    @staticmethod
    def create_product(product_type, name, category, prise):
        return ProductFactory.create(product_type, name, category, prise)

    def get_product(self, name: str):
        """
        Метод для поиска товара по его имени
        Args:
            name (str): название товара

        Returns:
            [type]: [description]
        """
        for item in self.products:
            if item.name == name:
                return item
        return None

    @staticmethod
    def get_product_type():
        """
        Метод для получения списка из доступных типов продуктов
        Returns:
            [type]: [description]
        """
        return [key for key in ProductFactory.product_types]

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace("%", "=").replace("+", " "), "UTF-8")
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode("UTF-8")


# порождающий паттерн Синглтон
class SingletonByName(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs["name"]

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Sotorage(metaclass=SingletonByName):
    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print("log--->", text)
