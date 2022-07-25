import asyncio
import os
import sys
import time
import discord
from discord.ext import commands
from urllib3.packages.six import StringIO

import config.config_b
from DataBase.global_db import DB_GAME
from config import config_b
from config.functional_config import super_admin, accept, failure, money_emj, SUCCESS_COLOR, FAILURE_COLOR, check_channels


class OutputInterceptor(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


class SuperAdminCommands(commands.Cog):
    def __init__(self, py):
        self.py = py

    def restart_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    async def stopper_role(self, ctx):
        embed = discord.Embed(title=f'{failure}',
                              description='Роль не найдена!', color=FAILURE_COLOR)
        await ctx.reply(embed=embed)

    async def stopper_member(self, ctx):
        embed = discord.Embed(title=f'{failure}',
                              description='Такой пользователь либо участник сервера не найден!', color=FAILURE_COLOR)
        await ctx.reply(embed=embed)

    async def stopper_error_not_found(self, ctx, error):
        embed = discord.Embed(title=f'{failure}',
                              description=f'Непредусмотренная ошибка: \n`{error}`', color=FAILURE_COLOR)
        await ctx.reply(embed=embed)

    @commands.command()
    async def restart(self, ctx):
        text = 'Ожидаю выключение бэкэнда'
        msg = await ctx.reply(text)
        config.config_b.run_bot = False
        while config_b.access_run_bot:
            await asyncio.sleep(0.1)
        await msg.edit(f'{text} - выключен.\n'
                       f'Перезагружаюсь.')


        self.restart_program()

    # Просто проверка, работает ли бот.
    @commands.command(aliases=['bot', 'бот'])
    async def _check_bot_work(self, ctx):
        if await check_channels(ctx) or ctx.author.id in super_admin:
            start_time = time.time()
            message = await ctx.message.reply("Да-да, я тута-здеся! Проверяю задержку...")
            end_time = time.time()

            await message.edit(
                content=f"Да-да, я здесь! Проверил задержку - проверяй.\n"
                        f"Задержка:\nDiscord-команда - {round(self.py.latency * 1000)}ms\n"
                        f"Discord-запрос-ответ - {round((end_time - start_time) * 1000)}ms")

    @commands.command(aliases=['fastreboot', 'быстрыйкд', 'кд'])
    async def check_files_bot_fast(self, ctx):
        if ctx.author.id in super_admin:
            zapusk = []
            for DirPath_1, DirName_1, filenames in os.walk("cogs"):
                for filename in filenames:
                    if not filename.endswith('.pyc'):
                        link = ''
                        for simvol in str(os.path.join(DirPath_1, filename)):
                            if simvol == '/':
                                simvol = '.'
                            link += simvol
                        zapusk.append(link)

            text = 'Проверка и перезагрузка файлов:\n'
            msg = await ctx.send(text)
            for file in zapusk:
                text += f'{file} '
                try:
                    self.py.unload_extension(str(file)[:-3])
                    self.py.load_extension(str(file)[:-3])
                    text += f'{accept}\n'
                except Exception as exc:
                    try:
                        self.py.load_extension(str(file)[:-3])
                        text += f'{accept} (перезапущен - {exc})\n'
                    except Exception as exc:
                        text += f'{failure} (не запускается - {exc})\n'
            await msg.edit(text)

    @commands.command(aliases=['check', 'проверка', 'чек'])
    async def check_files_bot(self, ctx):
        if ctx.author.id in super_admin:
            zapusk = []
            for DirPath_1, DirName_1, filenames in os.walk("cogs"):
                for filename in filenames:
                    if not filename.endswith('.pyc'):
                        link = ''
                        for simvol in str(os.path.join(DirPath_1, filename)):
                            if simvol == '/':
                                simvol = '.'
                            link += simvol
                        zapusk.append(link)

            text = 'Проверка файлов:\n'
            msg = await ctx.send(text)
            for file in zapusk:
                text += f'{file} '
                try:
                    self.py.unload_extension(str(file)[:-3])
                    self.py.load_extension(str(file)[:-3])
                    text += f'{accept}\n'
                except Exception as exc:
                    try:
                        self.py.load_extension(str(file)[:-3])
                        text += f'{accept} (перезапущен - {exc})\n'
                    except Exception as exc:
                        text += f'{failure} (не запускается - {exc})\n'
                await msg.edit(text)
            text += '\nКонец.'
            await msg.edit(text)

    @commands.command(aliases=['add-money', 'добавить-денег', 'добавить-баланс', 'add-balance', '+'])
    async def _add_balance(self, ctx, member: discord.User, amount: int):
        if ctx.author.id in super_admin:
            DB_GAME.update_one({'id_member': member.id},
                               {'$inc': {'balance': amount}})
            embed = discord.Embed(title=f'{accept}',
                                  description=f'Участнику `{member.display_name}` начислено {amount} {money_emj}',
                                  color=SUCCESS_COLOR)
            await ctx.send(ctx.author.mention, embed=embed)

    @commands.command(aliases=['reduce-money', 'уменьшить-денег', 'уменьшить-баланс', 'reduce-balance', '-'])
    async def _reduce_balance(self, ctx, member: discord.User, amount: int):
        if ctx.author.id in super_admin:
            DB_GAME.update_one({'id_member': member.id},
                               {'$inc': {'balance': -amount}})
            embed = discord.Embed(title=f'{accept}',
                                  description=f'У участника `{member.display_name}` вычтено {amount} {money_emj}',
                                  color=SUCCESS_COLOR)
            await ctx.send(ctx.author.mention, embed=embed)

    @commands.command(aliases=['reduce-waifu', 'убрать-вайфу'])
    async def _reduce_waifu(self, ctx, member: discord.User, member2: discord.User):
        if ctx.author.id in super_admin:
            search1_player = {'id_member': member}
            search2_player = {'id_member': member2}
            info1 = DB_GAME.find_one(search1_player)
            if member2.id in info1['waifs']:
                DB_GAME.update_one(search1_player,
                                   {'$pull': {'waifs': member2.id}})
                DB_GAME.update_one(search2_player,
                                   {'$set': {'owner': 0}})
                embed = discord.Embed(title=f'{accept}',
                                      description=f'У участника `{member.display_name}` убрана вайфу '
                                                  f'`{member2.display_name}`',
                                      color=SUCCESS_COLOR)
                await ctx.send(ctx.author.mention, embed=embed)
            else:
                embed = discord.Embed(title=f'{failure}',
                                      description=f'У участника `{member.display_name}` нет вайфу '
                                                  f'`{member2.display_name}`',
                                      color=FAILURE_COLOR)
                await ctx.send(ctx.author.mention, embed=embed)

    @commands.command(aliases=['gitgen', 'гитген'])
    async def _git(self, ctx, *, arg2=None):
        if ctx.author.id == 280303417568788482:
            os.system(f'git pull git@github.com:YarSav1/ForMCObot.git > out.txt')

            await ctx.reply(file=discord.File(r'out.txt'))
            os.remove('out.txt')

    @commands.command(aliases=['off', 'выкл'])
    async def _off(self, ctx):
        if ctx.author.id in super_admin:
            text = 'Ожидаю выключение бэкэнда'
            msg = await ctx.reply(text)
            config.config_b.run_bot = False
            while config_b.access_run_bot:
                await asyncio.sleep(0.1)
            await msg.edit(f'{text} - выключен.\n'
                           f'Бот вырублен.')
            await self.py.close()

    @commands.command(aliases=['add-role', 'дать-роль'])
    async def _give_role(self, ctx, member: discord.Member = None, role: discord.Role = None):
        if ctx.author.id in super_admin:
            if (member or role) is None:
                embed = discord.Embed(title=f'{failure} Super-admin',
                                      description=f'`!add-role` `участник` `role` - чтобы выдать роль участнику\n\n'
                                                  f'P.S. - роль будет записана в документ с участником! Роль будет '
                                                  f'считаться купленной в магазине!\n\n'
                                                  f'Команда не работает на вышедших с сервера участниках!')
                await ctx.reply(embed=embed)
            else:
                DB_GAME.update_one({'id_member': member.id},
                                   {'$push': {'buy_roles': role.id}})
                await member.add_roles(role)
                embed = discord.Embed(title=f'{accept} Super-admin',
                                      description=f'Роль {role.mention}({role}) выдана участнику {member.display_name}',
                                      color=SUCCESS_COLOR)
                await ctx.reply(embed=embed)

    @_give_role.error
    async def _error_add_role(self, ctx, error):
        if isinstance(error, commands.RoleNotFound):
            await self.stopper_role(ctx)
        elif isinstance(error, commands.MemberNotFound):
            await self.stopper_member(ctx)
        else:
            await self.stopper_error_not_found(ctx, error)

    @commands.command(aliases=['remove-role', 'удалить-роль'])
    async def _remove_role(self, ctx, member: discord.User = None, role: discord.Role = None):
        if ctx.author.id in super_admin:
            if (member or role) is None:
                embed = discord.Embed(title=f'{failure} Super-admin',
                                      description=f'`!remove-role` `участник` `role` - чтобы убрать роль у участника\n\n'
                                                  f'P.S. - роль будет удалена из документа с участником. '
                                                  f'Если роль была куплена и удалена этой командой - то роль нужно '
                                                  f'будет покупать по новой!\n\n'
                                                  f'Команда работает на **вышедших** с сервера участниках!')
                await ctx.reply(embed=embed)
            else:
                DB_GAME.update_one({'id_member': member.id},
                                   {'$pull': {'buy_roles': role.id}})
                if member in ctx.guild.members:
                    member = ctx.guild.get_member(member.id)
                    await member.remove_roles(role)
                embed = discord.Embed(title=f'{accept} Super-admin',
                                      description=f'Роль {role.mention}({role}) убрана у участника {member}',
                                      color=SUCCESS_COLOR)
                await ctx.reply(embed=embed)

    @_remove_role.error
    async def _error_add_role(self, ctx, error):
        if isinstance(error, commands.RoleNotFound):
            await self.stopper_role(ctx)
        elif isinstance(error, commands.UserNotFound):
            await self.stopper_member(ctx)
        else:
            await self.stopper_error_not_found(ctx, error)

    @commands.command()
    async def _check_backend(self, ctx):
        if ctx.author.id in super_admin:
            if config.config_b.run_backend:
                await ctx.send('Backend launched.')
            else:
                await ctx.send('Backend not running')


def setup(py):
    py.add_cog(SuperAdminCommands(py))
