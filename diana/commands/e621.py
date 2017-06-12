import requests
import random
import discord
from bs4 import BeautifulSoup
from discord.ext import commands
from cachetools import TTLCache
from diana import utils

class e621:

    def __init__(self, bot):
        self.bot = bot
        self.session = requests.Session()
        self.cache = TTLCache(maxsize=500, ttl=300)
        self.url = "https://e621.net/post/index.xml?tags="
        self.default_tags = "+shota"

    @commands.command(name='fur', pass_context=True, no_pm=True)
    async def e621_search(self, ctx, *args):
        """: !fur <tags>        | Post random a image from e621"""

        channel = ctx.message.channel
        message = utils.parse_message(ctx.message.content,
                                      tags=self.default_tags)

        # Only respond in the furry channels.
        if "fur" not in str(channel):
            return

        r = requests.get(self.url + message)

        # If response is OK, continue.
        if r.status_code == 200:
            # parse page and get number of posts
            soup = BeautifulSoup(r.content, "xml")
            count = len(soup.find_all("post"))

            # Calculate number of pages (posts/limit), and search one at random.
            maxpage = int(round(count/320))

            if maxpage < 1:
                maxpage = 1

            pid = list(range(0, maxpage))
            random.shuffle(pid)
            r = self.session.get(self.url + message + "&page=" + str(pid[0]))
            soup = BeautifulSoup(r.content, "lxml")
            posts = soup.find_all("post")

            if len(posts) is 0:
                msg = "No Results Found."
                await self.bot.send_message(ctx.message.channel, msg)
                return

            post = await self.getRandomPost(posts)

            if post:
                embed = self.create_embed(post)
                await self.bot.send_message(ctx.message.channel, embed=embed)

            else:
                msg = "All images have already been seen. Try again later."
                await self.bot.send_message(ctx.message.channel, msg)

    async def getRandomPost(self, posts):
        # create list of posts not recently seen.
        postlist = []
        for post in posts:
            postid = post.find('id').text
            if postid not in self.cache.keys():
                postlist.append(post)

        # if post list has posts, shuffle and select one
        if len(postlist):
            random.shuffle(postlist)
            postid = postlist[0].find('id').text
            self.cache[postid] = postid
            return postlist[0]

        else:
            return None

    def create_embed(self, post):
        post_url = post.find('file_url').text
        source_url = post.find("source").text
        postid = post.find("id").text
        orig_url = "https://e621.net/post/show/{id}".format(id=postid)
        embed = discord.Embed(title="\n", url=post_url, colour=0x006FFA)
        embed.set_image(url=post_url)
        embed.add_field(name="e261", value="*View on:* [[e261]]({o})  |  [[Source]]({s})".format(o=orig_url, s=source_url), inline=False)
        return embed



def setup(bot):
    bot.add_cog(e621(bot))
