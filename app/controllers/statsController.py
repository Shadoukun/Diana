from flask import render_template, Blueprint, request
from sqlalchemy.sql.expression import func
from app.forms import *
from ..models import db, User, Admin, Channel, Macro, Quote, MessageStat
import sys
import json
import itertools
import arrow
from collections import namedtuple  



blueprint = Blueprint('stats', __name__)


@blueprint.route('/stats')
def stats():
    """Main Stats Route"""
    hourly_stats = _hourlyStats()
    daily_stats = _dailyStats()
    quote_stats = _quoteStats()
    return render_template('stats/stats.html',
                           hourly_stats=hourly_stats,
                           daily_stats=daily_stats,
                           quote_stats=quote_stats)
                           

def _quoteStats():

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
        total = len(quotes)
        user_total = len(userlist[user]['quotes'])
        percentage = 100 * float(user_total) / float(total)
        data['data'].append([user, round(percentage, 1)])

    quote_stats = json.dumps(data)
    return quote_stats


def _hourlyStats():
    stats = MessageStat.query.all()
    hours = []
    msgcounts = []

    for s in stats:
        msgcounts.append(s.messagecount)
        if s.timestamp:
            s.timestamp.replace(minute=0, second=0, microsecond=0)
            hours.append(s.timestamp.strftime("%H:%M"))

    hourlyStats = (hours, msgcounts)
    return hourlyStats


def _dailyStats():
    stats = MessageStat.query.all()
    timestamps = []
    msgcounts = []

    for s in stats:
        msgcounts.append(s.messagecount)
        if s.timestamp:
            timestamps.append(s.timestamp)

    daily_stats = convert_dates(timestamps, msgcounts)

    return daily_stats



def convert_dates(tstamps, msgs):
    tstamps = [arrow.get(x).format('MMMM DD, YYYY') for x in tstamps]
    date = namedtuple('timestamps', ['timestamp', 'msgcount'])
    dates = [date(t, m) for t, m in zip(tstamps, msgs)]

    date_map = {
        key: [date.msgcount for date in group]
        for key, group in itertools.groupby(dates, lambda date: date.timestamp)
    }

    date_list = []
    date_list.append([k for k in date_map.keys()])
    date_list.append([sum(v) for v in date_map.values()])

    return date_list
