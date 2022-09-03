import datetime

import discord
from discord.ext import commands

from DataBase.global_db import ONLINE, DB_GAME
from config.functional_config import check_channels, check_fields, failure, FAILURE_COLOR, left_page, right_page


class left_no(discord.ui.View):
    def __init__(self, *, py, timeout=60):
        super().__init__(timeout=timeout)

    @discord.ui.button(label=left_page, style=discord.ButtonStyle.red, disabled=True)
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    @discord.ui.button(label=right_page, style=discord.ButtonStyle.green)
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    async def on_timeout(self):
        for btn in self.children:
            btn.disabled = True


class right_no(discord.ui.View):
    def __init__(self, *, py, timeout=60):
        super().__init__(timeout=timeout)

    @discord.ui.button(label=left_page, style=discord.ButtonStyle.green, disabled=True)
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    @discord.ui.button(label=right_page, style=discord.ButtonStyle.red)
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    async def on_timeout(self):
        for btn in self.children:
            btn.disabled = True


class stop(discord.ui.View):
    def __init__(self, *, py, timeout=60):
        super().__init__(timeout=timeout)

    @discord.ui.button(label=left_page, style=discord.ButtonStyle.red, disabled=True)
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    @discord.ui.button(label=right_page, style=discord.ButtonStyle.red)
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    async def on_timeout(self):
        for btn in self.children:
            btn.disabled = True


class right_and_left(discord.ui.View):
    def __init__(self, *, py, timeout=60):
        super().__init__(timeout=timeout)

    @discord.ui.button(label=left_page, style=discord.ButtonStyle.green, disabled=True)
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    @discord.ui.button(label=right_page, style=discord.ButtonStyle.green)
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

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

        doc=ONLINE.find_one({'server_name': server, 'name': nick})

        if len(doc['every_day'])/7*10 > len(doc['every_day'])/7:
            max_lists = int(len(doc['every_day'])/7)+1
        else:
            max_lists = int(len(doc['every_day'])/7)
        await send_online(author=self.ctx, server=server, doc=doc, max_lists=max_lists, now_list=1)

async def send_online(author, server, doc, max_lists, now_list):
    if now_list == 0:
        foring_start, foring_end = 0, datetime.datetime.today().weekday()+1
    else:
        if now_list*7+datetime.datetime.today().weekday()+8 > len(doc['every_day']):
            foring_start, foring_end = now_list * 7 + datetime.datetime.today().weekday(), \
                                       len(doc['every_day'])-1
        else:
            foring_start, foring_end = now_list*7+datetime.datetime.today().weekday(), \
                                       now_list*7+datetime.datetime.today().weekday()+8
    days = doc['every_day']
    print(days)
    days.reverse()
    print(days)
    text = await get_text_online(now_list, foring_start, foring_end, days=days)
    await author.send(text)
    # if now_list <= 0:
    #     left_no
    # elif now_list+1 >= max_lists:
    #     right_no
    # elif now_list-1 <= 0 and now_list+1 >= max_lists:
    #     stop
    # else:
    #     right_and_left

async def get_text_online(now_list, start, end, days):
    print(days)
    text = ''
    if now_list == 0:
        text+='Эта неделя:\n'
        all_hour, all_minute = 0, 0

        for i in range(start, end):
            time = days[i]
            hour = time//60
            minute = time%60
            all_hour+=hour
            all_minute+=minute
            text += f'**{await date_for_online(i-1)}**: `{hour}ч` `{minute}м`\n'
        text+=f'Общее: `{all_hour}ч` `{all_minute}м`'
    else:
        text += f'{await date_for_online(0)} - {await date_for_online(start - 1)}'
        all_hour, all_minute = 0, 0
        for i in range(start, end):
            time = days[i]
            hour = time // 60
            minute = time % 60
            all_hour += hour
            all_minute += minute
            text += f'**{await date_for_online(i - 1)}**: `{hour}ч` `{minute}м`\n'
        text += f'Общее: `{all_hour}ч` `{all_minute}м`'
    return text

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
        self.add_item(Select(self.servers, self.ctx))


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
                docs_online = ONLINE.find({'name': info['ds-minecraft'][1]})

                await ctx.send('test', view=SelectView(ctx=ctx, servers=docs_online))


def setup(py):
    py.add_cog(ShowMeOnline(py))
