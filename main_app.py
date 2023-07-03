from templator import render
from views import View


class FrameWorkApp:

    def __init__(self, views: View, fronts):
        self.fronts = fronts
        self.views = views

    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']
        request = {}
        # front controller
        for front in self.fronts:
            front(request)
        print(request)
        code, body = self.views.get_view(path, request)
        start_response(code, [('Content-Type', 'text/html')])
        return body




