import discord
from discord.ext import commands, tasks

from config import config_b
from config.functional_config import super_admin, GENERAL_COLOR


class CollectionInfoPlayers(commands.Cog):
    def __init__(self, py):
        self.py = py
        self.text = ''
        self.check_delay = False
        self.msg = None
        self.ctx = None
        self.timer = 60

    @commands.command(aliases=['прослушка'])
    async def _check_delay(self, ctx):
        if ctx.author.id in super_admin:
            if self.check_delay:
                self.ctx = None
                self.check_delay = False
                self.msg = None
                await ctx.reply("Вывод прекращен.")
                self.information_delay.stop()
                self.timer = 60
            else:
                self.ctx = ctx
                self.check_delay = True
                await ctx.reply("После следующей обработки начнется вывод статистики в этот чат!\n"
                                "**При включенном режиме скорость отклика бота понизится!**")
                self.information_delay.start()

    @commands.Cog.listener()
    async def on_ready(self):
        if self.py.is_ready():
            pass

    @tasks.loop(seconds=5)
    async def information_delay(self):
        if self.check_delay:
            self.timer -= 5
            if config_b.text_coordinates != '':
                embed = discord.Embed(title='Парсинг серверов.', color=GENERAL_COLOR)
                if self.msg is None:
                    embed.description=f'{config_b.text_coordinates}\n\n'\
                                      f'Сеанс прекратится через: {self.timer} сек.'
                    self.msg = await self.ctx.send(embed=embed)
                    config_b.text_coordinates = ''
                else:
                    if self.timer > 0:
                        embed.description = f'{config_b.text_coordinates}\n\n'\
                                            f'Сеанс прекратится через: {self.timer} сек.'
                        await self.msg.edit(embed=embed)
                        config_b.text_coordinates = ''
                    else:
                        embed.description = f'{config_b.text_coordinates}\n\n'\
                                            f'Сеанс окончен.'
                        await self.msg.edit(embed=embed)
                        config_b.text_coordinates = ''
                        self.information_delay.stop()
                        self.ctx = None
                        self.check_delay = False
                        self.msg = None
                        self.timer = 60


def setup(py):
    py.add_cog(CollectionInfoPlayers(py))
