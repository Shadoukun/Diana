import discord
from discord.ext import commands
import json
import requests
from pprint import pprint
from diana import utils

class IMDB:

    def __init__(self, bot):
        self.bot = bot
        self.session = requests.Session()
        self.url = "http://omdbapi.com/?t="

    @commands.command(name='imdb', pass_context=True, no_pm=True)
    async def imdb_search(self, ctx, *args):
        """: !imdb <title>      | lookup a movie on IMDB. """
        message = utils.parse_message(ctx.message.content)
        r = self.session.get(self.url + message)

        if r.status_code == 200:
            movie = json.loads(r.text)
        else:
            await self.bot.send_message(ctx.message.channel, "No Results Found.")

        if movie['Response'] == "True":
            embed = discord.Embed(title="\n", colour=0x006FFA)
            embed.set_image(url=movie['Poster'])
            embed.set_author(name="IMDB", icon_url="http://www.imdb.com/favicon.ico")
            embed.add_field(name="Title", value=movie['Title'], inline=False)
            embed.add_field(name="IMDB rating", value=movie['imdbRating'], inline=False)
            embed.add_field(name="Year", value=movie['Year'], inline=False)
            embed.add_field(name="Genre", value=movie['Genre'], inline=False)
            embed.add_field(name="Director", value=movie['Director'], inline=False)
            embed.add_field(name="Actors", value=movie['Actors'])
            embed.add_field(name="Plot", value=movie['Plot'])
            await self.bot.send_message(ctx.message.channel, embed=embed)

        else:
            await self.bot.send_message(ctx.message.channel, "No Results Found.")

def setup(bot):
    bot.add_cog(IMDB(bot))
