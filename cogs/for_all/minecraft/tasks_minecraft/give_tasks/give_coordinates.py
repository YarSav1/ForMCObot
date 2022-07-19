import asyncio
import random

from discord.ext import commands

from DataBase.global_db import DB_GAME
from config.minecraft_config import size_world_for_tasks


class CreateTasksCoordinates(commands.Cog):
    def __init__(self, py=None):
        self.py = py

    async def create_task(self):
        db = list(DB_GAME.find())
        players = []
        for i in db:
            try:
                check_field = i['ds-minecraft'][1]
                players.append(i)
            except Exception as exc:
                pass
        for doc in players:
            ttt = []
            while True:
                if len(doc['minecraft-coordinates']) < 5:
                    x = [-size_world_for_tasks[0] // 2, size_world_for_tasks[0] // 2]
                    z = [-size_world_for_tasks[1] // 2, size_world_for_tasks[1] // 2]
                    x = random.randint(x[0], x[1])
                    z = random.randint(z[0], z[1])
                    ttt.append([x, z, False])
                else:
                    break
            if len(ttt) != 0:
                DB_GAME.update_one({'id_member': doc['id_member']},
                                   {'$push': {'minecraft-coordinates': ttt}})


def setup(py):
    py.add_cog(CreateTasksCoordinates(py))
