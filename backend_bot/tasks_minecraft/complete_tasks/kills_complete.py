import requests
from bs4 import BeautifulSoup

from DataBase.global_db import DB_GAME
from backend_bot.tasks_minecraft.give_tasks.give_kill import amount_kills
from config.functional_config import HEADERS


def check_kills():
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
            if 'minecraft-kills' in doc:
                task_kills = doc['minecraft-kills']
                if task_kills[3] is False or len(task_kills) == 0:
                    nick = doc["ds-minecraft"][1]
                    html = requests.get(
                        f'https://minecraftonly.ru/index.php?player={nick}&view=search&do=tophungergames&server=0',
                        headers=HEADERS, params=None)
                    if html.status_code == 200:
                        html = html.text
                        soup = BeautifulSoup(html, 'html.parser')
                        rows = soup.find_all('tr')
                        if len(rows) > 1:
                            now_kills = amount_kills(rows)
                            if now_kills-task_kills[0] >= task_kills[1]:
                                massive = [task_kills[0], task_kills[1], task_kills[1], True]
                            else:
                                massive = [task_kills[0], task_kills[1], now_kills-task_kills[0], False]
                            DB_GAME.update_one({'id_member': doc['id_member']},
                                               {'$set': {'minecraft-kills': massive}})

