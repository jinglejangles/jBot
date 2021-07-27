'''
Created on Apr 21, 2021

@author: willd
'''
import aiohttp
import async_timeout
import asyncio
import random
import discord
import json
from jangle_utils import  fetch_response
from discord.ext import commands
from discord.ext.commands import Bot


class owstats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(name="owrank",
                      description="Returns competitive overwatch rank stats. Format must be Bnet-Name#BnetNumber",
                      brief="Gets Overwatch stuff",
                      pass_context=True)
    async def owrank(self, context, *args):
        tier_image_url = None
        try:
            (bnetname, bnetnumber) = args[0].split("#")
        except ValueError as e:
            await context.send(context.message.channel,"Incorrect format nerd, try again "+context.message.author.mention)
            return

        #await self.bot.send_typing(context.message.channel)
        response = None;
        mystr=bnetname+'-'+bnetnumber
        url = 'https://owapi.net/api/v3/u/'+mystr+'/blob'
        print(url)
        response = await fetch_response(url)
        print(str(response))
        parsed_json = json.loads(response)
        try:
            if parsed_json['error']:
                await context.send(context.message.channel,"API error code:{0}, {1}".format(parsed_json['error'],parsed_json['msg']))
                return
        except Exception as e:
            pass


        try:
            wins = parsed_json['us']['stats']['competitive']['overall_stats']['wins']
            damage_rank = parsed_json['us']['stats']['competitive']['overall_stats']['damage_comprank']
            tank_rank = parsed_json['us']['stats']['competitive']['overall_stats']['tank_comprank']
            support_rank = parsed_json['us']['stats']['competitive']['overall_stats']['support_comprank']
            avatar_url = parsed_json['us']['stats']['competitive']['overall_stats']['avatar']
            damage_tier_image_url = parsed_json['us']['stats']['competitive']['overall_stats']['damage_tier_image']
            tank_tier_image_url = parsed_json['us']['stats']['competitive']['overall_stats']['tank_tier_image']
            support_tier_image_url = parsed_json['us']['stats']['competitive']['overall_stats']['support_tier_image']
            print(damage_tier_image_url)
        except KeyError as e:
            print("key error for " + str(e))
            pass
        except Exception as e2:
            print("error for some gay reason", str(e2))

        
        #embed to make it pretty

        embed = discord.Embed(title="Stats for " + bnetname +'#'+bnetnumber, color=0x00ff00)
        embed.set_author(name=bnetname +'#'+bnetnumber,icon_url=avatar_url)
        embed.set_thumbnail(url=tank_tier_image_url)
        
        embed.add_field(name="Competitive wins",value=wins,inline=True)
        if damage_rank == None:
            embed.add_field(name="Damage rank",value="Not Available",inline=True)
        else:
            embed.add_field(name="Damage rank",value=damage_rank,inline=True)
        if damage_rank == None:
            embed.add_field(name="Tank rank",value="Not Available",inline=True)
        else:
            embed.add_field(name="Tank rank",value=tank_rank,inline=True)
        if damage_rank == None:
            embed.add_field(name="Support rank",value="Not Available",inline=True)
        else:
            embed.add_field(name="Support rank",value=support_rank,inline=True)    
            
        embed.set_footer(text="Using https://owapi.net api")
        await context.send(embed=embed)

    

def setup(bot):
    bot.add_cog(owstats(bot))