from jinja2 import FileSystemLoader
from time import time
from jinja2.environment import Environment


class BasicView:
    """
    Класс для показа статтичных страниц, без передачи параметров
    """

    def __init__(self, template):
        self.template = template

    def __call__(self, *args, **kwargs):
        return "200 OK", render(self.template)


def render(template_name, folder="templates", **kwargs):
    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    return template.render(**kwargs)
