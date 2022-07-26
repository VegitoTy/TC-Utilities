import discord, json, time, asyncio
from discord.ext.tasks import loop
from discord.ext import commands

with open("./config/configs.json") as f:
    bot_config = json.load(f)

default_guilds = bot_config["bot"]["default_guild"]

class events(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener('on_member_join')
    async def bannewmembers(self, member):
        if member.bot:
            return
        guild = self.bot.get_guild(981605071609532436)
        channel = discord.utils.get(guild.text_channels, name='〔💬〕main_chat')
        async with channel.typing():
            await channel.send('Checking if the user is an alt...')
            await asyncio.sleep(10)
            if time.time() - member.created_at.timestamp() <= 864000:
                alt = True
            else:
                alt = False
        if alt == True:
            try:
                await member.send(f"You have been banned from `{guild}` as your account is below 10 days of age. You may appeal by dm'ing VegitoTy#7922")
            except:
                pass
            await guild.ban(member, reason='Suspected alt.')
            await channel.send(f'Suspected alt. Banned {member}')
        if alt == False:
            await channel.send('Check Passed.')

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(
        events(bot),
        guilds = [discord.Object(id = default_guilds[0])]
    )