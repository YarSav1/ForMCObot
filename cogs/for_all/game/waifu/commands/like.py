import discord
from discord.ext import commands

from DataBase.global_db import DB_GAME
from config.functional import check_channels, failure, SUCCESS_COLOR, accept, FAILURE_COLOR


class LikeUser(commands.Cog):
    def __init__(self, py):
        self.py = py

    async def stopper1(self, ctx):
        embed = discord.Embed(title=f'{failure}',
                              description=f'Пример: !like `участник` - установить свою близость к кому-либо.',
                              color=FAILURE_COLOR)
        await ctx.reply(embed=embed)




    @commands.command(aliases=['like','нравится','нрав'])
    async def _like_user(self, ctx, member: discord.Member = None):
        if await check_channels(ctx):
            if member is None:
                await self.stopper1(ctx)
            else:
                DB_GAME.update_one({'id_member': ctx.author.id},
                                   {'$set': {'like': member.id}})
                embed = discord.Embed(title=f'{accept}',
                                      description=f'Теперь Вам нравится `{member.display_name}`!',
                                      color=SUCCESS_COLOR)
                await ctx.reply(embed=embed)


    @_like_user.error
    async def _like_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.reply('Игрок не найден!')

    @commands.command(aliases=['unlike','ненравится','ненрав'])
    async def _unlike_user(self, ctx):
        if await check_channels(ctx):
            DB_GAME.update_one({'id_member': ctx.author.id},
                               {'$set': {'like': 0}})
            embed = discord.Embed(title=f'{accept}',
                                  description=f'Теперь Вам никто не нравится!',
                                  color=SUCCESS_COLOR)
            await ctx.reply(embed=embed)


def setup(py):
    py.add_cog(LikeUser(py))