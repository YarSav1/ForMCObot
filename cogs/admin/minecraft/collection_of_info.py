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
                config_b.create_text_coord = False
                config_b.text_coordinates = []
                self.information_delay.stop()
                self.timer = 60
            else:
                self.ctx = ctx
                self.check_delay = True
                config_b.create_text_coord = True
                await ctx.reply("После окончания действующей обработки начнется вывод статистики в этот чат!\n"
                                "**Скорость отклика бота снижена!**")
                self.information_delay.start()

    @commands.Cog.listener()
    async def on_ready(self):
        if self.py.is_ready():
            pass

    @tasks.loop(seconds=1)
    async def information_delay(self):
        if self.check_delay:
            self.timer -= 1
            if len(config_b.text_coordinates) != 0:
                embed = discord.Embed(title='Парсинг серверов.', color=GENERAL_COLOR)
                if self.msg is None:
                    embed.description=f'{config_b.text_coordinates[len(config_b.text_coordinates)-1]}\n\n'\
                                      f'Сеанс прекратится через: {self.timer} сек.'
                    self.msg = await self.ctx.send(embed=embed)
                else:
                    if self.timer > 0:
                        embed.description = f'{config_b.text_coordinates[len(config_b.text_coordinates)-1]}\n\n'\
                                            f'Сеанс прекратится через: {self.timer} сек.'
                        await self.msg.edit(embed=embed)
                    else:
                        embed.description = f'{config_b.text_coordinates[len(config_b.text_coordinates)-1]}\n\n'\
                                            f'Сеанс окончен.'
                        await self.msg.edit(embed=embed)
                        config_b.text_coordinates = []
                        config_b.create_text_coord = False
                        self.information_delay.stop()
                        self.ctx = None
                        self.check_delay = False
                        self.msg = None
                        self.timer = 60


def setup(py):
    py.add_cog(CollectionInfoPlayers(py))
