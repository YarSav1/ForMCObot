import asyncio
import random

import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands

from DataBase.global_db import DB_GAME
from config.functional_config import check_channels, GENERAL_COLOR, failure, FAILURE_COLOR, form_send, payload, accept, \
    SUCCESS_COLOR, check_fields, HEADERS


class go_or_no(discord.ui.View):
    def __init__(self, *, py, timeout=30, ctx):
        self.py = py
        self.ctx = ctx
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Поехали!", style=discord.ButtonStyle.green)
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user == self.ctx.author:
            await interaction.response.edit_message(view=self)
            await ConnectDiscordForMinecraft(self.py).next_stage_nick(self.ctx)

    @discord.ui.button(label="Отмена", style=discord.ButtonStyle.red)
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user == self.ctx.author:
            await interaction.response.edit_message(view=self)
            title = f'{failure} Отмена {failure}'
            description = 'Вы отказались от связки "Дискорд-Майнкрафт".'
            await self.ctx.reply(embed=await ConnectDiscordForMinecraft(self.py).pucker(title, description,
                                                                                        FAILURE_COLOR))


class success_or_no(discord.ui.View):
    def __init__(self, *, py, timeout=30, ctx, nick):
        self.py = py
        self.ctx = ctx
        self.nick = nick
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Верно!", style=discord.ButtonStyle.green)
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user == self.ctx.author:
            await interaction.response.edit_message(view=self)
            title, description = f'{accept} Завершение {accept}', 'Произвожу связку.'
            await self.ctx.reply(embed=await ConnectDiscordForMinecraft(self.py).pucker(title, description,
                                                                                        SUCCESS_COLOR))
            DB_GAME.update_one({'id_member': self.ctx.author.id},
                               {'$set': {'ds-minecraft': [self.ctx.author.id, self.nick]}})
            title, description = f'{accept}', f'Аккаунты {self.ctx.author}-`{self.nick}` связаны!'
            await self.ctx.reply(embed=await ConnectDiscordForMinecraft(self.py).pucker(title, description,
                                                                                        SUCCESS_COLOR))

    @discord.ui.button(label="Не верно", style=discord.ButtonStyle.red)
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user == self.ctx.author:
            await interaction.response.edit_message(view=self)
            title = f'{failure} Отмена {failure}'
            description = 'Вы отказались от связки "Дискорд-Майнкрафт".'
            await self.ctx.reply(embed=await ConnectDiscordForMinecraft(self.py).pucker(title, description,
                                                                                        FAILURE_COLOR))


class ConnectDiscordForMinecraft(commands.Cog):
    def __init__(self, py):
        self.py = py

    async def pucker(self, title, description, color):
        embed = discord.Embed(title=title, description=description, color=color)
        return embed

    @commands.command(aliases=['auth-ds-minecraft'])
    async def __auth(self, ctx):
        if await check_channels(ctx):
            info = await check_fields(ctx.author)
            if len(info['ds-minecraft']) != 0:
                title, description = f'{failure}', f'У Вас уже привязан аккаунт!\n' \
                                                   f'{ctx.author}+`{info["ds-minecraft"][1]}`\n\n' \
                                                   f'Хотите отвязать? - Обратитесь к администраторам бота.'
                await ctx.reply(embed=await self.pucker(title, description, FAILURE_COLOR))
            else:
                title = 'Начало'
                description = "Процедура \"Дискорд-Майнкрафт\"\n" \
                              "Эта команда свяжет Ваш аккаунт в майнкрафте с аккаунтом дискорда.\n" \
                              "Станут доступны задачи для заработка внутриигровой валюты!\n\n" \
                              "P.S. - процедура действует до первой ошибки. Ошиблись - начинайте заново.\n" \
                              "P.S.2 - в связи с тем, что на форуме можно отправлять сообщение только раз в минуту - " \
                              "данная ошибка откатит Вас к самому началу. Извините за неудобства.\n\n" \
                              "**Продолжаем?**"

                await ctx.reply(embed=await self.pucker(title, description, GENERAL_COLOR),
                                view=go_or_no(py=self.py, ctx=ctx))

    async def next_stage_nick(self, ctx):
        title = '1 стадия.'
        description = 'И так, приступим.\n' \
                      'Напишите свой **ник**, точный, с учетом всех регистров, без аргументов, ' \
                      'без использования команд. Просто **ник**!\n\n' \
                      'P.S. - В противном случае будет взято первое слово из сообщения. Форматирование текста от ' \
                      'дискорда никак не помешает! Знаки форматирования использовать не нужно!'
        await ctx.reply(embed=await self.pucker(title, description, GENERAL_COLOR))

        def check(msg_response):
            if msg_response.author == ctx.author:
                if msg_response.channel == ctx.channel:
                    return msg_response.author == msg_response.author

        try:
            msg_nick = await self.py.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            return
        nick = msg_nick.content.split()[0]
        all_auth_nicks = []
        for player in list(DB_GAME.find()):
            try:
                all_auth_nicks.append(player['ds-minecraft'][1])
            except:
                pass
        if str(nick) in all_auth_nicks:
            title, description = f'{failure}', f'Этот ник уже привязан к другому дискорд участнику!'
            await msg_nick.reply(embed=await self.pucker(title, description, FAILURE_COLOR))
        else:
            await self.next_stage_forum(ctx, nick, msg_nick)

    async def next_stage_forum(self, ctx, nick, msg_nick):
        title = '2 стадия.'

        def dsn(desc2):
            description = 'Вам **нужно** зайти на форум проекта в личные сообщения!\n' \
                          'Вам придет код, который Я буду ждать от Вас, как только что ожидал ник!\n' \
                          'Т.е. просто отправьте голое сообщение с кодом.\n\n' \
                          'P.S. - Если Вы доверяете разработчику, то просто перейдите по ссылке **->** [клик](' \
                          f'https://minecraftonly.ru/forum/private.php) **<-** :){desc2}'
            return description

        description = dsn('\n\n'
                          '**Отправляю сообщение...**')
        stage_2 = await msg_nick.reply(embed=await self.pucker(title, description, GENERAL_COLOR))
        url = 'https://minecraftonly.ru/forum/private.php?do=newpm'

        ver_code = ''
        for i in range(8):
            ver_code += str(random.randint(0, 9))

        with requests.Session() as s:
            p = s.post('https://minecraftonly.ru/', headers=HEADERS, data=payload)
            html = s.get(url, headers=HEADERS, params=None)
            if html.status_code == 200:

                p = 0
                while True:
                    soup = BeautifulSoup(html.content, 'html.parser')
                    try:
                        tkn = soup.find('input', {'name': 'securitytoken'})['value']
                        break
                    except Exception:
                        p+=1
                        if p == 5:
                            description = dsn('\n\n'
                                              f'**Я не смог отправить сообщение. Попробуйте позже.**')
                            await stage_2.edit(embed=await self.pucker(title, description, GENERAL_COLOR))
                        else:
                            description = dsn('\n\n'
                                              f'**Возникли проблемы с отправкой. Все еще пробую. ({p})**')
                            await stage_2.edit(embed=await self.pucker(title, description, GENERAL_COLOR))

                    html = s.get(url, headers=HEADERS, params=None)
                    await asyncio.sleep(3)

                form = form_send(tkn, str(nick), ver_code)
                a = s.post('https://minecraftonly.ru/forum/private.php?do=insertpm&pmid=', data=form)
                if 'Следующие пользователи не найдены:' in a.text:
                    title = f'{failure} ОШИБКА'
                    description = 'Игрок с таким ником не найден!\n' \
                                  'Процесс связки отменен! Начинайте заново.'
                    await msg_nick.reply(embed=await self.pucker(title, description, FAILURE_COLOR))
                elif '<li>Приносим вам свои извинения, но у нас на сайте пользователи могут отправлять личное сообщение не чаще, чем раз в 60 секунд' in a.text:
                    title = f'{failure} ОШИБКА {failure}'
                    description = 'Извините, но на форуме можно отправлять сообщение лишь раз в минуту.\n' \
                                  'Попробуйте пройти связку заново.'
                    await msg_nick.reply(embed=await self.pucker(title, description, FAILURE_COLOR))
                else:
                    description = dsn('\n\n'
                                      '**Сообщение отправлено! Жду код!!!**')
                    await stage_2.edit(embed=await self.pucker(title, description, GENERAL_COLOR))

        def check(msg_response):
            if msg_response.author == ctx.author:
                if msg_response.channel == ctx.channel:
                    return msg_response.author == msg_response.author

        try:
            msg_code = await self.py.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            return
        code = msg_code.content.split()[0]
        if str(code) == str(ver_code):
            await self.ds_minecraft_end(ctx, nick, msg_code)
        else:
            title, description = f'{failure} ОШИБКА {failure}', f'Введенный Вами код не совпадает с тем, что был ' \
                                                                f'отправлен.\n' \
                                                                f'Связка отменена, начинайте заново.'
            await msg_code.reply(embed=await self.pucker(title, description, FAILURE_COLOR))

    async def ds_minecraft_end(self, ctx, nick, msg_code):
        title = '3 стадия'
        description = 'И так... Вот и конец.\n\n' \
                      f'Ваш аккаунт майнкрафт: `{nick}`\n' \
                      f'Ваш аккаунт дискорд: {ctx.author}\n\n' \
                      f'Будет произведена связка {ctx.author}+`{nick}` - всё верно?'

        await msg_code.reply(embed=await self.pucker(title, description, GENERAL_COLOR), view=success_or_no(py=self.py,
                                                                                                            ctx=ctx,
                                                                                                            nick=nick))


def setup(py):
    py.add_cog(ConnectDiscordForMinecraft(py))
