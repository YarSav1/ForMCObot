import random

import discord
from discord.ext import commands

from DataBase.global_db import DB_GAME
from config.functional_config import check_channels, failure, FAILURE_COLOR, win_ET, ET_shuffle, win_ET_balance, accept, \
    money_emj, SUCCESS_COLOR, check_fields, lvl_up, exp_from_games, counter_number, GENERAL_COLOR


class GameET(commands.Cog):
    def __init__(self, py):
        self.py = py

    async def stopper(self, ctx):
        embed = discord.Embed(title=f'{failure} Руководство {failure}',
                              description=f'Пример: !ор h/t n - `h - орел`, `t - решка`, `n - ставка`\n'
                                          f'Игра "Орёл и Решка" - угадай, какой стороной выпадет монета!\n'
                                          f'За выигрыш - `+{win_ET_balance}%`',
                              color=FAILURE_COLOR)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['et', 'bf', 'ор', 'орелрешка', 'орел-решка', 'орёл-решка', 'op'])
    async def _et(self, ctx, eort: str = None, amount: int = None):
        if await check_channels(ctx):

            if (eort and amount) is None:
                await self.stopper(ctx)
            elif amount <= 0:
                await self.stopper(ctx)
            else:
                info_author = await check_fields(ctx.author)
                if info_author['balance'] < amount:
                    embed = discord.Embed(title=f'{failure}',
                                          description='У Вас недостаточно средств!',
                                          color=FAILURE_COLOR)
                    await ctx.reply(embed=embed)
                else:
                    msg = await ctx.reply(embed=discord.Embed(title=f'Подкидываем монетку...', color=GENERAL_COLOR))
                    if eort.lower() in ['h', 'e', 'орел', 'орёл', 'eagle']:  # Орел
                        choice = 1
                        choice_name_win = 'Орёл'
                        choice_name_lose = 'Решка'
                    elif eort.lower() in ['t', 'решка', 'tail', 'tails']:  # Решка
                        choice = 2
                        choice_name_win = 'Решка'
                        choice_name_lose = 'Орёл'
                    else:
                        embed = discord.Embed(title=f'{failure} Руководство {failure}',
                                              description='Пример: !ор h/t n - `h - орел`, `t - решка`, `n - ставка`',
                                              color=FAILURE_COLOR)
                        return await ctx.reply(embed=embed)
                    await lvl_up(ctx.author, random.randint(exp_from_games[0], exp_from_games[1]))
                    lose = 100 - win_ET
                    all_chance = []
                    if choice == 1:
                        all_chance += [2] * lose
                        all_chance += [1] * win_ET
                    if choice == 2:
                        all_chance += [1] * lose
                        all_chance += [2] * win_ET
                    for stage_shuffle in range(ET_shuffle):
                        random.shuffle(all_chance)

                    result = random.choice(all_chance)

                    if result == choice:

                        win_balance = int(((amount / 100) * win_ET_balance))
                        DB_GAME.update_one({'id_member': ctx.author.id},
                                           {'$inc': {'balance': win_balance}})
                        DB_GAME.update_one({'id_member': ctx.author.id},
                                           {'$set': {'et': [info_author['et'][0] + 1, info_author['et'][1]]}})
                        embed = discord.Embed(title=f'{accept}',
                                              description=f'Ваш выбор: **{choice_name_win}**\n'
                                                          f'Выпала: **{choice_name_win}**\n'
                                                          f'Вы угадали! \n'
                                                          f'Ваш выигрыш - **{counter_number(win_balance + amount)}** {money_emj} | '
                                                          f'Чистыми - **{counter_number(win_balance)}** {money_emj}',
                                              color=SUCCESS_COLOR)
                        await msg.edit(embed=embed)


                    else:
                        DB_GAME.update_one({'id_member': ctx.author.id},
                                           {'$inc': {'balance': -amount}})
                        DB_GAME.update_one({'id_member': ctx.author.id},
                                           {'$set': {'et': [info_author['et'][0], info_author['et'][1] + 1]}})
                        embed = discord.Embed(title=f'{failure}',
                                              description=f'Ваш выбор: **{choice_name_win}**\n'
                                                          f'Выпало: **{choice_name_lose}**\n'
                                                          f'К сожалению, Вы не угадали! Повезет в следующий раз!\n'
                                                          f'Итог: -**{counter_number(amount)}** {money_emj}',
                                              color=FAILURE_COLOR)
                        await msg.edit(embed=embed)

    @_et.error
    async def error_game_et(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await self.stopper(ctx)


def setup(py):
    py.add_cog(GameET(py))
