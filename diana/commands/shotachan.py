from discord.ext import commands
from bs4 import BeautifulSoup, SoupStrainer
from functools import lru_cache
import requests
import random
import discord
import json
from cachetools import TTLCache
from diana import utils

class Shotachan:

    def __init__(self, bot):
        self.bot = bot
        self.session = requests.Session()
        self.cache = TTLCache(maxsize=500, ttl=300)
        self.count_url = "http://booru.shotachan.net/post?tags="
        self.post_url = "http://booru.shotachan.net/post/index.json?tags="

    @commands.command(name='shota', pass_context=True, no_pm=True)
    async def shotachan_search(self, ctx, *args):
        """: !shota <tags>      | Post a random image from the Shotachan Booru."""

        # if no tags, default
        message = utils.parse_message(ctx.message.content)

        # get number of pages
        maxpage = self.shotachan_count(message)

        # Choose random page number
        pid = list(range(0, int(maxpage)))
        random.shuffle(pid)

        # get posts
        url = self.post_url + message + "&page=" + str(pid[0])
        posts = json.loads(self.session.get(url).text)
        count = len(posts)

        # get random post
        if posts:
            post = await self.getRandomPost(posts)

        else:
            msg = "No Results Found."
            await self.bot.send_message(ctx.message.channel, msg)
            return

        # if random post returned, create embed.
        if post:
            embed = self.create_embed(post)
            await self.bot.send_message(ctx.message.channel, embed=embed)

        else:
            msg = "All images have already been seen. Try again later."
            await self.bot.send_message(ctx.message.channel, msg)
            return

    @lru_cache(maxsize=None)
    def shotachan_count(self, message):

        url = self.count_url + message
        r = self.session.get(url)
        try:
            # Get total number of posts.
            strainer = SoupStrainer('div', attrs={'id': 'paginator'})
            soup = BeautifulSoup(r.content, "html.parser", parse_only=strainer)
            maxpage = soup.find_all('a')[-2].getText()

        except:
            return 1

        return maxpage

    async def getRandomPost(self, posts):
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

        else:
            return None

    def create_embed(self, post):
        postid = str(post['id'])
        post_url = str(post['file_url'])
        source_url = str(post['source'])
        orig_url = "http://booru.shotachan.net/post/show/{id}".format(id=postid)

        embed = discord.Embed(title="\n", url=post_url, colour=0x006FFA)
        embed.set_image(url=post_url)
        embed.set_author(name="Shotachan", icon_url="http://booru.shotachan.net/favicon.ico")
        embed.add_field(name="\u200B", value="*View on:* [[Shotachan]]({o})  |  [[Source]]({s})".format(o=orig_url, s=source_url), inline=False)
        return embed


def setup(bot):
    bot.add_cog(Shotachan(bot))
