import os
import time

import discord
from discord.ext import commands

from DataBase.global_db import check_db
from config.secret import token

intents = discord.Intents.all()

py = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)
py.remove_command('help')

start_time = time.time()

print('\033[0mПробуем подключиться к БД.')
request = check_db()
if request:
    print('\033[32mПодключение есть!')
    print('\033[33m\033[40mЗапускаем коги.\n')
    zapusk = []

    for DirPath_1, DirName_1, filenames in os.walk("cogs"):
        # for DirName in DirName_1:
        #     print("Каталог:", os.path.join(DirPath_1, DirName))
        for filename in filenames:
            if not filename.endswith('.pyc'):
                # print("Файл:", os.path.join(DirPath_1, filename))
                link = ''
                for simvol in str(os.path.join(DirPath_1, filename)):
                    if simvol == '/':
                        simvol = '.'
                    link += simvol
                zapusk.append(link)
    for file in zapusk:
        print(file)
        py.load_extension(str(file)[:-3])
    print('\nВсе файлы в запуске.')


    @py.event
    async def on_ready():
        if py.is_ready():

            print("\033[0m\nЗапуск длился: %.2fс\n" % (time.time() - start_time))



    py.run(token)


else:
    print('\033[31m\n!!!WARNING!!!\nНевозможно подключиться к БД. Неверна ссылка для подключения!\n'
          'Остановка бота.\n')

