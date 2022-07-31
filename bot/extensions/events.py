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
        await asyncio.sleep(2)
        async with channel.typing():
            message = await channel.send('Checking if the user is an alt...')
            await asyncio.sleep(3)
            await message.edit(content=f'{message.content}\n\nChecking Account Age...')
            await asyncio.sleep(3)
            if time.time() - member.created_at.timestamp() <= 1209600:
                await message.edit(content=f'Potential Alt.\n\nAccount Age Is Younger Then 2 Weeks.')
                await asyncio.sleep(2)
                await message.edit(content=f'Account Age Is Younger Then 2 Weeks\n\nBanned {member}')
                try:
                   await member.send(f"You have been banned from `{guild}` as your account is below 14 days of age. You may appeal by dm'ing VegitoTy#7922")
                except:
                    pass
                await guild.ban(member, reason='Account Age Younger Then 2 Weeks.')
                return
            else:
                await message.edit(content=f"{message.content[:-3]} Passed\nChecking If Username Matches With Any Banned User...")
            bans = await guild.bans()
            for ban in bans:
                usercheck = ban[0]
                await asyncio.sleep(2)
                if member.name == usercheck.name:
                    await message.edit(content=f"Potential Alt.\n\nName Matches With A Banned User.")
                    await asyncio.sleep(2)
                    await message.edit(content=f"Name Matches With A Banned User.\n\nBanned {member}")
                    try:
                        await member.send(f"You have been banned from `{guild}` as your username matches with a banned user. You may appeal by dm'ing VegitoTy#7922")
                    except:
                        pass
                    await guild.ban(member, reason="Username Matches With A Banned Account's Username")
                    return
            await message.edit(content=f'{message[:-3]} Passed\nAll Checks Passed.')





async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(
        events(bot),
        guilds = [discord.Object(id = default_guilds[0])]
    )