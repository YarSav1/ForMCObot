import random

from discord.ext import commands
import discord

from DataBase.global_db import DB_GAME
from config.functional_config import money_emj, exp_emj
from config.minecraft_config import bounty_coordinates


class GetPrise(commands.Cog):
    def __init__(self, py):
        self.py = py

    @commands.command(aliases=['получить-приз', 'get-prise', 'п-п', 'g-p'])
    async def _get_prise(self, ctx):
        player_db = DB_GAME.find_one({'id_member': ctx.author.id})
        amount_ok_coordinate = 0
        text = ''
        for i in player_db['minecraft-coordinates']:
            if i[2]:
                amount_ok_coordinate += 1
                # DB_GAME.update_one({'id_member': ctx.author.id},
                #                    {'$pull': {'minecraft-coordinates': i}})
        prise_balance = 0
        prise_exp = 0
        for i in range(amount_ok_coordinate):
            prise_balance+=random.randint(bounty_coordinates[0][0],bounty_coordinates[0][1])
            prise_exp+=random.randint(bounty_coordinates[1][0],bounty_coordinates[1][1])

        text += f'Выполнено заданий с координатами: {amount_ok_coordinate} - Приз: **{prise_balance}** {money_emj} и ' \
                f'**{prise_exp}** {exp_emj}.'
        print(text)
        await ctx.send(text)


def setup(py):
    py.add_cog(GetPrise(py))
