import os
import glob
import math
import random
import time
from discord.ext import commands

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


def makeMacro(cmd, response):
    # Returns a generic send_message function for macro commands.

    # function for regular macros
    async def _macro(ctx):
        nonlocal response
        await ctx.bot.send_message(ctx.message.channel, response)


    # function for macros with multiple responses.
    # Chooses a response at random.
    async def _multimacro(ctx):
        nonlocal response
        randresponse = [r.rstrip() for r in response.split('\n')]
        random.shuffle(randresponse)
        randresponse = randresponse[0]
        await ctx.bot.send_message(ctx.message.channel, randresponse)

    if '\n' in response:
        return _multimacro
    else:
        return _macro


def editMacro(bot, macro):
    # Removes eddited macro and readds it.
    # Should probably have a more precise method for this.

    if macro.command in bot.commands.keys():
        bot.remove_command(macro.command)

    func = makeMacro(macro.command, macro.response)
    cmd = commands.Command(name=macro.command, callback=func, pass_context=True, no_pm=True)
    bot.add_command(cmd)


def loadCommands(bot):
    path = os.path.join(os.getcwd(), "diana", "commands", "*.py")
    cmd_path = glob.glob(path, recursive=True)

    for c in cmd_path:
        # Skip commands/files that contain with __
        if "__" in c:
            continue

        name = os.path.basename(c)[:-3]
        bot.load_extension("diana.commands." + name)


def loadMacros(bot):
    macros = bot.session.query(Macro).all()

    if len(macros) < 1:
        return

    for m in macros:
        if m.command not in bot.commands.keys():
            func = makeMacro(m.command, m.response)
            cmd = commands.Command(name=m.command, callback=func, pass_context=True, no_pm=True)
            bot.add_command(cmd)

def checkStats(bot, message):

    timediff = math.floor((message.timestamp - bot.time_check).seconds / 3600)
    print(timediff)
    if timediff >= 1:
        return True


def addStats(bot, message):
    timediff = math.floor((message.timestamp - bot.time_check).seconds / 3600)
    newtime = message.timestamp.replace(minute=0, second=0, microsecond=0)
    if timediff > 1:
        last_stat = bot.session.query(MessageStat).order_by(MessaageStat.id.desc()).first()
        diff = abs(message.timestamp-last_stat.timestamp) - 1

        while diff:
            empy_hour = message.timestamp.replace(hour=newtime.hour - diff, minute=0, second=0, microsecond=0)
            empty_stat = MessageStat(empty_hour, 0, message.channel.id)
            bot.session.add(empty_stat)
            print("empty added")
            diff = diff - 1

    stat = MessageStat(newtime, bot.message_counter, message.channel.id)
    bot.session.add(stat)
    bot.session.commit()
    print("added")
