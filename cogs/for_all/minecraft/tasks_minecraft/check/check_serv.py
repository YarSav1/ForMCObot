import asyncio
import json

import discord
import requests
from discord.ext import commands

from config.functional_config import check_channels, failure, FAILURE_COLOR, HEADERS, accept, loading, \
    SUCCESS_COLOR, GENERAL_COLOR
from config.online_config import server, URL_carta


async def checking(ctx, server_name):
    embed = discord.Embed(title='Проверка связи...', color=GENERAL_COLOR)
    msg = await ctx.reply(embed=embed)
    text = ''
    url = URL_carta[server.index(server_name)]
    html = requests.get(url, headers=HEADERS, params=None)
    r = requests.get(url, headers=HEADERS, params=None).text
    if html.status_code == 200:
        go_check = True
        r = json.loads(r)
        text += f'Подключение: {accept}'
        stamp = int(r["timestamp"])
        clr = SUCCESS_COLOR
    else:
        go_check = False
        text += f'Подключение: {failure}'
        clr = FAILURE_COLOR
    embed = discord.Embed(title='Проверка связи...',
                          description=text, color=clr)
    await msg.edit(embed=embed)
    if go_check:
        result = ''
        for i in range(5):
            await asyncio.sleep(1)
            html = requests.get(url, headers=HEADERS, params=None)
            r = requests.get(url, headers=HEADERS, params=None).text
            if html.status_code == 200:
                r = json.loads(r)
                serv = r["timestamp"]
                if int(serv) != stamp:
                    stamp = int(serv)
                    result += f'{accept}'
                else:
                    result += f'{failure}'
                embed = discord.Embed(title='Проверка связи...',
                                      description=f'{text}\n\n'
                                                  f'Дополнительные тесты {i + 1}/5\n'
                                                  f'{result}{loading * (5 - (i + 1))}', color=clr)
                await msg.edit(embed=embed)
        if result != failure * 5:
            result_end = 'Связь хорошая. Сервер мониторится нормально и доступен для выполнения заданий!'
        else:
            result_end = 'Связь нарушение. Сервер не мониторится. Выполнение заданий невозможно!'

        embed = discord.Embed(title='Проверка связи...',
                              description=f'{text}\n\n'
                                          f'Дополнительные тесты 5/5\n'
                                          f'{result}\n\n'
                                          f'**{result_end}**', color=clr)
        await msg.edit(embed=embed)


class CheckServer(commands.Cog):
    def __init__(self, py):
        self.py = py

    @commands.command(aliases=['minecraft-check'])
    async def _check_server(self, ctx, server_name):
        if await check_channels(ctx):
            if server_name in server:
                await checking(ctx, server_name)
            else:
                embed = discord.Embed(title=failure,
                                      description='Я не нашел такого сервера...',
                                      color=FAILURE_COLOR)
                await ctx.reply(embed=embed)


def setup(py):
    py.add_cog(CheckServer(py))
