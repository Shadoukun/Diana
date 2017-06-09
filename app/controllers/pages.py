from flask import render_template, Blueprint, request
from app.forms import *
from diana.diana import bot
from ..models import db, User, Admin, Channel, Macro, Quote
import sys

blueprint = Blueprint('pages', __name__)


################
#### routes ####
################


@blueprint.route('/')
def home():
    users = User.query.all()
    return render_template('pages/placeholder.home.html', users=users)


@blueprint.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@blueprint.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@blueprint.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@blueprint.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)
