import discord
from discord.ext import commands
from discord.utils import find
from jangle_utils import fetch_response
from config import fflogSecret,fflogID,graphQL,testQL,query222,query222dot1,queryReportBase,reportDDD,emojiConvert,xivAnalysisLink,profileQuery
import json
from yarl import URL
import re
import urllib.parse
from jangle_utils import fetchAPI_response
from aiohttp import BasicAuth
import datetime
from playerprofile import FFPlayerFight
import logging
from util.FFPlayer import FFPlayer
from util.FFReport import FFReport
import traceback


class finalfantasylog(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		self.endpointLink = 'https://www.fflogs.com/api/v2/client'
		self.tokenLink = 'https://www.fflogs.com/oauth/token'
		self.authToken = ''

	@commands.command(name="ff",description="fflogs get",brief="fflogs get" 
					,pass_context=True)
	async def ff(self,ctx,link,*args):
		
		if not link:
			raise commands.errors.MissingRequiredArgument(link)
		if len(args)>=1:
			raise commands.errors.TooManyArguments()
		if not re.match("https?:\/\/([\w\d]+\.)?fflogs\.com",link):
			print("bad link")
			raise commands.errors.BadArgument()
		fLink = URL(link)
		r = ''
		########################################################################
		try:
			if(fLink.raw_path.startswith("/character")):
				data = await self.getProfileFromUrl(fLink.raw_path)
				print(data)
				pembed = await self.characterEmbed(data)
				await ctx.send(embed=pembed)
				return
			elif(fLink.raw_path.startswith("/reports")):
				r = await self.buildReportFromURL(fLink)
				await ctx.send(embed=await self.reportEmbed(r))
				return
			else:
				await ctx.send("Something has gone horribly wrong or your link is bad, message owner")
		except Exception as e:
			print(e)
			await ctx.send(e)
			return

	@commands.is_owner()
	@commands.command(name="api",description="api get", brief="api get" \
						,pass_context=True,hidden=True)
	@ff.before_invoke
	async def api(self,ctx):
		if not self.authToken:
			try:
				self.authToken = await finalfantasylog.getAPITOKEN(self,ctx)
			except Exception as e:
				print(e)
				return
		print(self.authToken)
		return

	async def poop(self,ctx):
		print("poop")

	@ff.error
	async def ff_handler(self,ctx,error):
		if isinstance(error, commands.errors.TooManyArguments):
			await ctx.send(ctx.author.mention+ "Only one link please")
		elif isinstance(error,commands.errors.MissingRequiredArgument):
			await ctx.send(ctx.author.mention+ "You forgot the fflogs link")
		elif isinstance(error,commands.errors.BadArgument):
			await ctx.send(ctx.author.mention+"You didn't submit a fflogs.com link")
		else:
			await ctx.send(ctx.author.mention+" dm owner")
			
	async def getAPITOKEN(self,ctx):
			auth = BasicAuth(fflogID,fflogSecret)
			params={'grant_type':'client_credentials'}
			tokenResponse = await self.bot.session.post(self.tokenLink,auth=auth,data=params)
			tokenResponse = await tokenResponse.text()
			try:
				parsed_json = json.loads(tokenResponse)
				if parsed_json['access_token']:
					return parsed_json['access_token']
				else:
					raise Exception('API access token not found/imported. \
									Try again in a little bit')
			except Exception as e:
				print(e)
				await ctx.send("JSON parse error, try again later")
				return


	async def buildReportFromURL(self,url):
		fightID, reportID = None, None, 
		splitData= ''
		reportURL = url
		reportPath = reportURL.path
		frags = reportURL.fragment
		print("Frags: "+frags)
		print("report path: "+reportPath)
		reportID = ''

		if re.match("\/reports\/[a-zA-Z0-9]{16,16}",reportPath):
			print("match")
			reportID = reportPath[-16:]
		
		print("Report id: "+reportID)
		if frags == '':
			raise ValueError("You sent a base report page, please link a \
							 single fight")
			jsonResponse = await self.getFFLOGSREPORTPAGE(reportID)
			return


		try:
			print("trying to split")
			splitData = dict(x.split('=') for x in frags.split('&'))
		except Exception as e:
			raise Exception('Malformed Link: make sure the link is a valid \
							report/fight')
			#return

		print("fragments: "+frags)
		#try:
		#	splitData = splitData.split()
		#except Exception as e:
		#	print("huh {}".format(e))
		if splitData is not None:
			print("split data: "+str(splitData))
		if splitData is None:
			print("shit")
			raise Exception("You sent the base report page, please link a single fight from your report(This might change in the future :-).")
			return

		if splitData.get('fight').isdigit(): fightID = splitData.get('fight')
		
		if splitData.get('fight')=="last":#fightID = "last"
			print("In last")
			raise Exception("Last fightID currently not supported, yell at jangles to fix it")
			return

		print("report path: "+reportPath)
		
		jsonResponse = await self.getFFLOGSLINKDATA(reportID,fightID=fightID)
		print("going to trim")
		trimmed_data = await self.trimReportResponse(jsonResponse)
		return trimmed_data

	async def getFFLOGSREPORTPAGE(self,reportID,**kwargs):
		reportIDencode=urllib.parse.quote_plus(reportID)
		print(reportIDencode)
		graphQLSUB = re.sub("REPORT_CODE_INPUT",reportIDencode,reportDDD)
		print(urllib.parse.unquote(graphQLSUB))
		print(len(graphQLSUB))
		print(type(graphQLSUB))
		r = await self.buildQueryURL(urllib.parse.unquote(graphQLSUB),"ReportData")
		return "Hey"

	async def getFFLOGSLINKDATA(self,reportID,**kwargs):
		print("query222: "+query222dot1)
		reportIDencode=urllib.parse.quote_plus(reportID)
		if kwargs.get('fightID'):
			fightIDencode=urllib.parse.quote_plus(kwargs.get('fightID'))
		graphQLSUB = query222dot1.replace("REPORT_CODE_INPUT",reportIDencode).replace("FIGHT_ID_INPUT",fightIDencode)
		print("reportIDencode: "+reportIDencode)
		print(urllib.parse.unquote(graphQLSUB))
		r = await self.buildQueryURL(urllib.parse.unquote(graphQLSUB),"ReportData")
		return r

	async def buildQueryURL(self,query,operationName):
		data = {}
		data['query']=query
		data['operationName']=operationName
		json_query = json.dumps(data)
		print(json_query)
		print(type(json_query))
		r = await fetchAPI_response(testQL,self.authToken,json_query)
		#parsed_json = json.loads(r)
		#print(arsed_json)
		return r

	async def trimReportResponse(self,json):
		encounterID, fightName, tanks, damage, healers,duration,code,fightID = \
		None, None, None, None, None, None,None,None
		speedPercent, executionPercent = None, None
		masterData = None
		try:
			encounterID = json['data']['reportData']['report']['rankings']['data'][0]['encounter']['id']
			fightName = json['data']['reportData']['report']['rankings']['data'][0]['encounter']['name']
			tanks = json['data']['reportData']['report']['rankings']['data'][0]['roles']['tanks']['characters']
			damage = json['data']['reportData']['report']['rankings']['data'][0]['roles']['dps']['characters']
			healer = json['data']['reportData']['report']['rankings']['data'][0]['roles']['healers']['characters']
			speedPercent = json['data']['reportData']['report']['rankings']['data'][0]['speed']['rankPercent']
			executionPercent = json['data']['reportData']['report']['rankings']['data'][0]['speed']['rankPercent']
			duration = json['data']['reportData']['report']['rankings']['data'][0]['duration']
			print(duration)
			fightID = json['data']['reportData']['report']['rankings']['data'][0]['fightID']
			print(fightID)
			code = json['data']['reportData']['report']['code']
			print(code)
			print(json['data']['reportData']['report']['rankings']['data'][0]['speed']['rankPercent'])
			print("{}{}{}{}{}{}{}".format(fightID,fightName,tanks,damage,healer,speedPercent,executionPercent))
			masterData = json['data']['reportData']['report']['masterData']['actors']
			print("\n\n")
			print(type(masterData))
			print(masterData)
			#log data for checking later
		except Exception as e:
			print(e)

		masterDataDict = await self.createMasterDataDict(masterData)
		charList =[]
		healCombined: float
		tankCombined: float
		healPercentile : int
		tankPercentile : int

		try:
			for idx, x in enumerate(healer):
				if idx<len(healer)-1:
					#jobConverted = jobChange(x['class'])
					pID = masterDataDict.get(x['name']+x['class'],None)
					player = FFPlayer(x['name'],x['class'],x['amount'],x['rankPercent'],pID)
					charList.append(player)
				if idx==len(healer)-1:
					healCombined = x['amount']
					healPercentile= x['rankPercent']
			for idx, x in enumerate(tanks):
				if idx<len(tanks)-1:
					pID = masterDataDict.get(x['name']+x['class'],None)
					player = FFPlayer(x['name'],x['class'],x['amount'],x['rankPercent'],pID)
					charList.append(player)
				if idx==len(tanks)-1:
					tankCombined = x['amount']
					tankPercentile = x['rankPercent']
			for idx, x in enumerate(damage):
				pID = masterDataDict.get(x['name']+x['class'],None)
				player = FFPlayer(x['name'],x['class'],x['amount'],x['rankPercent'],pID)
				charList.append(player)
		except Exception as e:
			print(e)


		charList.sort(reverse=True)
		duration = datetime.timedelta(milliseconds=duration)
		d = FFReport(charList,healCombined,tankCombined,healPercentile, \
					tankPercentile,fightName,encounterID,duration,code,fightID)
		return d

	async def reportEmbed(self,report):
		xivFightLink = xivAnalysisLink+report.code+"/"+str(report.fightID)
		membed = discord.Embed(title=report.fightName, color=0x00ff00)
		membed.description = "Duration: " + str(report.duration).split(".")[0] 
		#emojiembed = discord.Embed(title="stats",color=0x00ff00)
		#emojiembed.add_field(name="Tooth",value=nin_emoji)
		membed.set_thumbnail(url=report.fightIcon)
		membed.set_footer(text='Jangbot 2021')
		for x in report.charList:
			hyperlink = report.link+"&source="+str(x.playerID)
			ppp = "["+str(x.playerID)+"]"+"("+hyperlink+")"
			print(ppp)
			buildClickable = "["+"""```"""+str(x.percentile)+""":"""+str(round(x.dps))+"""```]"""+"("+hyperlink+")"
			print(buildClickable)
			membed.add_field(name=str(self.bot.get_emoji(emojiConvert.get(x.shorthand)))+str(x.name),value=buildClickable,inline=True)
			#membed.add_field(name=x.name,value=int(round(x.dps)))
		#await ctx.send(embed=emojiembed)
		membed.add_field(name="xiv Analysis",value=xivAnalysisLink+report.code+"/"+str(report.fightID),inline=False)
		return membed

	async def createMasterDataDict(self,masterList):
		print("in create dict")
		dataDict = dict()
		for x in masterList:
			key = x['name']+x['subType']
			value = str(x['id'])
			dataDict[key] = value
		return dataDict

	async def getProfileFromUrl(self,url):
		if re.match("\/character\/[nej][aup]\/[a-zA-Z]{5,16}\/[a-zA-z']{1,15}%20[a-zA-Z']{1,15}",url):
			print(re.match("\/character\/[nej][aup]\/[a-zA-Z]{5,16}\/[a-zA-z']{1,15}%20[a-zA-Z']{1,15}",url))
		characterInfo = url[11::].split('/')
		region,server,name = characterInfo[0],characterInfo[1],characterInfo[2]
		query = profileQuery.replace("""INSERT CHARACTER""",name) \
			.replace("""INSERT SERVER""",server).replace("""INSERT REGION""",region)
		print("QUERY COMPAIRE")
		r = await self.buildQueryURL(query,"profile")
		data = await self.trimCharacterResponse(r)
		return data

	async def characterEmbed(self,character):
		pembed = discord.Embed(title="INSERT NAME?",color=0x00ff00)
		pembed.description = "THIS IS DESCRIPTION FOR SOMETHING"
		pembed.set_thumbnail(url="https://assets.rpglogs.com/img/ff/favicon.png")
		pembed.set_footer(text='Jangbot 2021')
		for dude in character:
			pembed.add_field(name=str(self.bot.get_emoji( \
							emojiConvert.get(dude.shorthand)))+" "+dude.fight \
							,value=str(dude.kills)+" kills, "+ str(dude.fastest) \
							+" fastest time, "+str(dude.amount)+" best dps, " \
							+str(dude.rank)+" percentile!",inline=False)
		return pembed

	async def trimCharacterResponse(self,data):
		fightList = list()
		print("\n")
		root = data['data']
		for k,v in root.items():
			start = v['character']['zoneRankings']['rankings']
			for x in start:
				name = x['encounter']['name']
				rankP = x['rankPercent']
				kills = x['totalKills']
				fastest = str(datetime.timedelta(milliseconds=x['fastestKill'])).split(".")[0]
				spec = x['spec']
				amount = x['bestAmount']			
				fightList.append(FFPlayerFight(name,rankP,kills,fastest,spec,amount))
		print(len(fightList))
		return fightList
		
def setup(bot):
    bot.add_cog(finalfantasylog(bot))