'''
Created on Apr 22, 2021

@author: willd
'''
import random
import discord
import config
from discord.ext import commands
from discord.ext.commands import Bot


class rngj(commands.Cog):
    overwatch_damage = config.overwatch_damage
    overwatch_tanks = config.overwatch_tanks
    overwatch_support = config.overwatch_support

    def __init__(self, bot):
            self.bot = bot

    @commands.command(name="roll",
                      description="Roll dice based on the format #d# where "
                      "the first # is the number of dice and second # is the "
                      "number of sides",
                      brief="Roll some dice",
                      pass_context=True)
    async def roll(self, context, dice: str):
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception as e:
            print(e)
        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await context.send("{0} : {1}".format(result, sum(int(x)
                            for x in result.split(","))))

    @roll.error
    async def roll_handler(self, ctx, error):
        await ctx.send("format incorrect ")
        print(error)

    @commands.group(name="chooseowhero",
                      description="--Picks a random overwatch hero. You can "
                      "specify a subgroup(tank, support, offense, defense) "
                      "or any random hero by not submitting any subcommand.",
                      brief="--Picks a random overwatch hero"
                      , invoke_without_command=True)
    async def chooseowhero(self, context, *args):
        if context.invoked_subcommand is None:
            await context.send(random.choice([*overwatch_tanks,\
                                              *overwatch_damage,\
                                              *overwatch_support]))

    @chooseowhero.command(aliases=['dps'])
    async def damage(self,ctx):
        await ctx.send(random.choice(overwatch_damage))

    @chooseowhero.command(aliases=['supports'])
    async def support(self,ctx):
        await ctx.send(random.choice(overwatch_support))

    @chooseowhero.command(aliases=['tanks'])
    async def tank(self,ctx):
        await ctx.send(random.choice(overwatch_tanks))

    @commands.command(name="deathroll", brief="Start a deathroll", \
                    description="Challenge another user to deathroll. "\
                    "Randomly picks who goes first and two challengers roll "\
                    "dice till someone rolls a one. Whoever rolls one loses.",
                    pass_context=True)
    async def deathroll(self, context, challenger: discord.Member,
                        number: int=None):
        if number is None:
            number = 1000

        if(challenger.id == context.author.id):
            await context.send("Cant challenge yourself")
            return

        #if(bool(random.getrandbits(1))):
        #    first = challenger
        #    second = context.author
        #else:
        #    first = context.author
        #    second = challenger

        winner = None
        results = []

        while(number!=1):
            number = random.randint(1,number)
            results.append(number)

        if(len(results)%2==0):
            winner = context.author
        else:
            winner = challenger
        
        await context.send((winner.mention)+" is the winner!\n"+str(results))

    @deathroll.error
    async def deathroll_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Can't find that user")
        else:
            await ctx.send(error)

    @commands.group(name="card",brief="Draw a card or hand",pass_context=True,
                        descrption="Draw a single card or cards based on "
                        "input",invoke_without_command=True)
    async def card(self,context):
        if context.invoked_subcommand is None:
            await context.send("Base command in progress")

    @card.command(name="duel")
    async def duel(self,context):
        await context.send("Work In Progress")

    @card.command(name="bj")
    async def bj(self,context):
        await context.send("In Progress")

def setup(bot):
    bot.add_cog(rngj(bot))
