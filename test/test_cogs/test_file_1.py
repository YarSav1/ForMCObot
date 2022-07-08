import asyncio

import discord
from discord.ext import commands
from discord.ui import button

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Button",style=discord.ButtonStyle.gray)
    async def blurple_button(self,button:discord.ui.Button,interaction:discord.Interaction):
        button.style=discord.ButtonStyle.green
        await interaction.response.edit_message(content=f"This is an edited button response!",view=self)


class TestCog(commands.Cog):
    def __init__(self, py):
        self.py = py
    @commands.Cog.listener()
    async def on_ready(self):
        print('ok')

    @commands.command()
    async def t(self, ctx):
        msg_idea = ctx.message




        await ctx.send('test', view=Buttons())

def setup(py):
    py.add_cog(TestCog(py))
