import discord
from discord.ext import commands

from DataBase.global_db import DB_GAME
from config.functional import check_channels, failure, FAILURE_COLOR, remove_waifu_and_get_balance, GENERAL_COLOR, \
    accept, money_emj, SUCCESS_COLOR, counter_number


class RemoveWaifu(commands.Cog):
    def __init__(self, py):
        self.py = py

    @commands.command(aliases=['refuse-waifu', 'отказаться-вайфу'])
    async def _remove_waifu(self, ctx, member: discord.User = None):
        if await check_channels(ctx):
            if member is None:
                embed = discord.Embed(title='Руководство',
                                      description=f'Добровольный отказ от вайфу. Процент возврата средств регулируется '
                                                  f'вышестоящими, сейчас это - `{remove_waifu_and_get_balance}%` '
                                                  f'от стоимости',
                                      color=GENERAL_COLOR)
                await ctx.reply(embed=embed)
            else:
                search_author = {'id_member': ctx.author.id}
                info_author = DB_GAME.find_one(search_author)
                if member.id in info_author['waifs']:
                    search_member = {'id_member': member.id}
                    info_member = DB_GAME.find_one(search_member)
                    returned = counter_number(int((info_member['price'] / 100) * remove_waifu_and_get_balance))
                    embed = discord.Embed(title=f'{accept}', description=f'Производится возврат в размере {returned} '
                                                                         f'{money_emj}'
                                                                         f'`({remove_waifu_and_get_balance}%)`',
                                          color=SUCCESS_COLOR)
                    msg = await ctx.reply(embed=embed)
                    DB_GAME.update_one(search_author,
                                       {'$inc': {'balance': returned}})

                    embed = discord.Embed(title=f'{accept}', description=f'Осуществляется удаление вайфу.',
                                          color=SUCCESS_COLOR)
                    await msg.edit(embed=embed)
                    DB_GAME.update_one(search_author,
                                       {'$pull': {'waifs': member.id}})
                    DB_GAME.update_one(search_member,
                                       {'$set': {'owner': 0}})

                    embed = discord.Embed(title=f'{accept}',
                                          description=f'`{member.display_name}` больше не Ваша вайфу!.',
                                          color=SUCCESS_COLOR)
                    await msg.edit(embed=embed)
                else:
                    embed = discord.Embed(title=f'{failure}',
                                          description='Это не ваша вайфу!', color=FAILURE_COLOR)
                    await ctx.reply(embed=embed)

    @_remove_waifu.error
    async def _error_remove_waifu(self, ctx, error):
        if isinstance(error, commands.MemberNotFound) or isinstance(error, commands.UserNotFound):
            await ctx.reply('Игрок не найден')


def setup(py):
    py.add_cog(RemoveWaifu(py))
