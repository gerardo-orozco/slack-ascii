import tornado.web


class PingHandler(tornado.web.RequestHandler):
    """Request handler that serves as system healthcheck."""

    def get(self):
        self.finish('OK')
