import time

import schedule as schedule

from backend_bot.handler.handler_coordinates import task_go_to_coordinates
from backend_bot.handler.handler_online import online_players
from config import config_b

schedule.every(1).minutes.do(online_players)

schedule.every(1).seconds.do(task_go_to_coordinates)


def setup_handlers():
    print('\033[32mПодключение установлено!')
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
