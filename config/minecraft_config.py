########################################################################################################################
# MINECRAFT CONFIG
"""
Нельзя ставить цифры с плавающей запятой! Только целочисленные числа и точка!
Лан. В комментариях будет указано, где можно шаманить :)
"""


size_world_for_tasks = [6000, 6000]  # взял цивкрафт с размером мира 6к на 6к(мне было лень под каждый сервак подгонять)


'''
Награда за выполнение задания "прибеги на координаты".
'''
bounty_coordinates = [[500, 1000], [50, 100]]  # [баланс[от, до], опыт[от, до]]

'''
Награда за выполнение задания "Первый вход на сервер в день". 
'''
bounty_login_1_in_day = [[250, 300], [15, 30]]  # [баланс[от, до], опыт[от, до]]

'''
Награда за выполнение задания "Зайди на сервер насколько раз".
'''
need_login_many = [10, 20]  # сколько раз надо зайти на серваки, чтоб выполнить задание "Зайди .. раз" [от, до] (РАНДОМ)
bounty_login = [[500, 1000], [20, 50]]  # [баланс[от, до], опыт[от, до]]
