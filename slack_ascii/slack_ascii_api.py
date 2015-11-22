# !/usr/bin/env python
import logging
import os

import tornado.httpserver
import tornado.options
import tornado.web

import handlers.ping
import handlers.api

log = logging.getLogger(__name__)


class Application(tornado.web.Application):
    def __init__(self):
        app_handlers = [
            ('/', handlers.api.APIHandler),
            ('/ping', handlers.ping.PingHandler),
        ]
        app_settings = {
            'debug': os.environ.get('ENV') == 'dev'
        }

        super(Application, self).__init__(app_handlers, **app_settings)


if __name__ == '__main__':
    tornado.options.define('port', default=9000)
    tornado.options.parse_command_line()

    port = tornado.options.options.port
    log.info('Listening on port %s' % port)

    httpserver = tornado.httpserver.HTTPServer(request_callback=Application(), xheaders=True)
    httpserver.listen(port, address='0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()
