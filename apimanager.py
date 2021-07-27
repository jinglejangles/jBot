#jangle_utils
import discord, logging, aiohttp, random, pytz,random,asyncio, async_timeout
import json


class apimanager():
	def __init__(self,bot):
	self.bot = bot
	self.sesion = aiohttp.
	self.loop = asyncio.get_event_loop()

async def fetch_response(url, **kwargs):
	auth = ''
	for kwarg in kwargs:
		print(kwarg)
	timeout = kwargs.get('timeout', 10)
	header = kwargs.get('header',{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"})

	if 'id' in kwargs:
		print('got id')
		params={'grant_type':'client_credentials'}
		auth = aiohttp.BasicAuth(kwargs.get('id'),kwargs.get('secret'))
		async with aiohttp.ClientSession(headers=header,auth=auth) as session:
			async with async_timeout.timeout(timeout):
				async with session.post(url,data=params) as r:
					print(r.status)
					return await r.text()

	async with aiohttp.ClientSession(headers=header) as session:
		async with async_timeout.timeout(timeout):
				async with session.get(url) as r:
					return await r.text()


async def build_response(url,**kwargs):


async def main():


def setup(bot):
    bot.add_cog(apimanager(bot))

if __name__ == "__main__":
	main()