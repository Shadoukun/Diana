from app import create_app
from threading import Thread
from diana.config import config
from diana.diana import bot
from app.models import db, FlaskUser
import sys
import os
import ctypes
import add_user

# To enable debugging,
# app = create_app('config.development', debug=True)


app = create_app('config', debug=False)
db.init_app(app)

#add_user.main(app)

if __name__ == '__main__':
    flaskThread = Thread(target=app.run)
    flaskThread.start()
    bot.run(config.discordToken)
