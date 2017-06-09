from app import create_app
from threading import Thread
from diana.config import config
from discord.ext import commands
from diana.diana import bot
from app.models import db, User
import asyncio
import glob
import os

app = create_app('config.development')
db.init_app(app)

if __name__ == '__main__':
    flaskThread = Thread(target=app.run)
    flaskThread.start()
    bot.run(config.discordToken)
