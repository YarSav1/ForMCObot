import discord
from discord.ext import commands

from DataBase.global_db import DB_GAME
from config.functional_config import check_channels, check_fields, GENERAL_COLOR, failure, FAILURE_COLOR, money_emj, lvl_emj, \
    exp_emj, lvl_up, accept, get_balancetop, get_lvltop, SUCCESS_COLOR, counter_number


class Profile(commands.Cog):
    def __init__(self, py):
        self.py = py

    async def pucker(self, ctx, info, number_balance=None, number_lvl=None):
        embed = discord.Embed(title=f'Профиль {ctx.display_name} - {info["status"]}', color=GENERAL_COLOR)

        embed.add_field(name='Баланс:', value=f'{counter_number(info["balance"])} {money_emj}', inline=True)

        needed_exp = await lvl_up(ctx, None, 1)
        embed.add_field(name=f'Уровень: **{counter_number(info["lvl"])}** {lvl_emj}',
                        value=f'Опыт: **{counter_number(info["exp"])}**/{counter_number(needed_exp)} {exp_emj}',
                        inline=True)
        if (number_balance and number_lvl) is None:
            embed.add_field(name='Топы:', value=f'<<<<<<<Высчитывается>>>>>>>', inline=False)
        else:
            embed.add_field(name='Топы:', value=f'Баланс: **{counter_number(number_balance)}** место | '
                                                f'Уровень: **{counter_number(number_lvl)}** место',
                            inline=False)

        embed.add_field(name='Выигрыши/Проигрыши', value=f'Орёл и Решка - {counter_number(info["et"][0])}/{counter_number(info["et"][1])}\n'
                                                         f'Кости - {counter_number(info["gd"][0])}/{counter_number(info["gd"][1])}\n'
                                                         f'Слоты - {counter_number(info["slots"][0])}/{counter_number(info["slots"][1])}\n'
                                                         f'Колесо удачи - {counter_number(info["wheel"][0])}/{counter_number(info["wheel"][1])}',
                        inline=False)

        return embed

    @commands.command(aliases=['profile', 'профиль'])
    async def _profile(self, ctx, member: discord.Member = None):
        if await check_channels(ctx):
            if member is None:
                check_member = ctx.author
            else:
                check_member = member
            info = await check_fields(check_member)

            msg = await ctx.reply(embed=await self.pucker(check_member, info, None, None))

            number_balance = await get_balancetop(1, info)
            number_lvl = await get_lvltop(1, info)
            await msg.edit(
                embed=await self.pucker(check_member, info, number_balance, number_lvl))

    @_profile.error
    async def error_profile(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(title=f'{failure}',
                                  description='Такого игрока не найдено!', color=FAILURE_COLOR)
            await ctx.reply(embed=embed)

    @commands.command(aliases=['balance', 'баланс'])
    async def _balance(self, ctx):
        if await check_channels(ctx):
            info = await check_fields(ctx.author)
            embed = discord.Embed(title=f'{accept}',
                                  description=f'Ваш баланс: **{counter_number(info["balance"])}** {money_emj}',
                                  color=GENERAL_COLOR)
            await ctx.reply(embed=embed)

    async def stopper(self, ctx):
        embed = discord.Embed(title=f'{failure} Руководство {failure}',
                              description='`!передать` `участник` `n` - `n - сумма перевода`',
                              color=FAILURE_COLOR)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['give', 'передать', 'дать', 'перевести'])
    async def _give_balance(self, ctx, member: discord.Member, amount: int = None):
        if await check_channels(ctx):

            if amount is None or amount <= 0:
                await self.stopper(ctx)
            else:
                info = await check_fields(ctx.author)
                if info['balance'] >= amount:
                    DB_GAME.update_one({'id_member': member.id},
                                       {'$inc': {'balance': amount}})
                    DB_GAME.update_one({'id_member': ctx.author.id},
                                       {'$inc': {'balance': -amount}})
                    embed = discord.Embed(title=f'{accept}',
                                          description=f'Вы передали участнику {member.display_name} '
                                                      f'**{counter_number(amount)}** {money_emj}',
                                          color=SUCCESS_COLOR)
                    await ctx.reply(embed=embed)
                else:
                    embed = discord.Embed(title=f'{failure}',
                                          description='У Вас недостаточно баланса!',
                                          color=FAILURE_COLOR)
                    await ctx.reply(embed=embed)

    @_give_balance.error
    async def _error_give(self, ctx, error):

        if isinstance(error, commands.MemberNotFound):
            await ctx.reply('Участник не найден!')
        elif isinstance(error, commands.BadArgument):
            await self.stopper(ctx)


def setup(py):
    py.add_cog(Profile(py))
