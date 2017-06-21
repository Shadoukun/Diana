import sys
import os
import ctypes
from threading import Thread
from app import db, create_app
from sqlalchemy_utils import database_exists
from diana.db import Base, engine
from diana.config import config
from diana.diana import bot, session
from diana.db import create_database, populate_database
import add_user


# requirements are in ./config/requirements.txt


# Check if database has been created.
if not database_exists('sqlite:///database.db'):
    create_database(Base, engine)
    populate_database(session, bot)
    print("database Created.")


# To enable debugging,
#app = create_app('config.development', debug=True)
app = create_app('config', debug=False)
db.init_app(app)

# Add an admin if none exists
add_user.add_user(app)

if __name__ == '__main__':
 
    # Run
    flaskThread = Thread(target=app.run, kwargs={'host': '0.0.0.0'})
    flaskThread.start()
    bot.run(config.discordToken)
