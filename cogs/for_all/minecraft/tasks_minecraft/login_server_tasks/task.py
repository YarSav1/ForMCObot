from discord.ext import commands


class ManyLoginTask(commands.Cog):
    def __init__(self, py):
        self.py = py


def setup(py):
    py.add_cog(ManyLoginTask(py))