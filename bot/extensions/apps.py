import discord
import json
from discord.ext import commands

with open("./config/configs.json") as f:
    bot_config = json.load(f)

default_guilds = bot_config["bot"]["default_guild"]

class AcceptDenyModView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='Accept', custom_id='accept_view', style=discord.ButtonStyle.green)
    async def accept(self, interaction:discord.Interaction, button:discord.ui.Button):
        def check(message):
            return message.author == interaction.user and message.channel == interaction.channel
        
        bot = getattr(interaction, "client", interaction._state._get_client())

        await interaction.channel.send("Are You Sure? Reply With Yes Or No")
        yesno_reply = await bot.wait_for('message', check=check)
        if yesno_reply.content.lower() == 'yes':
            pass
        elif yesno_reply.content.lower() == 'no':
            await interaction.channel.send('Ok!')
            return
        else:
            await interaction.channel.send('Invalid Response! Retry')
            return
        await interaction.channel.send("Any Reason You Want To Add?")
        reason = await bot.wait_for('message', check=check)
        reason = reason.content
        Trys = 0
        while Trys!=3:
            Trys+=1
            try:
                await interaction.channel.send("Please Send The ID Of The User")
                id = await bot.wait_for('message', check=check)
                if str(id.content).lower() == 'no':
                    await interaction.channel.send('Cancelled.')
                    return
                id = id.content
                id = int(id)
                break
            except:
                await interaction.channel.send("ID Must be a Integer, Retry!")
        if Trys >= 3:
            await interaction.channel.send('Too many Tries Taken.')
            return
        user = await interaction.guild.query_members(user_ids=[id])
        user = user[0]
        if not user:
            await interaction.channel.send('User Not Found')
            return
        role = discord.utils.get(interaction.guild.roles, id=981613135804907561)
        await user.add_roles(role)
        await user.send(f'Congratulations! Your Application Has Been Accepted! For The Reason:- {reason}\nMake Sure To Do Your Job Properly!')
        await interaction.channel.send("The User Has Been Given The Trial Mod Role! AND Has been dm'ed")
        self.accept.disabled = True
        self.deny.disabled = True
        await interaction.message.edit(view=self)   
    
    @discord.ui.button(label='Deny', custom_id='deny_view', style=discord.ButtonStyle.red)
    async def deny(self, interaction:discord.Interaction, button:discord.ui.Button):
        def check(message):
            return message.author == interaction.user and message.channel == interaction.channel
        
        bot = getattr(interaction, "client", interaction._state._get_client())

        await interaction.channel.send("Are You Sure? Reply With Yes Or No")
        yesno_reply = await bot.wait_for('message', check=check)
        if yesno_reply.content.lower() == 'yes':
            pass
        elif yesno_reply.content.lower() == 'no':
            return
        else:
            await interaction.channel.send('Invalid Response! Retry')
            return
        await interaction.channel.send("Any Reason You Want To Add?")
        reason = await bot.wait_for('message', check=check)
        reason = reason.content
        Trys = 0
        while Trys!=3:
            Trys+=1
            try:
                await interaction.channel.send("Please Send The ID Of The User")
                id = await bot.wait_for('message', check=check)
                if str(id.content).lower() == 'no':
                    await interaction.channel.send('Cancelled.')
                    return
                id = id.content
                id = int(id)
                break
            except:
                await interaction.channel.send("ID Must be a Integer, Retry!")
        if Trys >= 3:
            await interaction.channel.send('Too many Tries Taken.')
            return
        user = await interaction.guild.query_members(user_ids=[id])
        user = user[0]
        if not user:
            await interaction.channel.send('User Not Found')
            return
        await user.send(f'Sorry! Your Application Has Been Denied.. For The Reason:- {reason}\nTry Harder Next Time!')
        await interaction.channel.send('The users application has been Denied!')
        self.accept.disabled = True
        self.deny.disabled = True
        await interaction.message.edit(view=self)   

class AcceptDenyFruitStockerView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='Accept', custom_id='accept_view', style=discord.ButtonStyle.green)
    async def accept(self, interaction:discord.Interaction, button:discord.ui.Button):
        def check(message):
            return message.author == interaction.user and message.channel == interaction.channel
        
        bot = getattr(interaction, "client", interaction._state._get_client())

        await interaction.channel.send("Are You Sure? Reply With Yes Or No")
        yesno_reply = await bot.wait_for('message', check=check)
        if yesno_reply.content.lower() == 'yes':
            pass
        elif yesno_reply.content.lower() == 'no':
            await interaction.channel.send('Ok!')
            return
        else:
            await interaction.channel.send('Invalid Response! Retry')
            return
        await interaction.channel.send("Any Reason You Want To Add?")
        reason = await bot.wait_for('message', check=check)
        reason = reason.content
        Trys = 0
        while Trys!=3:
            Trys+=1
            try:
                await interaction.channel.send("Please Send The ID Of The User")
                id = await bot.wait_for('message', check=check)
                if str(id.content).lower() == 'no':
                    await interaction.channel.send('Cancelled.')
                    return
                id = id.content
                id = int(id)
                break
            except:
                await interaction.channel.send("ID Must be a Integer, Retry!")
        if Trys >= 3:
            await interaction.channel.send('Too many Tries Taken.')
            return
        user = await interaction.guild.query_members(user_ids=[id])
        user = user[0]
        if not user:
            await interaction.channel.send('User Not Found')
            return
        role = discord.utils.get(interaction.guild.roles, id=982052367195324436)
        await user.add_roles(role)
        await user.send(f'Congratulations! Your Application Has Been Accepted! For The Reason:- {reason}\nMake Sure To Do Your Job Properly!')
        await interaction.channel.send("The User Has Been Given The Fruit Stocker Role! AND Has been dm'ed")
        self.accept.disabled = True
        self.deny.disabled = True
        await interaction.message.edit(view=self)   
    
    @discord.ui.button(label='Deny', custom_id='deny_view', style=discord.ButtonStyle.red)
    async def deny(self, interaction:discord.Interaction, button:discord.ui.Button):
        def check(message):
            return message.author == interaction.user and message.channel == interaction.channel
        
        bot = getattr(interaction, "client", interaction._state._get_client())

        await interaction.channel.send("Are You Sure? Reply With Yes Or No")
        yesno_reply = await bot.wait_for('message', check=check)
        if yesno_reply.content.lower() == 'yes':
            pass
        elif yesno_reply.content.lower() == 'no':
            return
        else:
            await interaction.channel.send('Invalid Response! Retry')
            return
        await interaction.channel.send("Any Reason You Want To Add?")
        reason = await bot.wait_for('message', check=check)
        reason = reason.content
        Trys = 0
        while Trys!=3:
            Trys+=1
            try:
                await interaction.channel.send("Please Send The ID Of The User")
                id = await bot.wait_for('message', check=check)
                if str(id.content.lower()) == 'no':
                    await interaction.channel.send('Cancelled.')
                    return
                id = id.content
                id = int(id)
                break
            except:
                await interaction.channel.send("ID Must be a Integer, Retry!")
        if Trys >= 3:
            await interaction.channel.send('Too many Tries Taken.')
            return
        user = await interaction.guild.query_members(user_ids=[id])
        user = user[0]
        if not user:
            await interaction.channel.send('User Not Found')
            return
        await user.send(f'Sorry! Your Application Has Been Denied.. For The Reason:- {reason}\nTry Harder Next Time!')
        await interaction.channel.send('The users application has been Denied!')
        self.accept.disabled = True
        self.deny.disabled = True
        await interaction.message.edit(view=self)     

class StaffAppsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='Moderator', custom_id='moderator_app', emoji='<:moderator:997761303521284157>')
    async def mod_app(self, interaction:discord.Interaction, button:discord.ui.Button):
        acceptdenyview = AcceptDenyModView()
        role = discord.utils.get(interaction.guild.roles, name='( Knights of Black ) ・5+')
        if not role in interaction.user.roles:
            await interaction.user.send('You need atleast level 5 to apply for moderator')
            return
        questions = [
            "Send Your Username#Discriminator And Your ID",
            "How Long Have You Been In The Server?",
            "What Is Your Level In The Server?",
            "Do You Have Any Previous Modding Experience? If Yes Send The Server.",
            "Do You Understand The Job Of A Mod?",
            "What Does A Moderator Do?",
            "What Will You Do If Someone Is Spamming In General?",
            "What Will You Do If Another Moderator Is Abusing His/Her Powers?",
            "Whats Your Timezone?",
            "Any Other Thing You Want To Mention?"
        ]

        dmMessage = await interaction.user.send(f'Hi! Answer The Following Questions')

        def check(message):
            return message.author == interaction.user and message.channel == dmMessage.channel
        
        embed = discord.Embed(title=f'{interaction.user}', description='The Users Answers Are Below!', color=0x3498db)
        
        bot = getattr(interaction, "client", interaction._state._get_client())

        for question in questions:
            await interaction.user.send(question)
            userReply = await bot.wait_for('message', check=check)
            embed.add_field(name=question, value=userReply.content)
        
        await interaction.user.send(f'Thanks For Applying, Your Answers Have Been Recorded.')
        
        channel = discord.utils.get(interaction.guild.text_channels, name='〔📖〕application_responses')
        await channel.send(embed=embed, view=acceptdenyview)
    
    @discord.ui.button(label='Fruit Stocker', custom_id='fruit_stocker_app', emoji='🍎')
    async def fruit_stocker_app(self, interaction:discord.Interaction, button:discord.ui.Button):
        acceptdenyview = AcceptDenyFruitStockerView()
        role = discord.utils.get(interaction.guild.roles, name='( Demon ) ・3+')
        if not role in interaction.user.roles:
            await interaction.user.send('You need atleast level 3 to apply for a Fruit Stocker')
            return
        questions = [
            "Send Your Username#Discriminator And Your ID",
            "How Long Have You Been In The Server?",
            "What Is Your Level In The Server?",
            "Any Other Thing You Want To Mention?"
        ]

        dmMessage = await interaction.user.send(f'Hi! Answer The Following Questions')

        def check(message):
            return message.author == interaction.user and message.channel == dmMessage.channel

        embed = discord.Embed(title=f'{interaction.user}', description='The Users Answers Are Below!', color=0x3498db)
        
        bot = getattr(interaction, "client", interaction._state._get_client())

        for question in questions:
            await interaction.user.send(question)
            userReply = await bot.wait_for('message', check=check)
            embed.add_field(name=question, value=userReply.content)
        
        await interaction.user.send(f'Thanks For Applying, Your Answers Have Been Recorded.')

        channel = discord.utils.get(interaction.guild.text_channels, name='〔📖〕application_responses')
        await channel.send(embed=embed, view=acceptdenyview)

class staff_apps(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='StaffApps', aliases=['staffapps', 'SA', 'sa'], hidden=True)
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    async def sa(self, ctx):
        "Send The Staff Applications"
        staffapps = StaffAppsView()

        apps=discord.Embed(title='Applications', description=f'> Click On The Moderator Button To Apply For Moderator!\n> Click On The Fruit Stocker Button To Apply For The Fruit Stocker!', color=0x3498db)
        await ctx.send(embed=apps, view=staffapps)

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(
        staff_apps(bot),
        guilds = [discord.Object(id = default_guilds[0])]
    )