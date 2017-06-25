from threading import Thread
from app import create_app
from diana.config import config
from diana.diana import bot
import add_user


# requirements are in ./config/requirements.txt


# To enable debugging,
#app = create_app('config.development', debug=True)
app = create_app('config', debug=False)

# Add an admin if none exists
add_user.add_user(app)

if __name__ == '__main__':

    # Run
    flaskThread = Thread(target=app.run, kwargs={'host': '0.0.0.0'})
    flaskThread.start()
    bot.run(config.discordToken)
