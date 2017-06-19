import sys
from flask import render_template, Blueprint, redirect, url_for, flash
from flask.views import MethodView
from flask_wtf import Form
from flask_login import *
from wtforms import TextField, PasswordField, validators
from flask_bcrypt import check_password_hash

from app import db, login_manager
from app.forms import LoginForm

from app.models import User
from app.models import Admin
from app.models import Channel
from app.models import Macro
from app.models import Quote
from app.models import FlaskUser

blueprint = Blueprint('login', __name__)

login_manager.login_message = "This page requires you to sign in."
login_manager.login_view = "login.login"

@blueprint.route("/login", methods=["GET", "POST"])
def login():
    """For GET requests, display the login form. For POSTS, login the current user
    by processing the form."""

    form = LoginForm()
    print(form.hidden_tag, file=sys.stderr)
    if form.validate_on_submit():
        user = FlaskUser.query.filter_by(username=form.username.data).first()
        print(user, file=sys.stderr)
        if user:
            if check_password_hash(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for("index.home"))
    print(form.errors, file=sys.stderr)
    return render_template("index/login.html", form=form)


@blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for("index.home"))



@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return FlaskUser.query.get(user_id)

#@login_manager.unauthorized_handler
#def unauthorized():
#    # do stuff
#    flash
#    return redirect(url_for("login.login"))
