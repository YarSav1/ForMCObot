from DataBase.global_db import DB_GAME


def check_login(doc):
    task_login = doc['minecraft-login-1-in-day']
    if not task_login:
        search = {'id_member': doc['id_member']}
        DB_GAME.update_one(search,
                           {'$set': {'minecraft-login-1-in-day': True}})
        if doc['minecraft-login-many'][0]+1 == doc['minecraft-login-many'][1]:
            DB_GAME.update_one(search,
                               {'$set': {'minecraft-login-many': [doc['minecraft-login-many'][1],
                                                                  doc['minecraft-login-many'][1],
                                                                  True]}})
        else:
            DB_GAME.update_one(search,
                               {'$set': {'minecraft-login-many': [doc['minecraft-login-many'][0]+1,
                                                                  doc['minecraft-login-many'][1],
                                                                  doc['minecraft-login-many'][2]]}})


