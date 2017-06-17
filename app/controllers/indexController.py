from flask import render_template, Blueprint, request
from app.forms import *
from diana.diana import bot
from ..models import db, User, Admin, Channel, Macro, Quote
import sys

blueprint = Blueprint('index', __name__)


@blueprint.route('/')
def home():
    users = User.query.all()
    return render_template('index/placeholder.home.html', users=users)


@blueprint.route('/about')
def about():
    return render_template('index/placeholder.about.html')
