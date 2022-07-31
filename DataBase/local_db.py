import time

import requests

from DataBase.global_db import ONLINE

# while True:
#     try:
#         doc = ONLINE.find_one({'name': 'LamerBot2'})
#         print(doc)
#     except:
#         pass
from config.functional_config import HEADERS

a = 7200
while a != 9000:
    a += 1
    try:
        html = requests.get(f'http://51.75.53.35:{a}/up/world/world/', headers=HEADERS, params=None, timeout=0.5)
        print(f'==={a}===')
    except:
        pass
    if a % 100 == 0:
        print(a)
