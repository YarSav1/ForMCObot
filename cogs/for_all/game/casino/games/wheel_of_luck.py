import random

import discord
from discord.ext import commands

from DataBase.global_db import DB_GAME
from config.functional_config import check_channels, failure, FAILURE_COLOR, wheel_field, check_fields, lvl_up, exp_from_games, \
    SUCCESS_COLOR, accept, money_emj, GENERAL_COLOR


class WheelGame(commands.Cog):
    def __init__(self, py):
        self.py = py

    async def gener_wheel(self, request=None):
        wheel_now = ''
        for field in wheel_field:
            if field is None:
                if request is None:
                    wheel_now += '〚🔄〛 '
                else:
                    wheel_now += f'〚{request}〛 '
            else:
                wheel_now += f'`『{field[0]}%』` '
            if (int(len(wheel_field)) - int(wheel_field.index(field) + 1)) % 3 == 0:
                wheel_now += '\n\n'
        return wheel_now

    async def stopper(self, ctx):
        wheel_now = await self.gener_wheel()
        embed = discord.Embed(title=f'{failure} Руководство {failure}',
                              description=f'Пример: !wheel n - `n - ставка`\n'
                                          f'Колесо удачи. Сделай ставку и надейся на удачу!\n'
                                          f'Сейчас колесо выглядит так:\n'
                                          f'{wheel_now}',
                              color=FAILURE_COLOR)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['wheel', 'колесо'])
    async def _wheel(self, ctx, amount: int = None):
        if await check_channels(ctx):
            if amount is None:
                await self.stopper(ctx)
            elif amount <= 0:
                await self.stopper(ctx)
            else:
                search = {'id_member': ctx.author.id}
                info = await check_fields(ctx.author)
                if info['balance']>=amount:
                    wheel_now = await self.gener_wheel()
                    msg = await ctx.reply(embed=discord.Embed(title=f'Крутим колесо...',
                                                              description=f'{wheel_now}',
                                                              color=GENERAL_COLOR))
                    await lvl_up(ctx.author, random.randint(exp_from_games[0], exp_from_games[1]))
                    while True:
                        result = random.choice(wheel_field)
                        if result is not None:
                            break
                    text = f'Вам выпадает `{result[0]}%`\n\n'
                    wheel_now = await self.gener_wheel(result[1])
                    text+=f'{wheel_now}\n\n'
                    if result[0]>100:
                        DB_GAME.update_one(search,
                                           {'$set': {'wheel': [info['wheel'][0]+1, info['wheel'][1]]}})
                        embed = discord.Embed(title=f'{accept}', color=SUCCESS_COLOR)
                    else:
                        DB_GAME.update_one(search,
                                           {'$set': {'wheel': [info['wheel'][0], info['wheel'][1]+1]}})
                        embed = discord.Embed(title=f'{failure}', color=FAILURE_COLOR)
                    balance_minus_plus = int(((amount / 100) * result[0]) - amount)
                    if balance_minus_plus < 0:
                        text+=f'Итог: '
                    else:
                        text+=f'Итог: +'
                    DB_GAME.update_one(search,
                                       {'$inc': {'balance': balance_minus_plus}})
                    text+=f'{balance_minus_plus} {money_emj}'
                    embed.description = text
                    await msg.edit(embed=embed)



                else:
                    embed = discord.Embed(title=f'{failure}',
                                          description=f'У Вас недостаточно средств!',
                                          color=FAILURE_COLOR)
                    await ctx.reply(embed=embed)

    @_wheel.error
    async def _error_game_wheel(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await self.stopper(ctx)
        else:
            await ctx.reply(error)

def setup(py):
    py.add_cog(WheelGame(py))
