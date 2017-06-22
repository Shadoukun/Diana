import sys
import asyncio
import discord
import re
from discord.ext import commands
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists
import diana.utils as utils
from diana.db import *
from diana.tasks import *
import arrow
class Diana(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session = session
        self.time_check = arrow.utcnow()
        self.message_counter = 0

        self.responses = {}


    async def on_ready(self):

        utils.loadCommands(self)
        utils.loadMacros(self)

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
        message = re.sub("[!@#$%^&*()[]{};:,./<>?\|`~-=_+]", " ", message.content)

        for word in message.split(" "):
            if word in self.responses:
                await self.send_message(channel, self.responses[word])
                return

Session = sessionmaker(bind=engine)
session = Session()
bot = Diana(command_prefix='!', description="Diana Ross")
