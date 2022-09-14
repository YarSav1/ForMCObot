# import datetime
# import time
#
# import requests
# import schedule
#
# from DataBase.global_db import ONLINE

# while True:
#     try:
#         doc = ONLINE.find_one({'name': 'LamerBot2'})
#         print(doc)
#     except:
#         pass
# from config.functional_config import HEADERS
#
# a = 7200
# while a != 9000:
#     a += 1
#     try:
#         html = requests.get(f'http://51.75.53.35:{a}/up/world/world/', headers=HEADERS, params=None, timeout=0.5)
#         print(f'==={a}===')
#     except:
#         pass
#     if a % 100 == 0:
#         print(a)
# def te():
#     print(datetime.datetime.now())
#
# schedule.every().day.at("20:42").do(te)
# while True:
#     schedule.run_pending()
# import datetime
# import time
#
# tms = ''
# while True:
#     timenow = datetime.datetime.now()
#     timenow = f"{timenow.strftime('%Y.%m.%d %H:%M:%S')}"
#     if tms != timenow:
#         tms = timenow
#         print(end='\r')
#         print(timenow, end='')
import datetime

import requests
from bs4 import BeautifulSoup

from DataBase.global_db import ONLINE
from config.functional_config import HEADERS

# nick = 'XxromaxX'  # doc["ds-minecraft"][1]
# html = requests.get(f'https://minecraftonly.ru/index.php?player={nick}&view=search&do=tophungergames&server=0',
#                     headers=HEADERS, params=None)
# if html.status_code == 200:
#     html = html.text
#     soup = BeautifulSoup(html, 'html.parser')
#     rows = soup.find_all('tr')
#     if len(rows) > 1:
#         nav = []
#         info = []
#
#         for i in rows[0]:
#             if i.text != '\n':
#                 nav.append(i.text)
#         for i in rows[1]:
#             info.append(i.text)
#         index = nav.index('Убийств')
#         player_kills = info[index]
#         print(player_kills)

# print(datetime.datetime.today().weekday())
import requests
import random
from bs4 import BeautifulSoup as bs

from config.online_config import URL_md, server


def get_free_proxies():
    url = "https://free-proxy-list.net/"
    # получаем ответ HTTP и создаем объект soup
    soup = bs(requests.get(url).content, "html.parser")
    proxies = []
    for row in soup.find("table", attrs={"class": "table table-striped table-bordered"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            name = tds[4].text.strip()
            if name == 'elite proxy' and port == '8118':
                host = f"{ip}:{port}"
                proxies.append(host)
        except IndexError:
            continue
    return proxies


# free_proxies = get_free_proxies()
#
# print(f'Обнаружено бесплатных прокси - {len(free_proxies)}:')
# for i in range(len(free_proxies)):
#     print(f"{i+1}) {free_proxies[i]}")

# def get_session(proxies):
#     # создать HTTP‑сеанс
#     session = requests.Session()
#     # выбираем один случайный прокси
#     proxy = random.choice(proxies)
#     proxy = '37.230.154.57:3629'
#     session.proxies = {"http": proxy, "https": proxy}
#     # print(proxy)
#     return session


# for i in range(5):
#     s = get_session(get_free_proxies())
#     try:
#         print(f'{i+1}', end=' ')
#         print("Страница запроса с IP:", s.get("http://icanhazip.com", timeout=5).text.strip(), end='')
#     except Exception as e:
#         pass
#     print('')
# s = get_session(get_free_proxies())
# print('Пробуем')
# html = s.get('https://minecraftonly.ru/engine/scripts/moderators.php?action=showmoders&serverid=0', headers=HEADERS, params=None)
# if html.status_code == 200:
#     html = html.text
#     print('ok')
#     print(html)
# else:
#     print(html.status_code)
for i in range(len(server)):
    all_collection = list(ONLINE.find({'server_name': server[i]}))
    players = []
    print(server[i])
    print(len(all_collection))
    for player in range(len(all_collection)):
        if player % 10 == 0:
            print(f'{player}', end='\r')
        if all_collection[player]['name'] not in players:
            players.append(all_collection[player]['name'])

    print(len(players))
# print(players)
