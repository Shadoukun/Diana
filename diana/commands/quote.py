import discord
from discord.ext import commands
from diana import utils
from diana.config import config
from difflib import get_close_matches
import json
import random
import sqlite3
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import diana.db as db
import time


class Quote:

    def __init__(self, bot):
        self.bot = bot

        Session = sessionmaker(bind=db.engine)
        self.session = Session()


    def _add_quote(self, message):
        # timestamp too precise.
        timestamp = message.timestamp.strftime('%m/%d/%y')
        quote = db.Quote(message.id, message.content, timestamp, message.author.id, message.channel.id)
        self.session.add(quote)
        self.session.commit()

    def get_channel(self, channelName):
        '''Returns channel object from name'''

        channelList = [x for x in self.bot.get_all_channels()]

        for c in channelList:
            if channelName in str(c.name):
                channel = c
                return channel
            else:
                print("no channel id")
                return None

    def findUser(self, ctx):
        '''Returns user object from name'''

        message = ctx.message.content.split(' ')[2].lower()
        members = ctx.message.channel.server.members

        # If message is a @mention
        if ctx.message.mentions:
            return ctx.message.mentions[0]

        else:
            # fuzzy match username from list of users.
            userlist = [m.display_name.lower() for m in members]
            username = get_close_matches(message, userlist, 1)[0]

            for member in members:
                display_name = member.display_name.lower()
                name = member.name

                if display_name == username or name.lower() == username:
                    user = member
                    return user

            return None

    def create_embed(self, user, message):
        embed = discord.Embed(title=None, colour=0x006FFA)
        embed.set_author(name=user.display_name, icon_url=str(user.avatar_url))
        embed.add_field(name="\u200B", value=message)
        return embed




    @commands.group(name='quote', pass_context=True, no_pm=True, invoke_without_command=True)
    async def quote(self, ctx, *args):
        # if invoked without a subcommand, return a random message. eventually.
        if ctx.invoked_subcommand is None:
            pass

    @quote.command(name="add", pass_context=True)
    async def quote_add(self, ctx):
        message = ctx.message.content.split(' ')[2:]
        # TODO: Readd admin check.
        # if str(ctx.message.author.id) not in self.db['admins']:
            # return

        # if channel not included, use current channel
        if len(message) is 1:
            channel = self.get_channel(str(ctx.message.channel))
            messageID = message[0]
        else:
            return

        # ignore duplicates.
        # TODO: Readd duplicate check

        quoteMsg = await self.bot.get_message(channel, messageID)

        if quoteMsg:
            self._add_quote(quoteMsg)
            await self.bot.send_message(ctx.message.channel, "Quote added.")
            embed = self.create_embed(quoteMsg.author, quoteMsg.content)
            await self.bot.send_message(ctx.message.channel, embed=embed)
        else:
            await self.bot.send_message(ctx.message.channel, "Couldn't add quote.")

    @quote.command(name="remove", pass_context=True)
    async def remove(self, ctx):
        messageid = ctx.message.content.split(' ')[2:][0]
        channel = ctx.message.channel
        sender = ctx.message.author.id

        # TODO: readd admin check.
        #if sender not in self.db['admins']:
        #    return

        quotes = self.session.query(db.Quote).filter(db.Quote.channelid == channel.id)
        for quote in quotes:
            if messageid == quote.messageid:
                self.session.delete(quote)
                self.session.commit()
                await self.bot.send_message(ctx.message.channel, "Quote Removed.")

    @quote.command(name="get", pass_context=True)
    async def get_user_quote(self, ctx):

        message = ctx.message.content.split(' ')[2:]
        channel = ctx.message.channel

        quotes = self.session.query(db.Quote)
        quotes = quotes.filter(db.Quote.channelid == channel.id)

        if len(message) is 1:
            user = self.findUser(ctx)

        else:
            user = None

        if user:
            userid = user.id
            quotes = quotes.filter(db.Quote.userid == userid).all()

            random.shuffle(quotes)
            message = quotes[0].message

            embed = self.create_embed(user, message)
            await self.bot.send_message(channel, embed=embed)

        else:
            quotes = quotes.all()
            random.shuffle(quotes)
            user = await self.bot.get_user_info(quotes[0].userid)

            message = quotes[0].message


            embed = self.create_embed(user, message)
            await self.bot.send_message(channel, embed=embed)

    @quote.command(name="list", pass_context=True)
    async def quote_list(self, ctx):
        message = ctx.message.content.split(' ')[2:]
        channel = str(ctx.message.channel)

        if len(message) is 0:
            url = "http://{h}:5000/quotes/{c}".format(h=config.host, c=channel)
            await self.bot.send_message(ctx.message.channel, url)
            return

        user = self.findUser(ctx)

        for quote in self.db['quotes'][channel]:
            if user.id == quote['user_id']:
                userid = quote['user_idw']
                break

        url = "http://{h}:5000/quotes/{c}/{u}".format(h=config.host, c=channel, u=userid)
        await self.bot.send_message(ctx.message.channel, url)

    @quote.command(name="stats", pass_context=True)
    async def stats(self, ctx):
        message = ctx.message.content.split(' ')[2:]
        channel = ctx.message.channel
        quotes = quotes = self.session.query(db.Quote)
        # general channel stats
        if len(message) is 0:
            quotes = quotes.filter(db.Quote.channelid == channel.id).all()
            total = str(len(quotes))
            msg = "Quote Total: {c}".format(c=total)
            await self.bot.send_message(ctx.message.channel, msg)
            return

        # user stats for channel
        else:
            user = self.findUser(ctx)
            quotes = quotes.filter(db.Quote.userid == user.id).all()

            total = str(len(quotes))
            msg = "Quote Total: {c}".format(c=total)
            await self.bot.send_message(ctx.message.channel, msg)


def setup(bot):
    bot.add_cog(Quote(bot))
