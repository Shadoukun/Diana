import os
import sys
import re
import asyncio
import discord
import glob
import arrow
import random
from discord.ext import commands
from datetime import datetime
from sqlalchemy.orm import sessionmaker
import diana.utils as utils
from diana.db import *
from diana.tasks import *

class Diana(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session = session
        self.time_check = arrow.utcnow()
        self.message_counter = 0

        self.responses = {}


    async def on_ready(self):

        await self.load_plugin_commands()
        await self.load_macro_commands()

        print("Starting background tasks...", file=sys.stderr)

        self.loop.create_task(update_macros_task(self))
        self.loop.create_task(add_responses(self))
        self.loop.create_task(add_users_task(self))
        self.loop.create_task(add_channels_task(self))
        self.loop.create_task(update_existing_users_task(self))

        print('Logged in as ' + bot.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if message.author.bot:
            return

        await self.process_commands(message)
        await self.process_responses(message)

        # number of messages since last check_stats
        self.message_counter += 1

        # add row to message stats every hour
        if utils.checkStats(self, message):
            utils.addStats(self, message)
            self.message_counter = 0
            self.time_check = datetime.utcnow()

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
            return

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


Session = sessionmaker(bind=engine)
session = Session()
bot = Diana(command_prefix='!', description="Diana Ross")
