import datetime

import discord
from discord.ext import commands

from DataBase.global_db import ONLINE, DB_GAME
from config.functional_config import check_channels, check_fields, failure, FAILURE_COLOR, left_page, right_page, \
    SUCCESS_COLOR, GENERAL_COLOR


class left_no(discord.ui.View):
    def __init__(self, *, py=None, timeout=60, server, doc, list_now, msg):
        super().__init__(timeout=timeout)
        self.server = server
        self.doc = doc
        self.list_now = list_now
        self.msg = msg

    @discord.ui.button(label=left_page, style=discord.ButtonStyle.red, disabled=True)
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label=right_page, style=discord.ButtonStyle.green)
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.list_now += 1
        await get_online(self.server, self.doc, self.list_now, self.msg)

    async def on_timeout(self):
        for btn in self.children:
            btn.disabled = True


class right_no(discord.ui.View):
    def __init__(self, *, py=None, timeout=60, server, doc, list_now, msg):
        super().__init__(timeout=timeout)
        self.server = server
        self.doc = doc
        self.list_now = list_now
        self.msg = msg

    @discord.ui.button(label=left_page, style=discord.ButtonStyle.green)
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.list_now -= 1
        await get_online(self.server, self.doc, self.list_now, self.msg)

    @discord.ui.button(label=right_page, style=discord.ButtonStyle.red)
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction, disabled=True):
        await interaction.response.edit_message(view=self)

    async def on_timeout(self):
        for btn in self.children:
            btn.disabled = True


# class stop(discord.ui.View):
#     def __init__(self, *, py, timeout=60):
#         super().__init__(timeout=timeout)
#
#     @discord.ui.button(label=left_page, style=discord.ButtonStyle.red, disabled=True)
#     async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
#         pass
#
#     @discord.ui.button(label=right_page, style=discord.ButtonStyle.red)
#     async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
#         pass
#
#     async def on_timeout(self):
#         for btn in self.children:
#             btn.disabled = True


class right_and_left(discord.ui.View):
    def __init__(self, *, py=None, timeout=60, server, doc, list_now, msg):
        super().__init__(timeout=timeout)
        self.server = server
        self.doc = doc
        self.list_now = list_now
        self.msg = msg

    @discord.ui.button(label=left_page, style=discord.ButtonStyle.green)
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.list_now -= 1
        await get_online(self.server, self.doc, self.list_now, self.msg)

    @discord.ui.button(label=right_page, style=discord.ButtonStyle.green)
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.list_now += 1
        await get_online(self.server, self.doc, self.list_now, self.msg)

    async def on_timeout(self):
        for btn in self.children:
            btn.disabled = True


class Select(discord.ui.Select):
    def __init__(self, servers, ctx):
        self.servers = servers
        self.ctx = ctx
        options = []
        for i in self.servers:
            options.append(discord.SelectOption(label=i['server_name']))
        super().__init__(placeholder="Выберите сервер", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        server = self.values[0]
        nick = DB_GAME.find_one({'id_member': self.ctx.author.id})['ds-minecraft'][1]

        doc = ONLINE.find_one({'server_name': server, 'name': nick})

        await send_online(author=self.ctx.author, server=server, doc=doc, now_list=-1)


async def get_online(server, doc, list_now, msg):
    online = list(doc['every_day'])
    online.reverse()
    number_week = int(datetime.datetime.today().weekday())
    text = ''
    if list_now == -1:
        where = 'right'
        st, en = 0, number_week
        text += f'{await date_for_online(-1)} - {doc["today"]}\n'
    else:
        st, en = number_week + 7 * list_now, number_week + 7 * list_now + 7
        if en > len(online):
            en = int(len(online)) - 1
            where = 'left'
        else:
            where = 'rAl'
    for i in range(st, en):
        text += f'{await date_for_online(i)} - {online[i]}\n'
    embed = discord.Embed(title=f'Ваш онлайн на {server}',
                          description=text, color=GENERAL_COLOR)
    if where == 'right':
        await msg.edit(embed=embed, view=left_no(server=server, doc=doc, list_now=list_now, msg=msg))
    elif where == 'left':
        await msg.edit(embed=embed, view=right_no(server=server, doc=doc, list_now=list_now, msg=msg))
    elif where == 'rAl':
        await msg.edit(embed=embed, view=right_and_left(server=server, doc=doc, list_now=list_now, msg=msg))

async def send_online(author, server, doc, now_list):
    embed = discord.Embed(title='Получаю информацию...', color=SUCCESS_COLOR)
    msg = await author.send(embed=embed)
    await get_online(server,doc,now_list,msg)


# async def get_text_online(now_list, start, end, days):
#     print(days)
#     text = ''
#     if now_list == 0:
#         text += 'Эта неделя:\n'
#         all_hour, all_minute = 0, 0
#
#         for i in range(start, end):
#             time = days[i]
#             hour = time // 60
#             minute = time % 60
#             all_hour += hour
#             all_minute += minute
#             text += f'**{await date_for_online(i - 1)}**: `{hour}ч` `{minute}м`\n'
#         text += f'Общее: `{all_hour}ч` `{all_minute}м`'
#     else:
#         text += f'{await date_for_online(0)} - {await date_for_online(start - 1)}'
#         all_hour, all_minute = 0, 0
#         for i in range(start, end):
#             time = days[i]
#             hour = time // 60
#             minute = time % 60
#             all_hour += hour
#             all_minute += minute
#             text += f'**{await date_for_online(i - 1)}**: `{hour}ч` `{minute}м`\n'
#         text += f'Общее: `{all_hour}ч` `{all_minute}м`'
#     return text


async def date_for_online(otkat):
    delta = datetime.timedelta(hours=3, minutes=0)
    time_now = datetime.datetime.now(datetime.timezone.utc) + delta
    delta = datetime.timedelta(days=otkat + 1)
    time_now = time_now - delta
    time_now = str(time_now.strftime('%d.%m.%y'))
    return time_now


class SelectView(discord.ui.View):
    def __init__(self, *, timeout=180, servers, ctx):
        super().__init__(timeout=timeout)
        self.servers = servers
        self.ctx = ctx
        self.add_item(Select(servers=self.servers, ctx=self.ctx))


class ShowMeOnline(commands.Cog):
    def __init__(self, py):
        self.py = py

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.command(aliases=['o-me', 'online-me', 'мой-онлайн', 'м-о'])
    async def _me_online(self, ctx):
        if await check_channels(ctx):
            info = await check_fields(ctx.author)
            if len(info['ds-minecraft']) == 0:
                embed = discord.Embed(title=failure,
                                      description='Можно посмотреть только свой онлайн, а у Вас нет привязанного '
                                                  'аккаунта в майнкрафте!\n'
                                                  'Привяжите аккаунт командой `!auth-ds-minecraft`!',
                                      color=FAILURE_COLOR)
                await ctx.reply(embed=embed)
            else:
                docs_online = list(ONLINE.find({'name': info['ds-minecraft'][1]}))
                if len(docs_online) == 0:
                    embed = discord.Embed(title=f'{failure} Ошибка',
                                          description='Мне не удалось найти документы с Вами :(\n'
                                                      'Скорей всего Вы еще не поиграли на серверах.',
                                          color=FAILURE_COLOR)
                    return await ctx.reply(embed=embed)
                await ctx.reply('**Идем в личные сообщения.**')
                await ctx.author.send('Выберите сервер', view=SelectView(ctx=ctx, servers=docs_online))


def setup(py):
    py.add_cog(ShowMeOnline(py))
