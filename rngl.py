'''
Created on Apr 22, 2021

@author: willd
'''
import random
import discord
from discord.ext import commands
import config


class Rngj(commands.Cog):
    """rng cog. basically stuff like rolling dice or card draws is put here"""
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
        """roll a dice in the format <num>d<num> e.g, a 4d6 is four rolls of a
        six sided die
        """
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception as exc:
            print(exc)
        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await context.send("{0} : {1}".format(result, sum(int(x)
                                              for x in result.split(","))))

    @roll.error
    async def roll_handler(self, ctx, error):
        """error handler for invoking roll command"""
        await ctx.send("format incorrect ")
        print(error)

    @commands.group(name="chooseowhero",
                    description="--Picks a random overwatch hero. You can "
                    "specify a subgroup(tank, support, offense, defense) "
                    "or any random hero by not submitting any subcommand.",
                    brief="--Picks a random overwatch hero",
                    invoke_without_command=True)
    async def chooseowhero(self, context):
        """base group command for choosing overwatch heroes
        if no subcommand picks from all choices"""
        if context.invoked_subcommand is None:
            await context.send(random.choice([*Rngj.overwatch_tanks,
                                              *Rngj.overwatch_damage,
                                              *Rngj.overwatch_support]))

    @chooseowhero.command(aliases=['dps'])
    async def damage(self, ctx):
        """return random overwatch damage character"""
        await ctx.send(random.choice(Rngj.overwatch_damage))

    @chooseowhero.command(aliases=['supports'])
    async def support(self, ctx):
        """return random overwatch support character"""
        await ctx.send(random.choice(Rngj.overwatch_support))

    @chooseowhero.command(aliases=['tanks'])
    async def tank(self, ctx):
        """return random overwatch tank character"""
        await ctx.send(random.choice(Rngj.overwatch_tanks))

    @commands.command(name="deathroll", brief="Start a deathroll",
                      description="Challenge another user to deathroll. "
                      "Randomly picks who goes first and two challengers roll "
                      "dice till someone rolls a one. Whoever rolls one loses.",
                      pass_context=True)
    async def deathroll(self, context, challenger: discord.Member,
                        number: int = None):
        """do a deathroll between two users"""
        if number is None:
            number = 1000

        if challenger.id == context.author.id:
            await context.send("Cant challenge yourself")
            return

        winner = None
        results = []

        while number != 1:
            number = random.randint(1, number)
            results.append(number)

        if len(results)%2 == 0:
            winner = context.author
        else:
            winner = challenger

        await context.send((winner.mention)+" is the winner!\n"+str(results))

    @deathroll.error
    async def deathroll_error(self, ctx, error):
        """deathroll error handler"""
        if isinstance(error, commands.BadArgument):
            await ctx.send("Can't find that user")
        else:
            await ctx.send(error)

    @commands.group(name="card", brief="Draw a card or hand", pass_context=True,
                    descrption="Draw a single card or cards based on "
                               "input", invoke_without_command=True)
    async def card(self, context):
        """base command for card games"""
        if context.invoked_subcommand is None:
            await context.send("Base command in progress")

    @card.command(name="duel")
    async def duel(self, context):
        """card duel, highest card wins"""
        await context.send("Work In Progress")

    @card.command(name="bj")
    async def bj(self, context):
        """play blackjack"""
        await context.send("In Progress")

def setup(bot):
    """add cog to bot"""
    bot.add_cog(Rngj(bot))
