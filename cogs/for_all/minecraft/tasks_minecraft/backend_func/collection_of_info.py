from discord.ext import commands, tasks

from config import config_b
from config.functional_config import super_admin


class CollectionInfoPlayers(commands.Cog):
    def __init__(self, py):
        self.py = py
        self.text = ''
        self.check_delay = False
        self.msg = None
        self.ctx = None

    @commands.command(aliases=['прослушка'])
    async def _check_delay(self, ctx):
        if ctx.author.id in super_admin:
            if self.check_delay:
                self.ctx = None
                self.check_delay = False
                self.msg = None
                await ctx.reply("Вывод прекращен.")
            else:
                self.ctx = ctx
                self.check_delay = True
                await ctx.reply("После следующей обработки начнется вывод статистики в этот чат!\n"
                                "**При включенном режиме скорость отклика бота понизится!**")

    @commands.Cog.listener()
    async def on_ready(self):
        if self.py.is_ready():
            self.information_delay.start()

    @tasks.loop(seconds=1)
    async def information_delay(self):
        if self.check_delay:
            if config_b.text_coordinates != '':
                if self.msg is None:
                    self.msg = await self.ctx.send(config_b.text_coordinates)
                    config_b.text_coordinates = ''
                else:
                    await self.msg.edit(config_b.text_coordinates)
                    config_b.text_coordinates = ''

    # @commands.command(aliases=['test', 't', "тест"])
    # async def test_(self, ctx, nick):
    #     url = 'http://217.182.201.195:7777/up/world/world/'
    #     msg = await ctx.reply(f'Смотрю Ваши координаты: x: `вычисляется`, y: `вычисляется`, Высота: `вычисляется`')
    #     while True:
    #         html = requests.get(url, headers=HEADERS, params=None)
    #         r = requests.get(url, headers=HEADERS, params=None).text
    #         if html.status_code == 200:
    #             r = json.loads(r)
    #             cikl_online = r["currentcount"]
    #             for i in range(0, cikl_online):
    #                 player = r["players"][i]['name']
    #                 if player == nick:
    #                     await msg.edit(f'Смотрю Ваши координаты: x: `{r["players"][i]["x"]}`, '
    #                                    f'z: `{r["players"][i]["z"]}`, '
    #                                    f'Высота: `{r["players"][i]["y"]}`')
    #                     break
    #         else:
    #             await msg.edit("Повторное подключение...")
    #             await asyncio.sleep(5)
    #
    #         await asyncio.sleep(5)



def setup(py):
    py.add_cog(CollectionInfoPlayers(py))
