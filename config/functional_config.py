"""""
!!!ВНИМАНИЕ!!! Все выигрыши в этом файле прокоментированы с учетом СТАВКИ.
Код с игрой в дальнейшем убирает ставку из выигрыша - получается ЧИСТЫЙ выигрыш
числа обернутые в int() - нужно оставлять ЦЕЛОЧИСЛЕННЫМИ. В остальных случаях ставьте хоть по 100500 чисел после нуля
!!!НО!!! Код в дальнейшем будет переводить число в int() =) Никаких копеек! А то все слетит к херам(наверное)
"""""
import datetime

import discord

from DataBase.global_db import DB_SERVER_SETTINGS, DB_GAME, DB_IDEA_MEMBERS, LOGS_ERROR

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/87.0.4280.88 Safari/537.36',
           'accept': '*/*'}
# ID участников, которые будут иметь доступ к закрытым командам

super_admin = [280303417568788482, 434972774394494976, 313583698513756161]  # Ярик-Рома-Вячеслав...

len_status = int(20)

remove_waifu_and_get_balance = int(30)  # процент возвращаемых средств при личном отказе от вайфу и при выходе участника
buy_waifu_and_get_balance = int(50)  # процент возвращаемых средств при перекупе вайфу

win_ET = int(50)  # Это вероятность выигрыша в игре "Орел и Решка"
win_ET_balance = int(90)  # Это процент выигрыша(%) с игры "Орел и Решка" (Ставка+коэф. от ставки)
ET_shuffle = int(10)  # Сколь раз перемешивать массив для случайного исхода

# Слева выигрыш в процентах от ставки, справа число, после которого засчитывается выигрыш.
# То есть если выпало число больше, чем число справа - начинаются выигрыши
win_DG_balance_and_place1 = [int(200), int(57)]
win_DG_balance_and_place2 = [int(400), int(81)]
win_DG_balance_and_place3 = [int(1000), int(90)]

left_page = '⬅'
right_page = '➡'


def shop_bounty_massive():
    shop_bounty = [['🥔', 'Картошка', int(10)],
                   ['🥖', 'Батон', int(30)],
                   ['🌹', 'Роза', int(50)],
                   ['🌮', 'Тако', int(50)],
                   ['🥛', 'Молоко', int(25)],
                   ['🍫', 'Шоколадка', int(100)],
                   ['🍣', 'Суши/Роллы', int(1000)],
                   ['🍉', 'Арбуз', int(150)],
                   ['🎟', 'Билет', int(75)],
                   ['📔', 'Книга', int(500)],
                   ['🐶', 'Пёсик', int(5000)],
                   ['💄', 'Помада', int(2500)],
                   ['📱', 'Iphone', int(10000)],
                   ['💻', 'MacBook', int(25000)],
                   ['🎹', 'Пианино', int(3000)],
                   ['💍', 'Кольцо', int(7500)],
                   ['🏠', 'Дом', int(50000)],
                   ['🚀', 'Ракета', int(100000)],
                   ['🍪', 'Печенька', int(15)],
                   ['🍭', 'Леденец', int(20)],
                   ['🍺', 'Пиво', int(200)],
                   ['💌', 'Открытка', int(50)],
                   ['🍕', 'Пицца', int(500)],
                   ['🍦', 'Мороженое', int(60)],
                   ['🍚', 'Рис', int(40)],
                   ['🍱', 'Бэнто', int(2000)],
                   ['🍰', 'Тортик', int(500)],
                   ['🐱', 'Котик', int(5000)],
                   ['🐼', 'Панда', int(75000)],
                   ['👛', 'Кошелёк', int(1000)],
                   ['👗', 'Платье', int(9000)],
                   ['🎻', 'Скрипка', int(75000)],
                   ['🚗', 'Машина', int(250000)],
                   ['🛳', 'Корабль', int(700000)],
                   ['🚁', 'Вертолёт', int(1200000)],
                   ['🌕', 'Луна', int(10000000)]]

    def c_key(element):
        return element[2]

    shop_bounty.sort(key=c_key)
    return shop_bounty


failure = '❌'
accept = '✅'

loading = '🔄'

like_emj = '👍'
dislike_emj = '👎'

FAILURE_COLOR = 0xdc5c56
SUCCESS_COLOR = 0x7acc58
GENERAL_COLOR = 0xfde910

money_emj = '🍪'
lvl_emj = '⭐'
exp_emj = '💠'

#  Кол-во объектов на одной странице в магазинах МАКСИМУМ 10 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
amount_shop_roles = int(9)  # Роли
amount_shop_bounty = int(9)  # Подарки

slots_emj = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣']  # В последнем слоте находитсят ПОБЕДНАЯ эмодзи
# (эмодзи можно убавить и прибавить на свое усмотрение)
slots_factor = int(100)  # множитель одной ПОБЕДНОЙ эмодзи В ПРОЦЕНТАХ |ставка+(ставка(1%)*(КолВоЭмодзи*множитель))
slots_column = int(5)  # Кол-во колонн в рулетке
win_slots = False  # выроятность выпадения последнего слота в slots_emj(т.е. победной эмодзи) в каждой колонне
# (поставьте False для полнейшего рандома)
slot_shuffle = int(10)  # сколько раз перемешать массив для случайного исхода

wheel_field = [
    [int(150), '↖'], [int(10), '⬆'], [int(240), '↗'],
    [int(20), '⬅'], None, [int(120), '➡'],
    [int(170), '↙'], [int(30), '⬇'], [int(50), '↘']
]  # Тута можно менять процент выигрыша от ставки(менять значения в int() СТРЕЛКИ НЕ ТРОГАТЬ!!11!!1!)

exp_from_games = [0, 10]  # Укажите сколько опыта будет выдаваться за каждую игру. От (число слева) до (число справа)


async def check_channels(ctx):
    if ctx.channel.id in DB_SERVER_SETTINGS.find_one({'_id': 'Goodie'})['bot_channel']:
        return True
    else:
        return False


async def add_doc_in_db(id_member: int, name_field: str, amount):
    DB_GAME.update_one({'id_member': id_member},
                       {'$set': {f'{name_field}': amount}})


async def check_fields(author):  # Чертовски медленная функция, но вполне удобная ( я прост ламер :) )
    info = DB_GAME.find_one({'id_member': author.id})
    success = True
    try:
        info['active']
    except Exception as exc:
        print(exc)
        await add_doc_in_db(author.id, 'active', True)
        success = False
    try:
        info['status']
    except Exception as exc:
        print(exc)
        await add_doc_in_db(author.id, 'status', 'Новичок')
        success = False
    try:
        info['balance']
    except Exception as exc:
        print(exc)
        await add_doc_in_db(author.id, 'balance', 100)
        success = False

    try:
        info['lvl']
    except Exception as exc:
        print(exc)
        await add_doc_in_db(author.id, 'lvl', 1)
        success = False

    try:
        info['exp']
    except Exception as exc:
        print(exc)
        await add_doc_in_db(author.id, 'exp', 0)
        success = False

    try:
        info['waifs']
    except Exception as exc:
        print(exc)
        await add_doc_in_db(author.id, 'waifs', [])
        success = False

    try:
        info['like']
    except Exception as exc:
        print(exc)
        await add_doc_in_db(author.id, 'like', 0)
        success = False

    try:
        info['owner']
    except Exception as exc:
        print(exc)
        await add_doc_in_db(author.id, 'owner', 0)
        success = False
    try:
        info['present']
    except Exception as exc:
        print(exc)
        await add_doc_in_db(author.id, 'present', [])
        success = False
    try:
        info['price']
    except Exception as exc:
        print(exc)
        await add_doc_in_db(author.id, 'price', 2000)
        success = False
    try:
        info['et']
    except Exception as exc:
        print(exc)
        await add_doc_in_db(author.id, 'et', [0, 0])
        success = False
    try:
        info['gd']
    except Exception as exc:
        print(exc)
        await add_doc_in_db(author.id, 'gd', [0, 0])
        success = False
    try:
        info['slots']
    except Exception as exc:
        print(exc)
        await add_doc_in_db(author.id, 'slots', [0, 0])
        success = False
    try:
        info['wheel']
    except Exception as exc:
        print(exc)
        await add_doc_in_db(author.id, 'wheel', [0, 0])
        success = False
    try:
        info['buy_roles']
    except Exception as exc:
        print(exc)
        await add_doc_in_db(author.id, 'buy_roles', [])
        success = False
    try:
        info['ds-minecraft']
    except Exception as exc:
        print(exc)
        await add_doc_in_db(author.id, 'ds-minecraft', [])
        success = False
    try:
        info['minecraft-coordinates']
    except Exception as exc:
        print(exc)
        await add_doc_in_db(author.id, 'minecraft-coordinates', [])
        success = False
    try:
        info['minecraft-login-1-in-day']
    except Exception as exc:
        print(exc)
        await add_doc_in_db(author.id, 'minecraft-login-1-in-day', False)
        success = False
    try:
        info['minecraft-login-many']
    except Exception as exc:
        print(exc)
        await add_doc_in_db(author.id, 'minecraft-login-many', [])
        success = False
    if not success:
        info = DB_GAME.find_one({'id_member': author.id})
    return info


async def lvl_up(ctx, exp=None, request=None):
    search = {'id_member': ctx.id}
    info = DB_GAME.find_one(search)

    now_exp = int(info['exp'])
    now_lvl = int(info['lvl'])

    need_exp_for_lvl = int((100 * now_lvl) + (((100 * now_lvl) / 100) * 95))
    if request == 1:
        return need_exp_for_lvl
    else:
        if int(now_exp + exp) >= need_exp_for_lvl:
            bonus_balance = int((now_lvl + 1) * 100)

            rest_exp = int((now_exp + exp) - need_exp_for_lvl)
            DB_GAME.update_one(search,
                               {'$inc': {'balance': bonus_balance}})
            DB_GAME.update_one(search,
                               {'$inc': {'lvl': 1}})
            DB_GAME.update_one(search,
                               {'$set': {'exp': rest_exp}})
            embed = discord.Embed(title=f'{accept}',
                                  description=f'Поздравляю! Вы достигли **{now_lvl + 1}** {lvl_emj} уровня!\n'
                                              f'Получено **{bonus_balance}** {money_emj}',
                                  color=SUCCESS_COLOR)
            await ctx.send(embed=embed)
        else:
            DB_GAME.update_one(search,
                               {'$inc': {'exp': exp}})


async def get_balancetop(request, form_db):
    factor_start, factor_end = 0, 10
    docs = list(DB_GAME.find().sort('balance', -1))
    if len(docs) < factor_end:
        factor_end = len(docs)
    if request == 1:
        number = docs.index(form_db) + 1
        return number


async def get_lvltop(request, form_db):
    factor_start, factor_end = 0, 10
    docs = list(DB_GAME.find().sort('lvl', -1))
    if len(docs) < factor_end:
        factor_end = len(docs)
    if request == 1:
        number = docs.index(form_db) + 1
        return number


async def list_commands(ctx, admin=None):
    if admin:
        text_commands = \
            'Внутриботовские команды\n' \
            '`!чек` - Проверка и безопасная перезагрузка(без сброса активности). Работают ли все файлы?\n' \
            '`!restart` - Полная перезагрузка бота(Без обратной связи. Если бот не запустился -> идем на хост)\n' \
            '`!off` - ассинхронный отруб всего бота(Последующий запуск только через хост).' \
            '\n\n' \
            'Экономика\n' \
            '`add-money`(или `+`) `m` `a` - `m - участник сервера` `a - кол-во средств для добавления`. Добавить баланса участнику.\n' \
            '`reduce-money`(или `-`) `m` `a` - `m - участник сервера` `a - кол-во средств для уменьшения`. Забрать баланса у участника.' \
            '\n\n' \
            'Вайфу\n' \
            '`!reduce-waifu` `m1` `m2` - Убрать вайфу `m2` у участника `m1`.(без компенсации)' \
            '\n\n' \
            'Роли\n' \
            '`!add-shop` `r` `n` - `r - роль` `n - стоимость роли`. Добавить роль в магазин в конец списка.\n' \
            '`!add-shop` `r` `n` `t` - `r - роль` `n - стоимость роли` `t - индекс места, куда добавлять роль`. Добавить роль в магазин в определенное место.\n' \
            '`!remove-shop` `r` - `r - роль`. Удалить роль из магазина(При существовании дупликата – удалит все одинаковые роли).\n' \
            '`!add-role` `участник` `role` - чтобы выдать роль участнику. Роль будет записана в документ с участником! Роль будет считаться купленной в магазине! Команда не работает на вышедших с сервера участниках!\n' \
            '`!remove-role` `участник` `role` - чтобы убрать роль у участника. Hоль будет удалена из документа с участником. Если роль была куплена и удалена этой командой - то роль нужно будет покупать по новой! Команда работает на **вышедших** с сервера участниках!' \
            '\n\n' \
            'Настройки\n' \
            '`!add-channel` `channel` - `channel - id или название или упомяните канал`. Добавитьв разрешенный канал для команд бота.\n' \
            '`!remove-channel` `channel` - `channel - id или название или упомяните канал`. Убрать разрешенный канал для команд бота.' \
            '\n\n' \
            'Полезные винтики:\n' \
            '`!с-о` - создать канал статистику. Показывает онлайн серверов МКО.\n' \
            '`!прослушка` - выводит время парсинга каждого сервера.' \
            '\n\n' \
            'Общедоступные\n' \
            '`!bot` - проверка отклика бота.\n' \
            ''
        embed = discord.Embed(title=f'Команды бота(SuperAdmin)',
                              description=f'{text_commands}',
                              color=GENERAL_COLOR)

        await ctx.reply(embed=embed)
    else:
        text_commands = \
            f'Казино:\n' \
            f'`!профиль` - проверить информацию.\n' \
            f'`!профиль` `участник` - проверить информацию участника.\n' \
            f'`!баланс` - быстрый просмотр своего баланса.\n' \
            f'`!передать` `участник` `n` - передать баланс участнику. `n - сумма`\n\n' \
            f'`!ор h/t n` - сыграть в "Орёл и Решка". `h - орел`, `t - решка`, `n - ставка`\n' \
            f'`!br n` - сыграть в "Кости". `n - ставка`\n' \
            f'`!slot n` - сыграть в "Слоты". `n - ставка`\n' \
            f'`!wheel n` - сыграть в "Колесо удачи" `n - ставка`' \
            f'\n\n' \
            f'Вайфу:\n' \
            f'`!вайфу` - проверить информацию.\n' \
            f'`!вайфу` `участник` - проверить информацию участника.\n' \
            f'`!вайфу` `участник` `n` - купить вайфу. `n - сумма`\n' \
            f'`!список-вайфу` - проверить полный список вайфу.\n' \
            f'`!список-вайфу` `участник` - проверить полный список вайфу участника.\n' \
            f'`!отказаться-вайфу` `участник` - убрать вайфу из своего списка, вернув {remove_waifu_and_get_balance}% от ее стоимости' \
            f'\n\n' \
            f'Магазины:\n' \
            f'`!shop-roles` - магазин ролей. Сокращённо: `!sr`\n' \
            f'`!buy-role` `n` - купить роль. `n - номер роли в магазине`. \n' \
            f'`!shop-bounty` - магазин подарков. Сокращённо: `!sb`\n' \
            f'`!buy-bounty` `m` `n` - купить подарок участнику. `m - участник` `n - номер подарка в магазине`' \
            f'\n\n' \
            f'Общее:\n' \
            f'`!статус` `текст` - установить статус в профилях.' \
            f'\n\n' \
            f'Майнкрафт:\n' \
            f'`!auth-ds-minecraft` - связка дискорд аккаунта с аккаунтом в майнкрафте.\n' \
            f'`!minecraft-check` `s` - `s - сервер` **ТОЧНОЕ НАЗВАНИЕ**. Проверка сервера, можно ли выполнять задания.\n' \
            f'`!see-me` - бот покажет на каком(каких) сервере(ах) Вы находитесь и Ваши координаты на нем(них)'
        embed = discord.Embed(title=f'Команды бота',
                              description=f'{text_commands}',
                              color=GENERAL_COLOR)
        if ctx.author.id in super_admin:
            embed.set_footer(text='Вы имеете доступ к команде !adminhelp')

        await ctx.reply(embed=embed)


def counter_number(number):
    number = f'{number:,.0f}'.replace(',', '.')
    return number


payload = {  # НЕ ТРОГАТЬ - Аккаунт для отправки верификационного кода на форуме(связка дискорд-майнкрафт)
    'login_name': 'ChakaBot',
    'login_password': 'Nitro2000',
    'login_from_forum': 1,
    'login': 'submit'
}


def form_send(token, nick, CODE_VER):  # НЕ ТРОГАТь
    payload_send = {
        'recipients': f'{nick}',
        'title': 'Верификация',
        'message_backup': f'Пароль для подтверждения связки аккунта дискорд с аккаунтом в майнкрафте: {CODE_VER}',
        'message': f'Пароль для подтверждения связки аккунта дискорд с аккаунтом в майнкрафте: {CODE_VER}',
        'wysiwyg': 0,
        's': None,
        'securitytoken': str(token),
        'do': 'insertpm',
        'pmid': None,
        'forward': None,
        'sbutton': '%D0%9E%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D1%82%D1%8C+%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D0%B5',
        'savecopy': 1,
        'parseurl': 1,
        's': None,
        'securitytoken': str(token),
        'do': 'insertpm',
        'pmid': None,
        'forward': None
        # На ошибки внимания не обращать! Я не ебу, что у форума с формой POST запроса, другую не принимает
    }
    return payload_send


class LikeDislike(discord.ui.View):
    def __init__(self, *, timeout=None, py):
        super().__init__(timeout=timeout)
        self.py = py

    @discord.ui.button(emoji=like_emj, style=discord.ButtonStyle.green, custom_id='LikeIdea')
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.channel.id in DB_SERVER_SETTINGS.find_one({'_id': 'Goodie'})['idea_channel']:
            doc = DB_IDEA_MEMBERS.find_one({'msg': interaction.message.jump_url})
            author_click = interaction.user
            if author_click.id in doc['dislike']:
                embed = await create_block_idea(self.py.get_user(doc['author']), doc['title'], doc['text'],
                                                doc['footer'], (len(doc['like']) + 1), (len(doc['dislike']) - 1), 'No')
                await interaction.response.edit_message(embed=embed, view=self)

                DB_IDEA_MEMBERS.update_one({'msg': doc['msg']},
                                           {'$push': {'like': author_click.id}})
                DB_IDEA_MEMBERS.update_one({'msg': doc['msg']},
                                           {'$pull': {'dislike': author_click.id}})
            elif author_click.id in doc['like']:
                # embed = await create_block_idea(self.py.get_user(doc['author']), doc['title'], doc['text'],
                #                                 doc['footer'], (len(doc['like'])), (len(doc['dislike'])), 'No')
                await interaction.response.edit_message(view=self)

                DB_IDEA_MEMBERS.update_one({'msg': doc['msg']},
                                           {'$push': {'dislike': author_click.id}})
            else:
                embed = await create_block_idea(self.py.get_user(doc['author']), doc['title'], doc['text'],
                                                doc['footer'], (len(doc['like']) + 1), (len(doc['dislike'])), 'No')
                await interaction.response.edit_message(embed=embed, view=self)

                DB_IDEA_MEMBERS.update_one({'msg': doc['msg']},
                                           {'$push': {'like': author_click.id}})

    @discord.ui.button(emoji=dislike_emj, style=discord.ButtonStyle.red, custom_id='DislikeIdea')
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.channel.id in DB_SERVER_SETTINGS.find_one({'_id': 'Goodie'})['idea_channel']:
            doc = DB_IDEA_MEMBERS.find_one({'msg': interaction.message.jump_url})
            author_click = interaction.user
            if author_click.id in doc['dislike']:
                # embed = await create_block_idea(self.py.get_user(doc['author']), doc['title'], doc['text'],
                #                                 doc['footer'], (len(doc['like'])), (len(doc['dislike'])), 'No')
                await interaction.response.edit_message(view=self)
            elif author_click.id in doc['like']:
                embed = await create_block_idea(self.py.get_user(doc['author']), doc['title'], doc['text'],
                                                doc['footer'], (len(doc['like']) - 1), (len(doc['dislike']) + 1), 'No')
                await interaction.response.edit_message(embed=embed, view=self)

                DB_IDEA_MEMBERS.update_one({'msg': doc['msg']},
                                           {'$pull': {'like': author_click.id}})
                DB_IDEA_MEMBERS.update_one({'msg': doc['msg']},
                                           {'$push': {'dislike': author_click.id}})
            else:
                embed = await create_block_idea(self.py.get_user(doc['author']), doc['title'], doc['text'],
                                                doc['footer'], (len(doc['like'])), (len(doc['dislike']) + 1), 'No')
                await interaction.response.edit_message(embed=embed, view=self)

                DB_IDEA_MEMBERS.update_one({'msg': doc['msg']},
                                           {'$push': {'dislike': author_click.id}})


async def create_block_idea(author, title, description, footer, like, dislike, all_=None, py=None):
    if footer is None:
        footer = ''
    else:
        footer = f'{footer}'

    embed = discord.Embed(title=f'{author}\n'
                                f'{title}',
                          description=f'**Описание**\n{description}{footer}\n\n'
                                      f'Пальчики:\n'
                                      f'{like_emj} - {like} | {dislike_emj} - {dislike}',
                          color=GENERAL_COLOR)
    if all_ is None:
        components = LikeDislike(py=py)
        return embed, components
    else:
        return embed

def logger_errors(text):
    doc = {
        'errors': 'Goodie',
        'massive': []
    }
    timenow = datetime.datetime.now()
    timenow = f"{timenow.strftime('%d.%m.%Y %H:%M:%S')}"
    text = f'`{text}`. \nВремя: `{timenow}`'
    # print(text)
    if LOGS_ERROR.count_documents({'errors': 'Goodie'}) == 0:
        LOGS_ERROR.insert_one(doc)
    LOGS_ERROR.update_one({'errors': 'Goodie'},
                          {'$push': {'massive': text}})