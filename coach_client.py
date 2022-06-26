from datetime import datetime

import aiohttp
from aiohttp import ClientSession
from loguru import logger


class CoachClientAsync:
    session: ClientSession

    def __init__(self, coach_url, system_kit_id, token):
        self.url = coach_url + "api/v1/system-kits/" + str(system_kit_id) + "/point"
        self.headers = {"Authorization": f"Bearer {token}"}

    async def startup(self):
        self.session = aiohttp.ClientSession()

    async def shutdown(self):
        await self.session.close()

    async def send_point(self, data):
        data = data.copy()
        data["timestamp"] = datetime.utcnow().isoformat()
        resp = await self.session.post(self.url, json=data, headers=self.headers)
        if resp.status == 200:
            logger.info(f"Send success {self.url} {data}")
        else:
            logger.warning(f"Send error {self.url} {resp.text}")
