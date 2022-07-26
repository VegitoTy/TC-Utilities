import discord
import json
import time
from discord.ext import commands

with open("./config/configs.json") as f:
    bot_config = json.load(f)

default_guilds = bot_config["bot"]["default_guild"]

class YesNoView(discord.ui.View):
    """Shows All The Admin Commands."""

    COG_EMOJI = "<:admin:1000744203787194388>"

    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='Yes', custom_id='yes_view', style=discord.ButtonStyle.green)
    async def yes(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user.guild_permissions.administrator:
            banned_list = ""
            for member in interaction.guild.members:
                if time.time() - member.created_at.timestamp() < 604800:
                    if member.bot:
                        pass
                    else:
                        banned_list = f"{banned_list} {member}"
                        await interaction.guild.ban(member, reason=f'Prune Of New Accounts, Done By {interaction.user}')
            await interaction.channel.send(f'Prune Successful, Banned Users List:-\n{banned_list}')
        else:
            await interaction.channel.send('You must be a admin to do that.')
        self.yes.disabled = True
        self.no.disabled = True
        await interaction.message.edit(view=self) 
    
    @discord.ui.button(label='No', custom_id='no_view', style=discord.ButtonStyle.red)
    async def no(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user.guild_permissions.administrator:
            await interaction.channel.send('Action Cancelled.')
        else:
            await interaction.channel.send('You must be a admin to do that.')
        
        self.yes.disabled = True
        self.no.disabled = True
        await interaction.message.edit(view=self) 

class Admin(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
        
    @commands.group(name='prune', invoke_without_command=True, case_insensitive=True)
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    async def _prune(self, ctx:commands.Context):
        "Prune's The Specified Set Of Members"

        await ctx.send('Please tell from the list of subcommands that what exactly to do.')
    
    @_prune.command(name='NewAccounts')
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    async def _newaccounts(self, ctx:commands.Context):
        "Prune New Accounts."

        view = YesNoView()
        await ctx.send('Are you sure?', view=view)

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(
        Admin(bot),
        guilds = [discord.Object(id = default_guilds[0])]
    )