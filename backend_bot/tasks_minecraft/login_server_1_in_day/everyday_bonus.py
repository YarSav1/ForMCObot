from DataBase.global_db import DB_GAME


def restart_task_login():
    DB_GAME.update_many({}, {'$set': {'minecraft-login-1-in-day': False}})


