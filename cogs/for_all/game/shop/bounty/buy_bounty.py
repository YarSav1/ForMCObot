import discord
from discord.ext import commands

from DataBase.global_db import DB_GAME
from config.functional import check_fields, check_channels, failure, FAILURE_COLOR, shop_bounty_massive


class BuyBounty(commands.Cog):
    def __init__(self, py):
        self.py = py

    async def stopper(self, ctx):
        embed = discord.Embed(title=f'{failure} Руководство {failure}',
                              description='`!bb` `участник` `n` - купить подарок участнику. '
                                          '`n - номер предмета в магазине`', color=FAILURE_COLOR)
        await ctx.reply(embed=embed)


    @commands.command(aliases=['buy-bounty', 'bb', 'купить-подарок', 'кп'])
    async def _buy_bounty(self, ctx, member: discord.Member = None, number: int = None):
        if await check_channels(ctx):
            if (member or number) is None:
                await self.stopper(ctx)
            else:
                massive = shop_bounty_massive()
                if number-1 > len(massive):
                    embed = discord.Embed(title=f'{failure}',
                                          description='Такой позиции в магазине нет!', color=FAILURE_COLOR)
                    await ctx.reply(embed=embed)
                else:
                    search_author = {'id_member': ctx.author.id}
                    search_member = {'id_member': member.id}
                    info_author = await check_fields(ctx.author)
                    if info_author['balance'] >= massive[number-1][2]:
                        info_member = await check_fields(member)
                        DB_GAME.update_one(search_author,
                                           {'$inc': {'balance': -massive[number-1][2]}})
                    else:
                        embed = discord.Embed(title=f'{failure}',
                                              description='У Вас недостаточно средств для покупки!',
                                              color=FAILURE_COLOR)
                        await ctx.reply(embed=embed)



    @_buy_bounty.error
    async def _error_buy(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.reply('Участник не найден!')
        elif isinstance(error, commands.BadArgument):
            await self.stopper(ctx)


def setup(py):
    py.add_cog(BuyBounty(py))
