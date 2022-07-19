import asyncio

import discord
from discord.ext import commands

from DataBase.global_db import DB_SERVER_SETTINGS, DB_GAME
from config.functional_config import check_channels, accept, failure, FAILURE_COLOR, GENERAL_COLOR, SUCCESS_COLOR, \
    check_fields, counter_number, money_emj



class buy(commands.Cog):
    def __init__(self, py):
        self.py = py

    async def stopper(self, ctx):
        embed = discord.Embed(title=f'{failure} Руководство {failure}',
                              description=f'`!buy-role` `n` - `n - номер роли в магазине`. Укажите номер '
                                          f'роли в магазине и следуйте дальнейшим подсказкам.',
                              color=GENERAL_COLOR)
        await ctx.reply(embed=embed)

    async def accept_buy(self, ctx, role, buying_role_db):
        DB_GAME.update_one({'id_member': ctx.author.id},
                           {'$inc': {'balance': -int(buying_role_db[1])}})
        DB_GAME.update_one({'id_member': ctx.author.id},
                           {'$push': {'buy_roles': role.id}})
        embed = discord.Embed(title=f'{accept}',
                              description=f'Роль {role.mention}({role}) успешно приобретена!',
                              color=SUCCESS_COLOR)
        await ctx.reply(embed=embed)



    @commands.command(aliases=['buy-role', 'купить-роль'])
    async def _buy_role(self, ctx, number: int = None):
        if await check_channels(ctx):
            if number is None:
                await self.stopper(ctx)
            else:
                massive = DB_SERVER_SETTINGS.find_one({'_id': 'Goodie'})['shop_roles']

                if number-1 > len(massive):
                    embed = discord.Embed(title=f'{failure}',
                                          description=f'Не найдено такой позиции в магазине!',
                                          color=FAILURE_COLOR)
                    await ctx.reply(embed=embed)
                else:
                    role_block = massive[number-1]
                    role = ctx.guild.get_role(role_block[0])
                    info = await check_fields(ctx.author)
                    if role in ctx.author.roles or role.id in info['buy_roles']:
                        if role.id in info['buy_roles']:
                            await ctx.author.add_roles(role)
                        embed = discord.Embed(title=f'{failure}',
                                              description=f'Роль {role.mention}({role}) уже у Вас.',
                                              color=FAILURE_COLOR)
                        await ctx.reply(embed=embed)
                    else:
                        embed = discord.Embed(title=f'Подтверждение выбора',
                                              description=f'Подтвердите, что Вы хотите купить роль {role.mention}({role}) '
                                                          f'за **{counter_number(int(role_block[1]))}** {money_emj}',
                                              color=GENERAL_COLOR)
                        buttons = [
                            [
                                Button(label='Покупаю!', id='buy', style=3),
                                Button(label='Отмена', id='exit', style=4)
                            ]
                        ]

                        msg = await ctx.reply(embed=embed, components=buttons)
                        def check(click_response):
                            if click_response.author == ctx.author:
                                if click_response.channel == ctx.channel:
                                    if click_response.message == msg:
                                        return click_response.author == click_response.author

                        try:
                            click = await self.py.wait_for('button_click', check=check, timeout=30)
                        except asyncio.TimeoutError:
                            return await msg.reply('Время выбора вышло!')
                        if click.component.id == 'buy':
                            try:
                                await ctx.author.add_roles(role)
                            except Exception as exc:
                                embed = discord.Embed(title=f'{failure} Ошибка!',
                                                      description=f'`{exc}`\n\n'
                                                                  f'Попробуйте купить роль снова. В случае повторной неудачи '
                                                                  f'обратитесь к администраторам бота!',
                                                      color=FAILURE_COLOR)
                                return await ctx.reply(embed=embed)
                            await self.accept_buy(ctx, role, role_block)
                        if click.component.id == 'exit':
                            embed = discord.Embed(title='Отмена покупки',
                                                  description='Покупка роли отменена!',
                                                  color=GENERAL_COLOR)
                            await ctx.reply(embed=embed)
                        await click.respond(type=6)

    @_buy_role.error
    async def error_buy_role(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await self.stopper(ctx)
        else:
            await ctx.reply(f'Непредусмотренная ошибка: `{error}`')

def setup(py):
    py.add_cog(buy(py))