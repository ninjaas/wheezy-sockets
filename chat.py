import json

from wheezy.http import WSGIApplication
from wheezy.routing import url
from wheezy.web.handlers import BaseHandler, file_handler
from wheezy.web.middleware import bootstrap_defaults, path_routing_middleware_factory
from wheezy.html.ext.template import WidgetExtension
from wheezy.html.utils import html_escape
from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader
from wheezy.web.templates import WheezyTemplate
from geventwebsocket import WebSocketServer, WebSocketApplication, Resource


class ChatApplication(WebSocketApplication):

    def on_open(self):
        print "Some client connected!"

    def on_message(self, message):
        if message is None:
            return

        message = json.loads(message)

        if message['msg_type'] == 'message':
            self.broadcast(message)
        elif message['msg_type'] == 'update_clients':
            self.send_client_list(message)

    def send_client_list(self, message):
        current_client = self.ws.handler.active_client
        current_client.nickname = message['nickname']

        self.ws.send(json.dumps({
            'msg_type': 'update_clients',
            'clients': [
                getattr(client, 'nickname', 'anonymous')
                for client in self.ws.handler.server.clients.values()
            ]
        }))

    def broadcast(self, message):
        for client in self.ws.handler.server.clients.values():
            client.ws.send(json.dumps({
                'msg_type': 'message',
                'nickname': message['nickname'],
                'message': message['message']
            }))

    def on_close(self, reason):
        print "Connection closed! "


class Home(BaseHandler):

    def get(self):
        return self.render_response('templates/chat.html')

all_urls = [
    url('', Home),
    url('static/{path:any}',
        file_handler(root='static/'),
        name='static')
]


options = {}

# Template Engine
searchpath = ['']
engine = Engine(
    loader=FileLoader(searchpath),
    extensions=[
        CoreExtension(),
        WidgetExtension(),
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
    WebSocketServer(
        ('0.0.0.0', 8000),

        Resource({
            '^/chat': ChatApplication,
            '^/.*': main
        }),

        debug=False
    ).serve_forever()
