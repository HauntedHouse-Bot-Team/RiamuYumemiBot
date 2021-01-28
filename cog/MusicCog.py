import os
from dotenv import load_dotenv
from discord.ext import commands
import discord

from src.NextCloudModules import NextCloudModules as NextCloudMod

class MusicCog(commands.Cog):
    def __init__(self, bot):
        base_path = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.join(base_path, '.env')
        load_dotenv(dotenv_path)
        self.bot = bot
        self.volume = 1
        self.voice = None

    @commands.command()
    async def join(self, ctx):
        self.voice = await discord.VoiceChannel.connect(ctx.author.voice.channel)

    @commands.command()
    async def leave(self, ctx):
        await self.voice.disconnect()
        self.voice = None

    @commands.command()
    async def play(self, ctx, music_name):
        next_cloud_mod = NextCloudMod()            
        files = next_cloud_mod.get_file_list('share/Music')
        for file in files:
            if music_name in file:
                print('ok')
                file_path = next_cloud_mod.get_file(file, 'music.mp3')
                self.voice.play(discord.FFmpegPCMAudio(file_path))
def setup(bot):
    bot.add_cog(MusicCog(bot))