import requests
import random
import discord
from bs4 import BeautifulSoup
from functools import lru_cache
from discord.ext import commands
from cachetools import TTLCache
from diana import utils
import lxml


class Gelbooru:
    def __init__(self, bot):
        self.cache = TTLCache(maxsize=500, ttl=300)
        self.bot = bot
        self.session = requests.Session()

        self.url = "http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags="
        self.post_url = "http://gelbooru.com/index.php?page=post&s=view&id="

        self.default_tags = [
                             "+shota",
                             "-straight_shota",
                             "-trap",
                             "-androgynous"
                            ]

    @commands.command(name='cum', pass_context=True, no_pm=True)
    async def gelbooru_search(self, ctx, *args):
        """: !cum <tags>        | Post a random image from Gelboorur"""

        message = utils.parse_message(ctx.message.content,
                                      tags=self.default_tags)

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
