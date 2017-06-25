import random
from discord.ext import commands
import arrow

from diana.db import *

def parse_message(message, tags=None):
    """function to check and parse incoming messages

       kwargs:
       tags: a list of tags (for image searches)
    """

    if isinstance(tags, list):
        tags = '+'.join(tags)

    if len(message.split()) > 1:
        message = message.split(' ', 1)[1]
    else:
        message = ''

    if tags:
        if message:
            message = "+".join([message.replace(" ", "+"), tags])
            return message
        else:
            message = tags
            return message
    else:
        return message


def makeMacro(macro):
    """Returns a generic send_message command from command macro"""

    # function for regular macros
    async def _macro(ctx):
        nonlocal macro
        await ctx.bot.send_message(ctx.message.channel, macro.response)


    # function for macros with multiple responses.
    # Chooses a response at random.
    async def _multimacro(ctx):
        nonlocal macro
        randresponse = [r.rstrip() for r in macro.response.split('\n')]
        random.shuffle(randresponse)
        randresponse = randresponse[0]
        await ctx.bot.send_message(ctx.message.channel, randresponse)

    if '\n' in macro.response:
        return _multimacro
    else:
        return _macro


def checkStats(bot, message):
    """Check if enough has time has passed to add stats. Returns bool"""
    timestamp = arrow.get(message.timestamp).floor('hour')
    time_check = arrow.get(bot.time_check).floor('hour')

    timediff = int((timestamp - time_check).total_seconds() / 3600)

    if timediff >= 1:
        return True


def addStats(bot, message):
    """Checks length of time between last stats row and adds
       necessary amount of rows accordingly"""

    # Calculate difference between last stats check and now.
    timestamp = arrow.get(message.timestamp).floor('hour')
    time_check = arrow.get(bot.time_check).floor('hour')

    timediff = int((timestamp - time_check).total_seconds() / 3600)

    # If time difference is greater than one hour, add extra empty hours first.
    if timediff > 1:
        last_stat = bot.session.query(MessageStat).order_by(MessageStat.id.desc()).first()

        if not last_stat:
            return

        last_stat = arrow.get(last_stat.timestamp)
        diff = abs(timestamp - last_stat).total_seconds() / 3600
        diff -= 1
        while diff:
            empty_hour = timestamp.replace(hours=timestamp.hour - diff)
            empty_stat = MessageStat(empty_hour, 0, message.channel.id)
            bot.session.add(empty_stat)
            diff -= 1

    # add hourly stats
    stat = MessageStat(timestamp.datetime, bot.message_counter, message.channel.id)
    bot.session.add(stat)
    bot.session.commit()
