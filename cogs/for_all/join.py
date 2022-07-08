import asyncio

from discord.ext import commands

from DataBase.global_db import DB_GAME
from config.functional import check_fields


class JoinServer(commands.Cog):
    def __init__(self, py):
        self.py = py

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await asyncio.sleep(10)
        info = await check_fields(member)
        roles = info['buy_roles']
        for role in roles:
            role_on_server = member.guild.get_role(int(role))
            if role_on_server is not None:
                await member.add_roles(role_on_server)
            else:
                DB_GAME.update_one({'id_member': member.id},
                                   {'$pull': {'buy_roles': role}})


def setup(py):
    py.add_cog(JoinServer(py))