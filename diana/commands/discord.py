import discord
from discord.ext import commands
import discord.utils
from pprint import pprint
from difflib import get_close_matches
from diana.config import config
from diana.diana import session
import diana.db as db

class Discord:

    def __init__(self, bot):
        self.bot = bot
        self.session = session

    @commands.command(pass_context=True, no_pm=True)
    async def avatar(self, ctx):
        """: !avatar <username> | post a user's avatar."""

        user = self.findUser(ctx)
        if user:
            avatar_url = user.avatar_url.split("?")[0]
            print(avatar_url)
            embed = discord.Embed(title="Avatar: " + user.display_name, url=None)
            embed.set_image(url=avatar_url)
            print(embed.to_dict())
            await self.bot.send_message(ctx.message.channel, embed=embed)
        else:
            await self.bot.send_message(ctx.message.channel, "No Results Found.")

    @commands.command(name="uinfo", pass_context=True, no_pm=True)
    async def userInfo(self, ctx):
        """: !uinfo <username>  | Post a user's information."""
        # TODO: fix permissions.

        channel = ctx.message.channel
        embed = discord.Embed(title="User Info", url=None)

        user = self.findUser(ctx)
        if user:
            joindate = str(user.joined_at).split(' ', 1)[0]

            embed.add_field(name="Username", value=user.name, inline=False)
            embed.add_field(name="Join Date", value=joindate, inline=False)
            embed.add_field(name="Status", value=str(user.display_name), inline=False)

            # Only add 'Roles' field if there are roles
            roles = []
            if len(user.roles) > 1:
                for role in user.roles:
                    if 'everyone' in role.name:
                        continue

                    roles.append(role.name)

                roles = ', '.join(roles)
                embed.add_field(name="Roles", value=roles, inline=False)

            # add channel permissions for user
            permissions = []
            for permission in ctx.message.channel.permissions_for(user):
                # if permission is True
                if permission[1]:
                    permissions.append(permission[0])
            permissions = ', '.join(permissions)
            embed.add_field(name="Permissions", value=permissions)

            await self.bot.send_message(channel, embed=embed)
        else:
            await self.bot.send_message(ctx.message.channel, "No Results Found.")

    @commands.command(name="add_admin", pass_context=True)
    async def add_admin(self, ctx):

        sender = ctx.message.author
        user = self.findUser(ctx)
        userid = user.id

        admins = [a for a in self.session.query(db.Admin.userid).all()]
        if (sender.id in admins) or (len(admins) is 0):

            new_admin = db.Admin(userid)
            self.session.add(new_admin)
            self.session.commit()
            await self.bot.send_message(ctx.message.channel, "Admin added")

    @commands.command(name="remove_admin", pass_context=True)
    async def remove_admin(self, ctx):

        sender = ctx.message.author
        user = self.findUser(ctx)
        userid = user.id

        admins = [a for a in self.session.query(db.Admin).all()]
        if sender.id in [a.userid for a in admins]:
            for a in admins:
                if a.userid == userid:
                    self.session.delete(a)
                    self.session.commit()
                    await self.bot.send_message(ctx.message.channel, "Admin removed.")
        else:
            return

    def findUser(self, ctx):
        message = ctx.message.content.split(' ', 1)[1].lower()
        members = ctx.message.channel.server.members

        # If message is a @mention
        if ctx.message.mentions:
            return ctx.message.mentions[0]

        else:
            # fuzzy match username from list of users.
            userlist = [m.display_name.lower() for m in members]
            username = get_close_matches(message, userlist, 1)[0]

            for member in members:
                display_name = member.display_name.lower()
                name = member.name

                if display_name == username or name.lower() == username:
                    user = member
                    return user

            return None


def setup(bot):
    bot.add_cog(Discord(bot))
