import discord
from discord.ext import commands

from config.functional_config import LikeDislike


class RatingIdea(commands.Cog):
    def __init__(self, py):
        self.py = py



    @commands.Cog.listener()
    async def on_ready(self):
        self.py.add_view(LikeDislike(py=self.py))


def setup(py):
    py.add_cog(RatingIdea(py))
