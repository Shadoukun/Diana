from discord.ext import commands
import json
import requests
import discord
from diana import utils

class UrbanDictionary:

    def __init__(self, bot):
        self.bot = bot
        self.url = 'http://api.urbandictionary.com/v0/define?term='
        self.session = requests.Session()

    @commands.group(name='ud', pass_context=True, no_pm=True)
    async def urbandict_search(self, ctx, *args):
        """: !ud <word>         | lookup a word on UrbanDictionary."""

        message = utils.parse_message(ctx.message.content)

            # Returns first entry for requested word.

        try:
            r = self.session.get(self.url + message)
            response = json.loads(r.text)['list'][0]

        except:
            await self.bot.send_message(ctx.message.channel, "No Results Found.")
            return

        definition = response['definition']
        permalink = response['permalink']
        title = response['word']
        example = "_" + response['example'] + "_"

        embed = discord.Embed(title="\n", url=permalink, colour=0xE86222)
        embed.set_author(name="urbandictionary", icon_url="https://www.urbandictionary.com/favicon.ico")
        embed.add_field(name=title, value=definition + "\n\n" + example, inline=False)

        await self.bot.send_message(ctx.message.channel, embed=embed)


def setup(bot):
    bot.add_cog(UrbanDictionary(bot))
