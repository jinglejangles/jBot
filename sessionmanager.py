from aiohttp import ClientSession
import asyncio
import async_timeout
import config


class SessionManager:
	_session: ClientSession

	def __init__(self):
		self._session = ClientSession()

	async def __aexit__():
		self._session.close()

	async def close(self):
		await self._session.close()

	async def post(self,url,**kwargs):
		return await self.request("POST",url=url,**kwargs)

	async def get(self,url,**kwargs):
		return await request("GET",url=url,**kwargs)

	async def request(self, method, url, **kwargs):
		headers = kwargs.get('headers',{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"})
		data = kwargs.get('data',None)
		print("Session request?")
		return await self._session.request(method=method,url=url,**kwargs)