import discord
import ast, aiosqlite, datetime, json, humanfriendly, typing
from discord.ext import commands

with open("./config/configs.json") as f:
    bot_config = json.load(f)

default_guilds = bot_config["bot"]["default_guild"]

class Mod(commands.Cog):
    """Shows All The Moderator Commands."""


    COG_EMOJI = "<:moderator:997761303521284157>"

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener('on_ready')
    async def ready(self):
        setattr(self.bot, 'censordb', await aiosqlite.connect('censors.db'))
        async with self.bot.censordb.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS censors (guild INTEGER, word TEXT)")

    @commands.command(name='Eval', aliases=['eval', 'ev'], description="Owner Only So No Use Of Description lol.")
    @commands.is_owner()
    async def _eval(self, ctx, *, cmd):
        """Evaluates input.
Input is interpreted as newline seperated statements.
If the last statement is an expression, that is the return value.
Usable globals:
    - `bot`: the bot instance
    - `discord`: the discord module
    - `commands`: the discord.ext.commands module
    - `ctx`: the invokation context
    - `__import__`: the builtin `__import__` function
Such that `>eval 1 + 1` gives `2` as the result.
The following invokation will cause the bot to send the text '9'
to the channel of invokation and return '3' as the result of evaluating
>eval ```
a = 1 + 2
b = a * 2
await ctx.send(a + b)
a
```
"""

        def insert_returns(body):
            if isinstance(body[-1], ast.Expr):
                body[-1] = ast.Return(body[-1].value)
                ast.fix_missing_locations(body[-1])

            if isinstance(body[-1], ast.If):
                insert_returns(body[-1].body)
                insert_returns(body[-1].orelse)

            if isinstance(body[-1], ast.With):
                insert_returns(body[-1].body)

        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")

        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)
    
        result = (await eval(f"{fn_name}()", env))
        await ctx.send(result)
    
    @commands.command(name='Timeout', aliases=['timeout', 'To', 'to'], description=f"Times Out A Member.\nUsage:- &To [member] [duration] [reason=None]")
    @commands.check_any(commands.has_permissions(moderate_members=True), commands.is_owner())
    async def _timeout(self, ctx:commands.Context, member:discord.Member, duration:str='2h', reason:str=None):
        "Times Out A Member."

        if ctx.author.top_role > member.top_role:
            pass
        else:
            return await ctx.send('Your not high enough in the role hierarchy to do that.')
        if not reason:
            reason = 'No Reason Provided.'
        try:
            time = int(duration)
        except:
            convertTimeList = {'s':1, 'm':60, 'h':3600, 'd':86400, 'S':1, 'M':60, 'H':3600, 'D':86400}
            try:
                time = int(duration[:-1]) * convertTimeList[duration[-1]]
            except:
                return await ctx.send("Invalid duration")
        
        if time < 0:
            time = 0
        if time > 2419200:
            time = 2419200
        
        reason2 = f"Action requested by {ctx.author} | Reason: {reason}"
        try:
            await member.edit(timed_out_until=(discord.utils.utcnow() + datetime.timedelta(seconds=time)), reason=reason2)
            await ctx.reply(f"{member.mention} has been put to timeout for {datetime.timedelta(seconds = time)}\nReason: {reason}")
        except discord.Forbidden:
            await ctx.reply('I do not have the required permissions to do that.')
    
    @commands.command(name='RemoveTimeout', aliases=['removetimeout', 'Rto', 'rto'], description=f"Removes Timeout From A Member.\nUsage:- &Rto [member] [reason=None]")
    @commands.check_any(commands.has_permissions(moderate_members=True), commands.is_owner())
    async def _rto(self, ctx:commands.Context, member:discord.Member, reason:str=None):
        "Removes Timeout From A Member."

        if ctx.author.top_role > member.top_role:
            pass
        else:
            return await ctx.send('Your not high enough in the role hierarchy to do that.')
        if not reason:
            reason = 'No Reason Provided.'
        
        reason2 = f"Action requested by {ctx.author} | Reason: {reason}"
        try:
            await member.edit(timed_out_until=None, reason=reason2)
            await ctx.reply(f"{member.mention} has been removed from timeout\nReason: {reason}")
        except discord.Forbidden:
            await ctx.reply('I do not have the required permissions to do that.')

    @commands.command(name='Ban', aliases= ['ban', 'b'], description=f"Bans A User. Whether Or Not The User Is In The Server Or Not\nUsage:- &Ban [user] [reason=None]")
    @commands.check_any(commands.has_permissions(kick_members=True, ban_members=True), commands.is_owner())
    async def _ban(self, ctx:commands.Context, user:discord.User, reason:str=None):
        "Bans A User. Whether Or Not The User Is In The Server Or Not"

        if reason == None:
            reason = 'No Reason Provided'
        id = user.id
        member = await ctx.guild.query_members(user_ids=[id])
        if len(member) == 0:
            try:
                user.send(f"You have been banned from `{ctx.guild}` for `{reason}`")
            except:
                pass
            await ctx.guild.ban(user, reason=f"{reason}, Banned By {ctx.author}")
            await ctx.send(f'{user.name}#{user.discriminator} has been banned.')
            return
        member = member[0]
        if ctx.author.top_role > member.top_role:
            await member.send(f'You have been banned from `{ctx.guild}` for `{reason}`')
            await ctx.guild.ban(member, reason=f"{reason}, Banned by {ctx.author}")
            await ctx.send(f'{member} has been banned.')
        else:
            await ctx.send(f'Your not high enough in the role hierarchy to do that.')
    
    @commands.command(name='Unban', aliases=['unban'], description=f"Unban A User.\nUsage:- &Unban [user] [reason=None]")
    @commands.check_any(commands.has_permissions(ban_members=True), commands.is_owner())
    async def _unban(self, ctx:commands.Context, *, user:discord.User, reason:str="No Reason Provided"):
        "Unban A User."

        await ctx.guild.unban(user, reason=reason)
        await ctx.send(f'Unbanned {user}')
    
    @commands.command(name='Kick', aliases=['kick', 'k'], description=f"Kicks A Member.\nUsage:- &Kick [member] [reason=None]")
    @commands.check_any(commands.has_permissions(kick_members=True), commands.is_owner())
    async def _kick(self, ctx:commands.Context, user:discord.Member, reason:str=None):
        "Kicks A Member."

        if reason == None:
            reason = 'No Reason Provided'
        if ctx.author.top_role > user.top_role:
            await user.send(f'You have been kicked from `{ctx.guild}` for `{reason}`')
            await user.kick(reason=f'{reason}, Kicked by {ctx.author}')
            await ctx.send(f'{user} has been kicked.')
        else:
            await ctx.send(f'Your not high enough in the role hierarchy to do that.')
        
    @commands.group(name='Purge', invoke_without_command=True, case_insensitive=True, aliases=['purge'], description=f"Clears A Amount Of Messages.\nUsage:- &Purge [amount]")
    @commands.check_any(commands.has_permissions(manage_messages=True), commands.is_owner())
    async def _purge(self, ctx:commands.Context, amount:int):
        "Clears A Amount Of Messages."

        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'Purged {amount} Messages.', delete_after=6)
    
    @_purge.command(name='until', aliases=['unt'], description=f"Clears The Messages After A Message.\nUsage:- &Purge Until [message]")
    @commands.check_any(commands.has_permissions(manage_messages=True), commands.is_owner())
    async def _until(self, ctx:commands.Context, message:discord.Message):
        "Clears The Messages After A Message."

        channel = ctx.message.channel
        await ctx.message.delete()
        try:
            await channel.purge(after=message)
            await ctx.send(f'Purged the messages after that message', delete_after=6)
        except:
            await ctx.send('Invalid message')
    
    @_purge.command(name='user', description=f"Clear all messages of <User> in every channel within the last [n=5] minutes\nUsage:- &Purge User [user] [number_of_minutes=5]")
    @commands.check_any(commands.has_permissions(manage_messages=True), commands.is_owner())
    async def purge_user(self, ctx:commands.Context, user:discord.User, num_minutes:int=5):
        """Clear all messages of <User> in every channel within the last [n=5] minutes"""

        after = ctx.message.created_at - datetime.timedelta(minutes=num_minutes)

        def check(msg):
            return msg.author.id == user.id

        for channel in await ctx.guild.fetch_channels():
            if type(channel) is discord.TextChannel:
                try:
                    await channel.purge(limit=10*num_minutes, check=check, after=after)
                except discord.Forbidden:
                    continue
        await ctx.send('Done', delete_after=6)
    
async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(
        Mod(bot),
        guilds = [discord.Object(id = default_guilds[0])]
    )