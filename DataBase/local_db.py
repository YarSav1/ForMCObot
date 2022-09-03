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
import requests
from bs4 import BeautifulSoup

from config.functional_config import HEADERS

nick = 'XxromaxX'  # doc["ds-minecraft"][1]
html = requests.get(f'https://minecraftonly.ru/index.php?player={nick}&view=search&do=tophungergames&server=0',
                    headers=HEADERS, params=None)
if html.status_code == 200:
    html = html.text
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find_all('tr')
    if len(rows) > 1:
        nav = []
        info = []

        for i in rows[0]:
            if i.text != '\n':
                nav.append(i.text)
        for i in rows[1]:
            info.append(i.text)
        index = nav.index('Убийств')
        player_kills = info[index]
        print(player_kills)

