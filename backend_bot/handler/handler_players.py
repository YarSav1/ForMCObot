import json
import time
from threading import Thread

import requests

from DataBase.global_db import DB_GAME
from backend_bot.tasks_minecraft.complete_tasks import coordinates_complete
from config.functional_config import HEADERS
from config.online_config import URL_carta, server
from config import config_b

text = ''


def thread_task(serv, players):
    global text
    start_time = time.time()
    try:
        html = requests.get(URL_carta[server.index(serv)], headers=HEADERS, params=None, timeout=2)
    except Exception:
        if f'{serv}:' not in text:
            text += f'{serv}: Ошибка подключения. Превышено время ожидания!\n'
        # text += f'{serv} - Ошибка'
        return
    if html.status_code == 200:
        try:
            r = requests.get(URL_carta[server.index(serv)], headers=HEADERS, params=None).text
        except Exception as exc:
            if f'{serv}:' not in text:
                text += f'{serv}: Ошибка подключения\n'
            return
        r = json.loads(r)
        cikl_online = r["currentcount"]
        try:
            for i in range(0, cikl_online):
                player = r["players"][i]['name']
                if player in players:
                    coordinates_now = [int(r["players"][i]['x']), int(r["players"][i]['z'])]
                    if len(config_b.check_players) != 0:
                        for i in config_b.check_players:
                            if player == i[0]:
                                add = [serv,
                                       coordinates_now[0],
                                       coordinates_now[1]]
                                for sss in range(1, len(i)):
                                    if serv == config_b.check_players[config_b.check_players.index(i)][sss][0]:
                                        config_b.check_players[config_b.check_players.index(i)][sss] = add
                                        add = False
                                        break
                                if add:
                                    config_b.check_players[config_b.check_players.index(i)] += [add]

                    coordinates_complete.check_coordinates(doc=players[players.index(player) + 1],
                                                           coordinates_now=coordinates_now)
        except Exception as exc:
            pass
        if f'{serv}:' not in text:
            text += f'{serv}: %.2fс\n' % (time.time() - start_time)
    else:
        if f'{serv}:' not in text:
            text += f'{serv}: Ошибка подключения\n'
    # text += f'{serv} - %.2fс\n' % (time.time() - start_time)


def task_go_to_coordinates():
    global text
    start_time = time.time()
    db = list(DB_GAME.find())
    players = []
    for i in db:
        try:
            players.append(i['ds-minecraft'][1])
            players.append(i)
        except Exception as exc:
            pass
    ths = []

    for serv in server:
        t = Thread(target=thread_task, args=(serv, players))
        t.start()
        ths.append(t)
    for th in ths:
        th.join()
    if config_b.text_coordinates == '':
        text += f'\nЭта обработка длилась: %.2fс' % (time.time() - start_time)
        config_b.text_coordinates = text
        text = ''
