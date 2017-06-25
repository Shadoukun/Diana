import flickr_api
import random
import requests
from bs4 import BeautifulSoup, SoupStrainer
from cachetools import TTLCache
from discord.ext import commands
from discord import Embed
from diana.config import config

class Shiba:

    def __init__(self, bot):
        self.bot = bot
        self.session = requests.Session()
        self.cache = TTLCache(maxsize=500, ttl=300)

        public_key = config.flickrPublic
        secret_key = config.flickrSecret
        flickr_api.set_keys(public_key, secret_key)

    @commands.command(pass_context=True, no_pm=True)
    async def shiba(self, ctx, *args):
        """: !shiba             | post random Shibas"""

        shibas = flickr_api.Photo.search(per_page=500, tags='shiba dog')
        random.shuffle(shibas)
        sizes = ['Large', 'Medium', 'Small', 'Original']

        while shibas[0]['id'] in self.cache.keys():
            random.shuffle(shibas)

        photo_id = shibas[0]['id']
        self.cache[photo_id] = photo_id

        for size in sizes:
            try:
                r = self.session.get(shibas[0].getPhotoUrl(size))
                strainer = SoupStrainer('div', attrs={'id': 'allsizes-photo'})
                soup = BeautifulSoup(r.content, "html.parser", parse_only=strainer)

                file_url = soup.find('img')['src']

                embed = Embed()
                embed.set_author(name="Shiba", icon_url="http://i1.kym-cdn.com/entries/icons/facebook/000/013/564/aP2dv.jpg")
                embed.set_image(url=file_url)
                await self.bot.send_message(ctx.message.channel, embed=embed)
                return

            except:
                continue


def setup(bot):
    bot.add_cog(Shiba(bot))
