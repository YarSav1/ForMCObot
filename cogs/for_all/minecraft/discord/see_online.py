import discord
from discord.ext import commands

from DataBase.global_db import ONLINE
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
    def __init__(self):
        options = [
            discord.SelectOption(label="Option 1", emoji="👌", description="This is option 1!"),
            discord.SelectOption(label="Option 2", emoji="✨", description="This is option 2!"),
            discord.SelectOption(label="Option 3", emoji="🎭", description="This is option 3!")
        ]
        options.append(discord.SelectOption(label="Option 1", description="This is option 4!"))
        super().__init__(placeholder="Выберите сервер", max_values=1, min_values=1, options=options)


class SelectView(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(Select())


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

                msg = await ctx.send('test', view=SelectView())


def setup(py):
    py.add_cog(ShowMeOnline(py))
