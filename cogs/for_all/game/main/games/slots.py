import random

import discord
from discord.ext import commands

from DataBase.global_db import DB_GAME
from config.functional_config import failure, slots_emj, FAILURE_COLOR, slots_factor, check_channels, check_fields, \
    slots_column, win_slots, slot_shuffle, money_emj, accept, SUCCESS_COLOR, lvl_up, exp_from_games, GENERAL_COLOR


class SlotsGame(commands.Cog):
    def __init__(self, py):
        self.py = py

    async def stopper(self, ctx):
        embed = discord.Embed(title=f'{failure} Руководство {failure}',
                              description=f'Пример: !slot n - `n - ставка`\n'
                                          f'Игра в слоты. Победный слот - {slots_emj[len(slots_emj) - 1]}\n'
                                          f'Множитель победного слота - `{slots_factor}%`',
                              color=FAILURE_COLOR)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['slot', 'slots', 'слот', 'слоты'])
    async def _slots(self, ctx, amount: int = None):
        if await check_channels(ctx):
            if amount is None:
                await self.stopper(ctx)
            elif amount <= 0:
                await self.stopper(ctx)

            else:
                search = {'id_member': ctx.author.id}
                info = await check_fields(ctx.author)
                if info['balance'] >= amount:
                    msg = await ctx.reply(embed=discord.Embed(title=f'Крутим слоты...', color=GENERAL_COLOR))
                    await lvl_up(ctx.author, random.randint(exp_from_games[0], exp_from_games[1]))
                    if win_slots is False:
                        win_ch = int((100 / len(slots_emj)) + (100 % (len(slots_emj))))
                        lose_ch = 100 - win_ch

                        chance_win = ['win'] * win_ch + ['lose'] * lose_ch
                    else:
                        chance_win = ['win'] * win_slots + ['lose'] * (100 - win_slots)
                    for slots_sh in range(slot_shuffle):
                        random.shuffle(chance_win)
                    result = ''
                    factor_prize = 0
                    for column in range(slots_column):
                        result_chance = random.choice(chance_win)
                        if result_chance == 'win':
                            factor_prize += 1
                            result += f'{slots_emj[len(slots_emj) - 1]} | '

                        else:
                            result += f'{random.choice(slots_emj[:-1])} | '

                    result = result[:-2]
                    if factor_prize != 0:
                        plus_minus_balance = int(((amount / 100) * (factor_prize * slots_factor))-amount)
                        result += f'\n\nИтог: +{plus_minus_balance} {money_emj}'
                        DB_GAME.update_one(search,
                                           {'$set': {'slots': [info['slots'][0] + 1, info['slots'][1]]}})
                        embed = discord.Embed(title=f'{accept}', color=SUCCESS_COLOR)
                    else:
                        plus_minus_balance = -amount
                        result += f'\n\nИтог: {plus_minus_balance} {money_emj}'
                        DB_GAME.update_one(search,
                                           {'$set': {'slots': [info['slots'][0], info['slots'][1] + 1]}})
                        embed = discord.Embed(title=f'{failure}', color=FAILURE_COLOR)
                    result = f'Выпало **{factor_prize}шт** - {slots_emj[len(slots_emj) - 1]} !\n\n' + result
                    embed.description = result
                    DB_GAME.update_one(search,
                                       {'$inc': {'balance': plus_minus_balance}})

                    await msg.edit(embed=embed)

                else:
                    embed = discord.Embed(title=f'{failure}',
                                          description=f'У Вас недостаточно средств!',
                                          color=FAILURE_COLOR)
                    await ctx.reply(embed=embed)

    @_slots.error
    async def error_slots(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await self.stopper(ctx)


def setup(py):
    py.add_cog(SlotsGame(py))
