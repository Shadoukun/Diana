import logging

from flask import Flask, request as req

from app.controllers import pages
from app.controllers import quotesController
from sassutils.wsgi import SassMiddleware
# from sassutils.builder import build_directory


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    app.register_blueprint(pages.blueprint)
    app.register_blueprint(quotesController.blueprint)
    app.logger.setLevel(logging.NOTSET)

    app.wsgi_app = SassMiddleware(app.wsgi_app, {
        'app': ('static/scss', 'static/css', 'static/css')
    })

    # build_directory("app/static/sass", "app/static/css")

    @app.after_request
    def log_response(resp):
        app.logger.info("{} {} {}\n{}".format(
            req.method, req.url, req.data, resp)
        )
        return resp

    return app
