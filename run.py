from app import create_app
from threading import Thread
from diana.config import config
from diana.diana import bot
from app.models import db

# To enable debugging,
# app = create_app('config.development', debug=True)


app = create_app('config', debug=False)
db.init_app(app)

if __name__ == '__main__':
    flaskThread = Thread(target=app.run)
    flaskThread.start()
    bot.run(config.discordToken)
