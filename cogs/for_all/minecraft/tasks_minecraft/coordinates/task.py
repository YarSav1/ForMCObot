import asyncio

from discord.ext import commands


class GoToCoordinatesTask(commands.Cog):
    def __init__(self, py):
        self.py = py

    def check_coordinates(self, doc, coordinates_now):
        task_coordinates = doc['minecraft-coordinates']
        for task in task_coordinates:
            if task[0] == coordinates_now[0]:
                if task[1] == coordinates_now[1]:
                    pass
                    # задание выполнено





def setup(py):
    py.add_cog(GoToCoordinatesTask(py))
