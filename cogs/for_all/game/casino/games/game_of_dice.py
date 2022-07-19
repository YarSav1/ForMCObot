# 66-90-99
import random

import discord
from discord.ext import commands

from DataBase.global_db import DB_GAME
from config.functional_config import check_channels, failure, FAILURE_COLOR, win_DG_balance_and_place1, \
    win_DG_balance_and_place2, win_DG_balance_and_place3, money_emj, accept, SUCCESS_COLOR, check_fields, lvl_up, \
    exp_from_games, counter_number, GENERAL_COLOR


class GameGD(commands.Cog):
    def __init__(self, py):
        self.py = py

    async def stopper(self, ctx):
        embed = discord.Embed(title=f'{failure} Руководство {failure}',
                              description=f'Пример: !br n - `n - ставка`\n'
                                          f'Игра в кости. \nСистема '
                                          f'**{win_DG_balance_and_place1[1]}**`+{win_DG_balance_and_place1[0]}%`-**{win_DG_balance_and_place2[1]}**`+{win_DG_balance_and_place2[0]}%`-**{win_DG_balance_and_place3[1]}**`+{win_DG_balance_and_place3[0]}%`\n',
                              color=FAILURE_COLOR)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['gd', 'br', 'dice', 'кости'])
    async def _dice(self, ctx, amount: int = None):
        if await check_channels(ctx):
            if amount is None:
                await self.stopper(ctx)
            elif amount <= 0:
                await self.stopper(ctx)
            else:
                search = {'id_member': ctx.author.id}
                info = await check_fields(ctx.author)
                if info['balance'] >= amount:
                    msg = await ctx.reply(embed=discord.Embed(title=f'Подбрасываем кости...', color=GENERAL_COLOR))
                    await lvl_up(ctx.author, random.randint(exp_from_games[0], exp_from_games[1]))
                    dices = ''
                    result = 0
                    for dice in range(10):
                        number = random.randint(1, 10)
                        result += number
                        dices += f'{number} | '
                    dices = dices[:-2]
                    if result > win_DG_balance_and_place1[1]:
                        lose_win_balance = (int((amount / 100) * win_DG_balance_and_place1[0]))-amount
                        text = f'Поздравляю! У Вас выпало `{result}` -> больше `{win_DG_balance_and_place1[1]}`\n' \
                               f'+`{win_DG_balance_and_place1[0]}%` {money_emj} от ставки!\n' \
                               f'Чистыми: {counter_number(lose_win_balance)} {money_emj}'
                    elif result > win_DG_balance_and_place2[1]:
                        lose_win_balance = (int((amount / 100) * win_DG_balance_and_place2[0]))-amount
                        text = f'Поздравляю! У Вас выпало `{result}` -> больше `{win_DG_balance_and_place2[1]}`\n' \
                               f'+`{win_DG_balance_and_place2[0]}%` {money_emj} от ставки!\n' \
                               f'Чистыми: {counter_number(lose_win_balance)} {money_emj}'
                    elif result > win_DG_balance_and_place3[1]:
                        lose_win_balance = (int((amount / 100) * win_DG_balance_and_place3[0]))-amount
                        text = f'Поздравляю! У Вас выпало `{result}` -> больше `{win_DG_balance_and_place3[1]}`\n' \
                               f'+`{win_DG_balance_and_place3[0]}%` {money_emj} от ставки!\n' \
                               f'Чистыми: {counter_number(lose_win_balance)} {money_emj}'
                    else:
                        text = f'К сожалению, у Вас выпало `{result}`\n' \
                               f'-{counter_number(amount)} {money_emj}'
                        lose_win_balance = -amount
                    if lose_win_balance < 0:
                        title = failure
                        color = FAILURE_COLOR
                        DB_GAME.update_one({'id_member': ctx.author.id},
                                           {'$set': {'gd': [info['gd'][0], info['gd'][1] + 1]}})
                    else:
                        title = accept
                        color = SUCCESS_COLOR
                        DB_GAME.update_one({'id_member': ctx.author.id},
                                           {'$set': {'gd': [info['gd'][0] + 1, info['gd'][1]]}})
                    text += f'\n{dices}'

                    DB_GAME.update_one(search,
                                       {'$inc': {'balance': lose_win_balance}})

                    embed = discord.Embed(title=title,
                                          description=text, color=color)
                    await msg.edit(embed=embed)



                else:
                    embed = discord.Embed(title=f'{failure}',
                                          description='У Вас недостаточно средств!', color=FAILURE_COLOR)
                    await ctx.reply(embed=embed)

    @_dice.error
    async def error_game_dice(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await self.stopper(ctx)


def setup(py):
    py.add_cog(GameGD(py))
