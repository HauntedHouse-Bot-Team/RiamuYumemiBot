import configparser
import os
import random

import discord
from discord.ext import commands
from src.MyModules import MyModules as myMod

class MyBot(commands.Cog):

    def __init__(self, bot):
        base = os.path.dirname(os.path.abspath(__file__))
        conf_path = os.path.normpath(os.path.join(base, '../config'))
        conf = configparser.ConfigParser()
        conf.read(conf_path+'/config.ini', encoding='utf-8')
        self.bot = bot
        self.bot_id = int(conf['DEFAULT']['BOT_ID'])
        self.icon_url = 'https://cdn.discordapp.com/avatars/{id}/{avatar}.png'

    @commands.command()
    async def hello(self, ctx):
        bot = self.bot.get_user(self.bot_id)
        icon = self.icon_url.format(
            id = str(self.bot_id),
            avatar = bot.avatar,
        )
        embed = discord.Embed(title='こんにちはクズだよ！！', color=0xff66cf)
        embed.set_author(name='夢見りあむ', icon_url=icon)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        bot = self.bot.get_user(self.bot_id)
        icon = self.icon_url.format(
            id = str(self.bot_id),
            avatar = bot.avatar,
        )
        guild = member.guild

        greeting_list = [
            'オタク！ぼくをすこれ！よ！',
            'こんにちはクズだよ！！',
        ]

        embed = discord.Embed(description=random.choice(greeting_list))
        embed.set_author(name='夢見りあむ', icon_url=icon)
        embed.add_field(name='ようこそ！', value=f'{member.mention}', inline=False)

        if guild.name == 'プリムラでムラムラ':
            channel = discord.utils.get(guild.text_channels, name='入場ゲート')
            await channel.send(embed=embed)

        if guild.name == '幽霊屋敷':
            channel = discord.utils.get(guild.text_channels, name='入場ゲート')
            await channel.send(embed=embed)

    @commands.command(name='致した')
    async def masturbation(self, ctx, arg):
        if not arg:
            return False

        mod = myMod()

        bot = self.bot.get_user(self.bot_id)
        usr_name = ctx.author.name
        guild_name = ctx.guild.name

        bot_icon = self.icon_url.format(
            id = str(self.bot_id),
            avatar = bot.avatar,
        )
        icon = self.icon_url.format(
            id = str(ctx.author.id),
            avatar = ctx.author.avatar,
        )

        embed_description = f"{usr_name}が'{arg}'でシコったのを確認したぞ！"
        embed = discord.Embed(title='致した', description=embed_description, color=0xff66cf)
        embed.set_author(name=usr_name, icon_url=icon)
        embed.set_thumbnail(url=bot_icon)
        embed.set_footer(text=f'location: {guild_name}')

        mod.seve_masturbation_log(usr_name, arg, guild_name)
        await ctx.send(embed=embed)

    @commands.command(name='サーバー別致し件数')
    async def masturbation_count_list_by_servers(self, ctx):
        mod = myMod()
        bot = self.bot.get_user(self.bot_id)
        icon = self.icon_url.format(
            id = str(self.bot_id),
            avatar = bot.avatar,
        )
        embed_description = '>>> '
        list_by_guild = mod.get_count_list_by_guild()
        for row in list_by_guild:
            embed_description += f"{row['guild']}: {row['count']}件\n"

        embed = discord.Embed(title='サーバー別致し件数', description=embed_description, color=0xff66cf)
        embed.set_author(name='夢見りあむ', icon_url=icon)
        await ctx.send(embed=embed)

    @commands.command(name='オタク別致し件数')
    async def masturbation_count_list_by_users(self, ctx):
        mod = myMod()
        bot = self.bot.get_user(self.bot_id)
        icon = self.icon_url.format(
            id = str(self.bot_id),
            avatar = bot.avatar,
        )
        embed_description = '>>> '
        list_by_guild = mod.get_count_list_by_user()
        for row in list_by_guild:
            embed_description += f"{row['user']}: {row['count']}件\n"

        embed = discord.Embed(title='オタク別致し件数', description=embed_description, color=0xff66cf)
        embed.set_author(name='夢見りあむ', icon_url=icon)
        await ctx.send(embed=embed)

    @commands.command(name='おかずランキング')
    async def fap_material_ranking_list(self, ctx):
        mod = myMod()
        bot = self.bot.get_user(self.bot_id)
        icon = self.icon_url.format(
            id = str(self.bot_id),
            avatar = bot.avatar
        )
        embed_description = '>>> '
        fap_material_ranking = mod.get_count_list_by_fap_material()
        for row in fap_material_ranking:
            embed_description += f"{row['fap_material']}: {row['count']}回\n"

        embed = discord.Embed(title='おかずランキング', description=embed_description, color=0xff66cf)
        embed.set_author(name='夢見りあむ', icon_url=icon)
        await ctx.send(embed=embed)

    @commands.command(name='オタクのおかずリスト')
    async def fap_material_list_by_user(self, ctx, arg):
        mod = myMod()
        bot = self.bot.get_user(self.bot_id)
        icon = self.icon_url.format(
            id = str(self.bot_id),
            avatar = bot.avatar
        )
        embed_description = '>>> '
        list_by_fap_material = mod.get_list_by_otaku_fap_material(arg)

        if not list_by_fap_material:
            await ctx.send('誰だ？そいつ')
            return False

        for row in list_by_fap_material:
            embed_description += f"{row['user']}: {row['fap_material']} {row['count']}回\n"

        embed = discord.Embed(title='オタクのおかずリスト', description=embed_description, color=0xff66cf)
        embed.set_author(name='夢見りあむ', icon_url=icon)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MyBot(bot))
