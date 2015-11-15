import logging

import tornado.httpserver
import tornado.web

import handlers.ping
import handlers.api


class Application(tornado.web.Application):

    def __init__(self):
        app_handlers = [
            ('/ping', handlers.ping.PingHandler),
            ('/api', handlers.api.APIHandler),
        ]
        app_settings = {
            'debug': True
        }

        super(Application, self).__init__(app_handlers, **app_settings)


if __name__ == '__main__':
    httpserver = tornado.httpserver.HTTPServer(request_callback=Application(), xheaders=True)
    httpserver.listen(8080, address='0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()
