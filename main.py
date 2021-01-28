import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

INITIAL_EXTENSIONS = [
    'cog.MyCog',
    'cog.MusicCog',
]

class MyBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix, intents=intents)
        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog)
            except:
                traceback.print_exc()

    async def on_read(self):
        print('---start---')

def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    dotenv_path = os.path.join(base_path, '.env')
    load_dotenv(dotenv_path)
    intents = discord.Intents.all()

    bot = MyBot(command_prefix='$', intents=intents)
    bot.run(os.getenv('BOT_TOKEN'))

if __name__ == '__main__':
    main()
