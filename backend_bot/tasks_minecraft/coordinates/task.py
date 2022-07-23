from DataBase.global_db import DB_GAME


def check_coordinates(doc, coordinates_now):
    task_coordinates = doc['minecraft-coordinates']
    for task in task_coordinates:
        if task[0] == coordinates_now[0]:
            if task[1] == coordinates_now[1]:
                if not task[2]:
                    DB_GAME.update_one({'id_member': doc['id_member']},
                                       {'$pull': {'minecraft-coordinates': task}})
                    DB_GAME.update_one({'id_member': doc['id_member']},
                                       {'$push': {'minecraft-coordinates': [task[0], task[1], True]}})
                    # задание выполнено

