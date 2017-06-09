import os

DEBUG = False
SECRET_KEY = 'my precious'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.getcwd() + '/database.db'
print(SQLALCHEMY_DATABASE_URI)
HOST = 'localhost'
PORT = int(os.environ.get('PORT', 5000))
