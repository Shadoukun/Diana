from flask import render_template, Blueprint, request
from app.forms import *
import json
import discord

macrosBlueprint = Blueprint('quotes', __name__)


@macrosBlueprint.route('/macros')
@macrosBlueprint.route('/macros/<macro_id>')
def macros(macro_id=None):
    macros = query_db('select * from commands')
    form = CommandForm(request.form)

    if macro_id:
        return render_template('macros/macros.html', commands=macros, form=form, macro_id=macro_id)
    else:
        return render_template('macros/macros.html', commands=macros, form=form)
