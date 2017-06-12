from flask import render_template, Blueprint, request
from app.forms import *
from diana.diana import bot
from ..models import db, User, Admin, Channel, Macro, Quote
import sys
import json

blueprint = Blueprint('stats', __name__)


@blueprint.route('/stats')
def stats():
    userlist = dict()
    quotes = Quote.query.all()

    for quote in quotes:
        user = quote.user.display_name
        if user in userlist.keys():
            userlist[user]['quotes'].append(quote)
        else:
            userlist[user] = {"user": user, "quotes": [quote]}

    data = {
            'type': 'pie',
            'name': 'User share',
            'data': list()
            }

    for user in userlist.keys():
        name = user
        total = len(quotes)
        user_total = len(userlist[user]['quotes'])
        percentage = 100 * float(user_total) / float(total)
        data['data'].append([user, round(percentage, 1)])

    data = json.dumps(data)

    return render_template('stats/stats.html', quote_stats=data)
