from discord.ext import commands


class EveryDayLoginBounty(commands.Cog):
    def __init__(self, py):
        self.py = py


def setup(py):
    py.add_cog(EveryDayLoginBounty(py))