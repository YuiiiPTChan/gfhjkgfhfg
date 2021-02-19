import discord
from discord.ext import commands
import datetime
import asyncio

class base(commands.Cog):
    """Base core module"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")

    # comandos em python em cogs tem que seguir sempre a linha do def se nao da erro
    @commands.has_guild_permissions(manage_guild=True)
    @commands.command(
        name="prefix",
        aliases=["cp, sp"],
        description="Change your guilds prefix",
        usage="[prefix]",
    )
    async def prefix(self, ctx, *, prefix="py."): 
        """Change your guilds prefix""" # este aqui define a desc no comando help que o dpy tem integrado
        await self.bot.config.upsert({"_id": ctx.guild.id, "prefix": prefix})
        await ctx.send(f"The guild prefix has been set to `{prefix}`")
        
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True) 
    async def deleteprefix(self, ctx):
        await self.bot.config.unset({"_id": ctx.guild.id, "prefix": 1})
        await ctx.send("This guilds prefix has been set back to the default.")

    @commands.command(name="ping")
    @commands.guild_only()
    async def ping(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        embed = discord.Embed(title="Bot's latency", colour=member.color, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Websocket Latency", value=f"{'Pong! {0}'.format(round(self.bot.latency*1000, 2))}ms")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            
        await ctx.send(embed=embed)
        print(ctx.author.name, 'used the command ping')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog):
        """Reloads a module"""
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"`{cog}` was reloaded.")
        except Exception as e:
            print(f"{cog} can not be loaded.")
            raise e    

    @reload.error
    async def reload_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("What should i reload?")
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"{ctx.author.name}, you don't have permission to use this command.")    

            raise error


def setup(bot):
    bot.add_cog(base(bot))