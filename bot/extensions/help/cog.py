import discord
import json
from discord.ext import commands
from .help_command import MyHelpCommand

with open("./config/configs.json") as f:
    bot_config = json.load(f)

default_guilds = bot_config["bot"]["default_guild"]

class HelpCog(commands.Cog, name="Help"):
    """Shows help info for commands and cogs"""

    COG_EMOJI = "❔"

    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

async def setup(bot: commands.Bot):
    await bot.add_cog(
        HelpCog(bot),
        guilds = [discord.Object(id = default_guilds[0])]
    )