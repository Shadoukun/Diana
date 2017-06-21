import sys
import json
import discord
from diana.diana import bot
from sqlalchemy import func
from flask import render_template, Blueprint, request

from app import db
from app.forms import *

from app.models import User
from app.models import Admin
from app.models import Channel
from app.models import Macro
from app.models import Quote
from app.models import FlaskUser

blueprint = Blueprint('quotes', __name__)


@blueprint.route('/quotes')
@blueprint.route('/quotes/<channel>')
@blueprint.route('/quotes/<channel>/<user>')
def quotes(channel='all', user=None):

    # If no channel is given.
    if channel == 'all':
        channels, users, quotes = _getQuotes(user)

        return render_template('quotes/quotes.html',
                               quotes=quotes,
                               channels=channels,
                               users=users,
                               curchannel=None)

    # if channel is given
    else:
        channels, users, quotes = _getChannelQuotes(channel, user)
        channel = [c for c in channels if c.name == channel][0]

    return render_template('quotes/quotes.html',
                           quotes=quotes,
                           channels=channels,
                           users=users,
                           curchannel=channel.name)


# All code below sucks.


def _getQuotes(user=None):
    '''Returns a complete list of channels, users, and quotes
       Or a user filtered list'''

    channels = [c for c in Channel.query.filter_by(channeltype='text').filter(Channel.quotes.any()).all()]
    allusers = User.query.filter(User.quotes.any())

     # If a user is given
    if user:
        users = [u for u in allusers.all() if u.userid == user]
        quotes = Quote.query.filter_by(userid=users[0].userid).all()

    # No user given
    else:
        users = [u for u in allusers.all() if len(u.quotes) > 0]
        quotes = Quote.query.all()

    return channels, users, quotes


def _getChannelQuotes(channel, user=None):
    '''Returns a filtered list of channels, users, and quotes
       or a channel + user filtered list'''

    channels = [c for c in Channel.query.filter_by(channeltype='text').filter(Channel.quotes.any()).all()]
    allusers = User.query.filter(User.quotes.any())

    # If a user is given
    if user:
        users = [u for u in allusers.all() if u.userid == user]
        quotes = Quote.query.filter_by(channel=channel).filter_by(userid=users[0].userid).all()

    # No user is given.
    else:
        users = [u for u in allusers if len(u.quotes) > 0]
        quotes = Quote.query.filter_by(channel=channel).all()

    return channels, users, quotes
