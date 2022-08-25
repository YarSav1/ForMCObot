import discord
from discord.ext import commands

from DataBase.global_db import DB_SERVER_SETTINGS
from config.functional_config import super_admin, GENERAL_COLOR, FAILURE_COLOR, SUCCESS_COLOR


class TableModerators(commands.Cog):
    def __init__(self, py):
        self.py = py

    async def _create_channel(self, ctx, msg):
        embed = discord.Embed(title='Создаю канал', color=GENERAL_COLOR)
        await msg.edit(embed=embed)
        try:
            channel = await ctx.guild.create_channel(f'Модераторы-проекта')
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



def setup(py):
    py.add_cog(TableModerators(py))