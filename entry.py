"""entry file to start up the discord bot"""
#import sys
import traceback
import discord
from discord.ext import commands
import config
from sessionmanager import SessionManager


class JangBot(commands.AutoShardedBot):
    """jangbot class representation"""
    myIntents = discord.Intents.all()  #temporary
    prefix = "??"
    initial_extensions = ["rngl", "owstats", "finalfantasylog", "cogs.admin"]

    def __init__(self):
        super().__init__(command_prefix=self.prefix, pm_help=None,
                         fetch_offline_members=False, heartbeat_timeout=150.0)
        self.session = SessionManager()

        for extension in self.initial_extensions:
            try:
                self.load_extension(extension)
                print("loaded " + str(extension))
            except Exception as exc:
                exc = '{}: {}'.format(type(exc).__name__, exc)
                print('Failed to load extension {}\n{}'.format(extension, exc))
                traceback.print_exc()

    async def on_message(self, message):
        """on_message listener override.  Doesn't do anything except print
        the current message and ignores the message if it is from a bot
        """
        if message.author.bot:
            return
        print(message)
        await self.process_commands(message)

    async def on_ready(self):
        """
        on_ready override that just prints out some info once bot is
        has connected and logged in
        """
        print('Logged in as ' + self.user.name)
        print(self.user.id)
        print('------')
        print(discord.version_info)
        await self.change_presence(activity=discord.Game(name="totally not a"
                                                         +" bot, trust me"))

    async def close(self):
        """gracefully close any open sessions"""
        print("in close")
        await super().close()
        await self.session.close()

    def run(self, *args, **kwargs):
        """start the bot"""
        try:
            super().run(config.mccreetoken, reconnect=True)
        except Exception as exc:
            print(exc)
        finally:
            print("we out")

j = JangBot()
j.run()
