import aiohttp
import asyncio
import logging
import json

from .exceptions import SMMRYError

log = logging.getLogger(__name__)

class SMMRY:
    API_BASE = 'https://api.smmry.com/'

    def __init__(self, api_key, length, aiosession=None, loop=None):
        self.api_key = api_key
        self.aiosession = aiosession if aiosession else aiohttp.ClientSession()
        self.length = int(length)

        self._header = {
            "Expect": ""
        }

    async def get_tldr(self, uri):
        """TLDR, we don't wanna read everything do we?"""

        smmry_uripayload = f'{self.API_BASE}&SM_API_KEY={self.api_key}&SM_LENGTH={self.length}&SM_WITH_BREAK&SM_URL={uri}'
        res = await self.make_post(smmry_uripayload, '\{\}', self._header)

        try:
            log.debug(res)
        except KeyError:
            pass

        try:
            reduced = res['sm_api_content_reduced']
        except KeyError:
            reduced = 'Unknown'

        # Remove the [BREAK] with bullets
        result = res['sm_api_content'].replace("[BREAK]", "\n • ", (self.length - 1))
        # Last [BREAK] we should just leave it a nothing
        result = result.replace("[BREAK]", "")
        return f"**Reduced:** {reduced}\n**Summary:** \n • {result}"

    async def make_post(self, url, payload, headers=None):
        """Makes a POST request and returns the results"""
        async with self.aiosession.post(url, data=payload, headers=headers) as r:
            if r.status != 200:
                raise SMMRYError(f'Issue making POST request to url: [{r.status}] {await r.json()["sm_api_message"]}')
            return await r.json()

