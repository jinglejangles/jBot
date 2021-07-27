import discord, logging, aiohttp, random, pytz,random,asyncio,async_timeout

from datetime import datetime
from pytz import timezone
from discord import Game
from discord.ext.commands import Bot
from os import listdir
from os.path import isfile, join
import config
from jangle_utils import fetch_response
import json
import os
import traceback


myIntents = discord.Intents.all();
logger = logging.getLogger('discord')
logger.setLevel(level=logging.DEBUG)
handler = logging.FileHandler(filename='mccree.log',encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

animelist = "weeb","anime","baka", "BAKA", "0w0","OwO","manga","hentai"
ignoreList = ["__pycache__","config.py","mccree.py","admin"]
cogs_dir= config.cogdirectory
initial_extensions = ["rngl","owstats","finalfantasylog","boardgamegeek"]
mccree = Bot(command_prefix=config.prefix,description="a shitty bot",intents=myIntents)



@mccree.event
async def on_reaction_add(reaction,user):
    print("reaction added")
    if reaction.count >= 10:
        await context.send(reaction.message.channel, "My doggie das a good message")
    return


@mccree.event
async def on_member_join(member,pass_context=True):
    default_role = discord.utils.get(member.server.roles,name="civilized")
    await ctx.send("hey")
    await mccree.add_roles(member,default_role)


@mccree.event
async def on_message(message):
    #ignore if from bot
    if message.author.bot:
    	return

    print(message.content)
    if any(s in message.content for s in animelist):
        anime = random.random()
        print(str(anime))
        if anime * 100 > 50:
            #await mccree.delete_message(message)
            await message.channel.send("WEEBS OUT, {0} ".format(message.author.mention))

    splmessage = message.content.split(None, 1)
    if splmessage[0].startswith(("im", "i'm","I'm","Im", "IM")) and len(splmessage) > 1:
        if random.random() * 20 > 15:
            await mccree.send_message(message.channel, "Hi {0}, I'm Dad.".format(splmessage[-1]))
            return
    await mccree.process_commands(message)

@mccree.event
async def on_ready():
    print('Logged in as ' + mccree.user.name)
    print(mccree.user.id)
    print('------')
    print(discord.version_info)
    await mccree.change_presence(activity=discord.Game(name="totally not a bot, trust me"))
    #channel = discord.utils.get(mccree.get_all_channels(), name='nsfw-shitposting')
    #counter = 0
    #async for message in mccree.logs_from(channel,limit=50):
    #    mccree.messages.append(message)
    
  
@mccree.command(pass_context=True,
                hidden=True)
async def highnoon(context):
    #responses if it isn't noon
    responses = [
        'Knock it off,',
        'Not now,',
        "I'm your huckleberry,",
        "Don't sass me,",
        "Why don't you buy a watch,",
        "Sorry I don't use a watch"
    ]
    fmt = '%H:%M'
    dt = datetime.now(timezone('UTC'))
    dt = dt.astimezone(timezone('America/New_York'))


    if dt.hour is not 12: #is it not noon
        await context.send("{0} {1}".format(random.choice(responses),context.message.author.mention))
    else: #its noon
        await context.send("It's high noon {0}".format(context.message.author.mention))
        

@mccree.command(pass_context=True)
async def japan(context):
    await context.send("BAKA GAIJIN OMAE WA MO, SHINDERIRU")


@mccree.command(pass_context=True,description="Sends invite code to bot owner's discord server via DM")
async def invitecode(context):
    await context.author.send("https://discord.gg/bbhsFMN")


if __name__ == "__main__":
    print("going for extensions")
    #cwd = os.getcwd()
    #print("directory {}".format(cwd))
    #dir = listdir(cwd)
    #print(dir)
    #print(initial_extensions)
    for extension in initial_extensions:
        try:
            mccree.load_extension(extension)
            print("loaded " + str(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    #try:
    	#mccree.load_extension("cogs.finalfantasylog")
    	#print("loaded fflogs")
    #except Exception as e:
    	#exc = '{}: {}'.format(type(e).__name__, e)
mccree.run(config.mccreetoken)