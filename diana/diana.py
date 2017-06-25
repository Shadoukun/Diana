import os
import sys
import asyncio
import discord
import glob
import arrow
import random
from inspect import getmembers, isfunction
from discord.ext import commands
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists


from diana.db import *
import diana.utils as utils
from diana.tasks import Tasks

class Diana(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session = session
        self.responses = {}
        self.reactions = {}

        self.time_check = arrow.utcnow()
        self.message_counter = 0

        self.check_database()

    @asyncio.coroutine
    def on_command_error(self, exception, context):
        # supress command exceptions
        pass

    @asyncio.coroutine
    async def on_ready(self):

        await self.load_plugin_commands()
        await self.load_macro_commands()

        print("Starting background tasks...", file=sys.stderr)
        await self.load_tasks()

        print('Logged in as ' + bot.user.name)
        print('------')

    @asyncio.coroutine
    async def load_tasks(self):
        """Load background tasks from diana.tasks"""
        tasks = getmembers(Tasks, isfunction)

        for task in tasks:
            self.loop.create_task(task[1](self))

    @asyncio.coroutine
    async def on_message(self, message):
        if message.author.bot:
            return

        await self.process_commands(message)
        await self.process_responses(message)
        await self.process_reactions(message)

        # increment number of messages
        self.message_counter += 1

        # add row to message stats every hour
        if utils.checkStats(self, message):
            utils.addStats(self, message)
            self.message_counter = 0
            self.time_check = datetime.utcnow()

    @asyncio.coroutine
    async def process_responses(self, message):
        """Triggers a macro response if message contains trigger."""
        channel = message.channel
        message = str(message.content)
        # check for trigger in message
        for trigger in self.responses:
            if trigger in message.lower():
                resp = self.responses[trigger].split('\n')

                # check if there are multiple possible responses
                if len(resp) > 1:
                    resp = random.choice(resp)
                else:
                    resp = resp[0]

                await self.send_message(channel, resp)
                return

    async def process_reactions(self, message):
        """Triggers an automatic discord reaction on <message>"""

        message = message
        emojis = self.get_all_emojis()

        for trigger in self.reactions:
            if trigger in message.content.lower():
                reactions = self.reactions[trigger].split('\n')
                for r in reactions:
                    for e in emojis:
                        if r == e.name:
                            await self.add_reaction(message, e)

    async def load_macro_commands(self, macro=None):
        """Load/Reload macro commands from database
            takes single macro to reload as optional arg"""

        if macro is not None:
            macros = [macro]
        else:
            macros = self.session.query(Macro).all()

        if len(macros) < 1:
            return

        for m in macros:
            if m.command in self.commands:
                bot.remove_command(m.command)

            func = utils.makeMacro(m)
            cmd = commands.Command(name=m.command, callback=func, pass_context=True, no_pm=True)
            bot.add_command(cmd)


    async def load_plugin_commands(self):
        """Load plugins from commands folder."""

        print("Loading Plugins...")

        path = os.path.join(os.getcwd(), "diana", "commands", "*.py")
        cmd_path = glob.glob(path, recursive=True)
        for c in cmd_path:
            # Skip commands/files that contain with __
            if "__" in c:
                continue

            name = os.path.basename(c)[:-3]
            bot.load_extension("diana.commands." + name)

    def check_database(self):
        """Creates database if it doesnt exist"""

        if not database_exists('sqlite:///database.db'):
            Base.metadata.create_all(engine)
            self.populate_database()

    def populate_database(self):
        '''
        Takes sqlalchemy session and discord bot as args
        and populates database with channels, users.
        '''

        # list of channels and users from database.
        db_channels = [c.name for c in self.session.query(Channel.channelid).all()]
        db_users = [u.name for u in self.session.query(User.userid).all()]

        # List of channels and users from Discord.
        bot_channels = [c for c in self.get_all_channels()]
        bot_users = [m for m in self.get_all_members()]

        # Add missing channels to database.
        for channel in bot_channels:
            if channel.id not in db_channels:
                new_channel = Channel(channel.id, channel.name, str(channel.type))
                self.session.add(new_channel)

        # Add missing users to database.
        for user in bot_users:
            if user.id not in db_users:
                new_user = User(user.id, user.name, user.display_name, user.avatar_url)
                self.session.add(new_user)

                # Add user to channels.
                for channel in session.query(Channel):
                    channel.members.append(new_user)

        self.session.commit()


Session = sessionmaker(bind=engine)
session = Session()
bot = Diana(command_prefix='!', description="Diana Ross")
