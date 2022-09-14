import asyncio

import discord
from discord.ext import commands

from DataBase.global_db import DB_SERVER_SETTINGS, DB_IDEA_MEMBERS
from config.functional_config import GENERAL_COLOR, FAILURE_COLOR, failure, create_block_idea, accept, SUCCESS_COLOR


# components = [
#                 [
#                     Button(label='Создать идею', id='accept', style=3),
#                     Button(label='Отмена', id='exit', style=4),
#                 ]
#             ]
class verification(discord.ui.View):
    def __init__(self, *, py=None, timeout, msg):
        self.py = py
        super().__init__(timeout=timeout)
        self.message = msg

    @discord.ui.button(label="Создать идею", style=discord.ButtonStyle.green)
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user == self.message.author:
            discord.ui.View.stop(self)
            await self.message.delete()
            await interaction.message.delete()
            await CreateIdea(self).start_idea(self.message.author)
            # message = await self.py.wait_for('message', timeout=60)
            await CreateIdea(self.py).stage_1(self.message.author, self.message.channel)

    @discord.ui.button(label="Отмена", style=discord.ButtonStyle.red)
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user == self.message.author:
            discord.ui.View.stop(self)
            await self.message.delete()
            await interaction.message.delete()

    async def on_timeout(self):
        await self.message.delete()


class btn_stage_1(discord.ui.View):
    def __init__(self, *, py, timeout=60, author=None, channel=None, title=None):
        super().__init__(timeout=timeout)
        self.py = py
        self.author = author
        self.channel = channel
        self.title = title

    @discord.ui.button(label="Подтвердить", style=discord.ButtonStyle.green)
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        discord.ui.View.stop(self)
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(view=self)
        return await CreateIdea(self.py).stage_2(self.author, self.channel, self.title)

    @discord.ui.button(label="Изменить заголовок", style=discord.ButtonStyle.blurple)
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        discord.ui.View.stop(self)
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(view=self)
        return await CreateIdea(self.py).stage_1(self.author, self.channel)

    @discord.ui.button(label="Выход", style=discord.ButtonStyle.red)
    async def button3(self, button: discord.ui.Button, interaction: discord.Interaction):
        discord.ui.View.stop(self)
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(view=self)
        await CreateIdea(self.py).exit(self.author)
        return

    async def on_timeout(self):
        await CreateIdea(self.py).timeout(self.author)


class btn_stage_2(discord.ui.View):
    def __init__(self, *, py, timeout=60, author=None, channel=None, title=None, description=None):
        super().__init__(timeout=timeout)
        self.py = py
        self.author = author
        self.channel = channel
        self.title = title
        self.description = description

    @discord.ui.button(label="Подтвердить", style=discord.ButtonStyle.green)
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        discord.ui.View.stop(self)
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(view=self)
        await CreateIdea(self.py).stage_3_continue(self.author, self.channel, self.title, self.description)

    @discord.ui.button(label="Изменить описание", style=discord.ButtonStyle.blurple)
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        discord.ui.View.stop(self)
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(view=self)
        await CreateIdea(self.py).stage_2(self.author, self.channel, self.title)

    @discord.ui.button(label="Выход", style=discord.ButtonStyle.red)
    async def button3(self, button: discord.ui.Button, interaction: discord.Interaction):
        discord.ui.View.stop(self)
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(view=self)
        await CreateIdea(self.py).exit(self.author)

    async def on_timeout(self):
        await CreateIdea(self.py).timeout(self.author)


class btn_stage_3(discord.ui.View):
    def __init__(self, *, py, timeout=60, author=None, channel=None, title=None, description=None):
        super().__init__(timeout=timeout)
        self.py = py
        self.author = author
        self.channel = channel
        self.title = title
        self.description = description

    @discord.ui.button(label="Буду", style=discord.ButtonStyle.green)
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        discord.ui.View.stop(self)
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(view=self)
        await CreateIdea(self.py).stage_3(self.author, self.channel, self.title, self.description)

    @discord.ui.button(label="Пропустить", style=discord.ButtonStyle.blurple)
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        discord.ui.View.stop(self)
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(view=self)
        await CreateIdea(self.py).stage_end(self.author, self.channel, self.title, self.description, None)

    @discord.ui.button(label="Выход", style=discord.ButtonStyle.red)
    async def button3(self, button: discord.ui.Button, interaction: discord.Interaction):
        discord.ui.View.stop(self)
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(view=self)
        await CreateIdea(self.py).exit(self.author)

    async def on_timeout(self):
        await CreateIdea(self.py).timeout(self.author)


class btn_stage_3_write(discord.ui.View):
    def __init__(self, *, py, timeout=60, author=None, channel=None, title=None, description=None, footer=None):
        super().__init__(timeout=timeout)
        self.py = py
        self.author = author
        self.channel = channel
        self.title = title
        self.description = description
        self.footer = footer

    @discord.ui.button(label="Подтвердить", style=discord.ButtonStyle.green)
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        discord.ui.View.stop(self)
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(view=self)
        await CreateIdea(self.py).stage_end(self.author, self.channel, self.title, self.description, self.footer)

    @discord.ui.button(label="Изменить суть", style=discord.ButtonStyle.blurple)
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        discord.ui.View.stop(self)
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(view=self)
        await CreateIdea(self.py).stage_3(self.author, self.channel, self.title, self.description)

    @discord.ui.button(label="Выход", style=discord.ButtonStyle.red)
    async def button3(self, button: discord.ui.Button, interaction: discord.Interaction):
        discord.ui.View.stop(self)
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(view=self)
        await CreateIdea(self.py).exit(self.author)

    async def on_timeout(self):
        await CreateIdea(self.py).timeout(self.author)


class btn_stage_end(discord.ui.View):
    def __init__(self, *, py, timeout=60, author=None, channel=None, title=None, description=None, footer=None):
        super().__init__(timeout=timeout)
        self.py = py
        self.author = author
        self.channel = channel
        self.title = title
        self.description = description
        self.footer = footer

    @discord.ui.button(label="Отправляем!", style=discord.ButtonStyle.green)
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        discord.ui.View.stop(self)
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(view=self)
        msg_idea = await CreateIdea(self.py).send_idea(author=self.author, channel=self.channel, title=self.title,
                                                       description=self.description, footer=self.footer)
        await CreateIdea(self.py).push_in_db(self.author, self.channel, self.title, self.description,
                                             self.footer, msg_idea)
        embed = discord.Embed(title=f'{accept}',
                              description='Всё отлично! Ваша идея отправлена!',
                              color=SUCCESS_COLOR)
        await self.author.send(embed=embed)
        await msg_idea.create_thread(name='Обсуждение идеи')

    @discord.ui.button(label="Начать заново", style=discord.ButtonStyle.blurple)
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        discord.ui.View.stop(self)
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(view=self)
        await CreateIdea(self.py).stage_1(self.author, self.channel)

    @discord.ui.button(label="Выход", style=discord.ButtonStyle.red)
    async def button3(self, button: discord.ui.Button, interaction: discord.Interaction):
        discord.ui.View.stop(self)
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(view=self)
        await CreateIdea(self.py).exit(self.author)

    async def on_timeout(self):
        await CreateIdea(self.py).timeout(self.author)


class CreateIdea(commands.Cog):
    def __init__(self, py):
        self.py = py

    async def timeout(self, author):
        embed = discord.Embed(title=f'{failure}',
                              description='Время вышло.', color=FAILURE_COLOR)
        await author.send(embed=embed)

    async def exit(self, author):
        embed = discord.Embed(title=f'{failure}',
                              description='Вы отказались от создания идеи.', color=FAILURE_COLOR)
        await author.send(embed=embed)

    async def start_idea(self, author):
        embed = discord.Embed(title='Краткое руководство',
                              description=f'Создание блока идеи будет состоять из 3 стадий:\n'
                                          f'Заголовок - 1 стадия. Кратко заинтересуйте читателя\n'
                                          f'Описание - 2 стадия. Опишите суть идеи.\n'
                                          f'Суть - 3 стадия(необязательно). Самое краткое описание плюсов и минусов(если есть) идеи\n\n'
                                          f'**Через 10 секунд начнется 1 стадия. Приготовьтесь!**')
        await author.send(embed=embed)
        await asyncio.sleep(10)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel.id in DB_SERVER_SETTINGS.find_one({'_id': 'Goodie'})['idea_channel']:
            embed = discord.Embed(title='Подтверждение',
                                  description='Вы хотите создать идею?\n\n'
                                              '**Внимание!!!** В случае создания блока идеи не относящегося к теме – Вы '
                                              'рискуете потерять право создавать их вовсе.', color=GENERAL_COLOR)
            timeout = 60
            await message.reply(embed=embed, view=verification(py=self.py, msg=message, timeout=timeout),
                                delete_after=timeout)

    async def stage_1(self, author, channel):
        embed = discord.Embed(title='1 стадия',
                              description='Давайте дадим заголовок идее. Напишите его.\n'
                                          'Даю Вам минуту на это.',
                              color=GENERAL_COLOR)
        await author.send(embed=embed)

        def check(message):
            if author == message.author:
                if len(message.content) != 0:
                    return message.author == message.author

        try:
            message = await self.py.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            await self.timeout(author)
            return
        title = message.content
        await self.stage_1_accept(author, channel, title)

    async def stage_1_accept(self, author, channel, title):
        embed_author = discord.Embed(title=title)
        embed = discord.Embed(title='Подтверждение',
                              description='Оставляем заголовок? Даю 30 секунд на обдумывание.', color=GENERAL_COLOR)

        await author.send('Ваша идея', embed=embed_author)
        await author.send(embed=embed, view=btn_stage_1(py=self.py, author=author, channel=channel, title=title))

    async def stage_2(self, author, channel, title):
        embed = discord.Embed(title='2 стадия',
                              description='Теперь добавьте описание идее. Даю 5 минут!',
                              color=GENERAL_COLOR)
        await author.send(embed=embed)

        def check(message):
            if author == message.author:
                if len(message.content) != 0:
                    return message.author == message.author

        try:
            message = await self.py.wait_for('message', check=check, timeout=300)
        except asyncio.TimeoutError:
            await self.timeout(author)
            return
        description = message.content
        await self.stage_2_accept(author=author, channel=channel, title=title, description=description)

    async def stage_2_accept(self, author, channel, title, description):
        timeout = 30
        embed_author = discord.Embed(title=title, description=f'**Описание**:\n{description}')
        embed = discord.Embed(title='Подтверждение',
                              description=f'Оставляем описание? Даю {timeout} секунд на обдумывание.',
                              color=GENERAL_COLOR)

        await author.send('Ваша идея', embed=embed_author)
        await author.send(embed=embed,
                          view=btn_stage_2(py=self.py, timeout=timeout, author=author, channel=channel, title=title,
                                           description=description))

    async def stage_3_continue(self, author, channel, title, description):
        timeout = 30
        embed = discord.Embed(title='Подтверждение 3 стадии',
                              description=f'Будем писать суть идеи? Даю {timeout} секунд на обдумывание.',
                              color=GENERAL_COLOR)

        await author.send(embed=embed, view=btn_stage_3(py=self.py, author=author, channel=channel, title=title,
                                                        description=description, timeout=timeout))

    async def stage_3(self, author, channel, title, description):
        embed = discord.Embed(title='3 стадия',
                              description='Напишите плюсы и минусы, кратко охарактеризуйте свою идею. Даю 5 минут!',
                              color=GENERAL_COLOR)
        await author.send(embed=embed)

        def check(message):
            if author == message.author:
                if len(message.content) != 0:
                    return message.author == message.author

        try:
            message = await self.py.wait_for('message', check=check, timeout=300)
        except asyncio.TimeoutError:
            await self.timeout(author)
            return
        footer = message.content
        await self.stage_3_accept(author, channel, title, description, footer)

    async def stage_3_accept(self, author, channel, title, description, footer):
        embed_author = discord.Embed(title=title, description=f'**Описание:**\n{description}\n\n**Суть:**\n{footer}')
        embed = discord.Embed(title='Подтверждение',
                              description='Оставляем суть? Даю 30 секунд на обдумывание.', color=GENERAL_COLOR)

        await author.send('Ваша идея', embed=embed_author)
        await author.send(embed=embed, view=btn_stage_3_write(py=self.py, author=author, channel=channel,
                                                              title=title, description=description, footer=footer))


    async def stage_end(self, author, channel, title, description, footer=None):
        if footer is None:
            footer = ''
        else:
            footer = f'\n\n**Суть**:\n{footer}'
        embed_author = discord.Embed(title=title,
                                     description=f'**Описание**\n{description}{footer}')
        embed = discord.Embed(title='А вот и конец создания.',
                              description='Взгляните на свой блок идеи. Всё ли хорошо?\n'
                                          'К сожалению разработчик ламер и не сделал возможность вернуться к какой-либо'
                                          ' стадии редактирования.\n'
                                          'Подтвердите свою идею и она будет отослана в канал!',
                              color=GENERAL_COLOR)
        await author.send('Ваша идея', embed=embed_author)
        if footer == '':
            footer = None

        await author.send(embed=embed, view=btn_stage_end(py=self.py, author=author, channel=channel, title=title,
                                                          description=description, footer=footer))


    async def send_idea(self, author, channel, title, description, footer):
        embed, components = await create_block_idea(py=self.py, author=author, title=title, description=description,
                                                    footer=footer, like=0, dislike=0)
        msg_idea = await channel.send(embed=embed, view=components)
        return msg_idea

    async def push_in_db(self, author, channel, title, description, footer, msg_idea):
        doc = {
            'author': author.id,
            'channel': channel.id,
            'msg': msg_idea.jump_url,
            'title': title,
            'text': description,
            'footer': footer,
            'like': [],
            'dislike': []
        }
        DB_IDEA_MEMBERS.insert_one(doc)


def setup(py):
    py.add_cog(CreateIdea(py))
