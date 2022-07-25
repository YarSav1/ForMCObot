import requests

from config.functional_config import HEADERS

a = 7000

while a != 9000:
    try:
        html = requests.get(f'http://95.217.194.41:{a}/up/world/world/', headers=HEADERS, params=None, timeout=0.5)
        if html.status_code == 200:
            print(a)
    except:
        pass

    if a % 100 == 0:
        print(a)
    a+=1