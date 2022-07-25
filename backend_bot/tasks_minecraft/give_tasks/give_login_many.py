import random

from DataBase.global_db import DB_GAME
from config.minecraft_config import size_world_for_tasks, need_login_many


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
            need = random.randint(need_login_many[0], need_login_many[1])
            DB_GAME.update_one({'id_member': doc['id_member']},
                               {'$set': {'minecraft-login-many': [0, need, False]}})

