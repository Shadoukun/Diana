from discord.ext import commands
from wordnik import *
from wordnik import swagger
import discord
from diana import utils
from diana.config import config

class Wordnik:

    def __init__(self, bot):
        self.bot = bot
        self.apiUrl = 'http://api.wordnik.com/v4'
        self.apiKey = config.wordnikToken
        self.client = swagger.ApiClient(self.apiKey, self.apiUrl)
        self.wordApi = WordApi.WordApi(self.client)

    @commands.command(name='dict', aliases=['d'], pass_context=True, no_pm=True)
    async def wordnik_search(self, ctx, *args):
        """: !d <word>          | Lookup a word in the dictionary"""
        message = utils.parse_message(ctx.message.content)

        lookup = self.wordApi.getDefinitions(message)

        if lookup is None:
            await self.bot.send_message(ctx.message.channel, "No results found.")
            return

        else:
            # For now, only work with the first definition given. lookup[0]
            word = lookup[0].word
            pos = lookup[0].partOfSpeech
            definition = lookup[0].text
            examples = lookup[0].exampleUses

            embed = discord.Embed(name='\u2063', colour=0x006FFA)
            embed.set_author(name="Wordnik", icon_url="https://www.wordnik.com/favicon.ico")
            embed.add_field(name=word, value=pos)
            embed.add_field(name='\u2063', value=definition)

            if examples:
                embed.add_field(name="Example", value=examples)

            await self.bot.send_message(ctx.message.channel, embed=embed)


def setup(bot):
    bot.add_cog(Wordnik(bot))
