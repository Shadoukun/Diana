import wikipedia
import discord
from discord.ext import commands
from diana import utils

class Wikipedia:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="wiki", pass_context=True, no_pm=True)
    async def wiki_search(self, ctx, *args):
        """: !wiki <word>       | Lookup something up on Wikipedia."""

        message = utils.parse_message(ctx.message.content)

        try:
            article = wikipedia.page(message, auto_suggest=False)

            embed = discord.Embed(title="\u2063", colour=0xF9F9F9)
            embed.set_author(name="Wikipedia", icon_url="https://www.wikipedia.org/static/favicon/wikipedia.ico")
            embed.add_field(name=article.title, value=article.summary.split('\n', 1)[0], inline=True)

            await self.bot.send_message(ctx.message.channel, embed=embed)

        except wikipedia.DisambiguationError as e:
            title = "'{t}' may refer to:\n".format(t=e.title)
            text = '\n'.join(e.options[:10])

            embed = discord.Embed(title="\u2063", colour=0xF9F9F9)
            embed.set_author(name="Wikipedia", icon_url="https://www.wikipedia.org/static/favicon/wikipedia.ico")
            embed.add_field(name=title, value=text, inline=True)

            await self.bot.send_message(ctx.message.channel, embed=embed)

        except wikipedia.PageError as e:
            await self.bot.send_message(ctx.message.channel, "No results found.")



def setup(bot):
    bot.add_cog(Wikipedia(bot))
