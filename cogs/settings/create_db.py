import asyncio

import discord
from discord.ext import commands

from DataBase.global_db import DB_SERVER_SETTINGS, DB_GAME


class CheckingDB(commands.Cog):
    def __init__(self, py):
        self.py = py

    async def universal_check_db(self):
        doc = {
            '_id': 'Goodie',
            'bot_channel': [],
            'idea_channel': [],
            'shop_roles': [],
        }  # МАНИПУЛЯЦИИ С ДАННЫМ ДОКУМЕНТОМ НЕ ПРОВОДИТЬ!!!
        print('\n')
        if DB_SERVER_SETTINGS.count_documents({'_id': 'Goodie'}) == 0:
            print('Создаю начальный документ настроек.')
            DB_SERVER_SETTINGS.insert_one(doc)
            print('Документ создан')

        print('Документ с участниками:')
        print('Фиксирую участников для занесения в БД.')
        on_server = []
        for_db = []
        for guild in self.py.guilds:
            for member in guild.members:
                if not member.bot:
                    on_server.append(member.id)
        print('Достаю участников из БД для проверки.')
        players_DB_request = DB_GAME.find()
        players_code = []
        for i in players_DB_request:
            players_code.append(i['id_member'])
        print('Провожу проверку.')
        for member in on_server:
            if member not in players_code:
                doc = {
                    'id_member': member
                }
                for_db.append(doc)
        if len(for_db) != 0:
            print('Найдено несоответствие. Начинаю занесение в БД.')
            DB_GAME.insert_many(for_db)
            print('Участники занесены!')
        else:
            print('БД соответсвует серверу.')

    @commands.Cog.listener()
    async def on_ready(self):
        if self.py.is_ready():
            await self.universal_check_db()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.universal_check_db()


def setup(py):
    py.add_cog(CheckingDB(py))
