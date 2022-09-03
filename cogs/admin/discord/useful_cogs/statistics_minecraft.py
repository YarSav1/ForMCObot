import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands, tasks

from DataBase.global_db import DB_SERVER_SETTINGS
from config.functional_config import super_admin, GENERAL_COLOR, FAILURE_COLOR, SUCCESS_COLOR, HEADERS


class SuperAdminChannelStatisticsOnlineMinecraft(commands.Cog):
    def __init__(self, py):
        self.py = py

    @commands.Cog.listener()
    async def on_ready(self):
        if self.py.is_ready():
            self.reload_statistics_online.start()

    async def _create_channel(self, ctx, msg):
        embed = discord.Embed(title='Создаю канал', color=GENERAL_COLOR)
        await msg.edit(embed=embed)
        try:
            count = await self.get_count()
            channel = await ctx.guild.create_voice_channel(f'Онлайн-серверов: {count}')
        except:
            embed = discord.Embed(title='Не могу создать канал. Нет разрешений!', color=FAILURE_COLOR)
            return await msg.edit(embed=embed)
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.connect = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        embed = discord.Embed(title='Канал создан', color=SUCCESS_COLOR)
        await msg.edit(embed=embed)
        DB_SERVER_SETTINGS.update_one({'_id': 'Goodie'},
                                      {'$set': {'stat_online': channel.id}})
        embed = discord.Embed(title='Канал записан в БД', color=SUCCESS_COLOR)
        await msg.edit(embed=embed)

    @commands.command(aliases=['статистика-онлайн', 'с-о', 'c-o'])
    async def _create_channel_online(self, ctx):
        if ctx.author.id in super_admin:
            embed = discord.Embed(title='Проверяю существование канала', color=GENERAL_COLOR)
            msg = await ctx.reply(embed=embed)

            doc = DB_SERVER_SETTINGS.find_one({'_id': 'Goodie'})
            if 'stat_online' not in doc:
                await self._create_channel(ctx, msg)
            else:
                channel = ctx.guild.get_channel(DB_SERVER_SETTINGS.find_one({'_id': 'Goodie'})['stat_online'])
                if channel is None:
                    await self._create_channel(ctx, msg)
                else:
                    embed = discord.Embed(title='Канал уже существует', color=FAILURE_COLOR)
                    await msg.edit(embed=embed)

    async def get_count(self):
        url = 'https://minecraftonly.ru/'
        html = requests.get(url, headers=HEADERS, params=None)
        if html.status_code == 200:
            soup = BeautifulSoup(html.content, 'html.parser')
            f = soup.find(style="color:#000000")
            count = f['data-to']
            return count

    @tasks.loop(minutes=5)
    async def reload_statistics_online(self):
        doc = DB_SERVER_SETTINGS.find_one({'_id': 'Goodie'})
        if 'stat_online' in doc:
            id_channel = DB_SERVER_SETTINGS.find_one({'_id': 'Goodie'})['stat_online']
            channel_ds = self.py.get_channel(id_channel)
            if channel_ds is None:
                return
            count = await self.get_count()
            print(count)
            try:
                await channel_ds.edit(name=f'Онлайн-серверов: {count}')
            except Exception as exc:
                print(exc)
            print('ok')



def setup(py):
    py.add_cog(SuperAdminChannelStatisticsOnlineMinecraft(py))
