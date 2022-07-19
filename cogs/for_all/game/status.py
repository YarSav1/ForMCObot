import discord
from discord.ext import commands

from DataBase.global_db import DB_GAME
from config.functional_config import check_channels, failure, FAILURE_COLOR, accept, SUCCESS_COLOR, len_status


class Status(commands.Cog):
    def __init__(self, py):
        self.py = py
    async def stopper(self, ctx):
        embed = discord.Embed(title=f'{failure} Руководство {failure}',
                              description=f'Это твой статус около ника в профилях!\n'
                                          f'Максимальная длина статуса - **{len_status} символов**.',
                              color=FAILURE_COLOR)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['status','статус','описание'])
    async def _status(self, ctx, *, text=None):
        if await check_channels(ctx):

            if text is None:
                await self.stopper(ctx)
            elif len(text) > len_status:
                embed = discord.Embed(title=f'{failure}',
                                      description=f'Длина статуса не может превышать более {len_status} символов!',
                                      color=FAILURE_COLOR)
                await ctx.reply(embed=embed)
            else:
                search = {'id_member': ctx.author.id}
                DB_GAME.update_one(search,
                                   {'$set': {'status': text}})
                embed = discord.Embed(title=f'{accept}',
                                      description='Статус установлен!', color=SUCCESS_COLOR)
                await ctx.reply(embed=embed)



def setup(py):
    py.add_cog(Status(py))