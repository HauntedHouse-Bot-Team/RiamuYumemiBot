import os
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta, timezone
import discord
from discord.ext import commands
from src.MyModules import MyModules as MyMod
from src.UserModules import UserModules as UserMod
import src.WorldCloudModule as world_cloud
from src.NextCloudModules import NextCloudModules as NextCloudMod

class MyBot(commands.Cog):

    def __init__(self, bot):
        base_path = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.join(base_path, '.env')
        load_dotenv(dotenv_path)
        self.bot = bot
        self.bot_id = int(os.getenv('BOT_ID'))
        self.icon_url = 'https://cdn.discordapp.com/avatars/{id}/{avatar}.png'
        self.JST = timezone(timedelta(hours=+9), 'JST')

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
            'ばばーん！りあむちゃんの登場だよ！',
            'Pサマ！ぼくのザコメンタルを傷つけずに育ててほしい！',
        ]

        embed = discord.Embed(description=random.choice(greeting_list))
        embed.set_author(name='夢見りあむ', icon_url=icon)
        embed.add_field(name='ようこそ！', value=f'{member.mention}', inline=False)

        if guild.name == 'プリムラでムラムラ':
            channel = discord.utils.get(guild.text_channels, name='入場ゲート')
            await channel.send(embed=embed)

        if guild.name == '幽霊屋敷':
            channel = discord.utils.get(guild.text_channels, name='玄関')
            await channel.send(embed=embed)
            mod = UserMod()
            ghost = mod.registration_confirm(member.id)
            if ghost:
                mod.member_undelete(member.id)
                now = datetime.strptime(datetime.now(self.JST).strftime("%Y-%m-%d %H:%M:%S.%f"), '%Y-%m-%d %H:%M:%S.%f')
                wet = now - ghost[0]['updated_at']
                embed = discord.Embed(description='入学RTA')
                embed.set_author(name='夢見りあむ', icon_url=icon)
                embed.add_field(name=wet, value=f'{member.mention}', inline=False)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, msg):
        mod = MyMod()
        next_cloud_mod = NextCloudMod()
        if msg.content in ['I am up to no good', '我、よからぬ事をたくらむ者なり']:
            duplication_source_channel = 'われ、よからぬことをたくらむ者なり'
            guild = msg.guild
            channel = discord.utils.get(guild.text_channels, name=duplication_source_channel)
            new_channel = await mod.create_channel(msg, channel, 'いたずら部屋')
            await new_channel.send('@everyone')

        if msg.content in ['Mischief managed', 'いたずら完了'] and msg.channel.name == 'いたずら部屋':
            await mod.delete_channel(msg, 'いたずら完了')

        if '高田憂希' in msg.content:
            files = next_cloud_mod.get_file_list('Photos/takada_yuki')
            filie_path = next_cloud_mod.get_file(random.choice(files), 'takada_yuki.png')
            await msg.channel.send(file=discord.File(filie_path))

        for key_word in ['松井恵理子', 'まつえり']:
            if key_word in msg.content:
                files = next_cloud_mod.get_file_list('Photos/matsueri')
                filie_path = next_cloud_mod.get_file(random.choice(files), 'matsueri.png')
                await msg.channel.send(file=discord.File(filie_path))


    @commands.command(name='致した')
    async def masturbation(self, ctx, arg):
        if not arg:
            return False

        mod = MyMod()

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
        mod = MyMod()
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
        mod = MyMod()
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
        mod = MyMod()
        bot = self.bot.get_user(self.bot_id)
        icon = self.icon_url.format(
            id = str(self.bot_id),
            avatar = bot.avatar
        )
        embed_description = '>>> '
        fap_material_ranking = mod.get_count_list_by_fap_material()
        if not fap_material_ranking:
            return False
        for row in fap_material_ranking:
            embed_description += f"{row['fap_material']}: {row['count']}回\n"

        embed = discord.Embed(title='おかずランキング', description=embed_description, color=0xff66cf)
        embed.set_author(name='夢見りあむ', icon_url=icon)
        await ctx.send(embed=embed)

    @commands.command(name='オタクのおかずリスト')
    async def fap_material_list_by_user(self, ctx, arg):
        mod = MyMod()
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

    @commands.command('おかずの使用頻度可視化')
    async def fap_material_visualization(self, ctx, target: str = ''):
        mod = MyMod()
        fap_material_list: list = []
        photo_file_name: str = ''
        if (not target):
            for row in await mod.load_fap_material():
                fap_material_list.append(row['fap_material'])
            photo_file_name = world_cloud.create_world_cloud(fap_material_list)
        else:
            for row in await mod.get_fap_material_of_nard(target):
                fap_material_list.append(row['fap_material'])
            photo_file_name = world_cloud.create_world_cloud(fap_material_list, target)


        await ctx.send(file=discord.File(photo_file_name))

    # 機能廃止: 2021/11/06
    '''
    @commands.command(name='卒業')
    async def graduate(self, ctx, arg):
        for row in ctx.author.roles:
            if row.name == 'botter':
                usr = self.bot.get_user(int(arg))
                await ctx.guild.kick(usr)
                channel = discord.utils.get(ctx.guild.text_channels, name='玄関')
                invite = await channel.create_invite(max_arg=3600)
                dm_channel = await usr.create_dm()
                await dm_channel.send(invite)
                mod = UserMod()
                mod.member_delete(arg)
    '''

    @commands.command()
    async def member_register(self, ctx):
        if '幽霊屋敷' != ctx.guild.name:
            return False

        mod = UserMod()
        members = []
        for member in ctx.guild.members:
            await ctx.send(member.display_name)
            members.append([
                member.display_name,
                member.id,
                9000,
            ])
        mod.all_member_register(members)

def setup(bot):
    bot.add_cog(MyBot(bot))
