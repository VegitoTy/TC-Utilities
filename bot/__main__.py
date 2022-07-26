import discord
import json
from discord.ext import commands
import os
import pathlib
from dotenv import load_dotenv
from bot.extensions.apps import StaffAppsView, AcceptDenyModView, AcceptDenyFruitStockerView

dotenv_path = pathlib.Path('./.env')

load_dotenv(dotenv_path=dotenv_path)

TOKEN = os.getenv("TOKEN")

with open('./config/configs.json') as f:
    bot_config = json.load(f)

class TcUtilities(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix=['tc ', '&', 'TC '],
            status=discord.Status.idle,
            activity=discord.Activity(type=discord.ActivityType.watching, name='The Commandments'),
            intents=discord.Intents.all())
        
    async def setup_hook(self):
        default_guilds = bot_config["bot"]["default_guild"]
        for filename in os.listdir('./bot/extensions'):
            if filename.endswith('.py'):
                extension = f'bot.extensions.{filename[:-3]}'
                await self.load_extension(f"{extension}")
        await self.load_extension('jishaku')
        await self.load_extension('bot.extensions.help.cog')
        self.add_view(StaffAppsView())
        self.add_view(AcceptDenyModView())
        self.add_view(AcceptDenyFruitStockerView())
        await bot.tree.sync(guild = discord.Object(id = default_guilds[0]))

    async def on_ready(self):
        channel = await self.fetch_channel(bot_config["logging"]["startup"])
        await channel.send('Bot Has Started')
        print(f'Logged In As {self.user}')

bot = TcUtilities()
bot.run(TOKEN)