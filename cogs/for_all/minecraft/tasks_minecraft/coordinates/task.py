import asyncio

from discord.ext import commands

from DataBase.global_db import DB_GAME


class GoToCoordinatesTask(commands.Cog):
    def __init__(self, py):
        self.py = py


def setup(py):
    py.add_cog(GoToCoordinatesTask(py))
