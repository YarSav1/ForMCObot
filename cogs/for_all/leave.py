from discord.ext import commands

from DataBase.global_db import DB_GAME
from config.functional import remove_waifu_and_get_balance


class LeaveServer(commands.Cog):
    def __init__(self, py):
        self.py = py

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        search_leave_member = {'id_member': member.id}
        info = DB_GAME.find_one(search_leave_member)
        if len(info['waifs']) != 0: # Если выйдет - потеряет всех вайфу.
            for waifu in info['waifs']:
                DB_GAME.update_one({'id_member': waifu['id_member']},
                                   {'$set': {'owner': 0}})
        # if info['owner'] != 0: # Владелец вышедшего потеряет вайфу
        #     returned_balance = int((info['price'] // 100)) * remove_waifu_and_get_balance
        #     DB_GAME.update_one({'id_member': info['owner']},
        #                        {'$inc': {'balance': returned_balance}})
        #     DB_GAME.update_one(search_leave_member,
        #                        {'$set': {'owner': 0}})



def setup(py):
    py.add_cog(LeaveServer(py))