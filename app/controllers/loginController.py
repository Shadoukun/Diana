from ..models import db, User, Admin, Channel, Macro, Quote, FlaskUser
from flask import render_template, Blueprint, request, redirect, url_for, flash
from wtforms import TextField, PasswordField, validators
from flask_wtf import Form
from flask.views import MethodView
from flask_login import *
from flask_bcrypt import check_password_hash
import sys
from ..forms import LoginForm

blueprint = Blueprint('login', __name__)


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


