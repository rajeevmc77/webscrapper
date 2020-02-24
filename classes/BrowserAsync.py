#import asyncio as asy
#import multiprocessing
import aiohttp
#import time
#import os

class BrowserAsync:
    def __init__(self,loop=None):
        self.loop = loop
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        self.login_data ={

        }
        self.session = None

    def createSession(self,loop=None):
        try:
            self.session = aiohttp.ClientSession(loop=loop)
        except:
            print('Exception in creating session')
        return self.session

    async def get(self,  url):
        resp = None
        if not self.session:
            self.createSession(self.loop)
       # try:
        async with self.session.get(url, headers = self.headers, allow_redirects=True) as resp:
            # assert resp.status == 200
            if resp.status == 200:
                resp = await resp.read()
                return  resp
            else:
                return  resp
        #except:
        #    print('exception while connecting to URL -', url)


    async def post(self, url, data):
        resp = None
        if not self.session:
            self.createSession(self.loop)
        #try:

        async with self.session.post(url, headers=self.headers,  data=data,allow_redirects=True) as resp:
            if resp.status == 200:
                resp = await resp.read()
                return  resp
            else:
                return  resp
        #except:
        #    print('exception while posting to URL -  ', url, ' - data - ', data)


    async def Login(self, url, login_data=None):
        if not login_data:
            login_data = self.login_data
        return await self.post(url,login_data)
