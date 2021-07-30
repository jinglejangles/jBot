"""admin cog file"""
import traceback
#import asyncio
#import aiohttp
#import discord
from discord.ext import commands



class Admin(commands.Cog):
    """admin cog"""
    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()
        self._last_result = None

    def __local_check(self, ctx):
        return self.bot.is_owner(ctx.author)

    @commands.is_owner()
    @commands.command(name="load", hidden=True, description="load cog",
                      brief="load cog", passContext=True)
    async def load(self, context, module):
        """loads a cog"""
        try:
            self.bot.load_extension(module)
        except Exception as exc:
            await context.send(f'```py\n{traceback.format_exc()}\n```')
            print(exc)
        else:
            await context.send('Loaded')

    @commands.is_owner()
    @commands.command(name="unload", description="unload", brief="unload",
                      passContext=True, hidden=True)
    async def unload(self, context, module):
        """unloads a cog"""
        try:
            self.bot.unload_extension(module)
        except Exception as exc:
            await context.send(f'```py\n{traceback.format_exc()}\n```')
            print(exc)
        else:
            await context.send("unloaded")

    @commands.is_owner()
    @commands.command(name="reload", description="reload module",
                      brief="unload", hidden=True, passContext=True)
    async def reload(self, context, module):
        """reloads a cog"""
        try:
            self.bot.reload_extension(module)
        except commands.ExtensionError as exc:
            await context.send(f'{exc.__class__.__name__}:{exc}')
        else:
            await context.send("reloaded")

def setup(bot):
    """add cog to bot"""
    bot.add_cog(Admin(bot))
