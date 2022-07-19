# Здесь можно внутри кода менять параметры в бд, только и знай, что вставлять
import json
import time

import requests
from bs4 import BeautifulSoup

# Fill in your details here to be posted to the login form.
from config.functional_config import form_send, payload, HEADERS

url = 'http://217.182.201.195:7777/up/world/world/'

while True:
    html = requests.get(url, headers=HEADERS, params=None)
    r = requests.get(url, headers=HEADERS, params=None).text
    if html.status_code == 200:
        r = json.loads(r)
    else:
        break
    cikl_online = r["currentcount"]
    for i in range(0, cikl_online):
        player = r["players"][i]['name']
        if player == 'PythonchikY':
            print(f'{r["players"][i]["x"]}, {r["players"][i]["y"]}, {r["players"][i]["z"]}')
    time.sleep(1)