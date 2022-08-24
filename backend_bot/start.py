import threading
import time

import schedule as schedule

from backend_bot.handler.handler_players import task_go_to_coordinates
from backend_bot.handler.handler_online import online_players
from backend_bot.tasks_minecraft.give_tasks import give_coordinates, give_login_many
from backend_bot.tasks_minecraft.login_server_1_in_day.everyday_bonus import restart_task_login
from config import config_b


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


schedule.every(1).minutes.do(run_threaded, online_players)

schedule.every(1).minutes.do(run_threaded, give_coordinates.create_task)
schedule.every(1).minutes.do(run_threaded, give_login_many.create_task)

schedule.every(1).seconds.do(run_threaded, task_go_to_coordinates)
schedule.every().day.at("00:00").do(run_threaded, restart_task_login)

def setup_handlers():
    config_b.access_run_bot = True
    print('\033[32mПодключение установлено!')
    try:
        while True:
            if config_b.run_bot:
                try:
                    config_b.run_backend = True
                    schedule.run_pending()
                    time.sleep(1)
                except Exception as exc:
                    config_b.errors_backend += 1
                    if config_b.errors_backend > 5:
                        config_b.run_backend = False
                        break
                    config_b.errors_backend = 0
            else:
                break
    except Exception as exc:
        config_b.access_run_bot = False
    config_b.access_run_bot = False
