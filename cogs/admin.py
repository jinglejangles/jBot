import aiohttp
import async_timeout
import asyncio
import random
import discord
import json
from jangle_utils import fetch_response
from discord.ext import commands
from discord.ext.commands import Bot
import traceback


class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()
        self._last_result = None

    def __local_check(ctx):
        return self.bot.is_owner(ctx.author)

    @commands.is_owner()
    @commands.command(name="load", hidden=True, description="load cog",
                      brief="load cog", passContext=True)
    async def load(self, context, module):
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await context.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await context.send('Loaded')

    @commands.is_owner()
    @commands.command(name="unload", description="unload", brief="unload",
                      passContext=True, hidden=True)
    async def unload(self, context, module):
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await context.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await context.send("unloaded")

    @commands.is_owner()
    @commands.command(name="reload", description="reload module",
                      brief="unload", hidden=True, passContext=True)
    async def reload(self, context, module):
        try:
            self.bot.reload_extension(module)
        except commands.ExtensionError as e:
            await context.send(f'{e.__class__.__name__}:{e}')
        else:
            await context.send("reloaded")


def setup(bot):
    bot.add_cog(admin(bot))
