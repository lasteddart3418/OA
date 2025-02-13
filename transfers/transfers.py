import discord
from datetime import datetime
from discord.ext import commands


from core import checks
from core.models import PermissionLevel

options_menu="You have provided invalid dept code.\n\n`mod` - Moderation Team\n`pt ` - Partnership Team\n`ct` - Community Team\n`mkt` - Marketing Team\n`dev` - Design/Development Team\n`srv` - Services Team\n`hr` - Human Resources Team\n`exec` - Executive Team\n"

DEPS_DATA = {
        "mod": {
        "category_id": 1286879335348965457 ,
        "pretty_name": "Moderation Team",
        "reminders": "When reporting a member, please make sure to provide valid proof. Please also make sure you check the report to ensure it breaks the rules before sending it.",
        "role_id": 1286882211072835594,
        "send_message_to_user": True
    },
        "pt": {
        "category_id": 1286879382119518218 ,
        "pretty_name": "Partnership Team",
        "reminders": "Please have your advertisement ready to send and ensure you meet our requirements.",
        "role_id": 1286882463271878656,
        "send_message_to_user": True
    },
        "ct": {
        "category_id": 1286879984316579840 ,
        "pretty_name": "Community Team",
        "reminders": "None",
        "role_id": 1286882898527649883,
        "send_message_to_user": True
    },
        "mkt": {
        "category_id": 1286879517864099840 ,
        "pretty_name": "Marketing Team",
        "reminders": "Please visit our shop to learn more about our paid services. If you have any questions, a Marketing Team member will be happy to assist you! ",
        "role_id": 1286882681115901995,
        "send_message_to_user": True
                
    },
        "dev": {
        "category_id": 1311059627399446598 ,
        "pretty_name": "Design/Development Team",
        "reminders": "In order for us to most efficiently assist you, please provide us with as much detail about your project as possible.",
        "role_id": 1311062806971547719,
        "send_message_to_user": True
    },
        "srv": {
        "category_id": 1287515041385545900 ,
        "pretty_name": "Services Team",
        "reminders": "Please have proof of your purchase ready for our staff to assist you in getting our order started.",
        "role_id": 1311064170606755860,
        "send_message_to_user": True
    },        
        "hr": {
        "category_id": 1286880031301177344 ,
        "pretty_name": "Human Resources Team",
        "reminders": "If you're looking to report a staff member, please make sure to provide proof against this staff member. Please also make sure to check your report to ensure it breaks the rules before sending it.",
        "role_id": 1286882045380792350,
        "send_message_to_user": True
    },
        "exec": {
        "category_id": 1286880128659488799 ,
        "pretty_name": "Executive Team",
        "reminders": "None",
        "role_id": 1286881362183192617,
        "send_message_to_user": True
    },
}
class oa(commands.Cog, name="OA Main Commands"):
    def __init__(self, bot):
        self.bot = bot
        
        
       
    @commands.command()
    @checks.thread_only()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def transfer(self, ctx, *, to: str=None):
        """Command that transfers thread to other departments."""
        if to is None:
            embed = discord.Embed(title=f"Department Transfer", description=options_menu,
                                  color=discord.Color.red(), timestamp=datetime.utcnow())
            return await ctx.send(embed=embed)
        to = to.lower()
        data = None
        try:
            data = DEPS_DATA[to]
        except:
            embed = discord.Embed(title=f"Department Transfer",description=options_menu,
                                  color=discord.Color.red(), timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
            return

        if data["send_message_to_user"]:
            mes = "You are being transferred to **`"
            mes += data["pretty_name"]
            mes += "`**.\n"
            mes += "Please remain __patient__ while we find a suitable staff member to assist in your request.\n\n"
            
            if data["reminders"] is not None:
                mes += "**__Reminders__**\n"
                mes += data["reminders"]

            msg = ctx.message
            msg.content = mes
            
            await ctx.thread.reply(msg, anonymous = False)
        
        await ctx.channel.edit(category=self.bot.get_channel(data["category_id"]), sync_permissions=True) 
        await ctx.send("<@&%s>" % str(data["role_id"]))

    @commands.command()
    @checks.thread_only()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def stransfer(self, ctx, to: str=None):
        """Silently transfers thread"""
        if to is None:
            embed = discord.Embed(title=f"Silent Transfer", description=options_menu,
                                  color=discord.Color.red(), timestamp=datetime.utcnow())
            return await ctx.send(embed=embed)
        to = to.lower()
        data = None
        try:
            data = DEPS_DATA[to]
        except:
            embed = discord.Embed(title=f"Silent Transfer",description=options_menu,
                                  color=discord.Color.red(), timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
            return

        await ctx.channel.edit(category=self.bot.get_channel(data["category_id"]), sync_permissions=True) 
        await ctx.send("Silent Transfer - <@&%s>" % str(data["role_id"]))

    @commands.command()
    @checks.thread_only()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def id(self, ctx):
        await ctx.send(ctx.thread.id)

async def setup(bot):
    await bot.add_cog(oa(bot))
