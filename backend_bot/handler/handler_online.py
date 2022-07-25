import datetime
import json
import time
from threading import Thread

import requests

from DataBase.global_db import ONLINE
from config.functional_config import HEADERS
from config.online_config import server, URL_carta


def get_day_min(player):
    try:
        massive = player['every_day']
    except:
        own = {
            "name": player['name'],
            "today": 0,
            'server_name': player['server_name'],
            'every_day': [player['today']]
        }
        return own
    massive.append(player['today'])
    own = {
        "name": player['name'],
        "today": 0,
        'server_name': player['server_name'],
        'every_day': massive
    }
    return own


def get_player(player, server_name):
    own = {
        "name": player,
        "today": 1,
        "server_name": server_name,
        "every_day": []
    }
    return own


def online_day(server_name):
    all_collection = ONLINE.find({'server_name': server_name})
    players_del = []
    players_new = []
    for player in all_collection:
        new_old_player = get_day_min(player)
        players_del.append(player['name'])
        players_new.append(new_old_player)
    if players_new:
        ONLINE.delete_many({'server_name': server_name, 'name': {'$in': players_del}})
        ONLINE.insert_many(players_new)


def online(karta, serv):
    start_time = time.time()
    try:
        html = requests.get(karta, headers=HEADERS, params=None)
        r = requests.get(karta, headers=HEADERS, params=None).text
    except Exception:
        return
    if html.status_code == 200:
        r = json.loads(r)
    else:
        return
    cikl_online = r["currentcount"]
    in_db_pl = []
    all_players = ONLINE.find({'server_name': serv})

    new_db = []
    valid_players = []
    for player_bd in all_players:
        in_db_pl.append(player_bd['name'])

    try:
        for i in range(0, cikl_online):
            player = r["players"][i]['name']
            if player in in_db_pl:
                valid_players.append(player)
            else:
                new_player = get_player(player, serv)
                new_db.append(new_player)
    except Exception:
        pass
    if new_db:
        ONLINE.insert_many(new_db)
    if valid_players:
        tm = time.time() + 1 - start_time
        ONLINE.update_many({'server_name': serv, 'name': {'$in': valid_players}},
                           {'$inc': {'today': tm}})


def online_players():
    delta = datetime.timedelta(hours=3, minutes=0)
    time_now = datetime.datetime.now(datetime.timezone.utc) + delta
    time_now = str(time_now.strftime('%H:%M'))
    if time_now == '00:00':
        th = []
        for index in range(0, len(server)):
            x = Thread(target=online_day, args=(server[index],))
            x.start()
            th.append(x)
        for z in th:
            z.join()

    all_servers = len(URL_carta)
    for a in range(0, all_servers):
        t = Thread(target=online, args=(URL_carta[a], server[a]))
        t.start()
