import asyncio
import json
import time

import requests
from discord.ext import commands, tasks

from DataBase.global_db import DB_GAME
from config.functional import HEADERS
from config.online_config import server, URL_carta


class GoToCoordinates(commands.Cog):
    def __init__(self, py):
        self.py = py

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

    @tasks.loop(seconds=5)
    async def task_go_to_coordinates(self):
        start_time = time.time()
        db = list(DB_GAME.find())
        players = []
        for i in db:
            try:
                players.append(i['ds-minecraft'][1])
                players.append(i)
            except Exception as exc:
                pass
        index = 0
        text = ''
        for serv in server:
            html = requests.get(URL_carta[server.index(serv)], headers=HEADERS, params=None)
            r = requests.get(URL_carta[server.index(serv)], headers=HEADERS, params=None).text
            if html.status_code == 200:
                r = json.loads(r)
                cikl_online = r["currentcount"]
                try:
                    for i in range(0, cikl_online):
                        player = r["players"][i]['name']
                        if player in players:
                            text += f'Игрок: {player} - Сервер {serv}.\n' \
                                    f'Координаты: x - {int(r["players"][i]["x"])} | ' \
                                    f'z - {int(r["players"][i]["z"])} | ' \
                                    f'Высота - {int(r["players"][i]["y"])}'
                except Exception as exc:
                    pass
            if len(players) != index + 2:
                index += 2
            else:
                break

        if len(text) == 0:
            text = 'Никого не найдено.\n'
        text+='\nЭта обработка длилась: %.2fс\n ' % (time.time() - start_time)
        channel = self.py.get_channel(986434390122962955)
        await channel.send(text)


def setup(py):
    py.add_cog(GoToCoordinates(py))
