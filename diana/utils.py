from discord.ext import commands
import diana.db as db

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


def editMacro(bot, session, macro):
    # Removes eddited macro and readds it.
    # Should probably have a more precise method for this.

    if macro.command in bot.commands.keys():
        bot.remove_command(macro)

    addMacros(bot, session)
    print("Macro Edited.")


def addMacros(bot, session):
    macros = session.query(db.Macro).all()
    for m in macros:
        if m.command not in bot.commands.keys():
            func = makeMacro(m.command, m.response)
            cmd = commands.Command(name=m.command, callback=func, pass_context=True, no_pm=True)
            bot.add_command(cmd)
