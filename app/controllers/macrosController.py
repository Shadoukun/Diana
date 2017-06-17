from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask.views import MethodView
from app.forms import CommandForm
import json
import discord
import sys
from ..models import db, User, Admin, Channel, Macro, Quote, FlaskUser
from flask_login import login_required

blueprint = Blueprint('macros', __name__)


@blueprint.route('/macros')
@blueprint.route('/macros/<int:macro_id>')
@login_required
def macros(macro_id=None):
    form = CommandForm(request.form)
    macros = Macro.query.all()

    if macro_id:
        macro = Macro.query.filter_by(id=macro_id).first()
        return render_template('macros/macros.html', macros=macros, form=form, current_macro=macro)
    else:
        return render_template('macros/macros.html', macros=macros, form=form)

@login_required
@blueprint.route('/macros/<int:macro_id>/<string:operation>', methods=['POST', 'GET'])
@blueprint.route('/macros/<string:operation>', methods=['POST', 'GET'])
def edit_macros(operation, macro_id=None):
    if request.method == 'POST':
        form = CommandForm(request.form)

        if not form.validate_on_submit():
            flash(form.errors)

        if operation == 'new':
            print("New Macro", file=sys.stderr)
            macro = Macro(form.command.data, form.response.data)
            db.session.add(macro)
            db.session.commit()

        if operation == 'edit':
            macro = Macro.query.filter_by(id=macro_id).first()
            macro.command = form['command'].data
            macro.response = form['response'].data
            db.session.commit()

    if (request.method == 'GET') and (macro_id):

        if operation == 'delete':
            Macro.query.filter_by(id=macro_id).delete()
            db.session.commit()

    return redirect(url_for('macros.macros'))
