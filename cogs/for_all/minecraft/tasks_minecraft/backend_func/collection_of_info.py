import asyncio
import json
import time
from threading import Thread

import requests
from discord.ext import commands, tasks

from DataBase.global_db import DB_GAME
from cogs.for_all.minecraft.tasks_minecraft.coordinates.task import GoToCoordinatesTask
from config.functional_config import HEADERS, super_admin
from config.online_config import server, URL_carta

class CollectionInfoPlayers(commands.Cog):
    def __init__(self, py):
        self.py = py
        self.text = ''
        self.check_delay = False
        self.msg = None
        self.ctx = None

    @commands.command(aliases=['прослушка'])
    async def _check_delay(self, ctx):
        if ctx.author.id in super_admin:
            if self.check_delay:
                self.ctx = None
                self.check_delay = False
                self.msg = None
                await ctx.reply("Вывод прекращен.")
            else:
                self.ctx = ctx
                self.check_delay = True
                await ctx.reply("После следующей обработки начнется вывод статистики в этот чат!\n"
                                "**При включенном режиме скорость отклика бота понизится!**")

    @commands.Cog.listener()
    async def on_ready(self):
        if self.py.is_ready():
            self.task_go_to_coordinates.start()

    @commands.command(aliases=['test', 't', "тест"])
    async def test_(self, ctx, nick):
        url = 'http://217.182.201.195:7777/up/world/world/'
        msg = await ctx.reply(f'Смотрю Ваши координаты: x: `вычисляется`, y: `вычисляется`, Высота: `вычисляется`')
        while True:
            html = requests.get(url, headers=HEADERS, params=None)
            r = requests.get(url, headers=HEADERS, params=None).text
            if html.status_code == 200:
                r = json.loads(r)
                cikl_online = r["currentcount"]
                for i in range(0, cikl_online):
                    player = r["players"][i]['name']
                    if player == nick:
                        await msg.edit(f'Смотрю Ваши координаты: x: `{r["players"][i]["x"]}`, '
                                       f'z: `{r["players"][i]["z"]}`, '
                                       f'Высота: `{r["players"][i]["y"]}`')
                        break
            else:
                await msg.edit("Повторное подключение...")
                await asyncio.sleep(5)

            await asyncio.sleep(5)

    async def ttt(self):
        print('opaopaopa')

    def thread_task(self, serv, players):
        start_time = time.time()
        try:
            html = requests.get(URL_carta[server.index(serv)], headers=HEADERS, params=None)
        except Exception as exc:
            print(f'{exc}\n'
                  f'Ошибка подключения к {serv}')
            self.text += f'{serv} - Ошибка'
            return
        if html.status_code == 200:
            r = requests.get(URL_carta[server.index(serv)], headers=HEADERS, params=None).text
            r = json.loads(r)
            cikl_online = r["currentcount"]
            try:
                for i in range(0, cikl_online):
                    player = r["players"][i]['name']
                    if player in players:
                        coordinates_now = [int(r["players"][i]['x']), int(r["players"][i]['z'])]
                        GoToCoordinatesTask(self.py).check_coordinates(doc=players[players.index(player) + 1],
                                                                                coordinates_now=coordinates_now)
                        # вызов заданий
            except Exception as exc:
                pass

        self.text += f'{serv} - %.2fс\n' % (time.time() - start_time)

    @tasks.loop(seconds=5)
    async def task_go_to_coordinates(self):
        # start_time = time.time()
        db = list(DB_GAME.find())
        players = []
        for i in db:
            try:
                players.append(i['ds-minecraft'][1])
                players.append(i)
            except Exception as exc:
                pass
        ths = []

        for serv in server:
            t = Thread(target=self.thread_task, args=(serv, players))
            t.start()
            ths.append(t)
        for th in ths:
            th.join()
        if self.check_delay:
            if self.msg is None:
                self.msg = await self.ctx.send(self.text)
            else:
                await self.msg.edit(self.text)
        self.text = ''
        # 'Эта обработка длилась: %.2fс' % (time.time() - start_time)


def setup(py):
    py.add_cog(CollectionInfoPlayers(py))
