import asyncio
import os
import sys
import time
from threading import Thread

import discord
from discord.ext import commands

import config.config_b
from DataBase.global_db import check_db
from backend_bot.start import setup_handlers
from config import config_b
from config.functional_config import accept, failure, logger_errors
from config.secret import token
from urllib3.packages.six import StringIO


class OutputInterceptor(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


intents = discord.Intents.all()

py = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)
py.remove_command('help')

start_time = time.time()

print('\033[0mПробуем подключиться к БД.')
request = check_db()
if request:
    try:

        print('\033[32mПодключение есть!')

        config.config_b.run_bot = True
        print('\033[0mПодключение потока для счета онлайна и обработки заданий с майнкрафтом.')
        x = Thread(target=setup_handlers)
        x.start()

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
            print(file, end=' - ')
            try:
                py.load_extension(str(file)[:-3])
                print(f'{accept}')
            except Exception as exc:
                text = f'Ошибка - {exc}'
                logger_errors(text)
                print(f'{failure} | Ошибка: {exc}')

        print('\nВсе файлы в запуске.')


        @py.event
        async def on_ready():
            if py.is_ready():
                print("\033[0mЗапуск длился: %.2fс" % (time.time() - start_time))


        try:
            py.run(token)
        except Exception as exc:
            text = f'Критическая ошибка - {exc}'
            logger_errors(text)
            print('Токен неверен!')
            print('Выключаем бэкэнд')
            config.config_b.run_bot = False
            while config_b.access_run_bot:
                time.sleep(0.1)
            print('Бот выключен.')

    except Exception as exc:
        text = f'Критическая ошибка - {exc}'
        logger_errors(text)
        print('Выключаем бэкэнд')
        config.config_b.run_bot = False
        while config_b.access_run_bot:
            time.sleep(0.1)
        print('Пробуем перезагрузиться...')
        python = sys.executable
        os.execl(python, python, *sys.argv)


else:
    text = 'Невозможно подключиться к БД. Неверна ссылка для подключения!'
    logger_errors(text)
    print(f'\033[31m\n!!!WARNING!!!\n{text}\n'
          'Остановка бота.\n')
