import time

from DataBase.global_db import ONLINE

while True:
    try:
        doc = ONLINE.find_one({'name': 'LamerBot2'})
        print(doc)
    except:
        pass