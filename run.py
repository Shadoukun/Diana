import sys
import os
import ctypes
from threading import Thread
from app import db, create_app
from sqlalchemy_utils import database_exists
from diana.db import Base, engine
from diana.config import config
from diana.diana import bot, Session, session
import add_user


# requirements are in ./config/requirements.txt

# To enable debugging,
#app = create_app('config.development', debug=True)


app = create_app('config', debug=False)
db.init_app(app)

#add_user.main(app)

if __name__ == '__main__':
 
    # Run
    flaskThread = Thread(target=app.run)
    flaskThread.start()
    bot.run(config.discordToken)
