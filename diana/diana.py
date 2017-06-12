from discord.ext import commands
import discord
import asyncio
import os
import glob
import importlib
import wolframalpha
import cmd
from inspect import getmembers, isfunction
from .config import config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, event
from sqlalchemy_utils import database_exists
import diana.utils as utils
import os

from diana.db import *

bot = commands.Bot(command_prefix='!', description="Diana Ross")
Session = sessionmaker(bind=engine)
session = Session()


# -- Load commands. --
path = os.path.join(os.getcwd(), "diana", "commands", "*.py")
cmd_path = glob.glob(path, recursive=True)

for c in cmd_path:
    # Skip commands/files that contain with __
    if "__" in c:
        continue
    name = os.path.basename(c)[:-3]
    bot.load_extension("diana.commands." + name)


def _update_macros():
    # Update macros in DB.
    macros = session.query(Macro).all()
    if macros:
        for macro in macros:
            if macro.modified_flag == 1:
                utils.editMacro(bot, session, macro)
                macro.modified_flag = 0
                session.commit()
                print("Changed Macro")


def _add_channels():
    # add new channels to DB
    db_channels = [c.channelid for c in session.query(Channel).all()]
    bot_channels = [c for c in bot.get_all_channels()]

    for channel in bot_channels:
        if channel.id not in db_channels:
            new_channel = Channel(channel.id, channel.name, str(channel.type))
            session.add(new_channel)
            session.commit()


def _add_users():
    # add new users to DB
    db_users = [u.userid for u in session.query(User).all()]
    bot_users = [m for m in bot.get_all_members()]

    for user in bot_users:
        if user.id not in db_users:
            new_user = User(user.id, user.name, user.display_name, user.avatar_url)
            session.add(new_user)
            # Add user to channels.
            for channel in session.query(Channel):
                channel.members.append(new_user)

            session.commit()


def _update_existing_users():
    # update display name and avatar_url for users
    db_users = [u for u in session.query(User).all()]
    bot_users = [m for m in bot.get_all_members()]

    for dbuser in db_users:
        for botuser in bot_users:
            if dbuser.userid == botuser.id:
                dbuser.display_name = botuser.display_name
                dbuser.avatar_url = botuser.avatar_url
                session.commit()


async def update_macros_task():
    await bot.wait_until_ready()
    while not bot.is_closed:
        _update_macros()

        # Runs every 10 seconds.
        await asyncio.sleep(10)


async def add_channels_task():
    await bot.wait_until_ready()
    while not bot.is_closed:
        _add_channels()

        # Runs every minute.
        await asyncio.sleep(60)


async def add_users_task():
    await bot.wait_until_ready()
    while not bot.is_closed:
        _add_users()

        # Runs every 30 seconds.
        await asyncio.sleep(30)


async def update_existing_users_task():
    await bot.wait_until_ready()
    while not bot.is_closed:
        _update_existing_users()

        # Runs every 3 minutes
        await asyncio.sleep(90)


@bot.event
async def on_ready():
    if not database_exists('sqlite:///database.db'):
        create_database(Base, engine)
        populate_database(session, bot)
        print("database Created.")

    try:
        utils.addMacros(bot, session)
    except:
        print("No Macros. 2")

    # Create Background Tasks
    bot.loop.create_task(update_macros_task())
    bot.loop.create_task(add_channels_task())
    bot.loop.create_task(add_users_task())
    bot.loop.create_task(update_existing_users_task())


    print('Logged in as ' + bot.user.name)
    print(bot.user.id)
    print('------')
