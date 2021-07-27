#jangle_utils
import discord
import json
import logging
import aiohttp
import random
import pytz
import random
import asyncio
import async_timeout
from yarl import URL
from config import default_headers


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
					r.raise_for_status()
					return await r.text()

	async with aiohttp.ClientSession(headers=header) as session:
		async with async_timeout.timeout(timeout):
				async with session.get(url) as r:
					return await r.text()


async def fetchAPI_response(url,auth,query):
	print("in fetch api response")
	#fflogapilink = URL.build(scheme="http",host="www.fflogs.com",path="/api/v2/client",query_string=query,)
	#print(fflogapilink)
	header = {"User-Agent": "jangbot 2021.2.2","Authorization": "Bearer "+auth,"Content-Type":"""application/json"""}
	print(header)
	print(url)
	async with aiohttp.ClientSession(headers=header) as session:
		async with async_timeout.timeout(30):
			async with session.get("""https://www.fflogs.com/api/v2/client""",data=query) as r:
				print(await r.json())
				return await r.json()

