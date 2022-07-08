import discord
from discord.ext import commands

from DataBase.global_db import DB_GAME
from config.functional import check_channels, check_fields, GENERAL_COLOR, money_emj, failure, FAILURE_COLOR, accept, \
    SUCCESS_COLOR, remove_waifu_and_get_balance, buy_waifu_and_get_balance, counter_number


class MainWaifu(commands.Cog):
    def __init__(self, py):
        self.py = py

    @commands.Cog.listener()
    async def on_ready(self):
        pass



    async def pucker(self, info, author, ctx):
        embed = discord.Embed(title=f'{author.display_name} - {info["status"]}', color=GENERAL_COLOR)

        embed.add_field(name=f'Баланс:', value=f'{counter_number(info["balance"])} {money_emj}',
                        inline=True)

        player = ctx.guild.get_member(info['like'])
        if player is None:
            player = 'Никто'
        embed.add_field(name=f'Нравится', value=f'{player}', inline=True)

        player = ctx.guild.get_member(info['owner'])
        if info['owner'] != 0 and player is None:
            DB_GAME.update_one({'id_member': author.id},
                               {'$set': {'owner': 0}})
            DB_GAME.update_one({'id_member': info['owner']},
                               {'$pull': {'waifs': author.id}})
        if player is None:
            player = 'Свободно'
        else:
            player = player.display_name
        embed.add_field(name=f'Является вайфу:', value=f'{player}', inline=True)
        waifs_text = ''
        for i in info['waifs']:
            waifu = ctx.guild.get_member(i)
            if waifu is None:
                waifs_text += f'`{i}` - покинул сервер.\n'
            else:
                waifs_text += f'{waifu.display_name}\n'
            if info['waifs'].index(i) == 4:
                waifs_text += f'и т.д.\n'
                # info_member = DB_GAME.find_one({'id_member': i})['price']
                # returned = int((info_member['price'] / 100) * remove_waifu_and_get_balance)
                # DB_GAME.update_one({'id_member': author.id},
                #                    {'$inc': {'balance': returned}})
                # DB_GAME.update_one({'id_member': i},
                #                    {'$set': {'owner': 0}})

        if waifs_text == '':
            waifs_text = 'Список пуст.'
        embed.add_field(name=f'Список вайфу - Кол-во: {counter_number(len(info["waifs"]))}', value=f'{waifs_text}',
                        inline=False)
        present_text = ''
        for i in info['present']:
            present_text += f'{i[0]} x{counter_number([i[1]])}\n'
        if present_text == '':
            present_text = 'Подарков нет.'
        embed.add_field(name=f'Список подарков:', value=f'{present_text}', inline=True)
        embed.add_field(name=f'Стоимость:*', value=f'{counter_number(info["price"])} {money_emj}', inline=True)
        embed.set_footer(text=f'* - для покупки нужно ввести сумму больше стоимости вайфу!')
        return embed

    @commands.command(aliases=['вайфу', 'вайфы', 'waifu', 'waifs'])
    async def _waifu(self, ctx, member: discord.Member = None, amount: int = None):
        if await check_channels(ctx):
            author = ctx.author
            if member is None:  # info about me

                info = await check_fields(author)
                await ctx.reply(embed=await self.pucker(info, author, ctx))
            elif amount is None:  # info about member
                info = await check_fields(member)
                await ctx.reply(embed=await self.pucker(info, member, ctx))
            else:  # buy waifu
                if amount <= 0:
                    embed = discord.Embed(title=f'{failure}',
                                          description=f'Сумма покупки должна быть больше 0 !', color=FAILURE_COLOR)
                    return await ctx.reply(embed=embed)
                author = ctx.author
                info_author = await check_fields(author)
                if member.id in info_author['waifs']:
                    embed = discord.Embed(title=f'{failure}',
                                          description=f'Эта вайфу уже Ваша!', color=FAILURE_COLOR)
                    return await ctx.reply(embed=embed)
                if info_author['balance'] >= amount:
                    info_member = await check_fields(member)

                    search_author = {'id_member': author.id}
                    search_owner = {'id_member': info_member['owner']}
                    search_member = {'id_member': member.id}

                    price_member = info_member['price']
                    if amount >= price_member+1:
                        embed = discord.Embed(title=f'{accept}',
                                              description=f'Осуществяется перевод денег в размере {counter_number(amount)} {money_emj}',
                                              color=SUCCESS_COLOR)
                        edit_msg = await ctx.reply(embed=embed)
                        DB_GAME.update_one(search_author,
                                           {'$inc': {'balance': -amount}})
                        recovery_member = int((price_member/100)*buy_waifu_and_get_balance)
                        embed = discord.Embed(title=f'{accept}',
                                              description=f'Осуществяется возврат бывшему владельцу в размере '
                                                          f'{counter_number(recovery_member)}`({buy_waifu_and_get_balance}%)` {money_emj}',
                                              color=SUCCESS_COLOR)
                        await edit_msg.edit(embed=embed)
                        DB_GAME.update_one(search_owner,
                                           {'$inc': {'balance': recovery_member}})

                        embed = discord.Embed(title=f'{accept}',
                                              description=f'Осуществляется передача вайфу.',
                                              color=SUCCESS_COLOR)
                        await edit_msg.edit(embed=embed)
                        DB_GAME.update_one(search_author,
                                           {'$push': {'waifs': member.id}})
                        DB_GAME.update_one(search_owner,
                                           {'$pull': {'waifs': member.id}})
                        DB_GAME.update_one(search_member,
                                           {'$set': {'owner': author.id}})
                        DB_GAME.update_one(search_member,
                                           {'$set': {'price': amount}})

                        embed = discord.Embed(title=f'{accept}',
                                              description=f'Вайфу `{member.display_name}` теперь Ваша!',
                                              color=SUCCESS_COLOR)
                        await edit_msg.edit(embed=embed)

                    else:
                        need = (price_member+1)-amount
                        embed = discord.Embed(title=f'{failure}',
                                              description=f'Вайфу `{member.display_name}` стоит {counter_number(price_member)} {money_emj}\n'
                                                          f'Вам не хватает {counter_number(need)} {money_emj}', color=FAILURE_COLOR)
                        embed.set_footer(text=f'P.S. - для покупки нужно ввести сумму больше стоимости вайфу!')
                        await ctx.reply(embed=embed)
                else:
                    embed = discord.Embed(title=f'{failure}',
                                          description=f'У Вас на руках недостаточно средств для покупки!',
                                          color=FAILURE_COLOR)
                    await ctx.reply(embed=embed)

    @_waifu.error
    async def error_waifu(self, ctx, error):
        if isinstance(error, commands.MemberNotFound) or isinstance(error, commands.UserNotFound):
            await ctx.reply('Игрок не найден')
        elif isinstance(error, commands.BadArgument):
            if 'converting' and 'failed' in str(error).lower():
                await ctx.reply('Введите **целое** число для покупки!')

    @commands.command(aliases=['list-waifu','список-вайфу'])
    async def all_list_waifu(self, ctx, member: discord.Member = None):
        if await check_channels(ctx):
            if member is None:
                check = ctx.author
            else:
                check = member
            info = await check_fields(check)
            waifs_text = ''
            for i in info['waifs']:
                waifu = ctx.guild.get_member(i)
                if waifu is None:
                    waifs_text += f'`{i}` - покинул сервер.\n'
                else:
                    waifs_text += f'{waifu.display_name}, '
            if waifs_text == '':
                waifs_text = 'Список пуст.'
            embed = discord.Embed(title=f'Список вайфу {check.display_name}',
                                  description=waifs_text, color=GENERAL_COLOR)
            await ctx.reply(embed=embed)

    @all_list_waifu.error
    async def error_list_waifu(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.reply('Участник не найден!')


def setup(py):
    py.add_cog(MainWaifu(py))
