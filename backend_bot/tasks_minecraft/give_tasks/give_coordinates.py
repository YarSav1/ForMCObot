import random

from DataBase.global_db import DB_GAME
from config.minecraft_config import size_world_for_tasks


def create_task():
    db = list(DB_GAME.find())
    players = []
    for i in db:
        try:
            check_field = i['ds-minecraft'][1]
            players.append(i)
        except Exception as exc:
            pass
    if len(players) != 0:
        for doc in players:
            range_for = 5-len(doc['minecraft-coordinates'])
            ttt = []
            for i in range(range_for):
                x = [-size_world_for_tasks[0] // 2, size_world_for_tasks[0] // 2]
                z = [-size_world_for_tasks[1] // 2, size_world_for_tasks[1] // 2]
                x = random.randint(x[0], x[1])
                z = random.randint(z[0], z[1])
                ttt.append([x, z, False])
                print(ttt)
            ttt+=doc['minecraft-coordinates']
            if len(ttt) != 0:
                DB_GAME.update_one({'id_member': doc['id_member']},
                                   {'$set': {'minecraft-coordinates': ttt}})

