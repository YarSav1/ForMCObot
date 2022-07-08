import asyncio

import discord
from discord.ext import commands

from config.functional import GENERAL_COLOR, amount_shop_bounty, money_emj, counter_number, \
    shop_bounty_massive, left_page, right_page

class one_page_shop(discord.ui.View):
    def __init__(self, *, timeout=60):
        super().__init__(timeout=timeout)

    @discord.ui.button(label=left_page, style=discord.ButtonStyle.red, disabled=True)
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    @discord.ui.button(label=right_page, style=discord.ButtonStyle.red, disabled=True)
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass


class left_no(discord.ui.View):
    def __init__(self, *, py, timeout=60, page, ctx, massive, len_lists):
        super().__init__(timeout=timeout)
        self.py = py
        self.list_shop = page
        self.ctx = ctx
        self.massive = massive
        self.len_lists = len_lists

    @discord.ui.button(label=left_page, style=discord.ButtonStyle.red, disabled=True)
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    @discord.ui.button(label=right_page, style=discord.ButtonStyle.green)
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user == self.ctx.author:
            self.list_shop += 1
            embed, go = await ShopBounty(self.py).pucker(ctx=self.ctx, massive=self.massive, list_shop=self.list_shop,
                                                         len_lists=self.len_lists)
            await interaction.response.edit_message(embed=embed, view=left_and_right(py=self.py, page=self.list_shop,
                                                                                     ctx=self.ctx, massive=self.massive,
                                                                                     len_lists=self.len_lists))

    async def on_timeout(self):
        for btn in self.children:
            btn.disabled = True


class left_and_right(discord.ui.View):
    def __init__(self, *, py, timeout=60, page, ctx, massive, len_lists):
        super().__init__(timeout=timeout)
        self.py = py
        self.list_shop = page
        self.ctx = ctx
        self.massive = massive
        self.len_lists = len_lists

    @discord.ui.button(label=left_page, style=discord.ButtonStyle.green)
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user == self.ctx.author:
            self.list_shop -= 1
            embed, go = await ShopBounty(self.py).pucker(ctx=self.ctx, massive=self.massive, list_shop=self.list_shop,
                                                         len_lists=self.len_lists)
            if self.list_shop != 0:
                await interaction.response.edit_message(embed=embed, view=self)
            else:
                await interaction.response.edit_message(embed=embed, view=left_no(py=self.py, page=self.list_shop,
                                                                                  ctx=self.ctx, massive=self.massive,
                                                                                  len_lists=self.len_lists))

    @discord.ui.button(label=right_page, style=discord.ButtonStyle.green)
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user == self.ctx.author:
            self.list_shop += 1
            embed, go = await ShopBounty(self.py).pucker(ctx=self.ctx, massive=self.massive, list_shop=self.list_shop,
                                                         len_lists=self.len_lists)
            if self.list_shop != self.len_lists-1:
                await interaction.response.edit_message(embed=embed, view=self)
            else:
                await interaction.response.edit_message(embed=embed, view=right_no(py=self.py, page=self.list_shop,
                                                                                   ctx=self.ctx, massive=self.massive,
                                                                                   len_lists=self.len_lists))

    async def on_timeout(self):
        for btn in self.children:
            btn.disabled = True


class right_no(discord.ui.View):
    def __init__(self, *, py, timeout=60, page, ctx, massive, len_lists):
        super().__init__(timeout=timeout)
        self.py = py
        self.list_shop = page
        self.ctx = ctx
        self.massive = massive
        self.len_lists = len_lists

    @discord.ui.button(label=left_page, style=discord.ButtonStyle.green)
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user == self.ctx.author:
            self.list_shop -= 1
            embed, go = await ShopBounty(self.py).pucker(ctx=self.ctx, massive=self.massive, list_shop=self.list_shop,
                                                         len_lists=self.len_lists)
            await interaction.response.edit_message(embed=embed, view=left_and_right(py=self.py, page=self.list_shop,
                                                                                     ctx=self.ctx, massive=self.massive,
                                                                                     len_lists=self.len_lists))

    @discord.ui.button(label=right_page, style=discord.ButtonStyle.red, disabled=True)
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    async def on_timeout(self):
        for btn in self.children:
            btn.disabled = True


class ShopBounty(commands.Cog):
    def __init__(self, py):
        self.py = py

    async def pucker(self, ctx, massive, list_shop, len_lists):
        embed = discord.Embed(title='Магазин Подарков', color=GENERAL_COLOR)
        next_list = False
        if len(massive) < amount_shop_bounty:
            range_list_end = len(massive)
            range_list_start = 0
        else:
            if len(massive) > amount_shop_bounty:
                next_list = True
            range_list_end = (list_shop + 1) * amount_shop_bounty
            if len(massive) < range_list_end:
                range_list_end = len(massive)
            range_list_start = list_shop * amount_shop_bounty
        for i in range(range_list_start, range_list_end):
            index_role = massive[i]
            embed.add_field(name=f'**#{i + 1} - '
                                 f'{index_role[0]} {index_role[1]}**\n',
                            value=f'Цена: **{counter_number(index_role[2])}** {money_emj}')
        embed.set_footer(text=f"Страниц {list_shop + 1}/{len_lists}")
        return embed, next_list

    @commands.command(aliases=['shop-bounty', 'магазин-подарков', 'sb', 'мп'])
    async def _show_all_bounty(self, ctx):
        massive = shop_bounty_massive()
        list_shop = 0
        if len(massive) % amount_shop_bounty != 0:
            len_lists = len(massive) // amount_shop_bounty + 1
        else:
            len_lists = len(massive) // amount_shop_bounty
        embed, go = await self.pucker(ctx, massive, list_shop, len_lists)
        embed.set_footer(text=f"Страниц {list_shop + 1}/{len_lists}")
        if list_shop+1 == len_lists:
            await ctx.reply(embed=embed, view=one_page_shop())
        else:
            await ctx.reply(embed=embed, view=left_no(py=self.py, page=list_shop, ctx=ctx, len_lists=len_lists,
                                                      massive=massive))



def setup(py):
    py.add_cog(ShopBounty(py))
