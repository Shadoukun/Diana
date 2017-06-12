import logging

from flask import Flask, request as req
from flask_wtf import CSRFProtect
from app.controllers import indexController, quotesController, macrosController, statsController

from sassutils.wsgi import SassMiddleware
from sassutils.builder import build_directory


def create_app(config_filename, debug=False):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    log = logging.getLogger('werkzeug')
    CSRFProtect(app)

    app.register_blueprint(indexController.blueprint)
    app.register_blueprint(quotesController.blueprint)
    app.register_blueprint(macrosController.blueprint)
    app.register_blueprint(statsController.blueprint)

    if debug:
        log.setLevel(logging.NOTSET)
        app.logger.setLevel(logging.NOTSET)

        # compile SCSS to CSS with every request. useful for updating styles.
        app.wsgi_app = SassMiddleware(app.wsgi_app, {
            'app': ('static/scss', 'static/css', 'static/css')
            })

    else:
        log.setLevel(logging.INFO)
        app.logger.setLevel(logging.INFO)

        # compile once at start.
        build_directory("app/static/scss", "app/static/css")

    return app
