from discord.ext import commands
import discord
import asyncio
import os
import glob
from diana.config import config
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists
import diana.utils as utils
from datetime import datetime
import math
import time
import sys

from diana.db import *


class Diana(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._database_check()

        self.time_check = datetime.utcnow()
        self.message_counter = 0


    async def on_ready(self):

        # Load Commands.
        path = os.path.join(os.getcwd(), "diana", "commands", "*.py")
        cmd_path = glob.glob(path, recursive=True)

        for c in cmd_path:

            # Skip commands/files that contain with __
            if "__" in c:
                continue

            name = os.path.basename(c)[:-3]
            self.load_extension("diana.commands." + name)

        # Background Tasks
        
        
        # Macros
        try:
           cmd = utils.addMacros(self, session)
           self.add_command(cmd)
        
        except:
            pass
        
        print('Logged in as ' + bot.user.name)
        print(bot.user.id)
        print('------')

        print("Background Tasks", file=sys.stderr)
        self.loop.create_task(self.add_users_task())
        self.loop.create_task(self.update_macros_task())
        self.loop.create_task(self.add_channels_task())
        self.loop.create_task(self.update_existing_users_task())

    async def on_message(self, message):

        if message.author.bot:
            return

        await self.process_commands(message)

        # add row to message_stats every hour
        self.message_counter += 1
        timediff = math.floor((message.timestamp - self.time_check).seconds / 3600)

        if timediff >= 1:

            # if several hours have passed, insert extra empty values
            if timediff > 1:
                newtime = message.timestamp.replace(minute=0, second=0, microsecond=0)

                for _ in range(int(timediff) - 1):
                    empy_hour = message.timestamp.replace(hour=newtime.hour - 1, minute=0, second=0, microsecond=0)
                    stat = MessageStat(newtime, self.message_counter, message.channel.id)
                    session.add(stat)
                    session.commit()

            stat = MessageStat(newtime, self.message_counter, message.channel.id)
            session.add(stat)
            session.commit()
            self.message_counter = 0
            self.time_check = datetime.utcnow()


    def _database_check(self):

        if not database_exists('sqlite:///database.db'):
            create_database(Base, engine)
            populate_database(session, self)
            print("database Created.")


    def _update_macros(self):
        # Update macros in DB.
        macros = session.query(Macro).all()
        if macros:
            for macro in macros:
                if macro.modified_flag == 1:
                    utils.editMacro(self, session, macro)
                    macro.modified_flag = 0
                    session.commit()
                    print("Changed Macro")


    def _add_channels(self):
        # add new channels to DB
        db_channels = [c.channelid for c in session.query(Channel).all()]
        bot_channels = [c for c in self.get_all_channels()]

        for channel in bot_channels:
            if channel.id not in db_channels:
                new_channel = Channel(channel.id, channel.name, str(channel.type))
                session.add(new_channel)

        session.commit()


    def _add_users(self):
        # add new users to DB
        db_users = [u.userid for u in session.query(User).all()]
        bot_users = [m for m in self.get_all_members()]

        for user in bot_users:
            if user.id not in db_users:
                new_user = User(user.id, user.name, user.display_name, user.avatar_url)
                session.add(new_user)
                # Add user to channels.
                for channel in session.query(Channel):
                    channel.members.append(new_user)

        session.commit()


    def _update_existing_users(self):
        time.sleep(0.5)
        # update display name and avatar_url for users
        db_users = [u for u in session.query(User).all()]
        bot_users = [m for m in self.get_all_members()]

        for botuser in bot_users:
            for dbuser in db_users:
                if dbuser.userid == botuser.id:
                    dbuser.display_name = botuser.display_name
                    dbuser.avatar_url = botuser.avatar_url

        session.commit()


    async def update_macros_task(self):
        await self.wait_until_ready()
        while not self.is_closed:
            self._update_macros()
            # Runs every 20 seconds.
            await asyncio.sleep(20)


    async def add_channels_task(self):
        await self.wait_until_ready()
        while not self.is_closed:
            self._add_channels()
            # Runs every 3.5 minutes.
            await asyncio.sleep(210)


    async def add_users_task(self):
        await self.wait_until_ready()
        while not self.is_closed:
            self._add_users()
            # Runs every 2 hours
            await asyncio.sleep(7200)


    async def update_existing_users_task(self):
        await self.wait_until_ready()
        while not self.is_closed:
            self._update_existing_users()

            # Runs every 3.5 hours
            await asyncio.sleep(12600)


bot = Diana(command_prefix='!', description="Diana Ross")
Session = sessionmaker(bind=engine)
session = Session()
