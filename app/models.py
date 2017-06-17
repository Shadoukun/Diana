from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

channel_members = db.Table('channel_members',
                           db.Column('channel_id', db.Integer,
                           db.ForeignKey('channels.channelid')),
                           db.Column('user_id', db.Integer,
                           db.ForeignKey('users.userid'))
                           )


class User(db.Model):

    __tablename__ = "users"

    userid = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    display_name = db.Column(db.String)
    avatar_url = db.Column(db.String)
    quotes = db.relationship("Quote", backref=db.backref("user", lazy="joined"))

    def __init__(self, userid, name, display_name, avatar_url):
        self.userid = userid
        self.name = name
        self.display_name = display_name
        self.avatar_url = avatar_url


class Channel(db.Model):

    __tablename__ = "channels"

    channelid = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    channeltype = db.Column(db.String)
    members = db.relationship("User", secondary=channel_members, backref="channels")
    quotes = db.relationship("Quote", backref=db.backref("channel", lazy="joined"))

    def __init__(self, channelid, name, channeltype):
        self.channelid = channelid
        self.name = name
        self.channeltype = channeltype


class Quote(db.Model):

    __tablename__ = "quotes"

    messageid = db.Column(db.String, primary_key=True)
    message = db.Column(db.String)
    timestamp = db.Column(db.String)
    userid = db.Column(db.String, db.ForeignKey('users.userid'))
    channelid = db.Column(db.Integer, db.ForeignKey('channels.channelid'))

    def __init__(self, messageid, message, timestamp, userid, channelid):
        self.messageid = messageid
        self.message = message
        self.timestamp = timestamp
        self.userid = userid
        self.channelid = channelid


class Admin(db.Model):

    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String, db.ForeignKey('users.userid'))
    user = db.relationship("User", uselist=False)

    def __init__(self, userid):
        self.userid = userid


class Macro(db.Model):

    __tablename__ = "macros"

    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.String, unique=True)
    response = db.Column(db.String)
    modified_flag = db.Column(db.Integer)

    def __init__(self, command, response, modified_flag=None):
        self.command = command
        self.response = response
        self.modified_flag = modified_flag

class MessageStat(db.Model):
    """Total messages sent over time (Hourly)"""

    __tablename__ = "message_stats"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    messagecount = db.Column(db.Integer)
    channelid = db.Column(db.String, db.ForeignKey('channels.channelid'))

    def __init__(self, timestamp, messagecount, channelid):
        self.timestamp = timestamp
        self.messagecount = messagecount
        self.channelid = channelid

class FlaskUser(db.Model):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'

    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


