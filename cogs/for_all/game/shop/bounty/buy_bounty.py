import discord
from discord.ext import commands

from DataBase.global_db import DB_GAME
from config.functional_config import check_fields, check_channels, failure, FAILURE_COLOR, shop_bounty_massive, accept, \
    SUCCESS_COLOR, GENERAL_COLOR


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
                    embed = discord.Embed(title="Проверка баланса", color=GENERAL_COLOR)
                    msg = await ctx.reply(embed=embed)
                    if info_author['balance'] >= massive[number-1][2]:
                        embed = discord.Embed(title='Производим оплату...', color=SUCCESS_COLOR)
                        await msg.edit(embed=embed)
                        info_member = await check_fields(member)
                        DB_GAME.update_one(search_author,
                                           {'$inc': {'balance': -massive[number-1][2]}})
                        embed = discord.Embed(title='Оплачено!', color=SUCCESS_COLOR)
                        await msg.edit(embed=embed)
                        make = True
                        for pr in info_member['present']:
                            if pr[0] == massive[number-1][0]:
                                make = False
                                DB_GAME.update_one(search_member,
                                                   {'$pull': {
                                                       'present': pr}})
                                DB_GAME.update_one(search_member,
                                                   {'$push': {
                                                       'present': [pr[0], pr[1], pr[2]+1]}})
                        if make:
                            DB_GAME.update_one(search_member,
                                               {'$push': {'present': [massive[number-1][0], massive[number-1][1], 1]}})
                        embed = discord.Embed(title=accept,
                                              description=f'Подарок {massive[number-1][0]} доставлен вайфу {member}',
                                              color=SUCCESS_COLOR)
                        await ctx.reply(embed=embed)
                    else:
                        embed = discord.Embed(title=f'{failure}',
                                              description='У Вас недостаточно средств для покупки!',
                                              color=FAILURE_COLOR)
                        await msg.edit(embed=embed)



    @_buy_bounty.error
    async def _error_buy(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.reply('Участник не найден!')
        elif isinstance(error, commands.BadArgument):
            await self.stopper(ctx)


def setup(py):
    py.add_cog(BuyBounty(py))
