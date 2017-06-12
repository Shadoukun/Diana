from flask import render_template, Blueprint, request
from app.forms import *
import json
import discord
from diana.diana import bot
from sqlalchemy import func
from ..models import db, User, Admin, Channel, Macro, Quote
import sys

blueprint = Blueprint('quotes', __name__)


@blueprint.route('/quotes')
@blueprint.route('/quotes/<channel>')
@blueprint.route('/quotes/<channel>/<user>')
def quotes(channel=None, user=None):

    channels = [c for c in Channel.query.filter_by(channeltype='text').all()]
    allusers = User.query.all()

    if (channel is None) or (channel == 'all'):
        channels = [c for c in Channel.query.filter_by(channeltype='text').all()]

        if user:
            users = [u for u in allusers if u.userid == user]
            quotes = Quote.query.filter_by(userid=users[0].userid).all()
        else:
            users = [u for u in allusers if len(u.quotes) > 0]
            quotes = Quote.query.all()

        return render_template('quotes/quotes.html', quotes=quotes, channels=channels, users=users, curchannel=None)

    else:
        channels = [c for c in Channel.query.filter_by(channeltype='text').all()]
        channel = [c for c in channels if c.name == channel][0]
        allusers = User.query.all()

        if user:
            users = [u for u in allusers if u.userid == user]
            quotes = Quote.query.filter_by(channel=channel).filter_by(userid=users[0].userid).all()
        else:
            users = [u for u in allusers if len(u.quotes) > 0]
            quotes = Quote.query.filter_by(channel=channel).all()

    return render_template('quotes/quotes.html', quotes=quotes, channels=channels, users=users, curchannel=channel.name)


def _getUserList(quotes):
    user_list = []
    _user_list = []

    for quote in quotes:
        try:
            # Update User details
            user = discord.utils.get(bot.get_all_members(), id=quote["user_id"])
            if user:
                quote['username'] = user.display_name
                quote['avatar'] = user.avatar_url
            if quote['username'] not in _user_list:
                    _user_list.append(quote['username'])
                    user_list.append({"user_id": quote['user_id'],
                                      "username": quote['username'],
                                      "avatar": quote['avatar']})
        except:
            continue

    return user_list


def _getQuoteList(data, channel, user=None):

    quotes = data['quotes'][channel]

    if user:
        quote_list = []

        for q in quotes:
            if user == q['user_id']:
                quote_list.append(q)
        return quote_list

    else:
        return quotes
