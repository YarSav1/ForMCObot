import asyncio

import discord
from discord.ext import commands

from DataBase.global_db import DB_SERVER_SETTINGS
from config.functional import failure, accept, super_admin


class SettingsChannels(commands.Cog):
    def __init__(self, py):
        self.py = py

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.command(aliases=['add-channel', 'добавить-канал'])
    @commands.has_permissions(administrator=True)
    async def _add_channel_for_bot(self, ctx, channel: discord.TextChannel = None):
        if ctx.author.id not in super_admin:
            await ctx.reply('Упс, Вы не супер-админ для такой команды :)')
        else:
            if channel is None:
                await ctx.reply(f'{failure} Укажите текстовый канал! {failure}')

            else:
                channels = list(DB_SERVER_SETTINGS.find_one({'_id': 'Goodie'})['bot_channel'])
                if channel.id not in channels:
                    DB_SERVER_SETTINGS.update_one({'_id': 'Goodie'},
                                                  {'$push': {'bot_channel': channel.id}})
                    await ctx.reply(f'{accept} Текстовый канал <#{channel.id}> успешно добавлен в разрешенные! {accept}')
                else:
                    await ctx.reply(f'{failure} Текстовый канал <#{channel.id}> уже добавлен в разрешенные! {failure}')


    @_add_channel_for_bot.error
    async def error_channel(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(f'{failure}, у Вас недостаточно прав! {failure}')
        elif isinstance(error, commands.ChannelNotFound):
            await ctx.reply(f'{failure}, мне не удалось найти этот текстовый канал! {failure}')

    @commands.command(aliases=['remove-channel', 'удалить-канал'])
    async def _remove_channel_for_bot(self, ctx, channel: discord.TextChannel = None):
        if ctx.author.id not in super_admin:
            await ctx.reply('Упс, Вы не супер-админ для такой команды :)')
        else:
            if channel is None:
                await ctx.reply(f'{failure} Укажите текстовый канал! {failure}')
            else:
                channels = list(DB_SERVER_SETTINGS.find_one({'_id': 'Goodie'})['bot_channel'])
                if channel.id in channels:
                    DB_SERVER_SETTINGS.update_one({'_id': 'Goodie'},
                                                  {'$pull': {'bot_channel': channel.id}})
                    await ctx.reply(f'{accept} Канал успешно удален из разрешенных! {accept}')
                else:
                    text_channel = ''
                    for i in channels:
                        text_channel += f'**{channels.index(i)}:** <#{i}>\n'
                    await ctx.reply(f'{failure} Такого текстового канала в бд не нашлось! {failure} '
                                    f'Проверьте еще раз правильность вводимых '
                                    f'аргументов!\n'
                                    f'Вот список разрешенных каналов для бота:\n'
                                    f'{text_channel}')
    @_remove_channel_for_bot.error
    async def error_channel(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(f'{failure}, у Вас недостаточно прав! {failure}')
        elif isinstance(error, commands.ChannelNotFound):
            channels = list(DB_SERVER_SETTINGS.find_one({'_id': 'Goodie'})['bot_channel'])
            text_channel = ''
            for i in channels:
                text_channel += f'**{channels.index(i)}:** <#{i}>\n'
            await ctx.reply(f'{failure} Такого текстового канала в бд не нашлось! {failure}'
                            f'Проверьте еще раз правильность вводимых '
                            f'аргументов!\n'
                            f'Вот список действительных разрешенных каналов для бота:\n'
                            f'{text_channel}')

    # ==================================================================================================================
    # ==================================================================================================================
    # ==================================================================================================================
    # ==================================================================================================================
    # ==================================================================================================================

    @commands.command(aliases=['idea+', 'идеи+', 'идея+'])
    @commands.has_permissions(administrator=True)
    async def _add_channel_for_idea(self, ctx, channel: discord.TextChannel = None):
        if ctx.author.id not in super_admin:
            await ctx.reply('Упс, Вы не супер-админ для такой команды :)')
        else:
            if channel is None:
                await ctx.reply(f'{failure} Укажите текстовый канал! {failure}')

            else:
                channels = list(DB_SERVER_SETTINGS.find_one({'_id': 'Goodie'})['idea_channel'])
                if channel.id not in channels:
                    DB_SERVER_SETTINGS.update_one({'_id': 'Goodie'},
                                                  {'$push': {'idea_channel': channel.id}})
                    await ctx.reply(f'{accept} Текстовый канал <#{channel.id}> теперь для создания идей! {accept}')
                else:
                    await ctx.reply(f'{failure} Текстовый канал <#{channel.id}> уже для идей! {failure}')


    @_add_channel_for_idea.error
    async def error_channel_idea(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(f'{failure}, у Вас недостаточно прав! {failure}')
        elif isinstance(error, commands.ChannelNotFound):
            await ctx.reply(f'{failure}, мне не удалось найти этот текстовый канал! {failure}')

    @commands.command(aliases=['idea-', 'идея-', 'идеи-'])
    async def _remove_channel_for_idea(self, ctx, channel: discord.TextChannel = None):
        if ctx.author.id not in super_admin:
            await ctx.reply('Упс, Вы не супер-админ для такой команды :)')
        else:
            if channel is None:
                await ctx.reply(f'{failure} Укажите текстовый канал! {failure}')
            else:
                channels = list(DB_SERVER_SETTINGS.find_one({'_id': 'Goodie'})['idea_channel'])
                if channel.id in channels:
                    DB_SERVER_SETTINGS.update_one({'_id': 'Goodie'},
                                                  {'$pull': {'idea_channel': channel.id}})
                    await ctx.reply(f'{accept} Канал успешно удален из "Канал для идей"! {accept}')
                else:
                    text_channel = ''
                    for i in channels:
                        text_channel += f'**{channels.index(i)}:** <#{i}>\n'
                    await ctx.reply(f'{failure} Такого текстового канала в бд не нашлось! {failure} '
                                    f'Проверьте еще раз правильность вводимых '
                                    f'аргументов!\n'
                                    f'Вот список разрешенных каналов для бота:\n'
                                    f'{text_channel}')
    @_remove_channel_for_idea.error
    async def error_channel_idea(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(f'{failure}, у Вас недостаточно прав! {failure}')
        elif isinstance(error, commands.ChannelNotFound):
            channels = list(DB_SERVER_SETTINGS.find_one({'_id': 'Goodie'})['idea_channel'])
            text_channel = ''
            for i in channels:
                text_channel += f'**{channels.index(i)}:** <#{i}>\n'
            await ctx.reply(f'{failure} Такого текстового канала в бд не нашлось! {failure}'
                            f'Проверьте еще раз правильность вводимых '
                            f'аргументов!\n'
                            f'Вот список действительных разрешенных каналов для бота:\n'
                            f'{text_channel}')

def setup(py):
    py.add_cog(SettingsChannels(py))
