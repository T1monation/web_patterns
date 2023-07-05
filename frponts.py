class Front:
    """
    Класс front-controller
    """

    fronts = list()

    def add_front(self, front):
        """
        Метод добавления пользовательских фронт-контроллеров
        Args:
            front (function): функция пользовательского фронт-контроллера
        """
        self.fronts.append(front)

    def processing_request(self, request: dict) -> dict:
        """
        Метод для обработки словаря request пользовательскими фронт-контроллерами

        Args:
            request (dict): словарь request

        Returns:
            dict: словарь request после обработки фронт-контроллерами
        """
        for front in self.fronts:
            front(request)
        return request
