import asyncio
from diana.db import *

import diana.utils as utils


# Background tasks


class Tasks(object):

    async def update_macros_task(self):
        await self.wait_until_ready()
        while not self.is_closed:

            macros = self.session.query(Macro).all()

            if macros:
                for macro in macros:
                    # sqlalchemy seems to not refresh consistently
                    self.session.refresh(macro)

                    if macro.modified_flag == 1:
                        macro.modified_flag = 0
                        self.session.commit()

                        await self.load_macro_commands(macro)

            # Runs every 20 seconds.
            await asyncio.sleep(20)


    async def add_channels_task(self):
        """Add server channels to database"""
        await self.wait_until_ready()
        while not self.is_closed:

            db_channels = [c.channelid for c in self.session.query(Channel).all()]
            bot_channels = [c for c in self.get_all_channels()]
            for channel in bot_channels:
                if channel.id not in db_channels:
                    new_channel = Channel(channel.id, channel.name, str(channel.type))
                    self.session.add(new_channel)

            self.session.commit()


            # Runs every 3.5 minutes.
            await asyncio.sleep(210)


    async def add_users_task(self):
        """Add new users to database"""
        await self.wait_until_ready()
        while not self.is_closed:

            db_users = [u.userid for u in self.session.query(User).all()]
            bot_users = [m for m in self.get_all_members()]

            for user in bot_users:
                if user.id not in db_users:
                    new_user = User(user.id, user.name, user.display_name, user.avatar_url)
                    self.session.add(new_user)
                    # Add user to channels.
                    for channel in self.session.query(Channel):
                        channel.members.append(new_user)

            self.session.commit()

            # Runs every 2 hours
            await asyncio.sleep(7200)

    async def update_existing_users_task(self):
        """Update information for existing users"""
        await self.wait_until_ready()
        while not self.is_closed:

            db_users = [u for u in self.session.query(User).all()]
            bot_users = [m for m in self.get_all_members()]

            for botuser in bot_users:
                for dbuser in db_users:
                    if dbuser.userid == botuser.id:
                        dbuser.display_name = botuser.display_name
                        dbuser.avatar_url = botuser.avatar_url

            self.session.commit()

            # Runs every 3.5 hours
            await asyncio.sleep(12600)

    async def add_responses(self):
        """Add macro responses from database"""
        await self.wait_until_ready()
        while not self.is_closed:

            self.responses.clear()
            responses = self.session.query(MacroResponse).all()

            if responses:
                for resp in responses:
                    # sqlalchemy seems to not refresh consistently
                    self.session.refresh(resp)
                    self.responses[resp.trigger] = resp.response

            # Runs every 20 seconds.
            await asyncio.sleep(20)

    async def add_reactions(self):
        """Add macro reactions from database"""
        await self.wait_until_ready()
        while not self.is_closed:

            self.reactions.clear()
            reactions = self.session.query(MacroReaction).all()

            if reactions:
                for r in reactions:
                    # sqlalchemy seems to not refresh consistently
                    self.session.refresh(r)
                    self.reactions[r.trigger] = r.reaction.replace(':', '')

            # Runs every 20 seconds.
            await asyncio.sleep(20)

