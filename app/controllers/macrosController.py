import sys
import discord
import json
from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask.views import MethodView
from flask_login import login_required
from app.forms import CommandForm

from app import db
from app.models import User
from app.models import Admin
from app.models import Channel
from app.models import Macro
from app.models import Quote
from app.models import FlaskUser
from app.models import MacroResponse

blueprint = Blueprint('macros', __name__)

@blueprint.route('/macros')
def index():
    return render_template('macros/index.html')



@blueprint.route('/macros/macros')
@blueprint.route('/macros/macros/<int:macro_id>')
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
@blueprint.route('/macros/macros/<int:macro_id>/<string:operation>', methods=['POST', 'GET'])
@blueprint.route('/macros/macros/<string:operation>', methods=['POST', 'GET'])
def edit_macros(operation, macro_id=None):
    if request.method == 'POST':
        form = CommandForm(request.form)

        if not form.validate_on_submit():
            flash(form.errors)

        if operation == 'new':
            print("New Macro", file=sys.stderr)
            macro = Macro(form.command.data, form.response.data, 1)
            db.session.add(macro)
            db.session.commit()

        if operation == 'edit':
            macro = Macro.query.filter_by(id=macro_id).first()
            macro.command = form['command'].data
            macro.response = form['response'].data
            macro.modified_flag = 1
            db.session.commit()

    if (request.method == 'GET') and (macro_id):

        if operation == 'delete':
            Macro.query.filter_by(id=macro_id).delete()
            db.session.commit()

    return redirect(url_for('macros.macros'))


@blueprint.route('/macros/responses')
@blueprint.route('/macros/responses/<int:resp_id>')
@login_required
def responses(resp_id=None):
    form = CommandForm(request.form)
    response_list = MacroResponse.query.all()

    if resp_id:
        resp = MacroResponse.query.filter_by(id=resp_id).first()
        return render_template('macros/responses.html', responses=response_list, form=form, current_resp=resp)
    else:
        return render_template('macros/responses.html', responses=response_list, form=form)

@login_required
@blueprint.route('/macros/responses/<int:resp_id>/<string:operation>', methods=['POST', 'GET'])
@blueprint.route('/macros/responses/<string:operation>', methods=['POST', 'GET'])
def edit_responses(operation, resp_id=None):
    if request.method == 'POST':
        form = CommandForm(request.form)

        if not form.validate_on_submit():
            flash(form.errors)

        if operation == 'new':
            print("New Response", file=sys.stderr)
            resp = MacroResponse(form.command.data, form.response.data)
            db.session.add(resp)
            db.session.commit()

        if operation == 'edit':
            resp = MacroResponse.query.filter_by(id=resp_id).first()
            resp.trigger = form['command'].data
            resp.response = form['response'].data
            db.session.commit()

    if (request.method == 'GET') and (resp_id):

        if operation == 'delete':
            MacroResponse.query.filter_by(id=resp_id).delete()
            db.session.commit()

    return redirect(url_for('macros.responses'))
