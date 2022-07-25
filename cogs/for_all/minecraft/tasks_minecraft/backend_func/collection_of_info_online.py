from discord.ext import commands, tasks

from config import config_b
from config.functional_config import super_admin


class CollectionInfoOnlinePlayers(commands.Cog):
    def __init__(self, py):
        self.py = py
        self.text = ''
        self.check_delay = False
        self.msg = None
        self.ctx = None
        self.timer = 60

    @commands.command(aliases=['п-онлайн'])
    async def _check_delay_online(self, ctx):
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
                await ctx.reply("После следующей обработки начнется вывод статистики в этот чат(онлайн)!\n"
                                "**При включенном режиме скорость отклика бота понизится!**")
                self.information_delay_online.start()

    @commands.Cog.listener()
    async def on_ready(self):
        if self.py.is_ready():
            pass

    @tasks.loop(seconds=5)
    async def information_delay_online(self):
        if self.check_delay:
            self.timer -= 5
            if config_b.text_online != '':
                if self.msg is None:
                    self.msg = await self.ctx.send(f'{config_b.text_online}\n\n'
                                                   f'Сеанс прекратится через: {self.timer} сек.')
                    config_b.text_online = ''
                else:
                    if self.timer > 0:
                        await self.msg.edit(f'{config_b.text_online}\n\n'
                                            f'Сеанс прекратится через: {self.timer} сек.')
                        config_b.text_online = ''
                    else:
                        await self.msg.edit(f'{config_b.text_online}\n\nСеанс окончен.')
                        config_b.text_online = ''
                        self.information_delay_online.stop()
                        self.ctx = None
                        self.check_delay = False
                        self.msg = None
                        self.timer = 60


def setup(py):
    py.add_cog(CollectionInfoOnlinePlayers(py))
