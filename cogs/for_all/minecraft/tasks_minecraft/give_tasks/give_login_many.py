from discord.ext import commands

class GiveManyLogin(commands.Cog):
    def __init__(self, py=None):
        self.py = py

    async def _create_task(self):
        pass

def setup(py):
    py.add_cog(GiveManyLogin(py))