import random

import requests
from bs4 import BeautifulSoup

from DataBase.global_db import DB_GAME
from config.functional_config import HEADERS
from config.minecraft_config import size_world_for_tasks, need_kill

def amount_kills(rows):
    nav = []
    info = []
    for i in rows[0]:
        if i.text != '\n':
            nav.append(i.text)
    for i in rows[1]:
        info.append(i.text)
    index = nav.index('Убийств')
    player_kills = info[index]
    return player_kills

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
            if len(doc['minecraft-kills']) == 0:
                nick = doc["ds-minecraft"][1]
                html = requests.get(
                    f'https://minecraftonly.ru/index.php?player={nick}&view=search&do=tophungergames&server=0',
                    headers=HEADERS, params=None)
                if html.status_code == 200:
                    html = html.text
                    soup = BeautifulSoup(html, 'html.parser')
                    rows = soup.find_all('tr')
                    if len(rows) > 1:
                        player_kills = amount_kills(rows)
                        need_kill_task = random.randint(need_kill[0], need_kill[1])
                        massive = [player_kills, need_kill_task, 0, False]
                        DB_GAME.update_one({'id_member': doc['id_member']},
                                           {'$set': {'minecraft-kills': massive}})



