from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from wheezy.web.handlers import BaseHandler
from wheezy.http import WSGIApplication
from wheezy.routing import url
from wheezy.web.middleware import bootstrap_defaults, path_routing_middleware_factory
from wheezy.html.utils import html_escape
from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader
from wheezy.web.templates import WheezyTemplate
from geventwebsocket import WebSocketServer, WebSocketApplication, Resource


class Home(BaseHandler):

    def get(self):
        return self.render_response('templates/test.html')


class Api(BaseHandler):

    def get(self):
        if self.request.environ.get('wsgi.websocket'):
            ws = self.request.environ['wsgi.websocket']
            while True:
                message = ws.receive()
                ws.send(message)
        return

all_urls = [
    url('', Home),
    url('api', Api)
]


options = {}

# Template Engine
searchpath = ['']
engine = Engine(
    loader=FileLoader(searchpath),
    extensions=[
        CoreExtension(),
    ])
engine.global_vars.update({
    'h': html_escape
})

options.update({
    'render_template': WheezyTemplate(engine)
})


main = WSGIApplication(
    middleware=[
        bootstrap_defaults(url_mapping=all_urls),
        path_routing_middleware_factory
    ],
    options=options
)


if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), main, handler_class=WebSocketHandler)
    http_server.serve_forever()
