from discord.ext import commands
import discord
import asyncio
import os
import glob
import importlib
import wolframalpha
import cmd
import logging
from inspect import getmembers, isfunction
from .config import config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, event
from sqlalchemy_utils import database_exists
import diana.utils as utils
import os

from diana.db import *

logging.basicConfig()

bot = commands.Bot(command_prefix='?', description="test")
Session = sessionmaker(bind=engine)
session = Session()

bot.logger = logging.getLogger(__name__)
bot.logger.setLevel(level=logging.DEBUG)

# path for commands.
path = os.path.join(os.getcwd(), "diana", "commands", "*.py")
cmd_path = glob.glob(path, recursive=True)

# Load commands.
# Skip commands that begin with __
for c in cmd_path:
    if "__" in c:
        continue

    name = os.path.basename(c)[:-3]
    bot.load_extension("diana.commands." + name)

# database

async def my_background_task():
    await bot.wait_until_ready()
    print("Background Task")
    while not bot.is_closed:
        macros = session.query(Macro).all()
        if macros:
            for macro in macros:
                if macro.modified_flag == 1:
                    utils.editMacro(bot, session, macro)
                    macro.modified_flag = 0
                    session.commit()
                    print("Changed Macro")
        else:
            print("No Macros.")
        print("Background Task Finished.")
        await asyncio.sleep(10) # task runs every 60 seconds

@bot.event
async def on_ready():
    if not database_exists('sqlite:///database.db'):
        create_database(Base, engine)
        populate_database(session, bot)
        print("database Created.")

    try:
        utils.addMacros(bot, session)
    except:
        print("No Macros.")

    bot.loop.create_task(my_background_task())


    bot.logger.info('Logged in as')
    bot.logger.info(bot.user.id)
    bot.logger.info('------')

    
