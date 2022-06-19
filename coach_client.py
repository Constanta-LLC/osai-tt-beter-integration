from loguru import logger
from datetime import datetime

import requests


class CoachClient:
    def __init__(self, coach_url, system_kit_id, token):
        self.session = requests.Session()
        self.url = coach_url + "api/v1/system-kits/" + str(system_kit_id) + "/point"
        self.headers = {"Authorization": f"Bearer {token}"}

    def send_point(self, data):
        data = data.copy()
        data["timestamp"] = datetime.utcnow().isoformat()
        resp = self.session.post(self.url, json=data, headers=self.headers)
        if resp.status_code == 200:
            logger.info(f"Send success {self.url} {data}")
        else:
            logger.warning(f"Send error {self.url} {resp.text}")
