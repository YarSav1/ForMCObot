from discord.ext import commands

from config.functional_config import list_commands


class HelpCommands(commands.Cog):
    def __init__(self, py):
        self.py = py

    @commands.command(aliases=['help', 'хелп', 'команды', 'commands'])
    async def _help(self, ctx):
        await list_commands(ctx, False)

    @commands.command(aliases=['adminhelp', 'админхелп', 'админкоманды', 'admincommands'])
    async def admin_help(self, ctx):
        await list_commands(ctx, True)


def setup(py):
    py.add_cog(HelpCommands(py))
