import discord
from discord.ext import commands
import asyncio
import aiohttp
import sys
import config
import traceback
from sessionmanager import SessionManager


class JangBot(commands.AutoShardedBot):
    myIntents = discord.Intents.all()  '#'temporary
    prefix = "??"
    initial_extensions = ["rngl", "owstats", "finalfantasylog", "admin"]

    def __init__(self):
        super().__init__(command_prefix=self.prefix, pm_help=None,
                         fetch_offline_members=False, heartbeat_timeout=150.0)
        self.session = SessionManager()

        for extension in self.initial_extensions:
            try:
                self.load_extension(extension)
                print("loaded " + str(extension))
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))
                traceback.print_exc()

    async def on_message(self, message):
        if message.author.bot:
            return
        print(message)
        await self.process_commands(message)

    async def on_ready(self):
        print('Logged in as ' + self.user.name)
        print(self.user.id)
        print('------')
        print(discord.version_info)
        await self.change_presence(activity=discord.Game(name="totally not a "
                                   "bot, trust me"))

    async def close(self):
        print("in close")
        await super().close()
        await self.session.close()

    def run(self):
        try:
            super().run(config.mccreetoken, reconnect=True)
        except Exception as e:
            print(e)
        finally:
            print("we out")
j = JangBot()
j.run()
