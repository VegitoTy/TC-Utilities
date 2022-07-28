import discord
import random, json, time, os, asyncio
from PIL import Image, ImageFont, ImageDraw
from discord.ext import commands

with open("./config/configs.json") as f:
    bot_config = json.load(f)

default_guilds = bot_config["bot"]["default_guild"]

class Fun(commands.Cog):
    """Shows All Fun Commands."""

    COG_EMOJI = "🥳"

    def __init__(self, bot) -> None:
        self.bot = bot
    
    pass

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(
        Fun(bot),
        guilds = [discord.Object(id = default_guilds[0])]
    )