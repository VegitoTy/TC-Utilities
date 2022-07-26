import discord
import json, asyncio
from discord.ext import commands

with open("./config/configs.json") as f:
    bot_config = json.load(f)

default_guilds = bot_config["bot"]["default_guild"]

class Utility(commands.Cog):
    """Shows All The Utility Commands."""


    COG_EMOJI = "🛠️"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="Ping", aliases=['ping'])
    async def ping(self, ctx:commands.Context):
        """Shows The Latency Of The Bot"""
        await ctx.send(f'Latency :- `{round(self.bot.latency * 1000)} ms`')

    @commands.command(name='AV', aliases=['av'])
    async def avatar(self, ctx:commands.Context, member:discord.Member=None):
        """Shows Someone's Avatar."""
        if member == None:
            member = ctx.message.author
    
        embed = discord.Embed(color=0x3498db, title=f"{member}'s avatar")
        embed.set_image(url=member.display_avatar)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['embed'], name='Embed')
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    async def _embed(self, ctx:commands.Context, channel:discord.TextChannel, *, text:str):
        """Creates A Embed Separate The Title From The Description With |"""
        try:
            title, description = text.split("|", 1)
            embed = discord.Embed(title=title, description=description, color=0x3498db)
            await channel.send(embed=embed)
            await ctx.message.add_reaction("✅")
        except Exception as e:
            await ctx.message.add_reaction("❌")
            raise e

    @commands.command(name='Echo', aliases=['echo'])
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    async def _echo(self, ctx:commands.Context, *, message:str):
        """Make The Bot Send A Message"""
        await ctx.message.delete()
        await ctx.send(message)
    
    @commands.command(name='Userinfo', aliases=['whois', 'ui', 'UI'])
    async def _ui(self, ctx:commands.Context, user:discord.User=None):
        """Shows The Info Of A User"""
        if not user:
            user = ctx.author
        
        member = await ctx.guild.query_members(user_ids=[user.id])
        if len(member) == 0:
            embed = discord.Embed(colour=0x3498db, timestamp=ctx.message.created_at)
            embed.set_author(name=f'User Info - {user}')
            embed.set_thumbnail(url=user.avatar.url)
            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.display_avatar.url)
            embed.add_field(name='ID: ', value=user.id, inline=False)
            embed.add_field(name='Name: ',value=user.name,inline=False)
            embed.add_field(name='Created at:',value=user.created_at.timestamp(),inline=False)
            if user.bot:
                embed.add_field(name='Bot?', value='<:tick:1001065955213975604>')
            else:
                embed.add_field(name='Bot?', value='<:Cross:997740794171629590>')
        else:
            member:discord.Member = member[0]
            rlist = []
            ignored_roles = 0
            for role in member.roles:
                if len(rlist) >= 15:
                    ignored_roles += 1
                if role.name != "@everyone" and len(rlist) < 15:
                    rlist.append(role.mention)
            e = ""
            for role in rlist:
                e += f"{role}, "     
            embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
            embed.set_author(name=f'User Info - {member}')
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.display_avatar.url)
            embed.add_field(name='ID: ',value=member.id,inline=False)
            embed.add_field(name='Name:',value=member.name,inline=False)
            embed.add_field(name='Created at:',value=str(member.created_at)[:-22],inline=False)
            embed.add_field(name='Joined at:',value=str(member.joined_at)[:-22],inline=False)
            if ignored_roles == 0:
                embed.add_field(name=f'Roles: {len(member.roles)}', value=f'{e[:-2]}',inline=False)
            else:
                embed.add_field(name=f'Roles: {len(member.roles)}', value=f'{e[:-2]} And {ignored_roles} more roles..',inline=False)
            embed.add_field(name='Top Role:',value=member.top_role.mention,inline=False)
            if member.bot:
                embed.add_field(name='Bot?', value='<:tick:1001065955213975604>')
            else:
                embed.add_field(name='Bot?', value='<:Cross:997740794171629590>')
        await ctx.send(f'Info about {user}', embed=embed)

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(
        Utility(bot),
        guilds = [discord.Object(id = default_guilds[0])]
    )