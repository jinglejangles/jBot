#bgg cog
import discord, logging, aiohttp, random, pytz,random,asyncio, async_timeout, html, re
from discord.ext import commands
from datetime import datetime
import time
import urllib.parse as urlparse
import xml.etree.ElementTree as xmltree
from jangle_utils import fetch_response


class boardgamegeek(commands.Cog):
	buildstring_start = "```Select a number, prev for previous page, next for next page, or quit to stop\n\n"
	responses = ["1","2","3","4","5","6","7","8","9","prev","next","quit","0"]
	bgg_search_url = "https://boardgamegeek.com/xmlapi/search?search="
	bgg_search_url2 = "https://boardgamegeek.com/xmlapi2/search?query="
	bgg_type = "&type=boardgame"
	bgg_hot_url = "https://www.boardgamegeek.com/xmlapi2/hot?boardgame"
	bgg_base_game_url = "https://boardgamegeek.com/xmlapi/boardgame/"
	
	def __init__(self, bot):
		self.bot = bot
		self.sessions = []

	def buildbgglist(self, start, end, igamelist):
		buildstring = self.buildstring_start
		
		i = int()
		last = int()
		numberlistiterator = 0
		bool_next = False
		bool_prev = False

		if start<=0:
			print("star is <=0")
			i=0
			bool_prev = False
		else:
			i=start
			bool_prev = True

		if end >= len(igamelist):
			last = len(igamelist)
			bool_next = False
		else:
			last = end
			bool_next = True

		print("Start posistion:{0}    End posistion{1}.".format(start,end))
		print("Previous Bool:{0}    Next Bool:{1}".format(bool_prev,bool_next))

		if bool_prev:
			buildstring += "[prev]: Previous Page\n"

		for x in igamelist[i:end]:
			buildstring += "[{}]: {}\n".format(i-start,x[1])
			numberlistiterator += 1
			i += 1

		if bool_next:
			buildstring+= "[next]: Next Page\n"
	
		return "{0}{1}".format(buildstring,"```")


	@commands.command(name="bgg",
					  description="Look up a board game via board game geek's api ",
					  brief="find board game(??bgg <search term>)",
					  pass_context=True,
					  no_pm=True)
	
	async def bgg(self, context, *args):
		my_game_list = []


		if context.message.channel.id in self.sessions:
			await self.bot.say('Already running in channel. Exit bgg with quit')
			return


		
		bggstring = None
		if len(args) > 1:
			bggstring = '+'.join(str(i) for i in args)
		elif len(args) == 1:
			bggstring = args[0]
		else:
			await context.send("No search term submitted, please try again, {0}".format(context.message.author.mention))
			return

		await context.trigger_typing()

		#url = "{0}{1}".format(self.bgg_search_url,bggstring)
		url = "{0}{1}{2}".format(self.bgg_search_url2,bggstring,self.bgg_type)
		print(type(context.message.channel.id))

		print(url)
		print(bggstring)
		response = None
		response = await fetch_response(url,timeout=20)
		print(response)
		my_game_list = await self._parse_xml2(response)
		print(my_game_list)
		#return

		my_game_list.sort(key=lambda tup:tup[0])
		game_list_len = len(my_game_list)
		posistion = 0
		print(game_list_len)
		print(url)
		if game_list_len == 0:
			await context.send("No games found, try again {0}.".format(context.message.author.mention))
			return

		self.sessions.append(int(context.message.channel.id)) 
		################################################################################################################
		gamestring = self.buildbgglist(posistion,posistion+10,my_game_list)
		await context.send("Found {0} games.  Please select an option below:\n{1}".format(len(my_game_list),gamestring))

		
		return_message, next_bool, prev_bool = None, None, None

		
		while True:

			msg = await self.bot.wait_for(author=context.message.author,timeout=60)
			if msg is None or msg.channel is not context.message.channel:
				await self.bot.send_message(context.message.channel,"Quitting bgg search {0}".format(context.message.author.mention))
				self.sessions.pop(int(context.message.channel.id))
				break

			msginput = msg.content.split(' ')
			msginput = msginput[0].lower()
			



			if str(msginput) not in self.responses:
				await self.bot.send_message(context.message.channel,"Incorrect format try again please\n```{0}```".format(gamestring))
				continue

			else:
				if (posistion+10<=game_list_len) and msginput == "next":
					print("next triggered")
					posistion += 10
					await self.bot.send_message(context.message.channel,  self.buildbgglist(posistion,posistion+10,my_game_list))
					continue
				elif (posistion-10>=0) and msginput == "prev":
					print("prev triggered")
					posistion -= 10
					print(posistion)
					await self.bot.send_message(context.message.channel,  self.buildbgglist(posistion,posistion+10,my_game_list))
					continue
				elif msginput == "quit":
					await self.bot.send_message(context.message.channel,"Quitting search, {0}".format(context.message.author.mention))
					self.sessions.pop(int(context.message.channel.id))
					break
				elif int(msginput)+posistion<=game_list_len:
					await self.bot.send_message(context.message.channel,"sending game info your way,{0}".format(context.message.author.mention))
					await self.bot.send_message(context.message.channel, embed = await self.bbgembedinfo(int(msginput)+posistion, my_game_list))
					break
				else:
					await self.bot.send_message(context.message.channel,"Incorrect input, please try again, {0}".format(context.message.author.mention))
					continue
			
			
		

	async def cleargames(self):
		self.gamelist.clear()


	async def bbgembedinfo(self, posistion, gamelist):
		utc = datetime.utcfromtimestamp(time.time())
		

		for x in gamelist:
			print(x[0],x[1])

		print(posistion)
		game = gamelist[posistion]
		print(str(game[0]) + "THIS IS THE GAME0 CALL")

		url = "https://boardgamegeek.com/xmlapi/boardgame/{0}".format(str(game[0]))
		print(url)

		response = await fetch_response(url,timeout=20)

		boardgame = xmltree.fromstring(response)
		try:
			for boardgame in boardgame.findall('boardgame'):
				name = boardgame.find('name').text
				game_description = re.sub('<[^<]+?>',' ',html.unescape(boardgame.find('description').text))
				print(game_description)
				gamethumbnail_url = boardgame.find('thumbnail').text
				game_max_players = boardgame.find('maxplayers').text
				game_min_players = boardgame.find('minplayers').text
				game_year = boardgame.find('yearpublished').text
				game_min_time = boardgame.find('minplaytime').text
				game_max_time = boardgame.find('maxplaytime').text
				game_publisher = boardgame.find('boardgamepublisher').text
		except Exception as e:
			pass



		
		title_text = "{0}:   Published by: {1} in {2}".format(name,game_publisher,game_year)
		description_text = "{0}{1}".format(game_description[:500],"...")
		bgembed = discord.Embed(title=name, description=description_text, color=0x00ff00, timestamp=utc)
		bgembed.set_thumbnail(url=gamethumbnail_url)
		bgembed.add_field(name="Players:",value="{0} to {1}".format(game_min_players,game_max_players),inline=True)
		bgembed.add_field(name="Game Length:",value="{0} to {1} minutes".format(game_min_time,game_max_time),inline=True)
		bgembed.add_field(name="Designed by:",value="{0} in {1}".format(game_publisher,game_year),inline=True)
		bgembed.add_field(name="BGG Link:",value="http://boardgamegeek.com/boardgame/{0}".format(str(game[0])),inline=True)
		bgembed.set_footer(text="Game information taken from https://boardgamegeek.com api")

		return(bgembed)
		
	async def xml_single_game(self,id):
		attrib_dict = {}
		response = await fetch_response(self.bgg_base_game_url+str(id))

		boardgame = xmltree.fromstring(response)
		for boardgame in boardgame.findall('boardgame'):
			name = boardgame.find('name').text
			game_description = boardgame.find('description').text
			gamethumbnail_url = boardgame.find('thumbnail').text
			game_max_players = boardgame.find('maxplayers').text
			game_min_players = boardgame.find('minplayers').text
			game_year = boardgame.find('yearpublished').text
			game_min_time = boardgame.find('minplaytime').text
			game_max_time = boardgame.find('maxplaytime').text
			game_publisher = boardgame.find('boardgamepublisher').text

	@staticmethod
	async def _parse_xml(response_xml):
			gamelist = []

			print("xmlparse")
			root = xmltree.fromstring(response_xml)
			for boardgame in root.findall('boardgame'):
				print(boardgame)
				gameid = boardgame.get('objectid')
				name = boardgame.find('name').text
				gamelist.append((int(gameid),name))

			return gamelist

	@staticmethod
	async def _parse_xml2(response_xml):
			print("xmlparse2")
			gamelist = []
			root = xmltree.fromstring(response_xml)
			for boardgame in root.findall('item'):
				name = boardgame.find('name').get('value')
				gameid = boardgame.get('id')
				#print(gameid)
				#print(boardgame.find('name').get('value'))
				#print(boardgame.attrib.get('id'))
				#print(boardgame.tag)
				#gameid = boardgame.get('objectid')
				#name = boardgame.find('name').text
				gamelist.append((int(gameid),name))

			return gamelist

def setup(bot):
	bot.add_cog(boardgamegeek(bot))


