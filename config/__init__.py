import os

DEBUG = False
TESTING = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'my precious'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.getcwd() + '/database.db'
host = 'localhost'
PORT = int(os.environ.get('PORT', 5000))
