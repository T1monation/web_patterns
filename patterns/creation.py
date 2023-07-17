from copy import deepcopy
from quopri import decodestring
from sqlite3 import connect
from time import ctime, time
from patterns.behavior import Subject, FileWriter
from patterns.unit_of_work import DomainObject

connection = connect("patterns.sqlite")


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


class Product(ProductPrototype, Subject, DomainObject):
    def __init__(self, name: str, category: str, price: str, percent=0):
        """
        Экземпляр класса Product
        Args:
            name (str): наименование товара
            category (str): категория товара
            prise (str): цена товара
            percent (int): процент скидки на товар
        """
        self.name = name
        self.category = category
        self.price = float(price)
        self.category = category
        self.percent = percent
        super().__init__()

    def set_price(self, percent):
        """
        метод корректировки цены
        Args:
            percent : значение в процентах, на которое меняеться цена товара
        """
        self.percent = percent
        self.price = self.price * (100 - float(percent)) / 100
        self.notify()


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
    def create(cls, name: str, categoty: str, prise: str):
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


class Category(DomainObject):
    auto_id = 0

    def __init__(self, name: str):
        """
        Инициализация класса Category
        Args:
            name (str): название категории
            category (str): [description]
        """
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.products = []

    def __getitem__(self, item):
        return self.products[item]

    def add_product(self, product: Product):
        self.products.append(product)
        product.category = self.name


class Engine:
    def __init__(self):
        self.clients = []
        self.stuff = []
        self.products = []
        self.categories = []
        self.category_tree = dict()

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
    def create_category(name):
        return Category(name)

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
    def create_product(name, category, prise):
        return ProductFactory.create(name, category, prise)

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

    def add_to_tree(self, parrent: Category, child: Category = None):
        if not child:
            self.category_tree[str(parrent.id)] = []
        else:
            if str(parrent.id) in self.category_tree:
                self.category_tree[str(parrent.id)].append(str(child.id))
            else:
                self.category_tree[str(parrent.id)] = [str(child.id)]

    @property
    def get_tree(self):
        print(self.category_tree)
        returned_list = []
        for key in self.category_tree:
            returned_list.append(
                [
                    self.find_category_by_name(key),
                    [self.find_category_by_name(el) for el in self.category_tree[key]],
                ]
            )
        print(returned_list)
        return returned_list


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


class Logger(metaclass=SingletonByName):
    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f"log---> {text} [{ctime(time())}]"
        self.writer.write(text)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f"Db commit error: {message}")


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f"Db update error: {message}")


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f"Db delete error: {message}")


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f"Record not found: {message}")


class ProductMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = "product"

    def all(self):
        statement = f"SELECT * from {self.tablename}"
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name, category, price, percent = item
            product = Product(name, category, price)
            product.id = id
            product.percent = percent
            result.append(product)

    def find_by_id(self, id):
        statement = f"SELECT id, name, category, price, percent  FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Product(*result)
        else:
            raise RecordNotFoundException(f"record with id={id} not found")

    def find_by_category_name(self, name):
        statement = f"SELECT id, name, category, price, percent  FROM {self.tablename} WHERE category=?"
        self.cursor.execute(statement, (name,))
        result = []
        for item in self.cursor.fetchall():
            id, name, category, price, percent = item
            product = Product(name, category, price, percent)
            product.id = id
            result.append(product)
        if len(result) > 0:
            return result
        else:
            raise RecordNotFoundException(f"record with name={name} not found")

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, category, price, percent) VALUES (?, ?, ?, ?)"
        self.cursor.execute(statement, (obj.name, obj.category, obj.price, obj.percent))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = (
            f"UPDATE {self.tablename} SET name={obj.name}, category={obj.category}, "
            f"price={obj.price}, percent={obj.percent}  WHERE id={obj.id}"
        )

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class CategoryMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = "category"

    def all(self):
        statement = f"SELECT * from {self.tablename}"
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            category = Category(name)
            category.id = id
            result.append(category)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Product(*result)
        else:
            raise RecordNotFoundException(f"record with id={id} not found")

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name={obj.name}, WHERE id={obj.id}"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {"product": ProductMapper, "category": CategoryMapper}

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Product):
            return ProductMapper(connection)
        if isinstance(obj, Category):
            return CategoryMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)
