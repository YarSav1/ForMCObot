import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands, tasks

from DataBase.global_db import DB_SERVER_SETTINGS
from config.functional_config import super_admin, GENERAL_COLOR, FAILURE_COLOR, SUCCESS_COLOR, HEADERS
from config.online_config import URL_md, server


class TableModerators(commands.Cog):
    def __init__(self, py):
        self.py = py

    async def _create_channel(self, ctx, msg):
        embed = discord.Embed(title='Создаю канал', color=GENERAL_COLOR)
        await msg.edit(embed=embed)
        try:
            channel = await ctx.guild.create_text_channel(f'Модераторы-проекта')
        except:
            embed = discord.Embed(title='Не могу создать канал. Нет разрешений!', color=FAILURE_COLOR)
            return await msg.edit(embed=embed)
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        overwrite.read_messages = True
        overwrite.connect = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        embed = discord.Embed(title='Канал создан', color=SUCCESS_COLOR)
        await msg.edit(embed=embed)
        DB_SERVER_SETTINGS.update_one({'_id': 'Goodie'},
                                      {'$set': {'table_moderators': channel.id}})
        embed = discord.Embed(title='Канал записан в БД.\n'
                                    'Информация в канале вскоре появится.', color=SUCCESS_COLOR)
        await msg.edit(embed=embed)

    @commands.command(aliases=['таблица-модераторов', 'т-м'])
    async def _create_channel_moderators(self, ctx):
        if ctx.author.id in super_admin:
            embed = discord.Embed(title='Проверяю существование канала', color=GENERAL_COLOR)
            msg = await ctx.reply(embed=embed)

            doc = DB_SERVER_SETTINGS.find_one({'_id': 'Goodie'})
            if 'table_moderators' not in doc:
                await self._create_channel(ctx, msg)
            else:
                channel = ctx.guild.get_channel(DB_SERVER_SETTINGS.find_one({'_id': 'Goodie'})['table_moderators'])
                if channel is None:
                    await self._create_channel(ctx, msg)
                else:
                    embed = discord.Embed(title='Канал уже существует', color=FAILURE_COLOR)
                    await msg.edit(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        if self.py.is_ready():
            self.reload_table_moders.start()

    @tasks.loop(minutes=30)
    async def reload_table_moders(self):
        amount_servers = 3
        doc = DB_SERVER_SETTINGS.find_one({'_id': 'Goodie'})
        if 'table_moderators' in doc:
            id_channel = DB_SERVER_SETTINGS.find_one({'_id': 'Goodie'})['table_moderators']
            channel_ds = self.py.get_channel(id_channel)
            if channel_ds is None:
                return
            await channel_ds.purge(limit=100)

            cycles = int(len(URL_md) / amount_servers + 1)
            for i in range(cycles):
                embed = discord.Embed(title=f'Модератора проекта #{i + 1}', color=GENERAL_COLOR)
                if (i * amount_servers) + amount_servers >= len(URL_md):
                    cycles2 = len(URL_md)
                else:
                    cycles2 = (i * amount_servers) + amount_servers
                for x in range(i * amount_servers, cycles2):
                    text_serv = server[x]
                    html = requests.get(URL_md[x], headers=HEADERS, params=None)
                    if html.status_code == 200:
                        html = html.text
                    else:
                        return
                    soup = BeautifulSoup(html, 'html.parser')
                    spis_md = soup.find_all('tr')
                    cikl = len(spis_md)
                    helpers = ['**Хелперы:** ', False]
                    moders = ['**Модераторы:** ', False]
                    curator = ['**Кураторы:** ', False]
                    headmoder = ['**ХедМодераторы:** ', False]
                    if text_serv == 'HungerGames':
                        curator[0] += '`XxromaxX`, '
                        curator[1] += True
                    for i in range(1, cikl):
                        moder = soup.find_all('tr')[i]
                        moder_name = moder.find_all('td')[1].text
                        moder_rank = moder.find_all('td')[2].text
                        if moder_rank.lower() == 'helper':
                            helpers[0] += f'`{moder_name}`, '
                            helpers[1] += True
                        elif moder_rank.lower() == 'curator':
                            curator[0] += f'`{moder_name}`, '
                            curator[1] += True
                        elif moder_rank.lower() == 'headmoder':
                            headmoder[0] += f'`{moder_name}`, '
                            headmoder[1] += True
                        else:
                            moders[0] += f'`{moder_name}`, '
                            moders[1] += True
                    if not headmoder[1]:
                        headmoder[0] += '`Нет`  '
                    if not helpers[1]:
                        helpers[0] += '`Нет`  '
                    if not moders[1]:
                        moders[0] += '`Нет`  '
                    if not curator[1]:
                        curator[0] += '`Нет`  '
                    text_moders = f'{curator[0][:-2]}\n{headmoder[0][:-2]}\n{moders[0][:-2]}\n{helpers[0][:-2]}'
                    embed.add_field(name=f'| {text_serv} |', value=text_moders)
                await channel_ds.send(embed=embed)


def setup(py):
    py.add_cog(TableModerators(py))
