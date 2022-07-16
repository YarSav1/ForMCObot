import discord
from discord.ext import commands

from DataBase.global_db import DB_SERVER_SETTINGS
from config.functional import super_admin, GENERAL_COLOR, accept, SUCCESS_COLOR, failure, FAILURE_COLOR


class CreateShop(commands.Cog):
    def __init__(self, py):
        self.py = py

    async def stopper(self, ctx):
        embed = discord.Embed(title='Super-admin',
                              description=f'`!add-shop` `r` `n` `t` - `r - роль сервера` `n - стоимость роли` '
                                          f'`t - место в магазине(необязательно)`\n\n'
                                          f'При использовании команды без `t` - роль добавится в конец списка.',
                              color=GENERAL_COLOR)
        await ctx.reply(embed=embed)

    async def stopper_role(self, ctx):
        embed = discord.Embed(title=f'{failure}',
                              description='Роль не найдена!', color=FAILURE_COLOR)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['add-shop'])
    async def _add_role_for_shop(self, ctx, role: discord.Role = None, amount: int = None, place: int = None):
        if ctx.author.id in super_admin:
            if (role and amount) is None:
                await self.stopper(ctx)
            else:
                massive = list(DB_SERVER_SETTINGS.find_one({'_id': 'Goodie'})['shop_roles'])
                for check in massive:
                    if int(check[0]) == int(role.id):
                        embed = discord.Embed(title=f'{failure} Super-admin',
                                              description=f'Эта роль уже в магазине! Ее место - {massive.index(check)+1}',
                                              color=FAILURE_COLOR)
                        return await ctx.reply(embed=embed)
                if place is None:
                    DB_SERVER_SETTINGS.update_one({'_id': 'Goodie'},
                                                  {'$push': {'shop_roles': [role.id, amount]}})
                else:

                    massive = massive[0:(place - 1)] + [[role.id, amount]] + massive[place-1:]
                    DB_SERVER_SETTINGS.update_one({'_id': 'Goodie'},
                                                  {'$set': {'shop_roles': massive}})

                embed = discord.Embed(title=f'{accept} Super-admin',
                                      description=f'{role.mention} добавлена в магазин!',
                                      color=SUCCESS_COLOR)
                await ctx.reply(embed=embed)

    @_add_role_for_shop.error
    async def _error(self, ctx, error):
        if isinstance(error, commands.RoleNotFound):
            await self.stopper_role(ctx)



    @commands.command(aliases=['remove-shop'])
    async def _remove_role_for_shop(self, ctx, role: discord.Role=None):
        if ctx.author.id in super_admin:
            if role is None:
                embed = discord.Embed(title='Super-admin',
                                      description=f'`!remove-shop` `role` - удалит роль из магазина\n\n'
                                                  f'Если в магазине роль в 2 и более местах - удалит все.',
                                      color=GENERAL_COLOR)
                await ctx.reply(embed=embed)
            else:
                massive = list(DB_SERVER_SETTINGS.find_one({'_id': 'Goodie'})['shop_roles'])
                for check in massive:
                    if int(check[0]) == int(role.id):
                        DB_SERVER_SETTINGS.update_one({'_id': 'Goodie'},
                                                    {'$pull': {'shop_roles': check}})
                        embed = discord.Embed(title=f'{accept} Super-admin',
                                              description=f'Роль удалена из магазина!',
                                              color=SUCCESS_COLOR)
                        return await ctx.reply(embed=embed)

                embed = discord.Embed(title=f'{failure} Super-admin',
                                      description=f'Этой роли нет в магазине!',
                                      color=FAILURE_COLOR)
                return await ctx.reply(embed=embed)

    @_remove_role_for_shop.error
    async def _error(self, ctx, error):
        if isinstance(error, commands.RoleNotFound):
            await self.stopper_role(ctx)


def setup(py):
    py.add_cog(CreateShop(py))
