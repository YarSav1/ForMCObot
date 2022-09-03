import discord
from discord.ext import commands

from config.functional_config import check_channels, check_fields, failure, FAILURE_COLOR, accept, GENERAL_COLOR


class TasksProfile(commands.Cog):
    def __init__(self, py):
        self.py = py

    @commands.command(aliases=['tasks', 'задания'])
    async def _tasks_minecraft(self, ctx):
        if await check_channels(ctx):
            info = await check_fields(ctx.author)
            if len(info['ds-minecraft']) != 0:
                embed = discord.Embed(title='Ваши задания', color=GENERAL_COLOR)

                if len(info['minecraft-coordinates']) == 0:
                    text = 'Нет заданий'
                else:
                    text = ''
                    for coord in info['minecraft-coordinates']:
                        if coord[2]:
                            perf = accept
                        else:
                            perf = failure
                        text += f'{info["minecraft-coordinates"].index(coord) + 1} | `x:{coord[0]}` | `z: {coord[1]}` - {perf}\n'
                embed.add_field(name='Прибеги на координаты:', value=f'{text}')

                if len(info['minecraft-login-many']) == 0:
                    text = 'Нет задания'
                else:
                    if info["minecraft-login-many"][2]:
                        perf = accept
                    else:
                        perf = failure
                    text = f'Вы зашли {info["minecraft-login-many"][0]} раз из {info["minecraft-login-many"][1]} - ' \
                           f'{perf}'
                embed.add_field(name=f'Зайди на сервер несколько раз:', value=f'{text}')

                if info['minecraft-login-1-in-day']:
                    perf = accept
                else:
                    perf = failure

                text = f'Выполнение - {perf}'
                embed.add_field(name=f'Зайди на сервер один раз.', value=f'{text}', inline=False)

                if len(info['minecraft-kills']) != 0:
                    if info['minecraft-kills'][3]:
                        perf = accept
                    else:
                        perf = failure

                    text = f"Выполнение: убито {info['minecraft-kills'][2]} из {info['minecraft-kills'][1]} - {perf}"
                    embed.add_field(name=f'Убей игроков.', value=f'{text}', inline=False)
                else:
                    text = 'Нет заданий'
                    embed.add_field(name=f'Убей игроков.', value=f'{text}')

                embed.set_footer(text=f'{accept} - задание выполнено | {failure} - задание не выполнено.')

                await ctx.reply(embed=embed)


            else:
                embed = discord.Embed(title=failure,
                                      description='У Вас нет привязанного аккаунта в майнкрафте!',
                                      color=FAILURE_COLOR)
                await ctx.reply(embed=embed)


def setup(py):
    py.add_cog(TasksProfile(py))
