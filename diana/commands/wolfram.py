import wolframalpha
import discord
from discord.ext import commands
from diana import utils
from diana.config import config
from pprint import pprint

class WolframAlpha:

    def __init__(self, bot):
        self.bot = bot
        self.client = wolframalpha.Client(config.wolframToken)

    @commands.group(name='wolfram', aliases=['?'], pass_context=True, no_pm=True)
    async def wolfram_search(self, ctx, *args):
        """: !? <expression>    | Use WolframAlpha"""

        message = utils.parse_message(ctx.message.content)
        print(ctx.invoked_subcommand)

        if message:
            res = self.client.query(message, stream=True)

            embed = discord.Embed(title="\n", colour=0xFF6600)
            embed.set_author(name="WolframAlpha", icon_url="https://www.wolframalpha.com/favicon.ico")
            podlist = [x for x in res.pods]

            for pod in podlist[0:3]:
                embed.add_field(name=pod.title, value="`" + pod.text + "`", inline=False)

            pprint(res.results)

            await self.bot.send_message(ctx.message.channel, embed=embed)

    @wolfram_search.command(name="verbose")
    async def verbose_search():

        message = utils.parse_message(ctx.message.content)
        print("verbose")

        if message:
            res = self.client.query(message, stream=True)

            embed = discord.Embed(title="\n", colour=0xFF6600)
            embed.set_author(name="WolframAlpha", icon_url="https://www.wolframalpha.com/favicon.ico")
            #podlist = [x for x in res.pods]

            for pod in podlist[0:3]:
                embed.add_field(name=pod.title, value="`" + pod.text + "`", inline=False)

            pprint(res.results)

            await self.bot.send_message(ctx.message.channel, embed=embed)


def setup(bot):
    bot.add_cog(WolframAlpha(bot))
