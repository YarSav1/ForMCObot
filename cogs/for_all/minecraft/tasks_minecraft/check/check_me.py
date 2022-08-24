import asyncio

import discord
from discord.ext import commands

from config import config_b
from config.functional_config import check_fields, FAILURE_COLOR, failure


class CheckMeInMinecraft(commands.Cog):
    def __init__(self, py):
        self.py = py

    @commands.command(aliases=['see-me'])
    async def test_(self, ctx):
        info = await check_fields(ctx.author)
        if len(info['ds-minecraft']) == 0:
            embed = discord.Embed(title=failure,
                                  description='У Вас нет привязанного аккаунта в майнкрафте!\n'
                                              'Привяжите аккаунт командой `!auth-ds-minecraft`!',
                                  color=FAILURE_COLOR)
            await ctx.reply(embed=embed)
        else:
            msg = await ctx.reply(f'Ищу...')
            nick = info['ds-minecraft'][1]
            config_b.check_players.append([nick])
            old_text = ''
            timeout = 0
            while timeout != 60:
                await asyncio.sleep(0.5)
                timeout += 1
                text = ''
                for i in config_b.check_players:
                    if i[0] == nick:
                        new_doc = i
                        for args in range(1, len(new_doc)):
                            text += f'Сервер: {new_doc[args][0]}. `x: {new_doc[args][1]}` | `z: {new_doc[args][2]}`\n'
                if old_text != text:
                    old_text = text
                    await msg.edit(text)
            await msg.reply('Сеанс окончен.')

def setup(py):
    py.add_cog(CheckMeInMinecraft(py))