import discord
from discord.ext import commands

from backend_bot.tasks_minecraft.give_tasks.give_coordinates import CreateTasksCoordinates
from backend_bot.tasks_minecraft.give_tasks.give_login_many import GiveManyLogin
from config.functional_config import check_channels, check_fields


class TasksProfile(commands.Cog):
    def __init__(self, py):
        self.py = py

    @commands.command(aliases=['tasks', 'задания'])
    async def _tasks_minecraft(self, ctx):
        if await check_channels(ctx):
            info = await check_fields(ctx.author)
            if len(info['minecraft-coordinates']) < 5:
                await CreateTasksCoordinates(self.py).create_task()
            if len(info['minecraft-login-many']) == 0:
                await GiveManyLogin(self.py).create_task()
            embed = discord.Embed(title='Ваши задания')


def setup(py):
    py.add_cog(TasksProfile(py))
