import logging

from flask import Flask, redirect, url_for, request as req
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from app.controllers import indexController, quotesController, macrosController, statsController, loginController
from app.models import FlaskUser
from sassutils.wsgi import SassMiddleware
from sassutils.builder import build_directory

login_manager = LoginManager()

def create_app(config_filename, debug=False):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.login_manager = login_manager
    log = logging.getLogger('werkzeug')
    CSRFProtect(app)
    app.login_manager.init_app(app)

    app.register_blueprint(indexController.blueprint)
    app.register_blueprint(quotesController.blueprint)
    app.register_blueprint(macrosController.blueprint)
    app.register_blueprint(statsController.blueprint)
    app.register_blueprint(loginController.blueprint)
    

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


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return FlaskUser.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return redirect(url_for("login.login"))
