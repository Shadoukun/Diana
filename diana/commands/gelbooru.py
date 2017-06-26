import requests
import random
import discord
from bs4 import BeautifulSoup
from functools import lru_cache
from discord.ext import commands
from cachetools import TTLCache
from diana import utils
import lxml
import os
import yaml
from pathlib import Path
from diana.config import config
import diana.db as db


class Gelbooru:
    def __init__(self, bot):
        self.cache = TTLCache(maxsize=500, ttl=300)
        self.bot = bot
        self.session = requests.Session()

        self.url = "http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags="
        self.post_url = "http://gelbooru.com/index.php?page=post&s=view&id="


        self.default_tags = None

        self.tags_file = "./config/gelbooru_defaulttags.yaml"
        if Path(self.tags_file).is_file():
            with open(self.tags_file, 'r') as tagfile:
                self.default_tags = yaml.load(tagfile)
        else:
            open(self.tags_file, 'x')

        if self.default_tags is None:
            self.default_tags = dict()

    @commands.group(name='cum', pass_context=True, no_pm=True, invoke_without_command=True)
    async def gelbooru_search(self, ctx, *args):
        """: !cum <tags>        | Post a random image from Gelboorur"""

        channel = str(ctx.message.channel)
        if channel not in self.default_tags:
            self.default_tags[channel] = ['shota']

        if ctx.invoked_subcommand is None:
            print("test")
            message = utils.parse_message(ctx.message.content, tags=self.default_tags[channel])
            count = self.gelbooru_count(message)

            if count:
                pageid = self.getRandomPage(count)
            else:
                msg = "No Results Found."
                await self.bot.send_message(ctx.message.channel, msg)
                return

            # Search
            r = self.session.get(self.url + message + "&pid=" + str(pageid))
            soup = BeautifulSoup(r.content, "html.parser")
            posts = soup.find_all("post")
            post = await self.getRandomPost(posts, count)

            if post:
                embed = self.create_embed(post)
                await self.bot.send_message(ctx.message.channel, embed=embed)
            else:

                msg = "All images already seen, Try again later."
                await self.bot.send_message(ctx.message.channel, msg)
                return

    @gelbooru_search.group(name="default_tags", pass_context=True, no_pm=True, invoke_without_command=True)
    async def defaultTags(self, ctx):
        if ctx.invoked_subcommand is None:
            channel = str(ctx.message.channel)
            await self.bot.send_message(ctx.message.channel, self.default_tags[channel])


    @defaultTags.command(name="add", pass_context=True, no_pm=True)
    async def blacklist_add(self, ctx):
        #if str(ctx.message.author.id) not in admins:
        #   return

        admins = [a for a in self.bot.session.query(db.Admin.userid).all()]
        if str(ctx.message.author.id) not in admins:
            return

        msg = ctx.message.content.split(' ')[3:]
        channel = str(ctx.message.channel)
        writefile = False

        for tag in msg:
            if tag not in self.default_tags[channel]:
                self.default_tags[channel].append(tag)
                writefile = True

        if writefile:
            with open(self.tags_file, 'w') as tagfile:
                yaml.dump(self.default_tags, tagfile, default_flow_style=False)

            await self.bot.send_message(ctx.message.channel, self.default_tags[channel])

    @defaultTags.command(name="remove", pass_context=True, no_pm=True)
    async def blacklist_remove(self, ctx):

        admins = [a for a in self.bot.session.query(db.Admin.userid).all()]
        if str(ctx.message.author.id) not in admins:
            return

        msg = ctx.message.content.split(' ')[3:]
        channel = str(ctx.message.channel)
        writefile = False

        for tag in msg:
            if tag in self.default_tags[channel]:
                self.default_tags[channel].remove(tag)
                writefile = True

        if writefile:
            with open(self.default_tags, 'w') as tagfile:
                yaml.dump(self.default_tags, tagfile, default_flow_style=False)

            await self.bot.send_message(ctx.message.channel, self.default_tags[channel])

    async def getRandomPost(self, posts, count):
        # create list of posts not recently seen.
        postlist = []
        for post in posts:
            if post['id'] not in self.cache.keys():
                postlist.append(post)

        # if post list has posts, shuffle and select one
        if len(postlist):
            random.shuffle(postlist)
            postid = postlist[0]['id']
            self.cache[postid] = postid

            return postlist[0]

    def getRandomPage(self, count):
        maxpage = int(round(count/100))
        if maxpage < 1:
            maxpage = 1

        # return random page number from range(0, maxpage)
        pageid = random.sample(list(range(0, maxpage)), 1)[0]
        return pageid

    @lru_cache(maxsize=None)
    def gelbooru_count(self, message):
        # get total number of posts
        r = self.session.get(self.url + message)

        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "html.parser")
            count = int(soup.find("posts")['count'])

            if count:
                return count

    def create_embed(self, post):
        # create discord embed from post
        postid = str(post['id'])
        post_url = "https:" + str(post['file_url'])
        source_url = str(post['source'])
        orig_url = self.post_url + postid
        source_text = """*View on:* [[Gelbooru]]({o})  |  [[Source]]({s})""".format(o=orig_url,s=source_url)

        embed = discord.Embed(title="\n", url=post_url, colour=0x006FFA)
        embed.set_image(url=post_url)
        embed.set_author(name="Gelbooru", icon_url="https://gelbooru.com/favicon.png")
        embed.add_field(name="\u200B", value=source_text, inline=False)
        return embed


def setup(bot):
    bot.add_cog(Gelbooru(bot))
