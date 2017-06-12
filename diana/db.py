from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///database.db', echo=False)
Base = declarative_base()


channel_members = Table('channel_members',
                        Base.metadata,
                        Column('channel_id', Integer, ForeignKey('channels.channelid')),
                        Column('user_id', Integer, ForeignKey('users.userid'))
                        )


class User(Base):
    __tablename__ = "users"

    userid = Column(String, primary_key=True)
    name = Column(String)
    display_name = Column(String)
    avatar_url = Column(String)
    quotes = relationship("Quote", backref=backref("user", lazy="joined"))

    def __init__(self, userid, name, display_name, avatar_url):
        self.userid = userid
        self.name = name
        self.display_name = display_name
        self.avatar_url = avatar_url


class Channel(Base):
    __tablename__ = "channels"

    channelid = Column(String, primary_key=True)
    name = Column(String)
    channeltype = Column(String)
    members = relationship("User", secondary=channel_members, backref="channels")
    quotes = relationship("Quote", backref=backref("channel", lazy="joined"))

    def __init__(self, channelid, name, channeltype):
        self.channelid = channelid
        self.name = name
        self.channeltype = channeltype


class Quote(Base):

    __tablename__ = "quotes"

    messageid = Column(String, primary_key=True)
    message = Column(String)
    timestamp = Column(String)
    userid = Column(String, ForeignKey('users.userid'))
    channelid = Column(Integer, ForeignKey('channels.channelid'))

    def __init__(self, messageid, message, timestamp, userid, channelid):
        self.messageid = messageid
        self.message = message
        self.timestamp = timestamp
        self.userid = userid
        self.channelid = channelid


class Admin(Base):

    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    userid = Column(String, ForeignKey('users.userid'))
    user = relationship("User", uselist=False)

    def __init__(self, userid):
        self.userid = userid


class Macro(Base):

    __tablename__ = "macros"

    id = Column(Integer, primary_key=True)
    command = Column(String, unique=True)
    response = Column(String)
    modified_flag = Column(Integer)

    def __init__(self, command, response, modified_flag=None):
        self.command = command
        self.response = response
        self.modified_flag = modified_flag


# ---- Helper Functions ----

def create_database(base, engine):
    base.metadata.create_all(engine)


def populate_database(session, bot):
    '''
    Takes sqlalchemy session and discord bot as args
    and populates database with channels, users.
    '''

    # list of channels and users from database.
    db_channels = [c.name for c in session.query(Channel.channelid).all()]
    db_users = [u.name for u in session.query(User.userid).all()]

    # List of channels and users from Discord.
    bot_channels = [c for c in bot.get_all_channels()]
    bot_users = [m for m in bot.get_all_members()]

    # Add missing channels to database.
    for channel in bot_channels:
        if channel.id not in db_channels:
            new_channel = Channel(channel.id, channel.name, str(channel.type))
            session.add(new_channel)

    # Add missing users to database.
    for user in bot_users:
        if user.id not in db_users:
            new_user = User(user.id, user.name, user.display_name, user.avatar_url)
            session.add(new_user)

            # Add user to channels.
            for channel in session.query(Channel):
                channel.members.append(new_user)

    session.commit()
